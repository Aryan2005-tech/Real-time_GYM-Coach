import logging
from io import BytesIO
from gtts import gTTS

logger = logging.getLogger(__name__)


class TextToSpeech:
    def speak(self, text, lang="en"):
        cleaned = (text or "").strip()

        if not cleaned:
            return None
        
        try:
            buffer = BytesIO()
            gTTS(text=cleaned, lang=lang).write_to_fp(buffer)
            buffer.seek(0)
            return buffer.read()
        except Exception as e:
            logger.error(f"TTS audio generation failed: {e}")
            return None