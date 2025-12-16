from fastapi import APIRouter

# Import endpoint routers here once they are created
from .endpoints.processing import router as processing_router
# from .endpoints.interactive import router as interactive_router

api_router = APIRouter()

# Include endpoint routers here
api_router.include_router(processing_router, prefix="/processing", tags=["Data Processing"])
# api_router.include_router(interactive_router, prefix="/interactive", tags=["Interactive Session"])
