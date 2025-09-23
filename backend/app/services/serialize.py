import numpy as np

def to_bytes(vec: np.ndarray) -> bytes:
    return vec.tobytes()

def from_bytes(buf: bytes) -> np.ndarray:
    return np.frombuffer(buf, dtype=np.float32)
