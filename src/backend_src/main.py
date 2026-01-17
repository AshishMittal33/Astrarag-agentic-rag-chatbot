import logging
from fastapi import FastAPI
from src.backend_src.api.chat import router as chat_router

from src.backend_src.config.backend_settings import Settings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app=FastAPI()

app.include_router(chat_router)

setting= Settings()

if __name__ =="__main__":
    import uvicorn
    uvicorn.run(
        "src.backend_src.main:app",
        host=setting.API_HOST,
        port=setting.API_PORT
    )