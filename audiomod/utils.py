from functools import lru_cache

import glfw
import imgui
import numpy as np
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer
import imgui_datascience
import matplotlib.pyplot as plt


@lru_cache(maxsize=5)
def gen_sinewave(freq, samples, sample_rate):
    return np.sin(2 * np.pi * freq * np.arange(samples) / sample_rate)


def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i: i + n]


def impl_glfw_init():
    width, height = 1280, 720
    window_name = "Audiomod"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(
        int(width), int(height), window_name, None, None
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


def setup_imgui(func):
    def wrapper(*args, **kwargs):
        window = impl_glfw_init()
        imgui.create_context()
        impl = GlfwRenderer(window)

        while not glfw.window_should_close(window):
            glfw.poll_events()
            impl.process_inputs()

            imgui.new_frame()

            func(*args, **kwargs)

            gl.glClearColor(1., 1., 1., 1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            imgui.render()
            impl.render(imgui.get_draw_data())
            glfw.swap_buffers(window)

        impl.shutdown()
        glfw.terminate()
    return wrapper

