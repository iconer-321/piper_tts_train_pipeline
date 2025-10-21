import subprocess

class PiperModelTrainer:
    def __init__(
        self,
        dataset_path: str,
        checkpoint_path: str,
        max_epochs: int = 10000,
        devices: int = 1
    ):
        self.dataset_path = dataset_path
        self.checkpoint_path = checkpoint_path
        self.max_epochs = str(max_epochs)
        self.devices = str(devices)

    def train(self):
        command = [
            "python3", "-m", "viva_piper_fork/src/python/piper_train",
            "--dataset-dir", self.dataset_path,
            "--accelerator", "gpu",
            "--devices", self.devices,
            "--batch-size", "32",
            "--validation-split", "0.0",
            "--num-test-examples", "0",
            "--max_epochs", self.max_epochs,
            "--resume_from_checkpoint", self.checkpoint_path,
            "--checkpoint-epochs", "1",
            "--precision", "32",
            "--max-phoneme-ids", "400",
            "--quality", "medium",
            "--strategy", "ddp",
        ]

        try:
            print(f"🚀 Starting training with checkpoint: {self.checkpoint_path}")
            subprocess.run(command, check=True)
            print("✅ Training completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Training failed: {e}")
