import torch
import torchaudio
import os
import soundfile as sf
from pydub import AudioSegment
import uuid

# Constants for segment merging
MAX_DURATION_S = 28.0  # seconds
MAX_SILENCE_S = 1.5    # seconds

def _load_audio_for_vad(audio_path: str, target_sr: int = 16000):
    """Loads audio and resamples to target_sr for VAD model."""
    audio, sr = sf.read(audio_path)
    audio_tensor = torch.tensor(audio).float()

    # Convert to mono if stereo
    if audio_tensor.ndim > 1:
        audio_tensor = audio_tensor.mean(dim=1)

    if sr != target_sr:
        resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=target_sr)
        audio_tensor = resampler(audio_tensor)
        
    return audio_tensor, target_sr

def apply_vad(audio_path: str, output_dir: str) -> list[str]:
    """
    Uses Silero VAD to find speech timestamps, then merges them into longer segments
    (up to MAX_DURATION_S) and saves them to the output directory.
    """
    print(f"Applying VAD and merging segments for {audio_path}...")

    # Load Silero VAD model
    model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', trust_repo=True)
    (get_speech_timestamps, _, _, _, _) = utils

    # Load and preprocess audio for VAD
    wav_tensor, sr = _load_audio_for_vad(audio_path)

    # Get initial speech timestamps
    speech_timestamps = get_speech_timestamps(wav_tensor, model, sampling_rate=sr)
    print(f"Found {len(speech_timestamps)} initial speech intervals.")

    if not speech_timestamps:
        print("No speech detected.")
        return []

    # Merge timestamps
    merged_timestamps = []
    current_start = speech_timestamps[0]['start']
    current_end = speech_timestamps[0]['end']

    for i in range(1, len(speech_timestamps)):
        next_start = speech_timestamps[i]['start']
        next_end = speech_timestamps[i]['end']
        
        silence_duration_s = (next_start - current_end) / sr
        potential_duration_s = (next_end - current_start) / sr

        if silence_duration_s < MAX_SILENCE_S and potential_duration_s < MAX_DURATION_S:
            # Merge: extend the current segment
            current_end = next_end
        else:
            # Split: save the current segment and start a new one
            merged_timestamps.append({'start': current_start, 'end': current_end})
            current_start = next_start
            current_end = next_end
    
    # Add the last segment
    merged_timestamps.append({'start': current_start, 'end': current_end})
    
    print(f"Merged into {len(merged_timestamps)} segments.")

    # Export merged segments
    segmented_audio_paths = []
    full_audio = AudioSegment.from_wav(audio_path)

    for i, timestamp in enumerate(merged_timestamps):
        start_ms = timestamp['start'] / sr * 1000
        end_ms = timestamp['end'] / sr * 1000
        segment = full_audio[start_ms:end_ms]

        segment_filename = f"vad_segment_{i+1:04d}.wav"
        segment_path = os.path.join(output_dir, segment_filename)
        
        segment.export(segment_path, format="wav")
        segmented_audio_paths.append(segment_path)

    print(f"VAD and merging complete. Produced {len(segmented_audio_paths)} final speech chunks.")
    return segmented_audio_paths
