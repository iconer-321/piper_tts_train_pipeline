import os
import zipfile
from pathlib import Path


class PiperModelZipper:
    def __init__(self, model_dir: str):
        self.model_dir = Path(model_dir)
        if not self.model_dir.is_dir():
            raise ValueError(f"❌ Directory does not exist: {self.model_dir}")
        self.output_zip = self.model_dir.with_suffix('.zip')

    def zip_model(self):
        with zipfile.ZipFile(self.output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.model_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(self.model_dir)
                    zipf.write(file_path, arc_name)
        print(f"✅ Piper model zipped to: {self.output_zip}")



