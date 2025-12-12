"""
Quick verification script to check if setup is correct.
Run: python verify_setup.py
"""
import sys
import os

def check_python_version():
    """Check Python version."""
    if sys.version_info < (3, 8):
        print("[X] Python 3.8+ required. Current:", sys.version)
        return False
    print(f"[OK] Python version OK: {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if .env file exists."""
    if os.path.exists('.env'):
        print("[OK] .env file exists")
        return True
    else:
        print("[!] .env file not found (run setup_env.py or create manually)")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    required = [
        'fastapi',
        'uvicorn',
        'motor',
        'pymongo',
        'pydantic',
        'jose',
        'passlib',
        'dotenv'
    ]
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package} installed")
        except ImportError:
            missing.append(package)
            print(f"[X] {package} NOT installed")
    
    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True

def check_project_structure():
    """Check if project structure is correct."""
    required_files = [
        'app/main.py',
        'app/core/config.py',
        'app/core/database.py',
        'app/core/security.py',
        'app/services/org_service.py',
        'app/services/auth_service.py',
        'app/api/routes/org.py',
        'app/api/routes/admin.py',
        'requirements.txt'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"[OK] {file}")
        else:
            missing.append(file)
            print(f"[X] {file} missing")
    
    if missing:
        print(f"\n[!] Missing files: {len(missing)}")
        return False
    return True

def main():
    print("=" * 60)
    print("Organization Management Service - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Project Structure", check_project_structure),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        print("-" * 40)
        result = check_func()
        results.append(result)
    
    print()
    print("=" * 60)
    if all(results):
        print("[SUCCESS] All checks passed! Ready to run.")
        print()
        print("Next steps:")
        print("1. If .env is missing, run: python setup_env.py")
        print("2. Start the app: uvicorn app.main:app --reload --port 8000")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("[WARNING] Some checks failed. Please fix the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()

