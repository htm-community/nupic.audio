#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2019, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import wave
import audioop
import numpy as np
import resampy


def main():
  # Noise mix amounts
  noise_amts = [5.0, 10.0, 25.0, 50.0]  # percent

  # The noise to mix in with the speech samples
  nwav = wave.open("./Urban Traffic-SoundBible.com-1217469275.wav")
  # nwav = wave.open("./Shopping Mall Ambiance-SoundBible.com-1942498626.wav")

  # Read the frames, and convert to mono
  nframes = audioop.tomono(nwav.readframes(nwav.getnframes()), nwav.getsampwidth(), 1.414, 1.414)

  # Enforce 2 byte samples
  nsamples = audioop.lin2lin(nframes, nwav.getsampwidth(), 2)

  # numpy conversion of the raw byte buffers
  # '<i2' is a little-endian two-byte integer.
  nsamples = np.frombuffer(nsamples, dtype='<i2')
  nsamples = nsamples.astype(np.float64)

  # Down sample to match the speech samples
  nsamples = resampy.resample(nsamples, nwav.getframerate(), 8000)

  datapath = 'free-spoken-digit-dataset/recordings/'

  file_names = []
  file_names.append(datapath + "1_jackson_1.wav")

  for noise_amt in noise_amts:
    for file_name in file_names:
      wav = wave.open(file_name)

      frames = wav.readframes(wav.getnframes())

      samples = np.frombuffer(frames, dtype='<i2')
      samples = samples.astype(np.float64)

      # mix as much as possible
      n = len(samples)
      a = noise_amt / 100.0

      mix = (((1.0 - a) * samples[:n]) + (a * nsamples[:n])) * 0.5

      # Save the result
      file_name = file_name.replace(".wav", "_n{}.wav".format(int(noise_amt)))

      mix_wav = wave.open(file_name, 'w')
      mix_wav.setparams(wav.getparams())

      # before saving, we want to convert back to '<i2' bytes:
      mix_wav.writeframes(mix.astype('<i2').tobytes())
      mix_wav.close()


if __name__ == "__main__":
    main()
