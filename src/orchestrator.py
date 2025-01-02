from abc import ABC, abstractmethod
import logging
from pathlib import Path
import whisper
import pyaudio
import numpy as np

class SpeechRecognizer(ABC):
    """Base class for speech recognition. Makes it easy to swap between different systems."""

    @abstractmethod
    def listen(self) -> str:
        """Listen and convert speech to text."""
        pass

class WhisperRecognizer(SpeechRecognizer):
    """Whisper-based speech recognition implementation."""

    def __init__(self, model_size="base", record_seconds=5):
        # Audio recording settings
        self.FORMAT = pyaudio.paInt16  # Changed to Int16 for better compatibility
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.RECORD_SECONDS = record_seconds

        # Initialize PyAudio and Whisper
        self.audio = pyaudio.PyAudio()
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)

        # Keep track of the audio stream
        self.stream = None

    def __del__(self):
        """Cleanup resources."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()

    def _record_audio(self) -> np.ndarray:
        """Record audio from microphone."""
        if not self.stream:
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )

        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            try:
                data = self.stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(np.frombuffer(data, dtype=np.int16))
            except Exception as e:
                print(f"Error reading audio chunk: {e}")
                continue

        # Convert to float32 for Whisper
        audio_data = np.concatenate(frames).astype(np.float32) / 32768.0
        return audio_data

    def listen(self) -> str:
        """Listen and convert speech to text using Whisper."""
        try:
            audio_data = self._record_audio()
            # Use faster Whisper settings for real-time
            result = self.model.transcribe(
                audio_data,
                fp16=False,  # Faster CPU inference
                language='en',  # Specify English for faster processing
                initial_prompt="stop listening"  # Help with command recognition
            )
            text = result["text"].strip()
            print(f"[DEBUG] Raw transcription: '{text}'")  # Debug output
            return text
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            import traceback
            traceback.print_exc()
            return ""

class SpeechHandler:
    """Main class to handle all voice interactions."""

    def __init__(self, recognizer: SpeechRecognizer):
        """
        Args:
            recognizer: Which speech recognition system to use
        """
        # Set up basic logging
        self._setup_logging()

        # Store which recognizer we're using
        self.recognizer = recognizer

        self.logger.info("Speech Handler initialized")

    def _setup_logging(self):
        """Sets up basic logging to keep track of what's happening."""
        Path("logs").mkdir(exist_ok=True)

        self.logger = logging.getLogger("SpeechHandler")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler("logs/speech.log")
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.logger.addHandler(handler)

    def listen(self) -> str:
        """Listen for speech and return the text."""
        try:
            self.logger.info("Starting to listen...")
            text = self.recognizer.listen()
            self.logger.info(f"Heard: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Error while listening: {e}")
            return ""

# Example usage
if __name__ == "__main__":
    # Test with Whisper
    handler = SpeechHandler(WhisperRecognizer())

    print("Say something...")
    text = handler.listen()
    print(f"You said: {text}")
