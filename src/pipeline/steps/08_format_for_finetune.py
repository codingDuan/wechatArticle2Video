import json
import os

def format_for_finetuning(transcription_path: str, output_dir: str) -> tuple[str, str]:
    """
    Converts the transcription file into JSONL formats required for fine-tuning
    OpenAI and Gemini models.
    """
    print(f"Formatting transcriptions from {transcription_path} for fine-tuning...")

    try:
        with open(transcription_path, 'r', encoding='utf-8') as f:
            transcriptions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading transcription file: {e}")
        return "", ""

    openai_output_path = os.path.join(output_dir, "finetune_openai.jsonl")
    gemini_output_path = os.path.join(output_dir, "finetune_gemini.jsonl")

    # Format for OpenAI: typically a user/assistant conversation format
    with open(openai_output_path, 'w', encoding='utf-8') as f_openai:
        for item in transcriptions:
            record = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that speaks in the style of the user."}, 
                    {"role": "user", "content": "Transcribe the following audio segment."}, 
                    {"role": "assistant", "content": item.get("transcription", "")}
                ]
            }
            f_openai.write(json.dumps(record, ensure_ascii=False) + '\n')

    # Format for Gemini: typically a text-to-text format
    with open(gemini_output_path, 'w', encoding='utf-8') as f_gemini:
        for item in transcriptions:
            record = {
                "text": f"input: Transcribe this. output: {item.get('transcription', '')}"
            }
            f_gemini.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"Formatted files for fine-tuning created:")
    print(f"  - OpenAI: {openai_output_path}")
    print(f"  - Gemini: {gemini_output_path}")
    
    return openai_output_path, gemini_output_path
