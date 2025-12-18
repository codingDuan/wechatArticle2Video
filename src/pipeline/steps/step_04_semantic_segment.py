import os
import torch
import torchaudio

def semantic_segment(audio_paths: list[str]) -> dict:
    """Uses Silero's speech classifier to distinguish speech from music/noise.

    It processes each audio file and returns a dictionary mapping the file path
    to a list of (start, end) tuples for segments classified as 'speech'.
    """
    print(f"Performing semantic segmentation on {len(audio_paths)} segments using Silero Classifier...")

    try:
        # Load Silero classifier model and utils
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                      model='silero_classifier',
                                      trust_repo=True)
        (get_speech_probs, get_noise_probs, _, _) = utils
    except Exception as e:
        print(f"Error initializing Silero classifier: {e}")
        raise

    speech_timestamps_per_file = {}
    for audio_path in audio_paths:
        try:
            # Note: The classifier, like VAD, expects 16kHz mono audio.
            # The input from Demucs should already be in a compatible format, but we ensure it here.
            wav, sr = torchaudio.load(audio_path)
            if wav.shape[0] > 1: # If stereo, convert to mono
                wav = torch.mean(wav, dim=0, keepdim=True)
            if sr != 16000:
                resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
                wav = resampler(wav)

            # Get speech probabilities
            # The model returns probabilities for each timestamp
            speech_probs = get_speech_probs(wav, model)

            # Find segments where speech probability is high
            threshold = 0.5 # Confidence threshold
            speech_segments = []
            in_speech = False
            start_time = 0

            # This is a simplified logic to find contiguous speech segments.
            # A more robust implementation might use more advanced thresholding or smoothing.
            for i, prob in enumerate(speech_probs):
                is_speech = prob > threshold
                # Window size is typically 0.5s with 50% overlap, so each step is ~0.25s
                # This detail depends on the model's internal processing, we'll approximate.
                current_time = i * (wav.shape[1] / sr) / len(speech_probs)

                if is_speech and not in_speech:
                    in_speech = True
                    start_time = current_time
                elif not is_speech and in_speech:
                    in_speech = False
                    speech_segments.append((start_time, current_time))
            
            if in_speech: # Add the last segment if it was ongoing
                speech_segments.append((start_time, (wav.shape[1] / sr)))

            speech_timestamps_per_file[audio_path] = speech_segments
            print(f"  Processed {os.path.basename(audio_path)}: found {len(speech_segments)} speech segments.")
            
        except Exception as e:
            print(f"  Error during segmentation for {os.path.basename(audio_path)}: {e}")
            speech_timestamps_per_file[audio_path] = [] # Return empty list on error

    print("Semantic segmentation complete.")
    return speech_timestamps_per_file
