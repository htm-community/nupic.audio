# This file will demanstrate use of available sound encoders:

# WAV
data="./data/a0007.wav"
#from nupicaudio.encoders.wave import WAVEncoder #FIXME move to nupicaudio.examples
from encoders.wave import WAVEncoder
wav2rawEnc = WAVEncoder(data)
print wav2rawEnc.encode(1)

from nupic.encoders.random_scalar import RandomDistributedScalarEncoder as RDSE
rdse = RDSE(w=25)
wav2bitsEnc = WAVEncoder(data, subEncoder=rdse)
print wav2bitsEnc.encode(1)
