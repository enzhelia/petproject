from fastapi import FastAPI

from .endpoints.api_objects import router

app = FastAPI(title="ApiYandexDisk")
app.include_router(router)
