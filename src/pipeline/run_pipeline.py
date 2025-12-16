# T015: Main orchestrator for the audio processing pipeline.

import boto3
import os
import sys

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
)
from src.core.config import settings


def upload_to_s3(local_path: str, s3_key: str):
    """Placeholder for uploading a file to S3."""
    print(f"Uploading {local_path} to s3://{settings.S3_BUCKET_NAME}/{s3_key}")
    s3_client = boto3.client("s3", region_name=settings.AWS_REGION,
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    s3_client.upload_file(local_path, settings.S3_BUCKET_NAME, s3_key)
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

    # Final Step: Upload results to S3
    # final_s3_uris = []
    # for i, file_path in enumerate(final_audio_files):
    #     s3_clean_key = f"clean/{job_id}/segment_{i+1:04d}.wav"
    #     uri = upload_to_s3(file_path, s3_clean_key)
    #     final_s3_uris.append(uri)

    # print(f"Pipeline finished. Produced {len(final_s3_uris)} clean audio segments.")
    # return final_s3_uris

if __name__ == "__main__":
    # Example of how to run the pipeline
    run_full_pipeline("/Users/lianjia/Downloads/12101.mkv", "test-job-125")
