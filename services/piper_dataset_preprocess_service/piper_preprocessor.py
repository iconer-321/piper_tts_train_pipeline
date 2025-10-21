import os
import subprocess


class PiperDatasetPreprocessor:
    def __init__(
            self,
            input_dir,
            output_dir,
            language="bn",
            dataset_format="ljspeech",
            sample_rate=22050,
            single_speaker=True,
            max_workers=1
    ):
        self.input_dir = os.path.expanduser(input_dir)
        self.output_dir = os.path.expanduser(output_dir)
        self.language = language
        self.dataset_format = dataset_format
        self.sample_rate = sample_rate
        self.single_speaker = single_speaker
        self.max_workers = max_workers

    def preprocess(self):
        command = [
            "python3", "-m", "piper_train.preprocess",
            "--language", self.language,
            "--input-dir", self.input_dir,
            "--output-dir", self.output_dir,
            "--dataset-format", self.dataset_format,
            "--sample-rate", str(self.sample_rate),
            "--max-workers", str(self.max_workers)
        ]

        if self.single_speaker:
            command.append("--single-speaker")

        try:
            subprocess.run(command, check=True)
            print("Preprocessing completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Preprocessing failed: {e}")
