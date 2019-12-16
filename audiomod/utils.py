from functools import lru_cache

import bimpy
import numpy as np


@lru_cache(maxsize=5)
def gen_sinewave(freq, samples, sample_rate):
    return np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i : i + n]


def run_visual(mods):
    ctx = bimpy.Context()
    ctx.init(1280, 720, "test")
    while not ctx.should_close():
        with ctx:
            for mod in mods:
                mod.visualize()
