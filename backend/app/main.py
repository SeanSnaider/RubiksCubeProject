"""
FastAPI Application Entry Point

This file creates and configures the main FastAPI application.
FastAPI is a modern Python web framework that provides:
- Automatic API documentation (Swagger UI at /docs)
- Request/response validation using Pydantic models
- Async support for high performance
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.controllers import cube_controller, solve_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

# Create the FastAPI application instance
app = FastAPI(
    title="Rubik's Cube API",
    version="1.0.0",
    description="REST API for Rubik's Cube manipulation, solving, and solve time tracking",
    lifespan=lifespan 
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows your React frontend (running on port 5173) to make requests
# to this backend (running on port 8000). Without CORS, browsers block
# requests between different origins for security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:5173",   # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Health check endpoint - useful for testing if server is running
@app.get("/")
def root():
    """Root endpoint - confirms API is running"""
    return {"message": "Rubik's Cube API is running!", "docs": "/docs"}


app.include_router(
    cube_controller.router,
    prefix="/api/cube",  # All routes will start with /api/cube
    tags=["cube"]        # Groups endpoints in the docs
)

app.include_router(
    solve_controller.router, 
    prefix="/api/solves",
    tags=["solves"]
)


