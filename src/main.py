from fastapi import FastAPI
from routers import router
from database import lifespan


app = FastAPI(lifespan=lifespan)


# including apis in main
app.include_router(router)
