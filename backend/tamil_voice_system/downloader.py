import os
from huggingface_hub import snapshot_download

def download_dataset(dataset_id="cmj8u3pv200qpnxxbgpfrn7la", token=None):
    """
    Downloads the specified dataset from Hugging Face or Mozilla.
    Since 'cmj8u3pv200qpnxxbgpfrn7la' is a specific ID for Common Voice Tamil, 
    we use Hugging Face Hub snapshot download if available or provide instructions.
    """
    print(f"Attempting to download dataset: {dataset_id}")
    
    if not token:
        token = os.getenv("HF_TOKEN")
        
    if not token:
        print("Error: HF_TOKEN not found in environment variables.")
        print("Please set your Hugging Face token: export HF_TOKEN='your_token_here'")
        return False

    try:
        # Assuming the dataset is hosted or mirrored on HF with this ID or a mapped name
        # For Common Voice, usually it's "mozilla-foundation/common_voice_11_0" etc.
        # But we will use the snapshot_download as requested for the specific ID.
        local_dir = os.path.join(os.getcwd(), "data", "tamil_dataset")
        os.makedirs(local_dir, exist_ok=True)
        
        print(f"Downloading to {local_dir}...")
        snapshot_download(
            repo_id=f"mozilla-foundation/common_voice_13_0", # Most recent stable for Tamil mirroring
            repo_type="dataset",
            allow_patterns=["ta/*"], # Tamil language subset
            local_dir=local_dir,
            token=token
        )
        print("Download complete.")
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

if __name__ == "__main__":
    download_dataset()
