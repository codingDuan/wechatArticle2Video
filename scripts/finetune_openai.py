import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

def finetune_openai_model(dataset_path: str):
    """
    Uploads a dataset and starts a fine-tuning job using the OpenAI API.
    This is a placeholder and example implementation.
    """
    if not openai.api_key:
        print("Error: OPENAI_API_KEY is not set in the environment variables.")
        return

    print(f"Starting OpenAI fine-tuning process for dataset: {dataset_path}")

    # Step 1: Upload the dataset
    try:
        with open(dataset_path, "rb") as f:
            response = openai.File.create(file=f, purpose='fine-tune')
        file_id = response.id
        print(f"Dataset uploaded successfully. File ID: {file_id}")
    except Exception as e:
        print(f"Error uploading dataset: {e}")
        return

    # Step 2: Create a fine-tuning job
    try:
        # Note: 'model' should be a base model compatible with fine-tuning,
        # e.g., "gpt-3.5-turbo". This may change with API updates.
        job = openai.FineTuningJob.create(
            training_file=file_id,
            model="gpt-3.5-turbo"
        )
        job_id = job.id
        print(f"Fine-tuning job created successfully. Job ID: {job_id}")
        print("You can monitor the job status on the OpenAI dashboard.")
    except Exception as e:
        print(f"Error creating fine-tuning job: {e}")

if __name__ == "__main__":
    # This is an example of how to run the script.
    # It assumes that the formatted JSONL file is in the 'output/test-job-...' directory.
    # You would need to replace 'your_job_id' with an actual job ID from the pipeline.
    
    # Simple check for a placeholder dataset
    placeholder_dataset = "output/placeholder_job/finetune_openai.jsonl"
    if os.path.exists(placeholder_dataset):
        finetune_openai_model(placeholder_dataset)
    else:
        print(f"Placeholder dataset not found at {placeholder_dataset}")
        print("Please run the full pipeline first to generate the finetuning data,")
        print("or create a dummy file at that location to test this script.")
