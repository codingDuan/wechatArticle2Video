# T015: Main orchestrator for the audio processing pipeline.

import os
# This MUST be set before any other imports, especially before tensorflow or torch
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import boto3
import sys
import uuid

# When running this script directly, add the project root to the Python path
if __name__ == "__main__":
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# With the path set up, we can now use absolute imports
from src.pipeline.steps import (
    step_01_extract_audio as _01_extract_audio,
    step_02_vad_segment as _02_vad_segment,
    step_03_separate_instrumentals as _03_separate_instrumentals,
    step_04_semantic_segment as _04_semantic_segment,
    step_05_cut_and_filter as _05_cut_and_filter,
    step_06_normalize_audio as _06_normalize_audio,
    step_07_transcribe as _07_transcribe,
    post_process_transcription as _post_process_transcription,
    step_08_format_for_finetune as _08_format_for_finetune,
)
from src.pipeline.analysis import extract_style
from src.core.config import settings


def upload_to_s3(local_path: str, s3_key: str):
    """Placeholder for uploading a file to S3."""
    print(f"Uploading {local_path} to s3://{settings.S3_BUCKET_NAME}/{s3_key}")
    # s3_client = boto3.client("s3", region_name=settings.AWS_REGION,
    #                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    #                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    # s3_client.upload_file(local_path, settings.S3_BUCKET_NAME, s3_key)
    return f"s3://{settings.S3_BUCKET_NAME}/{s3_key}"


def run_full_pipeline(local_video_path: str, job_id: str):
    """
    Executes the complete audio processing pipeline from a local video file.
    """
    print(f"Starting pipeline for {local_video_path} with job_id {job_id}")

    # Create and define the output directory for this job
    output_dir = os.path.abspath(os.path.join("output", job_id))
    os.makedirs(output_dir, exist_ok=True)
    print(f"All temporary files will be stored in: {output_dir}")

    # T008: Upload original file to S3 for traceability
    # s3_raw_key = f"raw/{job_id}/{os.path.basename(local_video_path)}"
    # upload_to_s3(local_video_path, s3_raw_key)

    # Step 1: Extract Audio
    extracted_audio = _01_extract_audio.extract_audio(local_video_path, output_dir)

    # Step 2: VAD Segmentation
    speech_chunks = _02_vad_segment.apply_vad(extracted_audio, output_dir)

    # Step 3: Separate Instrumentals
    vocal_chunks = _03_separate_instrumentals.separate_instrumentals(speech_chunks, output_dir)

    # Step 4: Semantic Segmentation
    speech_timestamps = _04_semantic_segment.semantic_segment(vocal_chunks)

    # Step 5: Cut and Filter
    high_quality_chunks = _05_cut_and_filter.cut_and_filter(speech_timestamps, output_dir)

    # Step 6: Normalize Audio
    final_audio_files = _06_normalize_audio.normalize_audio(high_quality_chunks, output_dir)

    # Step 7: Transcribe Audio
    transcription_file = _07_transcribe.transcribe_audio(final_audio_files, output_dir)
    
    # Step 7b: Post-process transcriptions
    post_processed_file = _post_process_transcription.post_process_transcriptions(transcription_file)
    
    # Step 7c: Extract Style Dictionary
    extract_style.extract_style_dictionary(post_processed_file, output_dir)

    # Step 8: Format for Fine-tuning
    _08_format_for_finetune.format_for_finetuning(post_processed_file, output_dir)


    # Final Step: Upload results to S3
    # final_s3_uris = []
    # for i, file_path in enumerate(final_audio_files):
    #     s3_clean_key = f"clean/{job_id}/segment_{i+1:04d}.wav"
    #     uri = upload_to_s3(file_path, s3_key)
    #     final_s3_uris.append(uri)

    # print(f"Pipeline finished. Produced {len(final_s3_uris)} clean audio segments.")
    # return final_s3_uris

if __name__ == "__main__":
    # Example of how to run the pipeline
    # Assumes a file named `demo.wav` exists in the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    demo_file = os.path.join(project_root, "demo.wav")
    if not os.path.exists(demo_file):
        print(f"Error: Demo file not found at {demo_file}")
        print("Please add a `demo.wav` file to the project root to run the pipeline.")
    else:
        run_full_pipeline(demo_file, f"test-job-{uuid.uuid4().hex[:6]}")