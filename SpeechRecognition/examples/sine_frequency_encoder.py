#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To use ScalarEncoder on the power spectrum of unpredictable sound chunks, we
need an estimate of the maximum possible value that will occur in any of
these power spectra.

This scripts plots the frequency of the power spectra max values for
different chunk sizes.
"""
from __future__ import division, print_function, absolute_import

import sys
sys.path.append("../frequency-encoder")

from frequency_encoder import FrequencyEncoder, getFreqs

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as dsp
import thorns as th


numFrequencyBins = 8
freqBinN = 8
freqBinW = 1
minval = 0.0
maxval = 24.0


def plot_encoding(inputData, encoding, minval, maxval, title, color=None):
    global freqBinN, freqBinW, numFrequencyBins

    if color is None:
        color = 'b'

    # Raw data
    plt.figure(figsize=(4, 8))
    ax1 = plt.subplot(311)
    ax1.plot(inputData, c=color)
    ax1.set_title(title)

    # FFT
    fftData = getFreqs(inputData)
    ax2 = plt.subplot(312)
    ax2.plot(range(len(fftData)), fftData, c=color)

    w = (maxval - minval) / (freqBinN / freqBinW)
    for i in range(freqBinN // freqBinW):
        ax2.axhline(i * w, c='grey', ls='-.')

    w = len(fftData) / numFrequencyBins
    for k in range(numFrequencyBins):
        ax2.axvline(k * w, c='grey', ls='-.')

    ax2.set_xlim(0, len(fftData))
    ax2.set_ylim(minval, maxval)
    ax2.set_title('FFT')

    # Encoding
    ax3 = plt.subplot(313)
    ax3.imshow(np.flipud(encoding.reshape((numFrequencyBins, freqBinN)).T), cmap='Greys')
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.set_title('Encoding')
    plt.tight_layout()


def stft(samples, window_size, overlap_factor=0.5, window_function=np.hanning):
    """
    Perform Short-time Fourier transform to get the spectrogram for the given samples

    :param samples: Complex samples
    :param window_size: Size of DFT window
    :param overlap_factor: Value between 0 (= No Overlapping) and 1 (= Full overlapping) of windows
    :param window_function: Function for DFT window
    :return: short-time Fourier transform of the given signal
    """
    window = window_function(window_size)

    # hop size determines by how many samples the window is advanced
    hop_size = window_size - int(overlap_factor * window_size)

    # pad with zeros to ensure last window fits signal
    padded_samples = np.append(samples, np.zeros((len(samples) - window_size) % hop_size))
    num_frames = ((len(padded_samples) - window_size) // hop_size) + 1
    frames = [padded_samples[i * hop_size:i * hop_size + window_size] * window for i in range(num_frames)]
    return np.fft.fft(frames)


def main():
    sineEncoder = FrequencyEncoder(numFrequencyBins, freqBinN, freqBinW, minval, maxval)

    fs = 100e3  # Sampling frequency, Hz

    t = np.arange(0, 0.1, 1 / fs)

    # Make chirp, starting at 125Hz and ramp up to 1000Hz
    data = dsp.chirp(t, 125, t[-1], 1000, method='linear')

    encoding = sineEncoder.encode(data)
    # plot_encoding(s, encoding, minval, maxval, "Chirp - 125 to 1000Hz")

    # Three plots: Signal, Neurogram, Binary spike counts
    fig, ax = plt.subplots(3, 1)

    # Title with the number of High, Medium, and Low spontaneous rate fibers used
    # fig.suptitle('Cells: {} HSR, {} MSR, {} LSR'.format(anfs[0], anfs[1], anfs[2]))

    # Plot original signal
    th.plot_signal(
        signal=data,
        fs=fs,
        ax=ax[0]
    )

    #
    spec = stft(data, 1024)
    ax[1].specgram(data, Fs=fs)
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Frequency (Hz)')

    plt.show()


if __name__ == "__main__":
    main()
