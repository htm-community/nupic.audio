# WAV encoder - use any available transformators

from nupic.audio.encoders.iteration import IterationEncoder

from enum import Enum

class WAVEncoder(IterationEncoder):

  MODE = Enum('MODE', 'SCIPY') # TODO add others, matlab, ...
  def __init__(self, filePath, impl=MODE.SCIPY, subEncoder=None):
    super(WAVEncoder, self).__init__(filePath, subEncoder)
    self.rate = -1
    # opportunistic imports for transform libraries, if present:
    if(impl==WAVEncoder.MODE.SCIPY):
      from scipy.io.wavfile import read
      self.readSound=read # export the function


  def transform(self):
    """set rate and data, use self.readSound fn to parse the binary file"""
    a = self.readSound(self.path)
    self.rate = a[0]
    self.data = a[1]


  def getRate(self):
    """rate of the song"""
    return self.rate
