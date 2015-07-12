## Time-Frequency domain transforms

The mammalian cochlea can be viewed as a bank of tuned filters the output of which is a set of band-pass filtered versions of the input signal that are continuous in time. Because of this property, fine-timing information is preserved in the output of cochlea.  

### Amplitude modulation transfer functions (MTF)

A MTF [5] expresses, as a function of frequency, the complex ratio (magnitude and phase) of the modulation in the neural response to the modulation in the acoustic stimulus. The MTF step response represents the neural response to an abrupt increase in intensity, as occurs at the onset of a tone burst or noise burst.  

Steps in a functional model involve;  
  1. Linear, bandpass filter (e.g. Gammatone),  
  2. Compression and rectification (simulate limited dynamic range),  
  3. Linear, "MTF" filter (whose impulse response is the derivative of the MTF step response).  

### [Fourier](http://en.wikipedia.org/wiki/Fourier_transform) & [Wavelet](http://en.wikipedia.org/wiki/Wavelet) (eg Morlet) transforms

TBD

### [Constant-Q transform](http://en.wikipedia.org/wiki/Constant_Q_transform)

Given an initial minimum frequency <img src="Theory/images/f_0.png"> for the CQT, the centre frequencies for each band can be obtained from: <img src="Theory/images/f_k.png"> where k = 0,1,… and b is the number of bins per octave.  
The fixed ratio of centre frequency to bandwidth is then given by <img src="Theory/images/Q_cf.png">  
The desired bandwidth of each frequency band is then obtained by choosing a window of length, where <img src="Theory/images/f_s.png"> is the sampling frequency,  
<img src="Theory/images/N_k.png">  
The CQT is defined as

<img src="Theory/images/CQT.png">
 
Where _x(n)_ is the time domain signal and <img src="Theory/images/W_nk.png"> is a window function, such as the Hanning window, of length <img src="Theory/images/N_k_solo.png">

## Sparse shiftable kernel signal representation

The signal <img src="Theory/images/x(t).png"> is encoded with a set of kernel functions, <img src="Theory/images/kernel_range.png">, that can be positioned arbitrarily and independently of time [1].  

The representation with additive noise;

<img src="Theory/images/x(t)_equation.png">

Where <img src="Theory/images/tau_im.png"> and <img src="Theory/images/s_im.png"> are the temporal position and coefficient of the _i_ th instance of kernel <img src="Theory/images/phi_m.png">, respectively. The notation <img src="Theory/images/n_m.png"> indicates the number of instances of <img src="Theory/images/phi_m.png"> , which need not be the same across kernels. Kernels are not restricted in form or length.
 
A more general way of expressing this equation is in convolutional form,

<img src="Theory/images/x(t)_conv_form.png">
 
Where <img src="Theory/images/s_m(tau).png"> is the coefficient at time <img src="Theory/images/tau.png"> for <img src="Theory/images/phi_m.png"> 

#### References  
_1_ **Coding time-varying signals using sparse, shift-invariant representations.**  
Michael S. Lewicki & Terrence J. Sejnowski 1999 (doi: 10.1.1.52.1912)  
_2_ **Efficient Coding of Time-Relative Structure Using Spikes.**  
Evan C. Smith & Michael S. Lewicki 2005 (doi: 10.1162/0899766052530839)  
_3_ **Efficient auditory coding.**  
Evan C. Smith & Michael S. Lewicki 2006 (doi: 10.1038/nature04485)  
_4_ **State-dependent computations: spatiotemporal processing in cortical networks.**  
Dean V. Buonomano & Wolfgang Maass 2009 (doi: 10.1038/nrn2558)  
_5_ **Neural coding of the temporal envelope of speech: relation to modulation transfer functions.**  
B. Delgutte, B.M. Hammond, and P.A. Cariani, Massachusetts Eye and Ear Infirmary, Boston, MA  
Psychophysical and physiological advances in hearing (1998): 595-603  

### Auditory kernel functions

#### Gammatone filters
 
The gammatone filter was introduced to describe cochlea nucleus response [9][8]. For a review see [7], and [6] for a history of cochlea filters, from Helmholtz resonance theory to the following gammatone alternatives;  
 
##### Gammatone (GTF) <img src="Theory/images/GTF.png">
 
Three key limitations of the GTF are as follows [7];  
  1. It is inherently nearly symmetric, while physiological measurements show a significant asymmetry in the auditory filter.  
  2. It has a very complex frequency-domain description. Therefore, it is not easy to use parameterization techniques to realistically model level-dependent changes (gain control) in the auditory filter.  
  3. Due to its frequency-domain complexity, it is not easy to implement the GFT in the analog domain.

Lyon presented a close relative to the GTF, which he termed as All-Pole Gammatone Filter (APGF) to highlight its similarity to and distinction from the GTF.  
 
##### All-pole (APGF) <img src="Theory/images/APGF.png">, <img src="Theory/images/unity_gain.png"> for unity gain at DC
 
##### Differentiated All-pole (DAPGF) <img src="Theory/images/DAPGF.png">, <img src="Theory/images/consistency.png"> for dimensional consistency
 
##### One-zero (OZGF) <img src="Theory/images/OZGF.png">, <img src="Theory/images/consistency.png"> for dimensional consistency

The standard LP bi-quad transfer function is;
 
<img src="Theory/images/LP-biquad.png">

Where <img src="Theory/images/omega_0.png"> is the natural (or pole) frequency and Q is the quality factor.
 
The frequency, where the peak gain occurs or centre frequency (CF) is related to the natural frequency and Q, is;

<img src="Theory/images/omega_LP_CF.png">
 
Parameterized in terms of Q;
 
<img src="Theory/images/H_LP_max.png">

##### Gammachirp

See http://www.acousticscale.org/wiki/index.php/Gammachirp_Auditory_Filters for a review, and [1] for its use in continuous wavelet analysis.  

The gammachirp filter is an extension of the gammatone with a frequency modulation term. The frequency response of the gammachirp filters, are asymmetric and exhibit a sharp drop off on the high frequency side of the center frequency. This corresponds well to auditory filter shapes derived from masking data.

The amplitude spectrum of the gammachirp can be written in terms of the gammatone as;

<img src="Theory/images/gammachirp.png">
 
Where <img src="Theory/images/gammachirp_beta.png">
 
The [equivalent rectangular bandwidth](http://en.wikipedia.org/wiki/Equivalent_rectangular_bandwidth) (ERB) shows the relationship between the auditory filter, frequency, and the critical bandwidth. An ERB passes the same amount of energy as the auditory filter it corresponds to and shows how it changes with input frequency. At low sound levels, the ERB is approximated by the following equation;

<img src="Theory/images/ERB.png">  
Where the ERB is in Hz and F is the centre frequency in kHz.

#### References  
_1_ **Application of Gammachirp Auditory Filter as a Continuous Wavelet Analysis**  
Lotfi Salhi & Kais Ouni 2011 (arXiv:1107.5492 doi: 10.5121/sipij)  
http://arxiv.org/ftp/arxiv/papers/1107/1107.5492.pdf  
_2_ **Interspike interval method to compute speech signals from neural firing**  
Uwe Meyer-Baese 1998 (doi: 10.1117/12.304847)  
_3_ **A Spike-Based Analogue Circuit That Emphasises Transients In Auditory Stimuli**  
Natasha Chia and Steve Collins 2004 (doi: 10.1109/ISCAS.2004.1329589)  
_4_ **The robustness of speech representations obtained from simulated auditory nerve fibers under different noise conditions**  
Tim Jurgens, Thomas Brand, Nicholas R. Clark, Ray Meddis, Guy J. Brown 2013 (doi: 10.1121/1.4817912)  
_5_ **A 6 micro-Watt per Channel Analog Biomimetic Cochlear Implant Processor Filterbank Architecture With Across Channels AGC (Automatic Gain Control)**  
Guang Yang, Richard F. Lyon 2015 (doi: 10.1109/TBCAS.2014.2325907)  
_6_ **History and Future of Auditory Filter Models**  
Richard F. Lyon, Andreas G. Katsiamis, Emmanuel M. Drakakis 2010 (doi: 10.1109/ISCAS.2010.5537724)  
_7_ **Practical Gammatone-Like Filters for Auditory Processing**  
AG Katsiamis, EM Drakakis, and RF Lyon 2007 (doi: 10.1155/2007/63685)  
_8_ **The pre-response stimulus ensemble of neurons in the cochlear nucleus**  
Johannesma, P.I.M. 1972, Symposium on Hearing Theory IPO, Eindhoven, Holland, pp. 58--69  
_9_ **Models for approximating basilar membrane displacement**  
Flanagan, J.L. 1960, Journal of the Acoustical Society of America, vol. 32, no. 7, p. 937, 1960.  
