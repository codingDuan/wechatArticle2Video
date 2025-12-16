import os
import shutil
import subprocess
import tempfile

def separate_instrumentals(audio_paths: list[str], output_dir: str) -> list[str]:
    """Uses the Demucs command-line tool to separate vocals from other instruments.

    This approach is more robust and explicitly requests the vocal stem.
    """
    print(f"Separating instrumentals from {len(audio_paths)} segments using Demucs CLI...")

    vocal_segments_paths = []
    for i, audio_path in enumerate(audio_paths):
        print(f"  Processing {os.path.basename(audio_path)} for vocal separation...")
        
        # Use a temporary directory for demucs's output to keep things clean
        with tempfile.TemporaryDirectory() as demucs_output_dir:
            python_executable = "/Users/lianjia/Documents/workspace/wechatArticle2Video/.venv/bin/python"
            command = [
                python_executable, '-m', 'demucs',
                '--two-stems=vocals', # Explicitly separate vocals from the rest
                '-n', 'htdemucs_ft',  # Model name
                '-o', f'"{demucs_output_dir}"', # Output to a temporary directory
                '--', f'"{audio_path}"' # Input file path
            ]
            
            try:
                # We join the command to run it in a shell, which handles paths with spaces correctly
                subprocess.run(" ".join(command), check=True, capture_output=True, shell=True)

                # Demucs creates a nested directory structure: <out_dir>/<model_name>/<filename_stem>/vocals.wav
                input_filename_stem = os.path.splitext(os.path.basename(audio_path))[0]
                expected_vocal_path = os.path.join(
                    demucs_output_dir, 'htdemucs_ft', input_filename_stem, 'vocals.wav'
                )

                if os.path.exists(expected_vocal_path):
                    vocal_filename = f"vocals_{i+1:04d}.wav"
                    final_vocal_path = os.path.join(output_dir, vocal_filename)
                    shutil.move(expected_vocal_path, final_vocal_path)
                    vocal_segments_paths.append(final_vocal_path)
                    print(f"  Separated vocals saved to {os.path.basename(final_vocal_path)}")
                else:
                    print(f"  WARNING: Could not find vocal output for {os.path.basename(audio_path)}. Expected at: {expected_vocal_path}. Skipping.")

            except subprocess.CalledProcessError as e:
                print(f"  Error running Demucs for {os.path.basename(audio_path)}.")
                print(f"  Stderr: {e.stderr.decode()}")
                raise
            except Exception as e:
                print(f"  An unexpected error occurred during separation for {os.path.basename(audio_path)}: {e}")
                raise

    print(f"Instrumentals separation finished. Produced {len(vocal_segments_paths)} vocal chunks.")
    return vocal_segments_paths
