# T016: Service to manage audio processing jobs.
import asyncio
from uuid import uuid4
from src.pipeline.run_pipeline import run_full_pipeline
from ..models.domain import RawAudio, CleanSpeechSegment
from typing import Dict, Any

# In-memory "database" for storing job status
jobs: Dict[str, Dict[str, Any]] = {}


class AudioProcessingService:
    @staticmethod
    async def create_new_job(local_file_path: str) -> str:
        """
        Creates and starts a new audio processing job.
        Returns the job ID.
        """
        job_id = str(uuid4())
        jobs[job_id] = {"status": "starting", "result": None}

        # Run the pipeline in the background
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None, AudioProcessingService._run_job, local_file_path, job_id)

        return job_id

    @staticmethod
    def get_job_status(job_id: str) -> Dict[str, Any]:
        """
        Retrieves the status and result of a job.
        """
        return jobs.get(job_id, {"status": "not_found"})

    @staticmethod
    def _run_job(local_file_path: str, job_id: str):
        """
        The actual job execution wrapper.
        """
        try:
            jobs[job_id]["status"] = "processing"
            result_uris = run_full_pipeline(local_file_path, job_id)
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["result"] = result_uris
        except Exception as e:
            print(f"Job {job_id} failed: {e}")
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = str(e)


audio_processing_service = AudioProcessingService()
