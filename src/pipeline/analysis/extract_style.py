import json
import os
from collections import Counter
import re

def extract_style_dictionary(transcription_path: str, output_dir: str) -> str:
    """
    Analyzes the transcription file to build a "style dictionary" of the speaker's
    common filler words and phrases. This is a placeholder implementation.

    A real implementation would be more sophisticated, possibly using TF-IDF
    against a baseline corpus of "standard" speech to identify unique vocal tics,
    or using part-of-speech tagging to find interjections.
    """
    print(f"Extracting style dictionary from {transcription_path} (placeholder)...")

    try:
        with open(transcription_path, 'r', encoding='utf-8') as f:
            transcriptions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading transcription file: {e}")
        return ""

    # Consolidate all transcription text into a single block
    full_text = " ".join([item.get("transcription", "") for item in transcriptions])
    
    # Simple word frequency count
    # Remove punctuation and convert to lowercase
    words = re.findall(r'\b\w+\b', full_text.lower())
    word_counts = Counter(words)

    # In this placeholder, we'll assume the most common words that are also short
    # are the filler words. This is a very naive assumption.
    style_dictionary = {
        word: count for word, count in word_counts.items() 
        if len(word) <= 3 and count > len(transcriptions) // 4 # Appears in > 25% of segments
    }

    output_path = os.path.join(output_dir, "style_dictionary.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(style_dictionary, f, ensure_ascii=False, indent=4)

    print(f"Style dictionary extracted and saved to {output_path}")
    return output_path
