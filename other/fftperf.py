import numpy
import perfplot
import scipy.fftpack
import pyfftw

#numpy.use_fastnumpy = True

perfplot.save(
    "rfftperf.png",
    transparent=False,
    setup=lambda n: (numpy.random.rand(int(n))),  # or simply setup=numpy.random.rand
    kernels=[
        lambda a: numpy.fft.rfft(a),
        lambda a: scipy.fftpack.rfft(a),
        lambda a: pyfftw.interfaces.numpy_fft.rfft(a),
    ],
    labels=["numpy", "scipy", "pyfftw"],
    n_range=[2000, 4000, 8000, 16000, 32000, 48000, 48000 * 2],
    xlabel="len(a)",
    # More optional arguments with their default values:
    title="Comparison between different rfft functions",
    # logx=False,
    # logy=False,
    equality_check=None,  # set to None to disable "correctness" assertion
    # automatic_order=True,
    # colors=None,
    # target_time_per_measurement=1.0,
    # time_unit="auto",  # set to one of ("s", "ms", "us", or "ns") to force plot units
    # relative_to=1,  # plot the timings relative to one of the measurements
)