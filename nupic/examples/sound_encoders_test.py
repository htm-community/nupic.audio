# This file will demanstrate use of available sound encoders:

# WAV
data="../examples/data/a0007.wav"
from nupic.audio.encoders.wave import WAVEncoder

wav2rawEnc = WAVEncoder(data)
print wav2rawEnc.encode(1)

from nupic.encoders.random_distributed_scalar import RandomDistributedScalarEncoder as RDSE
rdse = RDSE(resolution=1)
wav2bitsEnc = WAVEncoder(data, subEncoder=rdse)
print wav2bitsEnc.encode(1)
