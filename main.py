import os
from dotenv import load_dotenv
from const import *
from services.piper_full_training_service import PiperFullTrainingService

load_dotenv()


def main():
    dataset_url = os.getenv("DATASET_URL", None)
    checkpoint_url = os.getenv("CHECKPOINT_URL", CHECKPOINT_URL)
    checkpoint_file = os.getenv("CHECKPOINT_FILE", CHECKPOINT_FILE)
    language = os.getenv("LANGUAGE", LANGUAGE)
    sample_rate = int(os.getenv("SAMPLE_RATE", SAMPLE_RATE))
    max_epochs = int(os.getenv("MAX_EPOCHS", MAX_EPOCHS))
    max_workers = int(os.getenv("MAX_WORKERS", MAX_WORKERS))
    devices = int(os.getenv("DEVICES", DEVICES))

    pipeline = PiperFullTrainingService(
        dataset_url=dataset_url,
        checkpoint_url=checkpoint_url,
        checkpoint_file=checkpoint_file,
        language=language,
        sample_rate=sample_rate,
        max_epochs=max_epochs,
        max_workers=max_workers,
        devices=devices
    )

    pipeline.run()

if __name__ == "__main__":
    print("Hello from main.py")
    main()
