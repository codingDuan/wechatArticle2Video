import os
from pydub import AudioSegment
import random # For mocking DNSMOS scores
import uuid

def _get_dnsmos_score(audio_path: str) -> dict:
    """Placeholder for DNSMOS quality scoring. Returns a mock score."""
    mock_ovrl_score = random.uniform(3.6, 4.5)  # Always return > 3.5 for placeholder
    print(f"  Mock DNSMOS score for {os.path.basename(audio_path)}: OVRL={mock_ovrl_score:.2f}")
    return {"OVRL": mock_ovrl_score}

def cut_and_filter(audio_segments_with_timestamps: dict, output_dir: str) -> list[str]:
    """Cuts audio based on timestamps and filters by DNSMOS score (placeholder)."""
    print(f"Cutting and filtering {len(audio_segments_with_timestamps)} unique source audio files...")

    high_quality_segments = []
    segment_counter = 1
    for original_audio_path, timestamps in audio_segments_with_timestamps.items():
        if not timestamps:
            print(f"  No speech timestamps for {os.path.basename(original_audio_path)}, skipping.")
            continue

        try:
            full_audio = AudioSegment.from_wav(original_audio_path)
            print(f"  Processing {os.path.basename(original_audio_path)} with {len(timestamps)} segments...")

            for i, (start_time, end_time) in enumerate(timestamps):
                start_ms = int(start_time * 1000)
                end_ms = int(end_time * 1000)
                
                if start_ms >= len(full_audio) or end_ms > len(full_audio) or start_ms >= end_ms:
                    print(f"    Warning: Invalid timestamp [{start_time:.2f}s, {end_time:.2f}s]. Skipping segment.")
                    continue

                segment = full_audio[start_ms:end_ms]
                
                # Save cut segment to a temporary path for scoring
                temp_cut_path = os.path.join(output_dir, f"temp_cut_{uuid.uuid4()}.wav")
                segment.export(temp_cut_path, format="wav")
                
                # DNSMOS scoring (placeholder)
                scores = _get_dnsmos_score(temp_cut_path)
                
                if scores["OVRL"] > 3.5:
                    # If high quality, move to a final path and add to list
                    final_segment_path = os.path.join(output_dir, f"filtered_{segment_counter:04d}.wav")
                    os.rename(temp_cut_path, final_segment_path)
                    high_quality_segments.append(final_segment_path)
                    print(f"    Segment {segment_counter} APPROVED (OVRL: {scores['OVRL']:.2f}) -> {os.path.basename(final_segment_path)}")
                    segment_counter += 1
                else:
                    # If low quality, delete the temporary file
                    print(f"    Segment REJECTED (OVRL: {scores['OVRL']:.2f}).")
                    os.remove(temp_cut_path)

        except Exception as e:
            print(f"  Error processing {os.path.basename(original_audio_path)}: {e}")

    print(f"Cutting and filtering finished. Produced {len(high_quality_segments)} high-quality segments.")
    return high_quality_segments
