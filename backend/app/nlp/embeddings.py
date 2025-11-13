import logging

import numpy as np
from sentence_transformers import LoggingHandler, SentenceTransformer

# Configure console logging (dev only)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("embeddings")
logger.addHandler(LoggingHandler())

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class Embeddings:
    def __init__(self) -> None:
        logger.info(f"Loading SentenceTransformer model: {_MODEL_NAME} (CPU)")
        self.model = SentenceTransformer(_MODEL_NAME)  # first time may download
        logger.info("SentenceTransformer model loaded.")

    def encode_text(self, text: str) -> np.ndarray:
        """Encode text to numpy embedding vector (384 dimensions)."""
        logger.info("Encoding text...")
        vec = self.model.encode([text], normalize_embeddings=True, show_progress_bar=True)  # (1, 384)
        logger.info("Encoding done.")
        return vec[0].astype(np.float32)
    
    def encode_to_list(self, text: str) -> list[float]:
        """Encode text and return as Python list for database storage."""
        vec = self.encode_text(text)
        return vec.tolist()

emb = Embeddings()
