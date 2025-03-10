import os
from dotenv import load_dotenv

# loading enviroment variables
load_dotenv()

# Dev Database configs
DB_USERNAME = os.getenv("DB_USERNAME", None)
DB_PASSWORD = os.getenv("DB_PASSWORD", None)
DB_HOSTNAME = os.getenv("DB_HOSTNAME", None)
DB_HOST = os.getenv("DB_HOST", None)
DB_PORT = os.getenv("DB_PORT", None)
DB_URI = f"""postgresql+asyncpg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_HOSTNAME}"""


# Redis configs
REDIS_HOST = os.getenv("REDIS_HOST", None)
REDIS_PORT = os.getenv("REDIS_PORT", None)

# By Pass OTP
BY_PASS_OTP = os.getenv("BY_PASS_OTP", None)

# JWT authentication configs
JWT_HASHING_ALGORITHM = os.getenv("JWT_HASHING_ALGORITHM", None)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", None)
JWT_ACCESS_TOKEN_EXPIRY_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRY_MINUTES", None)
JWT_REFRESH_TOKEN_EXPIRY_MINUTES = os.getenv("JWT_REFRESH_TOKEN_EXPIRY_MINUTES", None)