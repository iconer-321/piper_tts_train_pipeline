from pathlib import Path

from services.piper_dataset_preprocess_service.dataset_downloader import DatasetDownloader
from services.piper_dataset_preprocess_service.wav_converter import WavConverter
from services.piper_dataset_preprocess_service.metadata_generator import MetadataGenerator
from services.piper_dataset_preprocess_service.piper_preprocessor import PiperDatasetPreprocessor
from services.piper_dataset_preprocess_service.zip_file_processor import ZipFileProcessor


class DatasetPreprocessor:
    def __init__(
        self,
        dataset_url: str,
        input_dir: str = "datasets",
        converted_dir: str = "wavs",
        metadata_file: str = "metadata.csv",
        preprocessed_dir: str = "preprocessed",
        language: str = "bn",
        sample_rate: int = 22050,
        max_workers: int = 1
    ):
        self.dataset_url = dataset_url
        self.input_dir = input_dir
        self.zip_file_path = f"{input_dir}.zip"
        self.converted_dir = converted_dir
        self.metadata_file = metadata_file
        self.preprocessed_dir = preprocessed_dir
        self.language = language
        self.sample_rate = sample_rate
        self.max_workers = max_workers

    def preprocess_dataset(self):
        """
        Execute the complete dataset preprocessing pipeline.

        The pipeline consists of:
        1. Downloading and unzipping the dataset
        2. Converting the dataset to fixed format
        3. Generating metadata
        4. Running Piper preprocessing
        """
        self._print_header()
        try:
            self._download_and_unzip()
            self._convert_wav_files()
            self._generate_metadata()
            self._run_piper_preprocessing()
            self._print_success()

        except Exception as e:
            import traceback
            traceback.print_exc()
            self._print_error(e)

    def _download_and_unzip(self):
        """Downloads and unzips the dataset."""
        self._print_section_header(1, "Downloading and Unzipping Dataset", "📦")
        self._download_dataset()
        self._unzip_dataset()

    def _download_dataset(self):
        self._print_section_header(1, "Downloading dataset", "📦")
        downloader = DatasetDownloader(
            url=self.dataset_url,
            output_path=self.zip_file_path
        )
        print("🔄 Downloading dataset...")
        downloader.download()
        print("✅ Dataset downloaded successfully")

    def _unzip_dataset(self):
        self._print_section_header(2, "Unzipping dataset", "📦")
        zip_file_processor = ZipFileProcessor(
            zip_path=self.zip_file_path
        )
        print("🔄 Unzipping dataset...")
        zip_file_processor.extract()
        print("✅ Dataset unzipped successfully")

    @staticmethod
    def _print_header():
        """Print the preprocessing pipeline header."""
        print("\n" + "=" * 50)
        print("🚀 Starting Dataset Preprocessing Pipeline")
        print("=" * 50)

    @staticmethod
    def _print_section_header(step: int, title: str, emoji: str):
        """Print a section header with consistent formatting."""
        print("\n" + "-" * 30)
        print(f"{emoji} STEP {step}: {title}...")


    def _convert_wav_files(self) -> list:
        """Convert WAV files to the desired format."""
        self._print_section_header(1, "Converting WAV files", "🔊")
        print(f"📁 Input Directory: {Path(self.input_dir).absolute()}")
        print(f"💾 Output Directory: {Path(self.converted_dir).absolute()}")

        converter = WavConverter(
            input_dir=self.input_dir, output_dir=self.converted_dir
        )
        print("🔄 Converting WAV files...")
        converted_files = converter.convert_all_media_files()

        print(f"✅ Successfully converted files")
        return converted_files

    def _generate_metadata(self):
        """Generate metadata file for the from pathlib import Path dataset."""
        self._print_section_header(2, "Generating metadata file", "📝")
        print(f"📄 Output file: {Path(self.metadata_file).absolute()}")

        metadata = MetadataGenerator(
            txt_dir=self.input_dir,
            wav_dir=self.converted_dir,
            output_csv=self.metadata_file,
        )
        print("🔄 Generating metadata...")
        metadata.generate()
        print("✅ Metadata generation completed successfully")

    def _run_piper_preprocessing(self):
        """Run the Piper dataset preprocessing."""
        self._print_section_header(3, "Running Piper dataset preprocessing", "⚙️")
        print(f"🌐 Language: {self.language}")
        print(f"🔊 Sample rate: {self.sample_rate}Hz")
        print(f"📂 Output directory: {Path(self.preprocessed_dir).absolute()}")

        preprocessor = PiperDatasetPreprocessor(
            input_dir=self.input_dir,
            output_dir=self.preprocessed_dir,
            language=self.language,
            sample_rate=self.sample_rate,
            max_workers=self.max_workers
        )
        print("🔄 Running Piper preprocessing...")
        preprocessor.preprocess()

    def _print_success(self):
        """Print success message upon completion."""
        print("\n" + "=" * 50)
        print("✨ Preprocessing completed successfully! ✨")
        print(f"✅ Output directory: {Path(self.preprocessed_dir).absolute()}")
        print("=" * 50 + "\n")

    @staticmethod
    def _print_error(error: Exception):
        """Print error message when preprocessing fails."""
        print("\n" + "❌" * 10 + " ERROR " + "❌" * 10)
        print(f"Preprocessing failed: {str(error)}")
        print("❌" * 25 + "\n")
