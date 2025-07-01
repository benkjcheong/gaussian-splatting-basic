import os
from huggingface_hub import HfApi, upload_folder
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Define repo and folder
repo_id = "bcben/gaussian-splat"  # Change this to your repo
local_path = "../output"       # Path to folder to upload

# Instantiate API
api = HfApi()

# Create repo (optional, use exist_ok=True to skip error if it exists)
api.create_repo(repo_id=repo_id, repo_type="model", token=HF_TOKEN, exist_ok=True)

# Upload the folder
upload_folder(
    repo_id=repo_id,
    folder_path=local_path,
    repo_type="model",      # or "dataset"
    path_in_repo="",        # root of the repo
    token=HF_TOKEN
)

print(f"✅ Uploaded to: https://huggingface.co/{repo_id}")
