#!/usr/bin/env python3
"""
Generate a secure JWT secret key for production deployment.
Run this script and copy the output to your deployment platform's environment variables.
"""
import secrets
import string

def generate_jwt_secret(length=64):
    """Generate a cryptographically secure secret key."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

if __name__ == "__main__":
    secret = generate_jwt_secret()
    print("🔐 Generated JWT Secret Key:")
    print(f"JWT_SECRET_KEY={secret}")
    print("\n💡 Copy this to your deployment platform's environment variables!")
    print("   - Render: Settings → Environment Variables")
    print("   - Railway: Variables tab")
    print("   - Heroku: heroku config:set JWT_SECRET_KEY='...'")
