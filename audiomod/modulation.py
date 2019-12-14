from abc import ABC, abstractmethod
import numpy as np


class Modulation(ABC):
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

    @abstractmethod
    def encode(self, data: bytes):
        pass

    @abstractmethod
    def decode(self, audio: np.ndarray):
        pass
