from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime


class RawAudio(BaseModel):
    source_uri: str = Field(..., description="URI pointing to the raw audio file (e.g., s3://bucket/raw/livestream.mp4)")
    job_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the processing job")
    status: str = Field(default="uploaded", description="Status of the raw audio (e.g., uploaded, processing, failed, completed)")


class CleanSpeechSegment(BaseModel):
    segment_uri: str = Field(..., description="URI to the clean .wav file (e.g., s3://bucket/clean/job-id/segment-001.wav)")
    source_job_id: UUID = Field(..., description="The ID of the job that produced this segment")
    duration_seconds: float = Field(..., description="Duration of the audio segment in seconds")
    dnsmos_score: float = Field(..., description="Calculated DNSMOS quality score")
    transcription: Optional[str] = Field(None, description="Text transcription of the speech")


class TTSModel(BaseModel):
    model_id: str = Field(..., description="Unique identifier for the trained model (e.g., speaker-name-v1)")
    model_uri: str = Field(..., description="URI to the trained model weights and config files")
    status: str = Field(default="training", description="Status of the model (training, ready, deprecated)")
    source_segments_uris: List[str] = Field(..., description="List of CleanSpeechSegment URIs used for training")


class InteractiveSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4, description="Unique identifier for the session")
    user_id: str = Field(..., description="Identifier for the user in the session")
    start_time: datetime = Field(default_factory=datetime.utcnow, description="Session start timestamp")
    end_time: Optional[datetime] = Field(None, description="Session end timestamp")
    conversation_history: List[dict] = Field(default=[], description="Structured log of conversation turns")
