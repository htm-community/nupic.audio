from nupic.encoders.base import Encoder
import abc

class IterationFinished(Exception):
  """ 
  EOF exception
  """
  def __init__(self, msg):
    super(IterationFinished, self).__init__(msg)



class IterationEncoder(Encoder):
  __metaclass__ = abc.ABCMeta
  """ 
  Iteration encoder encapsulates parsing of some data, and then creates an iterator over the
  (otherwise monolithic) file. 

  An example is a WAV file, during init() the file is transformed to a numeric representation (array), 
  and each call of encode() moves over one element of this array. 

  Typical applicatios for IterationEncoder: binary files (sound, video, biosignals, ...)
  """
  def __init__(self, filePath, encoder=None):
    """
    @param filePath - string
    @param encoder - Encoder, use a subencoder to process each datapoint? None=return raw values
    """
    self.path = filePath
    self.enc = encoder
    self.data = None #FIXME can I call transform() here? 
    self.it = 0 # iteration


  @abc.abstractmethod
  def transform(self):
    """
    @return write data to self.data, return void;
    """
    raise Exception("Must implement in subclasses")


  def getRawValue(self):
    """
    @return the current datapoint in raw form
    """
    return self.data[self.it]


  def encode(self, input):
    """
    @return raw/bit-vector representation (depending if subencoder is set)
    """
    if(self.data is None): #load file for the first time
      self.transform()

    if(self.it >= len(self.data)-1):
      raise IterationFinished()

    val = self.getRawValue()
    if(self.enc):
      val = self.enc.encode(val) # encode with subencoder
    self.it+=1
    return val

