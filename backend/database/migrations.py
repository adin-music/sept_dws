from sqlalchemy import text
from database.db import engine


def run_lightweight_migrations():
    statements = [
        "ALTER TABLE posts ADD COLUMN IF NOT EXISTS link_url VARCHAR",
        "ALTER TABLE posts ADD COLUMN IF NOT EXISTS content_type VARCHAR DEFAULT 'clanak'",
        "ALTER TABLE posts ADD COLUMN IF NOT EXISTS category VARCHAR DEFAULT 'tehnologija'",
        "ALTER TABLE posts ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0",
        "ALTER TABLE posts ADD COLUMN IF NOT EXISTS shares_count INTEGER DEFAULT 0",
        "ALTER TABLE posts ADD COLUMN IF NOT EXISTS read_time_minutes INTEGER DEFAULT 1",
    ]
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
