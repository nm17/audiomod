from abc import ABC, abstractmethod

import bimpy
import numpy as np


class Modulation(ABC):
    __state = None

    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self.__state = {"text": bimpy.String(), "toggle": False}

    @abstractmethod
    def encode(self, data: bytes):
        pass

    @abstractmethod
    def decode(self, audio: np.ndarray):
        pass

    def visualize(self):
        bimpy.begin(type(self).__name__ + " - " + str(id(self)), bimpy.Bool(True))
        bimpy.input_text("Text", self.__state["text"], 256)

        button_pressed = bimpy.button("Plot", bimpy.Vec2(40, 20))

        if button_pressed or self.__state["toggle"]:
            if button_pressed:
                self.__state["toggle"] ^= True
            if len(self.__state["text"].value) > 0:
                bimpy.image("Graph", self.encode(self.__state["text"].value.encode()))
        bimpy.end()
