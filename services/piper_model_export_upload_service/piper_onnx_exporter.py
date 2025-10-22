import subprocess
import os
import shutil
from pathlib import Path
from typing import Optional

class PiperONNXExporter:
    def __init__(self, lightning_logs_dir: str, onnx_output_path: str, training_config_path: str):
        self.lightning_logs_dir = os.path.expanduser(lightning_logs_dir)
        self.onnx_output_path = os.path.expanduser(onnx_output_path)
        self.training_config_path = os.path.expanduser(training_config_path)

    def export(self):
        print("🚀 [ONNX Export] Starting model export...")

        latest_checkpoint_file = self._find_latest_checkpoint_file(self.lightning_logs_dir)
        if latest_checkpoint_file is None:
            raise FileNotFoundError(
                f"❌ [ONNX Export] No checkpoint files found in directory: {self.lightning_logs_dir}"
            )

        checkpoint_path = latest_checkpoint_file
        print(f"📁 [ONNX Export] Latest checkpoint found: {checkpoint_path}")

        command = [
            "python3", "-m", "piper_train.export_onnx",
            checkpoint_path, self.onnx_output_path,
        ]

        try:
            subprocess.run(command, check=True)
            print(f"✅ [ONNX Export] Model exported to: {self.onnx_output_path}")
        except subprocess.CalledProcessError as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"❌ [ONNX Export] Failed to export model: {e}")

        try:
            onnx_json_path = self.onnx_output_path + ".json"
            shutil.copyfile(self.training_config_path, onnx_json_path)
            print(f"📄 [ONNX Export] Copied config to: {onnx_json_path}")
        except Exception as e:
            raise RuntimeError(f"❌ [ONNX Export] Failed to copy config: {e}")

    @staticmethod
    def _find_latest_checkpoint_file(lightning_logs_dir: str, extension: str = ".ckpt") -> Optional[str]:
        lightning_logs_path = Path(lightning_logs_dir)
        latest_checkpoint_file = None
        latest_modification_time = -1

        for version_folder in lightning_logs_path.iterdir():
            if version_folder.is_dir() and version_folder.name.startswith("version_"):
                checkpoints_subdir = version_folder / "checkpoints"
                if checkpoints_subdir.is_dir():
                    for checkpoint_file in checkpoints_subdir.glob(f"*{extension}"):
                        modification_time = checkpoint_file.stat().st_mtime
                        if modification_time > latest_modification_time:
                            latest_modification_time = modification_time
                            latest_checkpoint_file = checkpoint_file
        return str(latest_checkpoint_file) if latest_checkpoint_file else None

