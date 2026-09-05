from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine, Base
from database.migrations import run_lightweight_migrations
from models import user, post, lajkovi, contact, social
from routers import (
    auth,
    contact,
    post as post_router,
    lajkovi,
    admin,
    recommendations,
    trending,
    collections,
    follow,
    author_stats,
)

Base.metadata.create_all(bind=engine)
run_lightweight_migrations()

app = FastAPI(title="AI Knowledge Sharing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(post_router.router)
app.include_router(lajkovi.router)
app.include_router(admin.router)
app.include_router(recommendations.router)
app.include_router(trending.router)
app.include_router(collections.router)
app.include_router(follow.router)
app.include_router(author_stats.router)


@app.get("/")
def pocetna():
    return {
        "message": "AI Knowledge Sharing API is running!",
        "modules": [
            "auth",
            "posts",
            "likes_comments_save",
            "ai_recommendations",
            "trending",
            "collections",
            "follow_interests",
            "author_stats",
            "admin",
        ],
    }
