# super simple "AI" matching - its just math with extra steps
# professor said AI feed so we pretend this is smart

from sqlalchemy.orm import Session
from models.post import Post
from models.lajkovi import Like, SavedPost
from models.social import UserInterest, UserFollow


def get_recommended_posts(db: Session, user_id: int, limit: int = 10):
    # grab all posts from db like a shopping bag
    posts = db.query(Post).all()
    if not posts:
        return []

    # what topics user clicked on homepage
    interests = {i.category for i in db.query(UserInterest).filter_by(user_id=user_id).all()}

    # posts user already liked or saved - we copy their categories
    liked_post_ids = [l.post_id for l in db.query(Like).filter_by(user_id=user_id).all()]
    saved_post_ids = [s.post_id for s in db.query(SavedPost).filter_by(user_id=user_id).all()]
    followed_ids = [f.followed_user_id for f in db.query(UserFollow).filter_by(follower_id=user_id).all()]

    liked_categories = set()
    for post in posts:
        if post.id in liked_post_ids or post.id in saved_post_ids:
            cat = post.category.value if hasattr(post.category, "value") else str(post.category)
            liked_categories.add(cat)

    scored = []
    for post in posts:
        category_value = post.category.value if hasattr(post.category, "value") else str(post.category)
        score = 0

        # interest match = big points
        if category_value in interests:
            score += 4

        # user likes similar stuff = medium points
        if category_value in liked_categories:
            score += 3

        # follow author = small bonus
        if post.author_id in followed_ids:
            score += 2

        # popular posts get tiny boost (cap so one post doesnt win forever)
        score += min(post.views or 0, 20) * 0.1

        scored.append((score, post))

    # highest score first = "AI recommendation"
    scored.sort(key=lambda item: item[0], reverse=True)
    return [post for _, post in scored[:limit]]
