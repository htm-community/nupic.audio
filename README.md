# nupic.audio

[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/nupic-community/nupic.audio?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) Gitter __public__ chat channel

Auditory experiments using [cortical learning algorithms](https://scholar.google.co.uk/scholar?q=cortical+learning+algorithms&hl=en&as_sdt=0&as_vis=1&oi=scholart&sa=X&ei=fYM6VZHVMIfqaIPcgNAI&ved=0CB4QgQMwAA) (CLA) and [hierarchical temporal memory](https://scholar.google.co.uk/scholar?q=hierarchical+temporal+memory&hl=en&as_sdt=0&as_vis=1&oi=scholart&sa=X&ei=1IM6Vfy6AZKO7AbSnYDgAQ&sqi=2&ved=0CB4QgQMwAA) (HTM).

## Repositories of interest

- Numenta's [nupic.critic](https://github.com/numenta/nupic.critic) Audio streaming
- [NuMozart](https://github.com/passiweinberger/NuMozart) Digital (MIDI) streaming and composition
- [HTMforGenreClassification](https://github.com/nupic.community/nupic.audio/HTMforGenreClassification) Genre classification
- Hackathon scripts and data for [Musenta](https://github.com/jinpan/Musenta)

_Note:_ These repositories currently are all work-in-progress.

## Online videos of interest

Taken from the collection gathered via Gitter channel https://gitter.im/rcrowder/EncodingSpecificityPrinciple -

- [From Ear to Primary Cortex](https://www.youtube.com/watch?v=H1B3_qZ-HRU)
- [Anatomy - Ear Overview](https://www.youtube.com/watch?v=qYv9V2qna6I&list)
- [Anatomy - Middle Ear](https://www.youtube.com/watch?v=-OuFKmZSZoY)
- [Introduction to Biological Audition - Part 1](https://www.youtube.com/watch?v=gr_B7wnl-ks)
- [Introduction to Biological Audition - Part 2](https://www.youtube.com/watch?v=NyqpsaWYbmY)
- [Auditory perception in speech technology](https://www.youtube.com/watch?v=HEsRrNh4UrU)
- [Auditory cortex 1 - Physiology and sound localization](https://www.youtube.com/watch?v=A0KpTR_Ujks)
- [Auditory cortex 2 - Language; bats and echolocation](https://www.youtube.com/watch?v=OAOec-To-84)

## Online books and references

- https://ccrma.stanford.edu/~jos/dft/  
**Mathematics of the Discrete Fourier Transform (DFT) with audio appliccations**  
By Julius O. Smith III, Center for Computer Research in Music and Acoustics (CCRMA)

- http://www.dspguide.com/  
**The Scientist and Engineer's Guide to Digital Signal Processing**  
By Steven W. Smith, Ph.D.

- http://www.eecs.qmul.ac.uk/~simond/pub/2012/PlumbleyDixon12-ima-tutorial-slides.pdf  
**Tutorial: Music Signal Processing**  
By Mark Plumbley and Simon Dixon, Centre for Digital Music (Queen Mary University of London)

## Potential areas of investigation

- Genre and style classification
- Musical prediction and composition
- Acoustic correlation using canonical correlation analysis (CCA)
- Transient analysis (harmonic tracking)
- Motion derivative encoding (similar to optical flow)
- Echo location and spatial positioning (e.g. Anterior Ventral Cochlea Nucleus)
- Stream segmentation and seperation (includes selective attention)
- Cortical pathways and projections, 'What' and 'Where' pathways (belts?)
- Auditory nerve spike firing (e.g. IHC to CN GBC integrators)
- Dendritic micro-circuits and synaptic placement (temporal smoothing)
- Spike-timing dependent plasticity
- Acetylcholine inhibition enhancing discharge frequency but decreasing synaptic adaption
- Acoustic related cell, and dendrite, membrane properties (cascading conductances, shunting)

An alternative for the encoding of audio signals is the modelling of _**spike firing of auditory-nerve fibers**_. A collection of models can be found in the EarLab @ Boston University (http://earlab.bu.edu/ See Modelling -> Downloadable Models). If you plan to use these models, beware of their history and limitations. For example, early models lack some necessary non-linearity in their responses. 
