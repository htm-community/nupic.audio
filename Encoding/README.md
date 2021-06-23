# Encoding of audio signals

## Introduction

Although this starts with "Encoding of audio signals", there is a huge amount of cross-over knowledge and analysis techniques that can be applied to other signal domains.

Various examples; speech only, music tracks, orca whale recordings, ultra-sonic carnivourous bat echo-location, insect mating calls, Electrocardiograms (ECG), sonar/radar signals, calcium signals in zebrafish (Danio rerio), water/oil flow through pipes, etc...

## Encoding process (generic approach)

The key aspect here is representational changes/transforms to the signal being analysed, and importantly the encoding of trajectories of changes that occur within the time and frequency domain of the signal. Various filtering can occur to restrict and modify the representation but care and deep understanding must be taken as to how that may decimate or mask potentially important time-varying features. For example, dropping fundamental frequencies and greater importance of harmonics/formants changing over time (slope/derivative tracking of formant transitions). As such, sequential analysis steps from the time-domain signal to a sparse distributed representation (SDR) could be -

- Use of a Marsyas analysis network
- Successive time windows over the signal (with/without overlap of these frames, window size considerations, and Nyquist/sampling frequency choosen for the particular signal)
- Discrete Fourier or Wavelet transform to take the time-domain signal into the **complex** frequency-domain (never drop from complex domain i.e. keep magnitude __and__ phase, issues with Mother wavelet basis Haar/DB7/etc.)
- Non-linear filtering of time and frequency signals/repregrip sentations, potential to group into bands of similar frequency (linear, or more probably non-linear depending on signal domain being analysed, e.g. Speech only, Music, ECG signals)
- Hilbert-like transform to obtain a spectral energy? curve
- Use of previous frame/window spectral curves to obtain first and second derivatives (can go higher, but no potential need past 5th order)
- Use of Marsyas to obtain statistical aspects from the frequency and time domain representations from the windowed signal, use of previous window statistics to track changes/trajectories (first and second derivatives, velocity of change and acceleration of that velocity change). E.g. means, variances, standard deviations, skewness, kurtosis, ...
- Use of NuPIC encoders to generate an SDR of the derivatives and statistical values per window (scalar, time?, automated placement of category labels?)

Then usual route for the SDR into Spatial Pooler (SP), Temporal Memory (TM), appropriate classifier to feature prediction/anamoly detection.

### Prerequisites

- NuPIC (incl. it's pip requirements installed)  
- Python (2.7 for NuPIC)  
- NumPy, SciPy, and matplotlib (3D graphing, signal analysis, continuous wavelet transforms)  
- Marsyas (analysis network creation, statistical aspects) [1]  
- Python bindings for Marsyas [2]  

**Marsyas** is an open source software framework (mainly C++) for Analysis, Retrieval, and Synthesis of Audio Signals and processing.

#### Optional

- **Sonic Visualiser** [3] is a Vamp [4] enabled application for viewing and analysing the contents of audio files.

The default Marsyas installation doesn't have VAMP support enabled, so requires it to be rebuilt using a CMake GUI (such as cmake-gui, or ccmake).

### Package Installation

The Marsyas user manual [5] has detailed installation instructions for Linux, Mac OSX, Windows, and MinGW. Typical build steps can be found in;

http://marsyas.info/doc/manual/marsyas-user/Step_002dby_002dstep-building-instructions.html  

In addition the Python bindings need to be setup within Marsyas so it can work alongside NuPIC, NumPy, and SciPy. A CMake GUI, such as CMake-GUI or ccmake, can be used to tweak optional settings in the Marsyas build, before rebuilding and installing the framework.

## References

1 http://marsyas.info/  
2 http://marsology.blogspot.co.uk/2011/09/installing-marsyas-with-python-bindings.html  
3 http://www.sonicvisualiser.org/  
4 http://www.vamp-plugins.org/  
5 http://marsyas.info/doc/manual

https://en.wikipedia.org/wiki/Formant  

Other terms can be found in the nupic.audio Glossary.md file found here;  
https://github.com/nupic-community/nupic.audio/blob/master/Theory/Music/Glossary.md

## Further reading

[TO-DO] Out-dated, applicable, but not apparent within review text as to application here!

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
