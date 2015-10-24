# Encoding

## Introduction

> **Marsyas** (Music Analysis, Retrieval and Synthesis for Audio Signals [1]) is an open source software framework for audio processing.

> **Sonic Visualiser** [2] is a Vamp [3] enabled application for viewing and analysing the contents of audio files.

1 http://marsyas.info/  
2 http://www.sonicvisualiser.org/  
3 http://www.vamp-plugins.org/  

### Prerequisites

- Python (2.7 for NuPIC)
- NuPIC (incl. it's requirements, e.g. NumPy)
- Marsyas (GPL2 https://github.com/marsyas/marsyas)
- Python bindings for Marsyas [1]    

1 http://marsology.blogspot.co.uk/2011/09/installing-marsyas-with-python-bindings.html  

#### Optional

Sonic Visualizer and VAMP plugin SDK. With Marsyas re-built with VAMP support.

http://www.sonicvisualiser.org/  
http://www.vamp-plugins.org/

### Package Installation

The Marsyas user manual [2] has detailed installation instructions for Debian/Ubuntu, Max OS X, Win32, and MinGW. Typical build steps can be found in -

http://marsyas.info/doc/manual/marsyas-user/Step_002dby_002dstep-building-instructions.html  

### Encoding process

[TO-DO] Outline Marsyas processing network

Wavelet transform, then for each octave frequency band;
- Full Wave Rectification
- Low-pass Filtering
- Downsampling
- Mean Removal
- Enhanced Autocorrelation
- Peak Detection and Histogram Calculation
- Beat Histogram Features
  
### Further reading

Patrick J. Loughlin, James W. Pitton, and Les E. Atlas, "**Construction of Positive Time-Frequency Distributions**"  
http://isdl.ee.washington.edu/papers/loughlin-1994-sptrans.pdf    

H. Hermansky, "**Perceptual linear predictive (PLP) analysis of speech**"  
J Acoust Soc Am. 1990 Apr;87(4):1738-52.  
http://www.ncbi.nlm.nih.gov/pubmed/2341679  

Arie A. Livshin , Xavier Rodet (2004). "**Instrument Recognition Beyond Separate Notes -- Indexing Continues Recordings**"  
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.4107  

S. Furui, “**On the use of hierarchical spectral dynamics in speech recognition**”  
Proc. ICASSP, pp. 789–792, 1990.  
http://dx.doi.org/10.1109/ICASSP.1990.115927  

H. Hermansky, B. Hanson, and H. Wakita, “**Low-dimensional representation of vowels based on all-pole modeling in the psychophysical domain**”  
Speech Communication, vol. 4, pp. 181–187, 1985  
http://dx.doi.org/10.1016/0167-6393(85)90045-7  

T. H. Applebaum and B. A. Hanson, “**Tradeoffs in the design of regression features for word recognition**”  
Proc. EUROSPEECH, pp. 1203–1206, 1991  

Seneff S, “**A joint synchrony/mean-rate model of auditory speech processing**"  
Journal of Phonetics 16, 55-76, 1988  

Sara Ahmadi, Seyed Mohammad Ahadi, Bert Cranen and Lou Boves, "**Sparse coding of the modulation spectrum for noise-robust automatic speech recognition**"  
doi:10.1186/s13636-014-0036-3  
http://asmp.eurasipjournals.com/content/2014/1/36  
  
Palmer AR, Winter IM. "**Coding of the fundamental frequency of voiced speech sounds and harmonic complex tones in the ventral cochlear nucleus**"  
In: Merchan MA, Juiz J, Godfrey DA, Mugnaini E, editors. Mammalian Cochlear Nuclei: Organization and Function. New York: Plenum Press; 1993. pp. 373–384.

Ian M Winter, Lutz Wiegrebe, and Roy D Patterson, "**The temporal representation of the delay of iterated rippled noise in the ventral cochlear nucleus of the guinea-pig**"  
http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2278959/  

Reinier W. L. Kortekaas, Dik J. Hermes, and Georg F. Meyer, "**Vowel-onset detection by vowel-strength measurement, cochlear-nucleus simulation, and multilayer perceptrons**"  
http://www.researchgate.net/publication/14591856_Vowel-onset_detection_by_vowel-strength_measurement_cochlear-nucleus_simulation_and_multilayer_perceptrons  
