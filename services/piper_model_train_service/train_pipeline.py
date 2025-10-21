import os
from services.piper_model_train_service import PiperModelTrainer
from services.piper_model_train_service.checkpoint_downloader import CheckpointDownloader


class PiperTrainingPipeline:
    def __init__(
        self,
        checkpoint_url: str,
        checkpoint_file: str = "epoch=2164-step=1355540.ckpt",
        checkpoint_dir: str = "checkpoints",
        dataset_path: str = "preprocessed",
        max_epochs: int = 10000,
        devices: int = 1
    ):
        self.checkpoint_url = checkpoint_url
        self.checkpoint_file = checkpoint_file
        self.checkpoint_dir = checkpoint_dir
        self.dataset_path = dataset_path
        self.max_epochs = max_epochs
        self.devices = devices

    def train(self):
        print("🚀 [Pipeline] Starting Piper training pipeline.")
        self._download_checkpoint()
        self._train_model()
        print("✅ [Pipeline] Finished Piper training pipeline.")

    def _download_checkpoint(self):
        if os.path.exists(f"{self.checkpoint_dir}/{self.checkpoint_file}"):
            print(f"📁 [Checkpoint] Already exists: {self.checkpoint_dir}/{self.checkpoint_file}")
            return
        print(f"⬇️ [Checkpoint] Downloading from: {self.checkpoint_url}")
        downloader = CheckpointDownloader(
            url=self.checkpoint_url,
            filename=self.checkpoint_file,
            checkpoint_dir=self.checkpoint_dir
        )
        downloader.download()
        print(f"📁 [Checkpoint] Saved to: {self.checkpoint_dir}/{self.checkpoint_file}")

    def _train_model(self):
        print("🧠 [Trainer] Starting training...")
        trainer = PiperModelTrainer(
            dataset_path=self.dataset_path,
            checkpoint_path=f"{self.checkpoint_dir}/{self.checkpoint_file}",
            max_epochs=self.max_epochs,
            devices=self.devices
        )
        trainer.train()
        print("🏁 [Trainer] Training complete.")
