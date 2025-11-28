from fastapi import FastAPI
from database import engine, Base
from routers import memo, ffxiv
from fastapi.middleware.cors import CORSMiddleware

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include Routers
app.include_router(memo.router)
app.include_router(ffxiv.router)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=7979)
