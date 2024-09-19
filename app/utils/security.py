from passlib.context import CryptContext

# Create a password context for hashing and verifying
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain-text password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a plain-text password against a hashed password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
