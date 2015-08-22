# HTM for Musical Genre Classification

> Tied to issue #14 https://github.com/nupic-community/nupic.audio/issues/14

<img src="https://github.com/rcrowder/nupic.audio/blob/HTMforGenreClassification/HTMforGenreClassification/example2.png" alt="" align="center">  

## Introduction

The paper "Musical Genre Classification of Audio Signals" ([1][2]) describes the creation of feature vectors from a variety of statistics. Taken over short-time frame analysis windows, and longer texture windows (containing groups of analysis windows), the signal's dimension is broken down into a variety of statistical features. For a comparisons from supervised learning; see "Learning features from music audio with deep belief networks" [3].

The idea is to use various statistical analysis techniques to investigate the recognition of musical genres. Using NuPIC and Marsyas toolkits [4], and optionally Sonic Visualizer [5] with Vamp plugins [6]. Potentionally using a Peaks.js frontend [7]. An alternative is to train with musical styles rather than genre, or instrument/speaker identification.

> **Marsyas** (Music Analysis, Retrieval and Synthesis for Audio Signals) is an open source software framework for audio processing with specific emphasis on Music Information Retrieval applications.

> **Sonic Visualiser** is a Vamp enabled application for viewing and analysing the contents of music audio files.

> **Vamp** is an audio processing plugin system for plugins that extract descriptive information from audio data, typically referred to as __audio analysis plugins__ or __audio feature extraction plugins__.

> **Peaks.js** is a modular frontend component designed for the display of and interaction with audio waveform material in the browser (BBC R&D). 

1a http://dx.doi.org/10.1109/TSA.2002.800560  
1b http://webhome.csc.uvic.ca/~gtzan/output/tsap02gtzan.pdf  
2a http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.6377  
2b http://ismir2001.ismir.net/pdf/tzanetakis.pdf  
3 http://musicweb.ucsd.edu/~sdubnov/Mu270d/DeepLearning/FeaturesAudioEck.pdf  
4 http://marsyas.info/  
5 http://www.sonicvisualiser.org/  
6 http://www.vamp-plugins.org/  
7 http://waveform.prototyping.bbc.co.uk/  

### Prerequisites

- Qt5 (tested with v5.5, GUI and Open Gl)
- [Marsyas](https://github.com/marsyas/marsyas) toolkit
- Compilers and build system (for NuPIC Core)
- NuPIC Core library (built/installed into ```nupic.core/```)
- [Optional] Python (2.7 for NuPIC)
- [Optional] NuPIC (incl. PiP Requirements.txt packages)
- [Optional] [Python bindings for Marsyas](http://marsology.blogspot.co.uk/2011/09/installing-marsyas-with-python-bindings.html)
- [Optional] [Python Cochlea package](https://pythonhosted.org/cochlea/) (https://github.com/mrkrd/cochlea)

Additional build support packages (tailor or skip for your OS) - 
 
> $ sudo apt-get install build-essential cmake cmake-curses-gui  
> $ sudo apt-get install libasound2-dev alsa-tools-gui libjack-dev  
> $ sudo apt-get install libfreetype6-dev swig python-dev ipython  
> $ sudo pip install matplotlib  
> $ sudo apt-get install python-matplotlib freeglut3-dev python-opengl  

After Qt 5 install -

> sudo apt-get install qtcreator-plugin-cmake libqt5quick5  
> sudo apt-get install mesa-common-dev libglu1-mesa-dev  

The following are required for building documentation -
  
> $ sudo apt-get install texlive texinfo texi2html doxygen  

#### Optional

**Sonic Visualizer** and **VAMP plugin SDK** (with Marsyas re-built with VAMP support).

http://www.sonicvisualiser.org/  
http://www.vamp-plugins.org/

**Peaks.js** is a browser based audio waveform visualisation frontend component from BBC R&D.  

https://github.com/bbcrd/peaks.js  
http://waveform.prototyping.bbc.co.uk/

**OpenCV** This vision package can be installed using the following -

http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html  
http://www.samontab.com/web/2014/06/installing-opencv-2-4-9-in-ubuntu-14-04-lts/  

### Package Installation

The Marsyas user manual [2] has detailed installation instructions for Debian/Ubuntu, Max OS X, Win32, and MinGW. 

2 http://marsyas.info/doc/manual/marsyas-user/Step_002dby_002dstep-building-instructions.html  

Typical build steps could be - 

> $ git clone https://github.com/marsyas/marsyas.git  
> $ cd marsyas  
> $ mkdir build  
> $ cd build  
> $ cmake ..  
> $ ccmake ..  
> Toggle optional items, such as PNG and SWIG  
> $ make  
> $ sudo make install  
> $ sudo ldconfig /usr/local/lib  

For Marsyas documentation -  

> $ make docs  
> $ firefox doc/out-www/index.html    

If the music_speech dataset has been installed -  

> $ bin/sfplay ../audio/music_speech/music_wav/ncherry.wav  

Test out PNG drawing of the Neneh Cherry (Neneh Cherry Ft. Gangstarr - Sassy) track snippet -  

> $ bin/sound2png -m waveform ../audio/music_speech/music_wav/ncherry.wav ncherry.png  
> $ firefox ncherry.png  

  <img src="https://github.com/rcrowder/nupic.audio/blob/HTMforGenreClassification/HTMforGenreClassification/example.png" alt="" align="center">  

 Try out the spectral analyser  

> $ cd $NUPIC_AUDIO/HTMforGenreClassification  
> $ ./spectral_analyser --fname ncherry.wav

### Datasets

GTZAN __Genre Collection__ and __Music Speech__ collection - http://marsyas.info/downloads/datasets.html

The instructions to install these two datasets into Marsyas are described in the doc/tour.texi file [1] (or it's HTML equivalent if docs have been built within a Marsyas repo clone).

1 https://github.com/marsyas/marsyas/blob/master/doc/tour.texi  

Citation: 
> B. L. Sturm, "**An Analysis of the GTZAN Music Genre Dataset**", Proc. ACM Workshop MIRUM, Nara, Japan, Nov. 2012  
> Bob L. Sturm, "**The GTZAN dataset: Its contents, its faults, their effects on evaluation, and its future use**", June 10, 2013 http://arxiv.org/pdf/1306.1461.pdf
  
#### Genres

__genres.tar.gz__ - 1.14 GB 

This dataset consists of 1000 audio tracks each 30 seconds long. Containing 10 genres, with each genre represented by 100 tracks. The tracks are all 22050 Hz Mono 16-bit audio files in .wav format.

The ten genres are: Blues, Classical, Country, Disco, Hiphop, Jazz, Metal, Pop, Reggae, Rock

#### Music and Speech

__music_speech.tar.gz__ - 283 MB

A similar dataset which was collected for the purposes of music/speech discrimination. The dataset consists of 120 tracks, each 30 seconds long. Each class (music/speech) has 60 examples. The tracks are all 22050Hz Mono 16-bit audio files in .wav format.

#### Mocha TIMIT?

Phonetically balanced dataset for training an automatic speech recognition system. A set of 460 sentences designed to include the main connected speech processes in English (eg. assimilations, weak forms ..).

http://www.cstr.ed.ac.uk/research/projects/artic/mocha.html

### Peripheral processing

- Outer and middle ear
- Cochlear filterbank
- Energy measures

### Feature Vectors

Which features to track and which feature moments to track over time?? Auditory flow non-iterative derivative based in which domain?

Refer to the following report for descriptions of the following features;  

Peeters G. (2003). "**A large set of audio features for sound description (similarity and classification) in the CUIDADO project**" http://recherche.ircam.fr/anasyn/peeters/ARTICLES/Peeters_2003_cuidadoaudiofeatures.pdf  

and the following for valuable aspects of time-frequency distributions (TFD), and their use of minimum cross-entropy optimizations (MCE);
 
Patrick J. Loughlin, James W. Pitton, and Les E. Atlas, "**Construction of Positive Time-Frequency Distributions**"  
http://isdl.ee.washington.edu/papers/loughlin-1994-sptrans.pdf    

#### Timbral Features

1 Spectral Centroid  
2 Spectral Rolloff  
3 Spectral Flux  
4 Time Domain Zero Crossing  
5 Mel-Frequency Cepstral Coefficients  
6 Analysis and Texture windowing  
7 Low-Energy Feature  

A resulting feature vector for describing timbral texture consists of the following features: means and variances of spectral centroid, rolloff, flux, zero crossings over the texture window (8), low energy (1), and means and variances of the first five MFCC coefficients over the texture window (excluding the coefficient corresponding to the DC component) resulting in a 19-dimensional feature vector, __as a starting point__.

#### Rhythmic Content Features

http://uk.mathworks.com/help/wavelet/gs/continuous-wavelet-transform.html  
See this link for a description of the Continuous Wavelet Transfrom (Constant-Q filter). DAUB4 filters proposed by Daubechies? I. Daubechies, “**Orthonormal bases of compactly supported wavelets**” Commun. Pure Appl. Math, vol. 41, pp. 909–996, 1988.

Wavelet transform, then for each octave frequency band;
- Full Wave Rectification
- Low-pass Filtering
- Downsampling
- Mean Removal
- Enhanced Autocorrelation
- Peak Detection and Histogram Calculation
- Beat Histogram Features
  
#### Pitch Content Features

- Beat Determination
- MIDI Codes

### Further reading

Patrick J. Loughlin, James W. Pitton, and Les E. Atlas, "**Construction of Positive Time-Frequency Distributions**"  
http://isdl.ee.washington.edu/papers/loughlin-1994-sptrans.pdf    

Arie A. Livshin , Xavier Rodet (2004). "**Instrument Recognition Beyond Separate Notes -- Indexing Continues Recordings**"  
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.5.4107  

S. Furui, “**On the use of hierarchical spectral dynamics in speech recognition**”  
Proc. ICASSP, pp. 789–792, 1990.  
http://dx.doi.org/10.1109/ICASSP.1990.115927  

H. Hermansky, B. Hanson, and H. Wakita, “**Low-dimensional representation of vowels based on all-pole modeling in the psychophysical domain**”  
Speech Communication, vol. 4, pp. 181–187, 1985  
http://dx.doi.org/10.1016/0167-6393(85)90045-7  

H. Hermansky, "**Perceptual linear predictive (PLP) analysis of speech**"  
J Acoust Soc Am. 1990 Apr;87(4):1738-52.  
http://www.ncbi.nlm.nih.gov/pubmed/2341679  

T. H. Applebaum and B. A. Hanson, “**Tradeoffs in the design of regression features for word recognition**”  
Proc. EUROSPEECH, pp. 1203–1206, 1991  

Seneff S, “**A joint synchrony/mean-rate model of auditory speech processing**"  
Journal of Phonetics 16, 55-76, 1988  
  
Palmer AR, Winter IM. "**Coding of the fundamental frequency of voiced speech sounds and harmonic complex tones in the ventral cochlear nucleus**"  
In: Merchan MA, Juiz J, Godfrey DA, Mugnaini E, editors. Mammalian Cochlear Nuclei: Organization and Function. New York: Plenum Press; 1993. pp. 373–384.

Ian M Winter, Lutz Wiegrebe, and Roy D Patterson, "**The temporal representation of the delay of iterated rippled noise in the ventral cochlear nucleus of the guinea-pig**"  
http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2278959/  

Reinier W. L. Kortekaas, Dik J. Hermes, and Georg F. Meyer, "**Vowel-onset detection by vowel-strength measurement, cochlear-nucleus simulation, and multilayer perceptrons**"  
http://www.researchgate.net/publication/14591856_Vowel-onset_detection_by_vowel-strength_measurement_cochlear-nucleus_simulation_and_multilayer_perceptrons  

Sara Ahmadi, Seyed Mohammad Ahadi, Bert Cranen and Lou Boves, "**Sparse coding of the modulation spectrum for noise-robust automatic speech recognition**"  
doi:10.1186/s13636-014-0036-3  
http://asmp.eurasipjournals.com/content/2014/1/36  
