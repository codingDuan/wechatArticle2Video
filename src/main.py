from fastapi import FastAPI
from starlette.responses import Response
from http import HTTPStatus

from .api.v1.router import api_router

app = FastAPI(
    title="Digital Human MVP Backend",
    description="Service for processing, cloning, and interacting with a digital human voice.",
    version="0.1.0",
)


@app.get("/health",
         tags=["Health Check"],
         summary="Health check endpoint",
         description="Returns a 200 OK status if the service is running.",
         )
def health_check():
    """
    Health check for the service.
    """
    return Response(status_code=HTTPStatus.OK.value)

# Placeholder for future routers
app.include_router(api_router, prefix="/api/v1")
