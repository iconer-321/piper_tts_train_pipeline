from pathlib import Path
import csv


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
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
        lines = []

        for txt_file in self.txt_dir.rglob("*.txt"):
            base_name = txt_file.stem
            converted_wav = self.wav_dir / f"{base_name}.wav"
            print(f"Found converted WAV for {base_name}.txt")

            if converted_wav.exists():
                with open(txt_file, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    print(converted_wav.name, text)
                    lines.append([converted_wav.name, text])
            else:
                print(f"Warning: Converted WAV not found for {base_name}.txt")
            txt_file.unlink()
        with open(self.output_csv, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter="|")
            writer.writerows(lines)

        print(f"Metadata written to: {self.output_csv}")
