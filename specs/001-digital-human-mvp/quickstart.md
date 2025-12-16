# Quickstart: Digital Human MVP Backend

This guide provides the basic steps to set up the development environment and run the services for the Digital Human MVP.

## Prerequisites

-   Docker and Docker Compose
-   Python 3.11+
-   An S3-compatible object storage (like a local MinIO instance or an AWS S3 bucket)
-   API keys for:
    -   Deepgram
    -   LiveKit Cloud
    -   A managed LLM provider (e.g., Amazon Bedrock)

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    git checkout 001-digital-human-mvp
    ```

2.  **Configure Environment Variables:**
    Copy the `.env.example` file to `.env` and fill in the required credentials for the S3 bucket and cloud services.

    ```bash
    cp .env.example .env
    # Edit .env with your credentials
    ```

3.  **Install Python Dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Running the Services

The backend consists of two main parts: the asynchronous processing pipeline and the real-time interactive API.

### 1. Running the Data Processing Pipeline (User Story 1)

The pipeline is run via a command-line script.

1.  **Upload a raw audio file** to your S3-compatible bucket (e.g., `s3://your-bucket/raw/test.mp4`).

2.  **Execute the pipeline script:**
    ```bash
    python -m src.pipeline.run_pipeline --source-uri s3://your-bucket/raw/test.mp4
    ```
    This will execute all the steps (vocal separation, speech segmentation, quality filtering) and upload the clean audio segments to the configured output bucket (e.g., `s3://your-bucket/clean/`...). 

### 2. Running the Real-time API Server (User Story 3)

The API server handles the real-time interaction.

1.  **Start the FastAPI server:**
    ```bash
    uvicorn src.main:app --reload
    ```
    The server will be running on `http://localhost:8000`.

2.  **Connect a client:**
    Use a simple WebRTC client (a sample will be provided in the frontend part of the project) to connect to the LiveKit instance, which will then communicate with this backend server.

## Testing the API

The API is designed to be highly testable.

1.  **Run unit tests:**
    ```bash
    pytest tests/unit
    ```

2.  **Run integration tests:**
    (This requires the server to be running and configured correctly)
    ```bash
    pytest tests/integration
    ```

3.  **Test the data processing API endpoint:**
    While the server is running, you can use a tool like `curl` or Postman to create a processing job:
    ```bash
    curl -X POST http://localhost:8000/v1/processing/jobs \
    -H "Content-Type: application/json" \
    -d '{"source_uri": "s3://your-bucket/raw/another-test.mp4"}'
    ```

