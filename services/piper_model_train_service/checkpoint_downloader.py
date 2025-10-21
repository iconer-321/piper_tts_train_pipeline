import requests
from pathlib import Path

class CheckpointDownloader:
    def __init__(self, url: str, checkpoint_dir: str = "checkpoints", filename: str = None):
        self.url = url
        self.checkpoint_dir = Path(checkpoint_dir)
        self.filename = filename or self._extract_filename_from_url()
        self.save_path = self.checkpoint_dir / self.filename

    def download(self, overwrite: bool = False):
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        if self.save_path.exists() and not overwrite:
            print(f"✅ File already exists: {self.save_path}")
            return

        try:
            print(f"⬇️  Downloading checkpoint to: {self.save_path}")
            response = requests.get(self.url, stream=True)
            response.raise_for_status()

            with open(self.save_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print("✅ Download complete.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to download: {e}")


    def _extract_filename_from_url(self) -> str:
        return Path(self.url.split("?")[0]).name
