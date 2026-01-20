import os
import json
import openai
from src.core.config import get_settings

def transcribe_audio(audio_paths: list[str], output_dir: str, model_name: str = None) -> str:
    """
    Transcribes a list of audio segments using the OpenAI Whisper API and returns
    the path to the consolidated transcription file.
    
    The model can be specified as a parameter or configured in the .env file
    via OPENAI_WHISPER_MODEL.
    """
    api_key = get_settings().OPENAI_API_KEY
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

    client = openai.OpenAI(api_key=api_key)
    
    # Use the provided model_name or fall back to the one from settings
    whisper_model = model_name if model_name else get_settings().OPENAI_WHISPER_MODEL
    
    print(f"Starting transcription for {len(audio_paths)} audio segments using OpenAI model: {whisper_model}...")

    transcriptions = []
    for audio_path in audio_paths:
        print(f"  Transcribing {os.path.basename(audio_path)}...")
        try:
            with open(audio_path, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model=whisper_model,
                    file=audio_file,
                    response_format="json" 
                )
            
            transcription_text = response.text
            
            transcription_data = {
                "audio_path": audio_path,
                "transcription": transcription_text,
                "model": whisper_model,
                "details": dict(response) # Store full response for more details if needed
            }
            transcriptions.append(transcription_data)
            print(f"  Successfully transcribed {os.path.basename(audio_path)}")
        
        except Exception as e:
            print(f"  Error transcribing {os.path.basename(audio_path)}: {e}")
            # Optionally, add an error record to the output file
            error_data = {
                "audio_path": audio_path,
                "transcription": None,
                "error": str(e)
            }
            transcriptions.append(error_data)

    # Save all transcriptions to a single JSON file
    output_file_path = os.path.join(output_dir, "transcriptions_openai.json")
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(transcriptions, f, ensure_ascii=False, indent=4)

    print(f"Transcription finished. Results saved to {output_file_path}")
    return output_file_path