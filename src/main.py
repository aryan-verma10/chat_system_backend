from fastapi import FastAPI
from routers import router


app = FastAPI()

# including apis in main
app.include_router(router)
