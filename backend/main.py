from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router
from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS with explicit settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow all origins (use ["http://localhost:5173"] in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Serve static files (certificate images)
app.mount("/modified_certs", StaticFiles(directory="modified_certs"), name="modified_certs")

# Include the routes
app.include_router(router)
