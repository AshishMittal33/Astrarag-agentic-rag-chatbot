from dotenv import load_dotenv
from pydantic_settings import BaseSettings


load_dotenv()

class AgentsSettings(BaseSettings):
    GROQ_API_URL: str
    DOCUMENTS_DIR: str
    VECTOR_STORE_DIR: str
    COLLECTION_NAME: str
    MODEL_NAME: str
    MODEL_TEMPREATURE: float


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"