# T017: API endpoints for audio processing.
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from starlette.responses import JSONResponse
from src.services.audio_processing_service import audio_processing_service
import shutil
import os

router = APIRouter()

# A temporary directory to store uploaded files
TEMP_DIR = "/tmp/audio_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


@router.post("/jobs", status_code=202, summary="Create a new audio processing job")
async def create_processing_job(file: UploadFile = File(...)):
    """
    Accepts a video file, saves it locally, and starts the processing pipeline.
    """
    try:
        temp_path = os.path.join(TEMP_DIR, file.filename)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        job_id = await audio_processing_service.create_new_job(temp_path)
        
        return {"job_id": job_id, "message": "Job started successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start job: {e}")


@router.get("/jobs/{job_id}", summary="Get the status of a processing job")
def get_job_status(job_id: str):
    """
    Retrieves the current status and, if completed, the results of a processing job.
    """
    status = audio_processing_service.get_job_status(job_id)
    if status["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Job not found")
    return status

