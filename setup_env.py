"""
Helper script to create .env file interactively.
Run: python setup_env.py
"""
import os
import secrets

def generate_secret_key():
    """Generate a secure random secret key."""
    return secrets.token_urlsafe(32)

def create_env_file():
    """Create .env file with user input."""
    print("=" * 60)
    print("Organization Management Service - Environment Setup")
    print("=" * 60)
    print()
    
    if os.path.exists('.env'):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    print("Please provide the following information:")
    print()
    
    # MongoDB URI
    print("MongoDB Atlas Connection:")
    print("1. Go to https://www.mongodb.com/cloud/atlas")
    print("2. Create a free M0 cluster")
    print("3. Create a database user")
    print("4. Add your IP to network access")
    print("5. Click 'Connect' -> 'Connect your application'")
    print()
    mongo_uri = input("Enter MongoDB URI (mongodb+srv://...): ").strip()
    
    if not mongo_uri:
        print("Error: MongoDB URI is required!")
        return
    
    # JWT Secret
    print()
    print("JWT Secret Key:")
    use_generated = input("Generate random secret key? (y/n) [y]: ").strip().lower()
    if use_generated != 'n':
        jwt_secret = generate_secret_key()
        print(f"Generated secret key: {jwt_secret}")
    else:
        jwt_secret = input("Enter JWT secret key (min 32 chars): ").strip()
        if len(jwt_secret) < 32:
            print("Warning: Secret key should be at least 32 characters!")
    
    # Other settings (with defaults)
    print()
    app_name = input("App name [Org Management Service]: ").strip() or "Org Management Service"
    jwt_algo = input("JWT Algorithm [HS256]: ").strip() or "HS256"
    jwt_expire = input("JWT Expire Minutes [1440]: ").strip() or "1440"
    master_db = input("Master Database Name [master_db]: ").strip() or "master_db"
    
    # Create .env file
    env_content = f"""APP_NAME={app_name}
JWT_SECRET={jwt_secret}
JWT_ALGO={jwt_algo}
JWT_EXPIRE_MINUTES={jwt_expire}

MONGO_URI={mongo_uri}
MASTER_DB={master_db}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print()
        print("=" * 60)
        print("✅ .env file created successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the app: uvicorn app.main:app --reload --port 8000")
        print("3. Visit http://localhost:8000/docs for API documentation")
    except Exception as e:
        print(f"Error creating .env file: {e}")

if __name__ == "__main__":
    create_env_file()

