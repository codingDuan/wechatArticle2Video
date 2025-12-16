# Data Models: Digital Human MVP

This document outlines the key data entities for the project, as identified in the feature specification. These will be implemented using Pydantic for type-safe data handling within the Python services.

## Entity Definitions

### 1. RawAudio
Represents the initial, unprocessed audio asset provided to the system.

-   **source_uri** (string): A URI pointing to the location of the raw audio file (e.g., `s3://bucket-name/raw/livestream.mp4`).
-   **job_id** (string, UUID): A unique identifier for the processing job associated with this audio.
-   **status** (string): The current status of the raw audio (e.g., `uploaded`, `processing`, `failed`, `completed`).

### 2. CleanSpeechSegment
Represents a single, processed audio chunk that contains only the clean, high-quality speech of the target speaker. This is the primary output of the data processing pipeline and the input for TTS training.

-   **segment_uri** (string): A URI pointing to the location of the clean .wav file (e.g., `s3://bucket-name/clean/job-id/segment-001.wav`).
-   **source_job_id** (string, UUID): The ID of the job that produced this segment.
-   **duration_seconds** (float): The duration of the audio segment in seconds.
-   **dnsmos_score** (float): The calculated DNSMOS quality score for the segment.
-   **transcription** (string, optional): The text transcription of the speech in the segment.

### 3. TTSModel
Represents a trained voice model ready for synthesis.

-   **model_id** (string): A unique identifier for the trained model (e.g., `speaker-name-v1`).
-   **model_uri** (string): A URI pointing to the location of the trained model weights and configuration files (e.g., `s3://bucket-name/models/speaker-name-v1/`).
-   **status** (string): The status of the model (`training`, `ready`, `deprecated`).
-   **source_segments** (list[string]): A list of URIs of the `CleanSpeechSegment`s used to train this model.

### 4. InteractiveSession
Represents a single real-time conversation between a user and the digital human.

-   **session_id** (string, UUID): A unique identifier for the session.
-   **user_id** (string): An identifier for the user in the session.
-   **start_time** (datetime): The timestamp when the session began.
-   **end_time** (datetime, optional): The timestamp when the session ended.
-   **conversation_history** (list[object]): A structured log of the conversation turns, with each entry containing the user's transcription and the digital human's response.
