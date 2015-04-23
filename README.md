# nupic.audio
Auditory experiments using NuPIC HTM/CLA

Initial thoughts and ideas are being discussed in the Wiki at the moment;  
https://github.com/nupic-community/nupic.audio/wiki

Fluctuating towards;

## A sparse, shiftable kernel method of signal representation
 
The signal <img src="docs/x(t).png"> is encoded with a set of kernel functions, <img src="docs/kernel_range.png">, that can be positioned arbitrarily and independently of time [1].  

The representation with additive noise;

<img src="docs/x(t)_equation.png">

Where <img src="docs/tau_im.png"> and <img src="docs/s_im.png"> are the temporal position and coefficient of the _i_ th instance of kernel <img src="docs/phi_m.png">, respectively. The notation <img src="docs/n_m.png"> indicates the number of instances of <img src="docs/phi_m.png"> , which need not be the same across kernels. Kernels are not restricted in form or length.
 
A more general way of expressing this equation is in convolutional form,

<img src="docs/x(t)_conv_form.png">
 
Where <img src="docs/s_m(tau).png"> is the coefficient at time <img src="docs/tau.png"> for <img src="docs/phi_m.png"> 

References:  
_1_ **Coding time-varying signals using sparse, shift-invariant representations.**  
Michael S. Lewicki & Terrence J. Sejnowski 1999 (DOI: 10.1.1.52.1912)  
_2_ **Efficient Coding of Time-Relative Structure Using Spikes.**  
Evan C. Smith & Michael S. Lewicki 2005 (DOI: 10.1162/0899766052530839)  
_3_ **Efficient auditory coding.**  
Evan C. Smith & Michael S. Lewicki 2006 (DOI: 10.1038/nature04485)  
_4_ **State-dependent computations: spatiotemporal processing in cortical networks.**   
Dean V. Buonomano & Wolfgang Maass 2009 (DOI: 10.1038/nrn2558)
