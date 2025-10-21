import subprocess
from pathlib import Path


class WavConverter:
    def __init__(self, input_dir: str = ".", output_dir: str = "wavs"):
        self.input_dir = Path(input_dir)
        if not self.input_dir.exists() or not self.input_dir.is_dir():
            raise FileNotFoundError(
                f"Input directory '{self.input_dir}' does not exist."
            )

        self.output_dir = self.input_dir / output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.supported_exts = [".mp3", ".mp4", ".webm", ".wav", ".m4a", ".flac", ".aac", ".ogg"]

    def convert_all_media_files(self):
        all_files = [
            file for file in self.input_dir.rglob("*")
            if file.is_file() and file.suffix.lower() in self.supported_exts
        ]
        for file in all_files:
            self.convert_to_wav(file)

    def convert_to_wav(self, filepath: Path):
        output_file = self.output_dir / f"{filepath.stem}.wav"

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(filepath),
            "-ar", "22050",
            "-ac", "1",
            "-sample_fmt", "s16",
            str(output_file),
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"✅ Converted: {filepath.relative_to(self.input_dir)} → {output_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to convert {filepath.name}: {e.stderr.decode()}")
        finally:
            filepath.unlink(missing_ok=True)
