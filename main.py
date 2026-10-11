from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.proposals import router as proposals_router
from routers.votes import router as votes_router

app = FastAPI(
    title="Community Digital Voting System",
    description="API for community proposals and voting with deadline and revocation support",
    version="1.0.0",
)

# CORS setup for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(proposals_router)
app.include_router(votes_router)


@app.get("/", summary="Health Check")
def home():
    return {
        "message": "Community Digital Voting System API is running",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }
