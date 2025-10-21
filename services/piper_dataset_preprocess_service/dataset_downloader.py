import os
from urllib.parse import urlparse

import requests


class DatasetDownloader:
    def __init__(self, url: str, output_path: str = None, chunk_size: int = 1024 * 1024):
        self.url = url
        self.chunk_size = chunk_size
        self.output_path = output_path or self._extract_filename_from_url(url)

    def download(self):
        try:
            with requests.get(self.url, stream=True) as response:
                response.raise_for_status()
                with open(self.output_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=self.chunk_size):
                        if chunk:
                            f.write(chunk)
            print(f"✅ File downloaded successfully: {self.output_path}")
        except requests.exceptions.HTTPError as http_err:
            print(f"❌ HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"❌ Connection error: {conn_err}")
        except requests.exceptions.RequestException as e:
            print(f"❌ General error: {e}")

    @staticmethod
    def _extract_filename_from_url(url: str) -> str:
        """Extract file name from URL path."""
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded.zip"
        return filename
