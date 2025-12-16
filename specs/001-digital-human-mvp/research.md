# Research: Digital Human MVP Backend

## 1. Cloud vs. Self-Hosted Audio Models

### Decision
For the MVP, we will proceed with **self-hosting the specialized audio models** (UVR5, inaSpeechSegmenter, GPT-SoVITS) using containerized Python services.

### Rationale
The core challenge of this project, as identified in the initial research report, is the high-complexity task of separating speech from background music that *also contains singing*.

-   **Specialization is Key**: The chosen open-source models (BS-Roformer in UVR5, inaSpeechSegmenter) are specifically designed or configured for this nuanced task. BS-Roformer excels at complex spectral separation, and inaSpeechSegmenter's key feature is its ability to semantically differentiate *speech* from *singing*.
-   **Cloud Service Limitations**: Standard cloud AI services (e.g., AWS Transcribe's audio redaction, Google's Speech-to-Text) are primarily designed for noise reduction (e.g., removing background hums) or speaker diarization. They are not optimized for separating two overlapping human vocal tracks (one speaking, one singing) and are highly likely to either fail or produce low-quality output, compromising the entire project foundation.
-   **Voice Cloning Fidelity**: GPT-SoVITS is chosen for its high-fidelity, few-shot voice cloning capability. While cloud providers offer TTS services (like AWS Polly's Neural TTS), they typically require more data and may not capture the specific nuances of the target speaker's voice as effectively as a purpose-built model like GPT-SoVITS.
-   **MVP Risk Reduction**: Relying on generic cloud services for the most critical and risky part of the project (data cleaning) would be a significant gamble. By self-hosting the proven, specialized models, we directly follow the successful path laid out in the research report, maximizing the chances of a successful MVP.

### Alternatives Considered
-   **Using only Cloud APIs**: Rejected due to the high risk of failing to meet the core requirement of clean data separation and high-fidelity voice cloning. The MVP's success hinges on solving this specific problem, which generic tools are not built for.
