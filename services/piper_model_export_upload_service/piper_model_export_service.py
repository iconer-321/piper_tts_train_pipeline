from pathlib import Path

from services.piper_model_export_upload_service.piper_model_uploader import PiperModelUploader
from services.piper_model_export_upload_service.piper_model_zipper import PiperModelZipper
from services.piper_model_export_upload_service.piper_onnx_exporter import PiperONNXExporter


class PiperModelExportService:
    def __init__(self, model_dir: str, lightning_logs_dir: str, onnx_output_path: str, training_config_path: str):
        self.model_dir = Path(model_dir)
        self.lightning_logs_dir = Path(lightning_logs_dir)
        self.onnx_output_path = Path(onnx_output_path)
        self.training_config_path = Path(training_config_path)

    def export(self):
        print("🚀 [Service] Starting Piper model export service...")
        self._export_onnx_model()
        self._zip_model_directory()
        self._upload_model_to_s3()
        print("✅ [Service] All steps completed successfully.")

    def _export_onnx_model(self):
        print("🔧 [Step 1] Exporting ONNX model...")
        exporter = PiperONNXExporter(
            lightning_logs_dir=str(self.lightning_logs_dir),
            onnx_output_path=str(self.onnx_output_path),
            training_config_path=str(self.training_config_path)
        )
        exporter.export()
        print("✅ [Step 1] ONNX model export complete.\n")

    def _zip_model_directory(self):
        print("📦 [Step 2] Zipping model directory...")
        self.zipper = PiperModelZipper(model_dir=str(self.model_dir))
        self.zipper.zip_model()
        print(f"✅ [Step 2] Model zipped: {self.zipper.output_zip}\n")

    def _upload_model_to_s3(self):
        print("☁️ [Step 3] Uploading model to S3...")
        uploader = PiperModelUploader()
        uploader.upload_zip(zip_file_path=self.zipper.output_zip)
        print("✅ [Step 3] Upload completed.\n")
