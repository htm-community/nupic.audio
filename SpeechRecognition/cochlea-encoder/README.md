# Cochlea Encoder

## Encoder design

The `CochleaEncoder` encodes a ...

## Parameter tweaking
 
## Usage

 ```python
import numpy as np
from cochlea_encoder import CochleaEncoder
 
# Example input to encode
chunk = np.array([1.0, 2.0, 1.0, 1.0])  

# Encoder params
numFrequencyBins = 8
freqBinN = 8
freqBinW = 1

# Encoding
encoder = CochleaEncoder(numFrequencyBins, freqBinN, freqBinW)
encoding = encoder.encode(chunk)

# Plot encoding (optional)
import matplotlib.pyplot as plt
plt.imshow(encoding.reshape(numFrequencyBins, freqBinN))
```
