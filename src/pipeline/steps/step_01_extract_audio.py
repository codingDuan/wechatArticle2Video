import subprocess
import os
import tempfile
import uuid

def extract_audio(video_path: str, output_dir: str) -> str:
    """Uses FFmpeg to extract the audio track from a video file and converts it to 16-bit 44.1kHz WAV format."""
    print(f"Extracting audio from {video_path}...")

    # Generate a unique filename in the specified output directory
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_audio_path = os.path.join(output_dir, f"{base_name}_extracted.wav")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-y",  # Overwrite output file if it exists
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM signed 16-bit little-endian
        "-ar", "44100",  # 44.1 kHz sample rate
        "-ac", "1",  # Mono audio
        output_audio_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, timeout=180)
        print(f"Audio extracted to {output_audio_path}")
        return output_audio_path
    except subprocess.TimeoutExpired as e:
        print(f"FFmpeg command timed out after 3 minutes.")
        print(f"Stdout: {e.stdout.decode() if e.stdout else 'N/A'}")
        print(f"Stderr: {e.stderr.decode() if e.stderr else 'N/A'}")
        raise
    except subprocess.CalledProcessError as e:
        print(f"Error during audio extraction: {e}")
        print(f"Stdout: {e.stdout.decode()}")
        print(f"Stderr: {e.stderr.decode()}")
        raise
    except FileNotFoundError:
        print("FFmpeg not found. Please ensure FFmpeg is installed and accessible in your PATH.")
        raise
