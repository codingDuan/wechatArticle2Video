# Digital Human MVP Backend

This project contains the backend services for a prototype digital human capable of real-time voice interaction. It includes a data processing pipeline for voice cloning and a real-time interaction server.

## Architecture Overview

The system is built in Python using a service-oriented architecture. Key components include:

-   **Data Processing Pipeline**: A series of scripts to process raw audio/video, extract clean speech, transcribe it, and format it for model training.
-   **LLM Service**: An abstraction for language models, supporting both OpenAI and Google Gemini, to generate conversational responses.
-   **TTS Service**: A service for text-to-speech, designed to use a high-fidelity voice cloning model like GPT-SoVITS.
-   **Real-time Interaction Service**: A service using LiveKit to manage the real-time flow of audio and orchestrate the STT, LLM, and TTS services.
-   **API Server**: A FastAPI application that exposes endpoints for data processing and real-time interaction.

## Prerequisites

-   Python 3.11+
-   Docker and Docker Compose
-   An S3-compatible object storage (e.g., MinIO, AWS S3)
-   API Keys for the following cloud services:
    -   OpenAI or Google Gemini (for the LLM)
    -   Deepgram (for real-time Speech-to-Text)
    -   LiveKit Cloud (for WebRTC-based real-time communication)

## Project Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd digital-human-backend
    ```

2.  **Create a Python virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    Create a `.env` file in the project root by copying the `.env.example` (not yet created). Fill in the necessary API keys and configuration for S3 and other services.

    **Example `.env`:**
    ```env
    # Cloud Services
    OPENAI_API_KEY="sk-..."
    GEMINI_API_KEY="..."
    DEEPGRAM_API_KEY="..."
    LIVEKIT_API_KEY="..."
    LIVEKIT_API_SECRET="..."

    # LLM Configuration
    LLM_PROVIDER="openai"  # or "gemini"

    # AWS S3 Configuration (or other S3-compatible storage)
    AWS_ACCESS_KEY_ID="..."
    AWS_SECRET_ACCESS_KEY="..."
    AWS_REGION="us-east-1"
    S3_BUCKET_NAME="your-digital-human-bucket"
    ```

## How to Run

### 1. Data Processing Pipeline

This offline pipeline processes a video or audio file to extract clean voice data and prepare it for training.

```bash
python src/pipeline/run_pipeline.py
```
*Note: You will need to modify the `run_pipeline.py` script to point to your local audio/video file.*

### 2. Real-time API Server

This server handles the real-time voice interaction.

```bash
uvicorn src.main:app --reload
```
The API will be available at `http://localhost:8000`.

## Testing

Run the unit tests to ensure all components are working as expected:

```bash
pytest
```
