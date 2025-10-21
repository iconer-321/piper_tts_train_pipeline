import os

from services.piper_dataset_preprocess_service import DatasetPreprocessor
from services.piper_model_export_upload_service.piper_model_export_service import PiperModelExportService
from services.piper_model_train_service import PiperTrainingPipeline


class PiperFullTrainingService:
    def __init__(
            self,
            dataset_url: str,
            checkpoint_url: str,
            checkpoint_file: str,
            language: str = "bn",
            sample_rate: int = 22050,
            devices: int = 1,
            max_epochs: int = 10000,
            max_workers: int = 1,
    ):
        self.dataset_url = dataset_url
        self.checkpoint_url = checkpoint_url
        self.checkpoint_file = checkpoint_file
        self.language = language
        self.sample_rate = sample_rate
        self.devices = devices
        self.max_epochs = max_epochs
        self.max_workers = max_workers

        # Intermediate variables
        self._converted_dir = "wavs"
        self._preprocessed_dir = "preprocessed"
        self._metadata_file = "metadata.csv"
        self._model_dir = "models"

    def run(self):
        try:
            print("🔧 [Service] Starting full Piper training workflow...\n")
            self._run_preprocessing()
            self._run_training()
            self._run_export()
            print("\n✅ [Service] Full Piper pipeline completed successfully.")
        except Exception as e:
            print(f"❌ [Service] Full Piper pipeline failed: {e}")
        finally:
            self._cleanup()

    def _cleanup(self):
        ...
        # if os.path.exists(self._preprocessed_dir):
        #     os.remove(self._preprocessed_dir)
        # if os.path.exists(self.input_dir):
        #     os.remove(self.input_dir)

    def _run_preprocessing(self):
        print("📦 [Step 1] Running dataset preprocessing...")
        preprocessor = DatasetPreprocessor(
            dataset_url=self.dataset_url,
            converted_dir=self._converted_dir,
            metadata_file=self._metadata_file,
            preprocessed_dir=self._preprocessed_dir,
            language=self.language,
            sample_rate=self.sample_rate,
            max_workers=self.max_workers
        )
        preprocessor.preprocess_dataset()

    def _run_training(self):
        print("🎯 [Step 2] Running Piper training pipeline...")
        trainer = PiperTrainingPipeline(
            checkpoint_url=self.checkpoint_url,
            checkpoint_file=self.checkpoint_file,
            dataset_path=self._preprocessed_dir,
            max_epochs=self.max_epochs,
            devices=self.devices,
        )
        trainer.train()

    def _run_export(self):
        print("📤 [Step 3] Exporting trained model to ONNX...")
        os.makedirs(self._model_dir, exist_ok=True)
        exporter = PiperModelExportService(
            model_dir=self._model_dir,
            lightning_logs_dir=f"{self._preprocessed_dir}/lightning_logs",
            onnx_output_path=f"{self._model_dir}/{self.language}_model.onnx",
            training_config_path=f"{self._preprocessed_dir}/config.json",
        )
        exporter.export()
