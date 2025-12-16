# Implementation Plan: Digital Human MVP Backend

**Branch**: `001-digital-human-mvp` | **Date**: 2025-12-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-digital-human-mvp/spec.md`

## Summary

This plan outlines the backend architecture for the Digital Human MVP. The primary goal is to build a modular, testable system in Python that orchestrates the data processing, voice cloning, and real-time interaction components. The architecture prioritizes managed cloud services for inference and real-time communication to align with the "Simplicity is Key" MVP principle, while allowing for self-hosted, specialized open-source models where necessary to meet quality requirements.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI (for API), PyTest (for testing), Docker
**Storage**: S3-compatible object storage (e.g., AWS S3, MinIO) for audio assets.
**Testing**: PyTest for unit and integration tests. Each service will have dedicated tests.
**Target Platform**: Containerized services running on a cloud platform (e.g., AWS ECS, Google Cloud Run).
**Project Type**: Single backend project with a modular, service-oriented architecture.

**Key Technology Decisions**:
-   **Data Processing Pipeline (US1)**: Self-hosted containerized Python scripts using **UVR5 (BS-Roformer)** and **inaSpeechSegmenter**. Cloud offerings are not specialized enough to guarantee the required separation quality for this core task.
-   **Voice Cloning & Synthesis (US2)**: Self-hosted **GPT-SoVITS** model exposed via an internal API. This is necessary to achieve the high-fidelity voice cloning required by the spec.
-   **Speech-to-Text (US3)**: **Deepgram Nova-2** (Cloud Service). Chosen for its low latency as recommended in the research.
-   **LLM (US3)**: **Amazon Bedrock / Google Vertex AI** (Cloud Service) running a base model like Llama-3 or Qwen-2.5. This aligns with the user's preference for managed services to reduce operational overhead for the MVP.
-   **Real-time Communication (US3)**: **LiveKit Cloud**. A managed WebRTC service is the simplest way to achieve low-latency, full-duplex audio streaming and barge-in.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **MVP First:** Yes. The plan focuses on delivering the three user stories sequentially, with P1 and P2 providing the core assets and P3 providing the user-facing interactive MVP.
- **Core Functionality Only:** Yes. The architecture strictly supports the defined functional requirements without adding any non-essential features.
- **Simplicity is Key:** Yes. The plan uses managed services (LiveKit, Bedrock, Deepgram) wherever possible to reduce complexity. The project is a single monolith with logical separation, not a complex microservices architecture.
- **Manual Operations Acceptable:** Yes. The data processing pipeline is designed as an offline job, not a real-time service, which is simpler to implement.
- **Feedback-Driven Iteration:** Yes. The modular design allows individual components (like the LLM or TTS model) to be swapped or updated based on feedback without redesigning the entire system.

## Project Structure

### Documentation (this feature)

```text
specs/001-digital-human-mvp/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
# Option 1: Single project (DEFAULT)
src/
├── api/                  # FastAPI endpoints and routing
│   ├── __init__.py
│   └── v1/
│       ├── endpoints/
│       │   ├── processing.py # Endpoints for data processing jobs
│       │   └── interactive.py# WebSocket/RTC handlers for LiveKit
│       └── router.py
├── core/                 # App configuration, settings
│   ├── __init__.py
│   └── config.py
├── services/             # Business logic for each domain
│   ├── __init__.py
│   ├── audio_processing_service.py # Orchestrates UVR5, inaSpeechSegmenter, etc.
│   ├── tts_service.py              # Interface to GPT-SoVITS
│   └── livekit_service.py          # Handles LiveKit agent logic
├── models/               # Pydantic models for data structures
│   ├── __init__.py
│   └── domain.py         # Defines RawAudio, CleanSpeechSegment, etc.
└── pipeline/             # Standalone scripts for the data processing
    ├── __init__.py
    ├── steps/
    │   ├── 01_separate_vocals.py
    │   ├── 02_segment_speech.py
    │   └── 03_quality_filter.py
    └── run_pipeline.py

tests/
├── integration/
│   └── test_api_endpoints.py
└── unit/
    └── test_services.py
```

**Structure Decision**: A single Python project is chosen for simplicity, aligning with the MVP principles. The code is organized by function (api, services, pipeline) to ensure clear separation of concerns and high testability, as requested.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| *None* | | |