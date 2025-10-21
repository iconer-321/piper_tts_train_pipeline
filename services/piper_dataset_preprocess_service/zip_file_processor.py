import os
import zipfile


class ZipFileProcessor:
    def __init__(self, zip_path: str):
        self.zip_path = zip_path

    def extract(self, extract_to: str = None) -> str:
        extract_path = extract_to or os.path.splitext(self.zip_path)[0]
        try:
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            print(f"✅ File unzipped successfully to: {extract_path}")
            return extract_path
        except zipfile.BadZipFile:
            print(f"❌ Failed to unzip: Bad zip file: {self.zip_path}")
        except Exception as e:
            print(f"❌ Error during unzipping: {e}")
        return ""
