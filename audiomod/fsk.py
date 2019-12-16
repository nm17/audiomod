import bitstring
import numpy as np
import scipy.fftpack
import scipy.io.wavfile

from audiomod.modulation import Modulation
from audiomod.utils import gen_sinewave, chunks


class BFSK(Modulation):
    def __init__(
        self, sample_rate: int, baud_rate: int, mark_freq: int, space_freq: int
    ):
        super().__init__(sample_rate)
        self.baud_rate = baud_rate
        self.mark_freq = mark_freq
        self.space_freq = space_freq

    def encode(self, data: bytes):
        result = []
        sample_length = self.sample_rate // self.baud_rate

        for bit in bitstring.BitArray(data):
            result.append(
                gen_sinewave(
                    self.mark_freq if bit else self.space_freq,
                    sample_length,
                    self.sample_rate,
                ),
            )

        return np.concatenate(result)

    def decode(self, audio: np.ndarray):
        result = ""

        for part in chunks(audio, self.sample_rate // self.baud_rate):
            loudest_freq = scipy.fftpack.rfft(part) ** 2
            loudest_freq = np.argmax(loudest_freq) * self.baud_rate
            result += (
                "1"
                if int(loudest_freq)
                in range(
                    self.mark_freq - self.baud_rate, self.mark_freq + self.baud_rate + 1
                )
                else "0"
            )

        return bitstring.BitArray("0b" + result).bytes
