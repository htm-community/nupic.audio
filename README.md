# nupic.audio
Auditory experiments using [cortical learning algorithms](https://scholar.google.co.uk/scholar?q=cortical+learning+algorithms&hl=en&as_sdt=0&as_vis=1&oi=scholart&sa=X&ei=fYM6VZHVMIfqaIPcgNAI&ved=0CB4QgQMwAA) (CLA) and [hierarchical temporal memory](https://scholar.google.co.uk/scholar?q=hierarchical+temporal+memory&hl=en&as_sdt=0&as_vis=1&oi=scholart&sa=X&ei=1IM6Vfy6AZKO7AbSnYDgAQ&sqi=2&ved=0CB4QgQMwAA) (HTM).


Initial thoughts and ideas are being discussed in the Wiki at the moment;  
https://github.com/nupic-community/nupic.audio/wiki

Fluctuating towards;

## A sparse, shiftable kernel method of signal representation

Typically signal processing of audio signals involves Cepstral analysis, via lpc or discrete fourier transforms for example. One drawback of this approach is that the transform produces a linearly spaced representations of the signal. With humans able to reliably detect interaural time differences as small as 10 us, sampling dimensionality using Fourier or Wavelet transforms increases. 

The signal <img src="docs/x(t).png"> is encoded with a set of kernel functions, <img src="docs/kernel_range.png">, that can be positioned arbitrarily and independently of time [1].  

The representation with additive noise;

<img src="docs/x(t)_equation.png">

Where <img src="docs/tau_im.png"> and <img src="docs/s_im.png"> are the temporal position and coefficient of the _i_ th instance of kernel <img src="docs/phi_m.png">, respectively. The notation <img src="docs/n_m.png"> indicates the number of instances of <img src="docs/phi_m.png"> , which need not be the same across kernels. Kernels are not restricted in form or length.
 
A more general way of expressing this equation is in convolutional form,

<img src="docs/x(t)_conv_form.png">
 
Where <img src="docs/s_m(tau).png"> is the coefficient at time <img src="docs/tau.png"> for <img src="docs/phi_m.png"> 

#### References  
_1_ **Coding time-varying signals using sparse, shift-invariant representations.**  
Michael S. Lewicki & Terrence J. Sejnowski 1999 (doi: 10.1.1.52.1912)  
_2_ **Efficient Coding of Time-Relative Structure Using Spikes.**  
Evan C. Smith & Michael S. Lewicki 2005 (doi: 10.1162/0899766052530839)  
_3_ **Efficient auditory coding.**  
Evan C. Smith & Michael S. Lewicki 2006 (doi: 10.1038/nature04485)  
_4_ **State-dependent computations: spatiotemporal processing in cortical networks.**   
Dean V. Buonomano & Wolfgang Maass 2009 (doi: 10.1038/nrn2558)

### Choice of kernel functions

#### GammaTone (GTF), All-pole (APGF), One-zero (OZGF), and Pole-zero filter cascade

For a review see [7]
#### Gammachirp

#### References  
_1_ **Application of Gammachirp Auditory Filter as a Continuous Wavelet Analysis**  
Lotfi Salhi & Kais Ouni 2011 (arXiv:1107.5492 doi: 10.5121/sipij)  
_2_ **Interspike interval method to compute speech signals from neural firing**  
Uwe Meyer-Baese 1998 (doi: 10.1117/12.304847)  
_3_ **A Spike-Based Analogue Circuit That Emphasises Transients In Auditory Stimuli**  
Natasha Chia and Steve Collins 2004 (doi: 10.1109/ISCAS.2004.1329589)  
_4_ **The robustness of speech representations obtained from simulated auditory nerve fibers under different noise conditions**  
Tim Jurgens, Thomas Brand, Nicholas R. Clark, Ray Meddis, Guy J. Brown 2013 (doi: 10.1121/1.4817912)  
_5_ **A 6uW per Channel Analog Biomimetic Cochlear Implant Processor Filterbank Architecture With Across Channels AGC (Automatic Gain Control)**  
Guang Yang, Richard F. Lyon 2015 (doi: 10.1109/TBCAS.2014.2325907)  
_6_ **The All-Pole Gammatone Filter and Auditory Models**  
Richard F. Lyon 1996  
_7_ **Practical Gammatone-Like Filters for Auditory Processing**  
AG Katsiamis, EM Drakakis, and RF Lyon 2007 (doi: 10.1155/2007/63685)
