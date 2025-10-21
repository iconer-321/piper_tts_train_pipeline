import csv
import shutil
from pathlib import Path

class MetadataGenerator:
    def __init__(
        self,
        txt_dir: str = ".",
        wav_dir: str = "wavs",
        output_csv: str = "metadata.csv",
    ):
        self.txt_dir = Path(txt_dir)
        self.wav_dir = Path(txt_dir) / wav_dir
        self.output_csv = Path(txt_dir) / output_csv

        if not self.txt_dir.exists() or not self.txt_dir.is_dir():
            raise FileNotFoundError(f"Text directory '{self.txt_dir}' does not exist.")
        if not self.wav_dir.exists() or not self.wav_dir.is_dir():
            raise FileNotFoundError(f"WAV directory '{self.wav_dir}' does not exist.")

    def generate(self):
        found_metadata = next(self.txt_dir.rglob("metadata.csv"), None)

        if found_metadata:
            print(f"✅ Found existing metadata.csv in '{found_metadata.parent}', copying to '{self.output_csv}'...")
            self.output_csv.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(found_metadata, self.output_csv)
            print(f"📋 Copied: '{found_metadata}' → '{self.output_csv}'")
            return

        # ❌ Case 2: No metadata.csv — run legacy generation
        print("⚙️ No existing metadata found — generating from text files...")
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
        lines = []

        for txt_file in self.txt_dir.rglob("*.txt"):
            base_name = txt_file.stem
            converted_wav = self.wav_dir / f"{base_name}.wav"
            print(f"Checking {base_name}.txt...")

            if converted_wav.exists():
                with open(txt_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    lines.append([converted_wav.name, text])
                    print(f"✅ Matched: {converted_wav.name} | {text}")
            else:
                print(f"⚠️ Missing WAV for: {base_name}.txt")

            txt_file.unlink()  # remove processed txt file

        with open(self.output_csv, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter="|")
            writer.writerows(lines)
        print(f"✅ Generated metadata CSV: {self.output_csv}")
