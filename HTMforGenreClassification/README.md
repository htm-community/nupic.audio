# HTM for Musical Genre Classification

> Tied to issue #14 https://github.com/nupic-community/nupic.audio/issues/14

<img src="https://github.com/rcrowder/nupic.audio/blob/HTMforGenreClassification/HTMforGenreClassification/example2.png" alt=""">

## Introduction

The paper "Musical Genre Classification of Audio Signals" ([1][2]) describes the creation of feature vectors from a variety of statistics. Taken over short-time frame analysis windows, and longer texture windows (containing groups of analysis windows), the signal's dimension is broken down into a variety of statistical features. For a comparisons from supervised learning; see "Learning features from music audio with deep belief networks" [3].

The idea is to use various statistical analysis techniques to investigate the recognition of musical genres. Using NuPIC and Marsyas toolkits [4], and optionally Sonic Visualizer [5] with Vamp plugins [6]. Potentionally using a Peaks.js frontend [7]. An alternative is to train with musical styles rather than genre, or instrument/speaker identification.

1a http://dx.doi.org/10.1109/TSA.2002.800560  
1b http://webhome.csc.uvic.ca/~gtzan/output/tsap02gtzan.pdf  
2a http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.6377  
2b http://ismir2001.ismir.net/pdf/tzanetakis.pdf  
3  http://musicweb.ucsd.edu/~sdubnov/Mu270d/DeepLearning/FeaturesAudioEck.pdf
4  http://marsyas.info/
5  http://www.sonicvisualiser.org/
6  http://www.vamp-plugins.org/
7  http://waveform.prototyping.bbc.co.uk/


### Prerequisites

- [Qt 5.5](http://www.qt.io/) - [Qt 5 Launch Demo video](https://www.youtube.com/watch?t=272&v=vhWS_bN-T3k)
- [NuPIC Core](https://github.com/numenta/nupic.core) library
- [Marsyas](https://github.com/marsyas/marsyas) toolkit

Marsyas (Music Analysis, Retrieval and Synthesis for Audio Signals) is an open source software framework for audio processing with specific emphasis on Music Information Retrieval (MIR) applications.

#### Optional

- Python (2.7 x64 for NuPIC)
- NuPIC (incl. PiP Requirements.txt packages)
- [Python bindings for Marsyas](http://marsology.blogspot.co.uk/2011/09/installing-marsyas-with-python-bindings.html)
- [Python Cochlea package](https://pythonhosted.org/cochlea/) (https://github.com/mrkrd/cochlea)

Additional packages required - 

> $ sudo pip install scipy  
> $ sudo apt-get install python-tables  
> $ sudo pip install thorns  

- Sonic Visualizer and VAMP plugin SDK

Sonic Visualiser is a Vamp enabled application for viewing and analysing the contents of music audio files. Vamp is an audio processing plugin system for plugins that extract descriptive information from audio data, typically referred to as __audio analysis plugins__ or __audio feature extraction plugins__. Marsyas needs to be re-built via ```ccmake``` to enable VAMP support (off by default).

http://www.sonicvisualiser.org/ http://www.vamp-plugins.org/

- Peaks.js - Is a modular frontend component designed for the display of and interaction with audio waveform material from within a browser (BBC R&D).

https://github.com/bbcrd/peaks.js http://waveform.prototyping.bbc.co.uk/

- OpenCV - Open Source Computer Vision Library http://opencv.org

http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html  
http://www.samontab.com/web/2014/06/installing-opencv-2-4-9-in-ubuntu-14-04-lts/  


## Package Installation

Additional build support packages (tailor or skip for your OS) - 
 
> $ sudo apt-get install build-essential cmake cmake-curses-gui  
> $ sudo apt-get install libasound2-dev alsa-tools-gui libjack-dev  
> $ sudo apt-get install libfreetype6-dev swig python-dev ipython  
> $ sudo pip install pyplot  
> $ sudo pip install matplotlib  
> $ sudo apt-get install python-matplotlib freeglut3-dev python-opengl  

#### [Qt 5.5](http://www.qt.io/)

Go to http://www.qt.io/ and step through the questions. Once installed you may need to add the following -

> sudo apt-get install qtcreator-plugin-cmake libqt5quick5  
> sudo apt-get install mesa-common-dev mesa-utils libglu1-mesa-dev  

#### [Marsyas](https://github.com/marsyas/marsyas)

The Marsyas user manual has detailed installation instructions for Debian/Ubuntu, Mac OS X, MinGW, and Windows - http://marsyas.info/doc/manual/marsyas-user/

Typical build steps could be - 

> $ git clone https://github.com/marsyas/marsyas.git  
> $ cd marsyas  
> $ mkdir build  
> $ cd build  
> $ cmake ..  
> $ ccmake ..  
> Toggle optional items, such as Qt5, PNG, and SWIG  
> $ make  
> $ sudo make install  
> $ sudo ldconfig /usr/local/lib  

For Marsyas documentation -  

> $ sudo apt-get install texlive texinfo texi2html doxygen  
> $ make docs  
> $ firefox doc/out-www/index.html    

If the music_speech dataset has been installed -  

> $ bin/sfplay ../audio/music_speech/music_wav/ncherry.wav  

Test out PNG drawing of the Neneh Cherry (Neneh Cherry Ft. Gangstarr - Sassy) track snippet -  

> $ bin/sound2png -m waveform ../audio/music_speech/music_wav/ncherry.wav ncherry.png  
> $ firefox ncherry.png  

Try out the spectral analyser  

> $ cd $NUPIC_AUDIO/HTMforGenreClassification  
> $ ./spectral_analyser --fname ncherry.wav

<img src="https://github.com/rcrowder/nupic.audio/blob/HTMforGenreClassification/HTMforGenreClassification/example.png" alt="">

#### [NuPIC Core](https://github.com/numenta/nupic.core)

Building the NuPIC Core library from source, requires GCC 4.8 on Linux (inc. Mac OS) and Visual Studio 2015 on Windows. A NuPIC Core deployment package needs to be installed system-wide or into the local project directory '''$NUPIC_AUDIO/HTMforGenreClassification/nupic.core/''' (i.e. bin, include, and lib folders).

### Qt5 project build

Once NuPIC Core and Marsyas have been installed, the Qt5 project file (.pro) can be fed through QMake to produce Makefiles. The ```Makefile``` is used to build the main cross-platform application. For example;

> $ cd $NUPIC_AUDIO/HTMforGenreClassification  
> $ qmake  
> $ make  
> $ ./HTMforGenreClassification ncherry.wav


## Datasets

### GTZAN __Genre Collection__ and __Music Speech__ collection

http://marsyas.info/downloads/datasets.html

The instructions to install these two datasets, is described in the doc/tour.texi file https://github.com/marsyas/marsyas/blob/master/doc/tour.texi

> Citation:  
> B. L. Sturm, "**An Analysis of the GTZAN Music Genre Dataset**", Proc. ACM Workshop MIRUM, Nara, Japan, Nov. 2012  
> Bob L. Sturm, "**The GTZAN dataset: Its contents, its faults, their effects on evaluation, and its future use**", June 10, 2013 http://arxiv.org/pdf/1306.1461.pdf  
  
#### Genres - __genres.tar.gz__ (1.14 GBytes)

This dataset consists of 1000 audio tracks each 30 seconds long. Containing 10 genres, with each genre represented by 100 tracks. The tracks are all 22050 Hz Mono 16-bit audio files in .wav format.

The ten genres are: Blues, Classical, Country, Disco, Hiphop, Jazz, Metal, Pop, Reggae, Rock

#### Music and Speech - __music_speech.tar.gz__ (283 MBytes)

A similar dataset which was collected for the purposes of music/speech discrimination. The dataset consists of 120 tracks, each 30 seconds long. Each class (music/speech) has 60 examples. The tracks are all 22050Hz Mono 16-bit audio files in .wav format.

### MOCHA-TIMIT

MOCHA (MultiCHannel Articulatory database) is a phonetically balanced dataset for training an automatic speech recognition system. A set of 460 sentences designed to include the main connected speech processes in English (eg. assimilations, weak forms ..).

http://www.cstr.ed.ac.uk/research/projects/artic/mocha.html

The following instrumentation were used:

- Microphone 16kHz sample rate (audio-technica ATM10a)
- Fourcin Laryngograph 16kHz sample rate
- Carstens Articulograph 500Hz sample rate 10 2mm sensors
- Reading Electropalatograph (EPG) 200Hz sample rate

And software:

- Edinburgh Speech Tools - File format conversion and Speech signal processing functions
- MATLAB-EMATools - Graphical Interface for simultaneous analysis  of EMA EPG audio and laryngograph data

Further information can be found in - http://data.cstr.ed.ac.uk/mocha/README_v1.2.txt

### TI Digits

Found in The Linguistic Data Consortium (LDC, https://www.ldc.upenn.edu/about) - https://catalog.ldc.upenn.edu/LDC93S10

> This corpus contains speech which was originally designed and collected at Texas Instruments, Inc. (TI) for the purpose of designing and evaluating algorithms for speaker-independent recognition of connected digit sequences. There are 326 speakers (111 men, 114 women, 50 boys and 51 girls) each pronouncing 77 digit sequences. Each speaker group is partitioned into test and training subsets.


## Cochlea processing

- **PCP** - Outer and middle ear (Glasberg & Moore, 2002).
Frequency dependant transmission.

- **BMM** - Basilar Membrane Motion (multi-channel)
Equal spaced points along the membrane respond to frequencies spaced along a quasi-logarithmic scale (i.e. ERB).

- **Cochlea inspired filters**
Gammatone - Passive linear filter. No level dependant properties.
dcGC - Dynamic compressive gamma-chirp. With level dependant asymmetry and fast active compression.
pzFC - Pole-zero filter cascade. With level dependant asymmetry and fast active compression.

- **NAP** - Neural Activity Pattern
Represents the neural transduction occuring in the inner hair cells. Signal is half-wave rectified, unipolar response, phase-locked. Can apply compression at this stage (already included in dcGC and pzFC).

- **STI** - Strobed Temporal Integration (strobe point finding)
Strobe points convert the NAP into a SAI (see below). Short window to detect strobes (~35 milliseconds). Form of autocorrelation. Deconvolution of Glottal Pulses from associated resonances.

- **SAI** - Stabalized Auditory Image

- **SSI** - Size-Shape Image
Processes SAI trucating signal in each channel after first pitch ridge and scaling time axis. SSI tries to be pitch invariant and scale-shift covariant.

- **Mellin Image** - Scale-shift invariant representation, Wavelet-Mellin transform (Irino & Patterson, 1999)
__Gammachirp filters__ is minimal uncertainty function for a joint __time-scale representation__ of the signal.
__Gabor filters__ is minimal uncertainty function for a joint __time-frequency representation__ of the signal.

- **MFCC** - Mel-frequency Cepstral Coefficients
Dropping ("lifting") of DCT coefficients same as low-pass filtering. Short spectral windows ~25ms. First 13 coefficients retained become the MFCC signature. Good to capture overall spectral shape of a sound, but not very sensitive to pitch.

## Feature Vectors

Refer to the following report for descriptions of the following features;

> Peeters G. (2003). "**A large set of audio features for sound description (similarity and classification) in the CUIDADO project**"  
> http://recherche.ircam.fr/anasyn/peeters/ARTICLES/Peeters_2003_cuidadoaudiofeatures.pdf  

And the following for time-frequency distributions (TFD), and their use of minimum cross-entropy optimizations (MCE);

> Patrick J. Loughlin, James W. Pitton, and Les E. Atlas, "**Construction of Positive Time-Frequency Distributions**"  
> http://isdl.ee.washington.edu/papers/loughlin-1994-sptrans.pdf    

#### Timbral Features

1 Spectral Centroid  
2 Spectral Rolloff  
3 Spectral Flux  
4 Time Domain Zero Crossing  
5 Mel-Frequency Cepstral Coefficients  
6 Analysis and Texture windowing  
7 Low-Energy Feature  

A resulting feature vector for describing timbral texture consists of the following features: means and variances of spectral centroid, rolloff, flux, zero crossings over the texture window (8), low energy (1), and means and variances of the first five MFCC coefficients over the texture window (excluding the coefficient corresponding to the DC component) resulting in a multi-dimensional feature vector, __as a starting point__.

#### Rhythmic Content Features

http://uk.mathworks.com/help/wavelet/gs/continuous-wavelet-transform.html  
See this link for a description of the Continuous Wavelet Transfrom (Constant-Q filter). I. Daubechies, “**Orthonormal bases of compactly supported wavelets**” Commun. Pure Appl. Math, vol. 41, pp. 909–996, 1988. Use DAUB4 filters proposed by Daubechies?

Wavelet transform, then for each octave frequency sub-band;
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


## Selective Attention and Tuning

For an overview of attention, with respect to vision, see John K. Tsotsos webpage - http://www.cse.yorku.ca/~tsotsos/Research/Foundations.html (http://www.cse.yorku.ca/~tsotsos/Research/Attention,_Binding_and_Recognition.html)

Also, Michael Spratling et al.'s work on pre-synaptic lateral inhibition - http://www.inf.kcl.ac.uk/staff/mike/publications.html

#### Selection 
-    spatio-temporal region of interest
-    world/task/object/event model
-    gaze/viewpoint
-    best interpretation/response

#### Restriction
-    task relevant search space pruning
-    location cues
-    fixation points
-    search depth control

#### Suppression
-    spatial/feature surround inhibition
-    inhibition of return 
-    suppress task-irrelevant computations


## Further reading

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
