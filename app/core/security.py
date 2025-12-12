from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
import hashlib
import sys
import traceback
from app.core.config import settings


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt_sha256 (SHA256 + bcrypt).
    This avoids the 72-byte limitation by hashing with SHA256 first.
    
    Process:
    1. Validate password
    2. Hash password with SHA256 (always 32 bytes)
    3. Hash SHA256 result with bcrypt (no 72-byte limit issue)
    
    Args:
        password: Plain text password string (ONLY the password)
        
    Returns:
        Hashed password string in format: $bcrypt-sha256$...
        
    Raises:
        ValueError: If password is invalid
    """
    # DEBUG: Log what we received
    if not isinstance(password, str):
        error_msg = f"DEBUG hash_password: Received non-string. Type: {type(password)}, Value: {str(password)[:100] if password else 'None'}"
        print(error_msg, file=sys.stderr)
        raise ValueError(f"Password must be a string. Received type: {type(password).__name__}")
    
    # DEBUG: Check password length and content
    password_len = len(password)
    password_bytes_len = len(password.encode('utf-8'))
    
    if password_len > 100 or password_bytes_len > 100:
        error_msg = f"DEBUG hash_password: Suspiciously long value. Length: {password_len} chars, {password_bytes_len} bytes. First 100 chars: {password[:100]}"
        print(error_msg, file=sys.stderr)
        print(f"DEBUG hash_password: Full value type: {type(password)}, repr: {repr(password)[:200]}", file=sys.stderr)
        raise ValueError(f"Password appears to be incorrect value. Length: {password_len} chars. Expected password string, got something else.")
    
    # Validate password length (reasonable limits)
    if password_len == 0:
        raise ValueError("Password cannot be empty")
    
    if password_len > 4096:  # Reasonable upper limit
        raise ValueError("Password is too long (maximum 4096 characters)")
    
    # Ensure we're only hashing the password string, nothing else
    password_to_hash = str(password).strip()
    
    if not password_to_hash:
        raise ValueError("Password cannot be empty or whitespace only")
    
    # DEBUG: Log the actual password being hashed (truncated for security)
    print(f"DEBUG hash_password: Hashing password of length {len(password_to_hash)} chars", file=sys.stderr)
    
    try:
        # Step 1: Hash password with SHA256 (always produces 32 bytes)
        # This ensures we never hit bcrypt's 72-byte limit
        password_bytes = password_to_hash.encode('utf-8')
        sha256_hash = hashlib.sha256(password_bytes).digest()
        
        # DEBUG: Verify SHA256 hash is 32 bytes
        if len(sha256_hash) != 32:
            error_msg = f"DEBUG hash_password: SHA256 hash is not 32 bytes! Length: {len(sha256_hash)}"
            print(error_msg, file=sys.stderr)
            raise ValueError("SHA256 hash generation failed")
        
        print(f"DEBUG hash_password: SHA256 hash created successfully, length: {len(sha256_hash)} bytes", file=sys.stderr)
        
        # Step 2: Hash the SHA256 result with bcrypt
        # Since SHA256 is always 32 bytes, this is safe
        try:
            salt = bcrypt.gensalt(rounds=12)
            print(f"DEBUG hash_password: Salt generated, length: {len(salt)} bytes", file=sys.stderr)
            
            # Ensure we're passing bytes to bcrypt.hashpw
            if not isinstance(sha256_hash, bytes):
                error_msg = f"DEBUG hash_password: sha256_hash is not bytes! Type: {type(sha256_hash)}"
                print(error_msg, file=sys.stderr)
                sha256_hash = bytes(sha256_hash)
            
            if not isinstance(salt, bytes):
                error_msg = f"DEBUG hash_password: salt is not bytes! Type: {type(salt)}"
                print(error_msg, file=sys.stderr)
                salt = bytes(salt)
            
            bcrypt_hash = bcrypt.hashpw(sha256_hash, salt)
            print(f"DEBUG hash_password: bcrypt hash created successfully, length: {len(bcrypt_hash)} bytes", file=sys.stderr)
            
        except ValueError as bcrypt_error:
            # If bcrypt still complains, log detailed info
            error_msg = f"DEBUG hash_password: bcrypt.hashpw failed. SHA256 hash length: {len(sha256_hash)} bytes. Error: {str(bcrypt_error)}"
            print(error_msg, file=sys.stderr)
            print(f"DEBUG hash_password: SHA256 hash type: {type(sha256_hash)}, salt type: {type(salt)}", file=sys.stderr)
            print(f"DEBUG hash_password: SHA256 hash value (first 50): {sha256_hash[:50] if isinstance(sha256_hash, bytes) else 'not bytes'}", file=sys.stderr)
            raise ValueError(f"Bcrypt hashing failed: {str(bcrypt_error)}")
        
        # Return in bcrypt-sha256 format for compatibility
        # Format: $bcrypt-sha256$<bcrypt_hash>
        result = f"$bcrypt-sha256${bcrypt_hash.decode('utf-8')}"
        print(f"DEBUG hash_password: Password hashed successfully", file=sys.stderr)
        return result
        
    except ValueError:
        # Re-raise ValueError as-is
        raise
    except Exception as e:
        # Log full traceback for debugging
        error_msg = f"DEBUG hash_password: Unexpected error. Password length: {len(password)}, Type: {type(password)}"
        print(error_msg, file=sys.stderr)
        print(f"DEBUG hash_password: Exception: {str(e)}", file=sys.stderr)
        print(f"DEBUG hash_password: Traceback:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise ValueError(f"Failed to hash password: {str(e)}")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    
    Args:
        plain_password: Plain text password to verify (ONLY the password)
        hashed_password: Previously hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        # Validate inputs
        if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
            return False
        
        if not plain_password or not hashed_password:
            return False
        
        # Strip whitespace from password
        password_to_verify = plain_password.strip()
        
        # Check if hash is in bcrypt-sha256 format
        if hashed_password.startswith("$bcrypt-sha256$"):
            # Extract the bcrypt hash
            bcrypt_hash = hashed_password.replace("$bcrypt-sha256$", "")
            
            # Hash the plain password with SHA256
            sha256_hash = hashlib.sha256(password_to_verify.encode('utf-8')).digest()
            
            # Verify against bcrypt hash
            return bcrypt.checkpw(sha256_hash, bcrypt_hash.encode('utf-8'))
        else:
            # Legacy format: assume it's a direct bcrypt hash (for backward compatibility)
            # Hash with SHA256 first, then verify
            sha256_hash = hashlib.sha256(password_to_verify.encode('utf-8')).digest()
            return bcrypt.checkpw(sha256_hash, hashed_password.encode('utf-8'))
            
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None
