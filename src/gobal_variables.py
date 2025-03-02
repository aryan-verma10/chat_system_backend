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



DB_URI = f"""postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_HOSTNAME}"""