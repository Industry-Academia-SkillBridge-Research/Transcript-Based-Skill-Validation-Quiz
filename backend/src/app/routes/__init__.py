from .admin import router as admin_router
from .transcript import router as transcript_router
from .skills import router as skills_router
from .parent_skills import router as parent_skills_router
from .quiz import router as quiz_router

__all__ = ["admin_router", "transcript_router", "skills_router", "parent_skills_router", "quiz_router"]
