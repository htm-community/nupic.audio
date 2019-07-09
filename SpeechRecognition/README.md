# Speech Recognition

The aim of this example is to:

- Test the ability of NuPIC unsupervised online learning, along with a supervised trained SDR Classifier, to recognize spoken digits.
- To test traditional Fourier Analysis approaches to encoding and simulated biological spike encoding.
- Compare recognition ability with existing ML Neural Networks, particularly and _importantly_, with regards to added background noise and other speakers.

A number of existing ML based examples can be used to compare with this example. For example:

1. [Speech Classification Using Neural Networks: The Basics](https://towardsdatascience.com/speech-classification-using-neural-networks-the-basics-e5b08d6928b7)
1. [Audio Classification using FastAI and On-the-Fly Frequency Transforms](https://towardsdatascience.com/audio-classification-using-fastai-and-on-the-fly-frequency-transforms-4dbe1b540f89)
1. [Using CNNs and RNNs for Music Genre Recognition](https://towardsdatascience.com/using-cnns-and-rnns-for-music-genre-recognition-2435fb2ed6af)

Further information on audio signal processing can be found here: [SPECTRAL AUDIO SIGNAL PROCESSING](https://ccrma.stanford.edu/~jos/sasp/), Stanford's Center for Computer Research in Music and Acoustics (CCRMA)

A brief overview of human ear anatomy can be found here: [Anatomy - Ear Overview](https://www.youtube.com/watch?v=qYv9V2qna6I), Armando Hasudungan.

## Encoding

### [Frequency Encoding](https://github.com/marionleborgne/frequency-encoder)

As described in the Frequency Encoder [README.md](https://github.com/marionleborgne/frequency-encoder/blob/master/README.md) file;  

> The FrequencyEncoder encodes a time series chunk (or any 1D array of numeric values) by taking the power spectrum of the signal and discretizing it. The discretization is done by slicing the frequency axis of the power spectrum into bins. The maximum amplitude of the power spectrum in this frequency bin is encoded by a [Scalar Encoder](http://nupic.docs.numenta.org/1.0.3/api/algorithms/encoders.html#scalar-encoders).

To make use of the Frequency Encoder, continuous signal data needs to be broken into chunks. Achieving this is done by extracting a contiguous chunk of input data and applying an appropriate window function to this chunk of data. The next contiguous chunk of input data is extracted with appropriate overlay with the previous chunk. These chunks of data can then be passed into the Frequency Encoder to obtain a sparse distributed representation (SDR) for each chunk.

https://ccrma.stanford.edu/~jos/sasp/Spectrum_Analysis_Windows.html

Following is an example of using a window function applied to a chunk of input data.

<img src="./docs/windowing.png" alt="Hann window function" style="width: 400px;"/>

The Frequency Encoder uses a Short Time Fourier Transform (STFT). Care must be taken when determining how big a chunk of input data is (number of data samples),
and the parameters used for the STFT and Frequency Encoder (specifically the Scalar Encoder).

> One of the pitfalls of the STFT is that it has a fixed resolution. The width of the windowing function relates to how the signal is represented - it determines whether there is good frequency resolution (frequency components close together can be separated) or good time resolution (the time at which frequencies change). A wide window gives better frequency resolution but poor time resolution. A narrower window gives good time resolution but poor frequency resolution.  
Source: https://en.wikipedia.org/wiki/Short-time_Fourier_transform

For a great overview of processes involved, and related, to the Frequency Encoder, refer to the following article: [Speech Processing for Machine Learning: Filter banks, Mel-Frequency Cepstral Coefficients (MFCCs) and What's In-Between](https://haythamfayek.com/2016/04/21/speech-processing-for-machine-learning.html)

TODO:
* https://github.com/jameslyons/python_speech_features
* [HIERARCHICAL RESIDUAL-PYRAMIDAL MODEL FOR LARGE CONTEXT BASED MEDIA
PRESENCE DETECTION](https://s3.us-east-2.amazonaws.com/alexapapers/HierarchicalResidualPyramidalModelForLargeContextBasedMediaPresenceDetection.pdf)
* Discuss MFCC features, log mel-filter bank energy (LFBE) features, wrt to SDR encoding and ASR

### [Cochlea Encoding](https://github.com/mrkrd/cochlea)

For spike encoding a Python package called [cochlea](https://github.com/mrkrd/cochlea) can be used.

> cochlea is a collection of inner ear models. All models are easily accessible as  Python functions. They take sound signal as input and return spike trains of the auditory nerve fibers (ANF).

From the three inner ear models implemented in the [cochlea](https://github.com/mrkrd/cochlea) package, one compelling reason to use spike encoding is:

> The ability of auditory models to code speech is already very elaborate, all three outperform classical [Mel-frequency cepstral](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum) features (MFCC), the “gold standard” of automatic speech recognition.

As mentioned in the accompanying research paper [1], the **Zilany model (2014)** [2,3] is the most feature rich.

1. Rudnicki M., Schoppe O., Isik M., Völk F. and Hemmert W. (2015). Modeling auditory coding: from sound to spikes. Cell and Tissue Research, Springer Nature, 361, 159—175. http://link.springer.com/article/10.1007/s00441-015-2202-z
1. Zilany MSA, Bruce IC, Nelson PC, Carney LH (2009) A phenomenological model of the synapse between the inner hair cell and auditory nerve: Long-term adaptation with power-law dynamics. J Acoust Soc Am 126(5):2390
1. Zilany MSA, Bruce IC, Carney LH (2014) Updated parameters and expanded simulation options for a model of the auditory periphery. J Acoust Soc Am 135(1):283–286

Also:
> Offset adaptation is only implemented in Zilany’s phenomenological model. Offset adaptation can be very important for further neuronal processing. Therefore, if modeled auditory nerve fibers (ANF) spike trains are used as input to neurons in the brainstem (or even higher), one should consider the Zilany et al. (2014) model.

Another advantage of using the [cochlea](https://github.com/mrkrd/cochlea) Zilany model implementation, over the Frequency Encoder, is that an entire sample can be input into it, and it returns a convenient [pandas](https://pandas.pydata.org/) data frame. No need to segment/chunk the data and apply a window function.

Disadvantages are that the Zilany model has a lower frequency bound of 125 Hz, and a lower bound of 100 kHz expected sampling frequency. The original Zilany implementaion (2009) used a 10th order cascade filter and lower bound of 500 kHz, this was subsequently changed to a simpler 5th order cascade filer and 100 kHz sampling frequency lower bound.

The output of the CochleaEncoder is a neurogram (an image of neural activity). The following figure shows a [SciPy Chirp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.chirp.html), starting at 300 Hz and ramp up to 3000 Hz. With the output neurogram as the central graph, and the bottom graph is a binary representation of the neurogram.

<img src="./docs/sine_spike_encoding.png" alt="Chirp spike encoding" style="width: 400px;"/>

The following shows an input speech signal (the spoken word 'Zero'), with the same central neurogram, and binary representation of the neurogram at the bottom.

<img src="./docs/wav_spike_encoding.png" alt="Wav spike encoding" style="width: 400px;"/>

The following shows the amount of bit sparsity in the binary neurogram of the speech signal (spoken word 'Zero').

<img src="./docs/wav_spike_sparsity.png" alt="Wav spike sparsity" style="width: 400px;"/>

### Resampling speech data

The [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) has been recorded using an 8000 Hz sampling rate. With each mono sample typically around one second long. Samples can be up-sampled using a Python package called [resampy](https://github.com/bmcfee/resampy).

> `resampy` is a python module for efficient time-series resampling. It is based on the band-limited sinc interpolation method for sampling rate conversion as described by [1].

1.	Smith, Julius O. Digital Audio Resampling Home Page Center for Computer Research in Music and Acoustics (CCRMA), Stanford University, 2015-02-23. Web published at http://ccrma.stanford.edu/~jos/resample/.

Other resampling methods can be used in Python. Refer to this blog post for an overview: http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html

### Batch encoding

The Zilany inner ear simulation used in the CochleaEncoder can take quite a while to process an entire sample.

Once the [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) (FSDD) repository has been cloned (see below, `RepoClone.py`), the `batch_encode.py` Python script can be used to run the CochleaEncoder on all the FSDD wav files, and produce corresponding NumPy data files.

The CochleaEncoder default entry function is the `encodeIntoNeurogram` that returns the 2-dimensional NumPy neurogram array, that is then saved out.

## Network setup

Spoken digit speech is first encoded (using the Cochlea or Frequency encoder), and sparse distributed representations (SDR) are passed into a Spatial Pooler (SP).

The output of the SP is an array of active column indices that is passed into a Temporal Memory (TM).

The output of the TM is an array of active cells that is passed into the SDR Classifier (CL). Which outputs 1-step ahead classification predictions for each digit shown to the network.

Below are links to further information on the HTM parts used within training and testing.

### Encoder

Further information on Encoders can be found in the Numenta BaMI:
- https://numenta.com/assets/pdf/biological-and-machine-intelligence/BaMI-Encoders.pdf

### Spatial Pooler

Further information on Spatial Pooling can be found in the following Numenta website pages:
- https://numenta.com/neuroscience-research/research-publications/papers/htm-spatial-pooler-neocortical-algorithm-for-online-sparse-distributed-coding/
- https://numenta.com/resources/biological-and-machine-intelligence/spatial-pooling-algorithm/

### Temporal Memory

Further information on Temporal Memory can be found in the following Numenta website page:
- https://numenta.com/resources/biological-and-machine-intelligence/temporal-memory-algorithm/

### SDR Classifier

[Andrew Dillon](https://andrewjdillon.com/) has produce an excellent breakdown of the SDR Classifier. Refer to his webpage for further information: http://hopding.com/sdr-classifier

> The purpose of the SDR Classifier is identical to that of the older CLA Classifier: learn associations between a given state of the Temporal Memory at time t, and the value that is to be fed into the Encoder at time t+n (where n is the number of steps into the future you want to predict. t+1, t+5, t+2 - or all three!). You can also think of it as mapping activation patterns (vector of Temporal Memory’s active cells) to probability distributions (for the possible encoder buckets).

## Training

### Classifier training

One question arises from the supervised training required by the SDR Classifier. How many times do the speech samples need to be presented to the classifier, via the spatial pooler and temporal memory.

The following graph shows the progress of the classifier when presenting the four speech samples (random order) twice, four, eight, sixteen, and thirty two times. The classifier is tested with the spoken "One" speech sample. The classifier achieves a 92% prediction accuracy when it trained with the four speech samples thirty two times. And as expected, the prediction of the other speech samples diminishes.

<img src="./classifier_performance.png" alt="Classifier performance" style="width: 400px;"/>

## Testing

### Heard and Unheard spoken digits

Training using four speech samples (spoken words "Zero", "One", "Two", and "Three"). 16 times randomly, i.e. 64 speech samples total.

Testing with one **heard** spoken word "One", achieves 74% prediction accuracy:
<img src="./results_16x.png" alt="Classifier predictions" style="width: 400px;"/>

Testing with one **unheard** spoken word "One", achieves 59% accuracy:
<img src="./results_16x_un.png" alt="Classifier predictions" style="width: 400px;"/>

### Speaker variation

Training with six variations of the digits "Zero", "One", "Two", and "Three". Randomly presented for a total of 64 spoken digits.

Testing with four **unheard** variations of the spoken digit "One".

<img src="./speaker_variation.png" alt="Speaker variation" style="width: 400px;"/>

### Additive background noise

The `mix_noise.py` Python script takes an Urban Traffic wav file and mixes it with a speech sample. Outputting new speech wav files with 5%, 10%, 25%, and 50% of the noisy traffic mixed in.

The Urban Traffic wav file can be downloaded here: http://soundbible.com/641-Urban-Traffic.html

Similar to the speaker variation the network is trained using 6 variations of the spoken words "Zero", "One", "Two", and "Three". The **unheard** spoken word "One", with added traffic noise, is then tested against the network.

Below are the results from the SDR Classifier:
<img src="./additive_noise.png" alt="Additive noise" style="width: 400px;"/>

### Alternative speakers

Similar to the speaker variation test. One speakers ("Jackson") speech is used during network and classifier training. Then the network is tested with three other speakers, all saying the spoken word "One".

Below are the results from the SDR Classifier for all four speakers:
<img src="./alternative_speakers.png" alt="Alternative speakers" style="width: 400px;"/>

## Dimensionality reduction/attention

The majority of the tests conducted so far, have used small sections of each individual speech sample for training and testing (10 - 25 milliseconds worth). The main reason for this is that the Zilany inner ear model, used in the CochleaEncoder, requires the input data to use a minimum of 100 kHz sampling frequency. That creates around 50K SDRs for each speech sample, which has big implications on the time it takes to train and test a HTM network on a typical laptop/PC.

Rasha Ibrahim's [Ph.D Theses](http://hdl.handle.net/11375/11980) (Figure 3.6) provides a comparison between the simpler 5th order middle-ear filter and the original 10th order filter model ([Bruce et al., 2003](https://doi.org/10.1121/1.1519544), Figure 19, Appendix A) for sampling frequencies down to 40 kHz. The 100 kHz preset minimum sampling frequency in the CochleaEncoder (via the Cochlea Python package) is used to provide the best lowest alternative for the middle-ear filtering. We should therefore be able to use a sampling frequency below the 100 kHz preset.

We know that using 2.5K SDRs (25 milliseconds @ 100 kHz) per speech data provides a manageable amount of training and testing. But can we reduce the number of SDRs that get sent into a HTM network _and_ still maintain the encouraging results seen so far?

Reviewing the passage of auditory sensory information from the inner ear through to the cortex, there are quite a few processing stages containing a variety of cell types. A tonotopic layout is maintained from hair cell layout to cortex. So we can investigate the contribution of various cell types with respect to dimensionality reduction and/or attentional mechanisms.

> Neurons in the primary auditory cortex are tuned to the intensity and specific frequencies of sounds, but the synaptic mechanisms underlying this tuning remain uncertain. Inhibition seems to have a functional role in the formation of cortical receptive fields, because stimuli often suppress similar or neighboring responses, and pharmacological blockade of inhibition broadens tuning curves...  
> Inhibition and excitation occurred in a precise and stereotyped temporal sequence: an initial barrage of excitatory input was rapidly quenched by inhibition, truncating the spiking response within a few (1–4) milliseconds. Balanced inhibition might thus serve to increase the temporal precision6 and thereby reduce the randomness of cortical operation, rather than to increase noise as has been proposed previously. 
>  
> Source: Balanced inhibition underlies tuning and sharpens spike timing in auditory cortex, Michael Wehr & Anthony M. Zador. Nature 426, 442–446 (2003). https://doi.org/10.1038/nature02116


### Ventral Cochlea Nucleus (VCN)

Pathways from the Ventral Cochlea Nucleus towards the thalamas and cortex:
- Superior Olivary cluster (SO, incl. horizontal sound localization)
- Ventral Nuclei of the Lateral Lemnicus (VNLL, incls. pattern recognition)
- Inferior Colliculus (IC, incls. vertical sound localization assisted by the Dorsal Cochlea Nucleus)

The VCN feeds into the SO and VNLL, then they both feed into the IC.

### Ventral Nuclei of the Lateral Lemniscus (VNLL)

> The function of the ventral nucleus of the lateral lemniscus (VNLL), a secondary processing site within the auditory brain stem, is unclear. It is known to be a major source of inhibition to the inferior colliculus (IC). It is also thought to play a role in coding the temporal aspects of sound, such as onsets and the periodic components of complex stimuli...  
> Our data suggest it is a result of an intrinsic circuit activated by the octopus cell pathway originating in the contralateral cochlear nucleus; this pathway is known to convey exquisitely timed and broadly tuned onset information. This powerful inhibition within the VNLL appears to control the timing of this structure's inhibitory output to higher centers, which has important auditory processing outcomes. The circuit also provides a pathway for fast, broadly tuned, onset inhibition to the IC.
>
> Various lines of evidence indicate that inhibition plays as important a role as excitation in controlling spike timing in auditory nuclei. One of the major inhibitory pathways within the auditory brain stem originates in the ventral nucleus of the lateral lemniscus (VNLL), a nucleus thought to play a role in temporal pattern processing. This structure is a crucial integration site for a subset of fibers from the lower auditory brain stem en route to the inferior colliculus (IC). VNLL neurons receive convergent excitatory input from a variety of cell types within the contralateral cochlear nucleus (CN), including an exclusive projection from the octopus cell area (OCA) of the contralateral CN. Octopus cells give rise to thick axons that terminate in large calyx-like synapses, akin to endbulbs of Held in other auditory nuclei. These characteristics suggest that this pathway provides fast and faithful transmission of timing information. Octopus cells respond to the onsets of sounds with exquisitely timed responses, termed onset-ideal (OI). This response pattern is a result of the detection of synchrony in auditory nerve fiber inputs representing a wide range of characteristic frequencies (CFs). The function of these cells and their projection to the VNLL is unknown, although they seem well suited to encode onsets, transients, and temporal features of complex, periodic stimuli. The role of the VNLL's projection to the IC, which is inhibitory is equally uncertain.
>
> Source: Powerful, Onset Inhibition in the Ventral Nucleus of the Lateral Lemniscus, David A. X. Nayagam, Janine C. Clarey, and Antonio G. Paolini. https://doi.org/10.1152/jn.00167.2005

> Two patterns of responses to tones have been observed in recordings from the ventral lemniscal nuclei. Regular, sustained firing and are sharply tuned; others respond with a sharply timed action potential at the onset of a tone and are broadly tuned. While many authors consider the ventral lemniscal nuclei to be monaural, many studies shown that neurons in this area are indeed consistently driven through the contralateral ear.  
> Spherical bushy cells (SBCs) in the VNLLv are broadly tuned and respond at the onset of sounds. The responses to sound of neurons in the columnar region of the bat and and the VNLLv of the cat resemble responses to sound of octopus cells in many ways. Like neurons in the columnar area of the VNLL of bats, octopus cells responded to the directionality of sweeps.  
> Other neurons in the VNLL and INLL respond to tones with regular, sustained firing or "chopping". These neurons were sharply tuned. Their nonmonotonic firing rates as a function of intensity that inhibition contributed to responses to sounds. Bushy and stellate cells that provide the major excitatory input to the more sharply tuned and tonically firing multipolar cells of the ventral lemniscal nuclei are sharply tuned and respond to tones with more sustained firing.  
>
> Source: Chapter 6.4, Integrative Functions in the Mammalian Auditory Pathway, Editors Oertel, Fay, and Popper. Springer ISBN 0-387-98903-X

### Inferior Colliculus (IC)

...

## Dataset, Git clones, and Python packages

Dependent python packages can be install using the following command:

```sh
pip install -r requirements.txt
```

### Repository cloning

Dependent Git repositories can be cloned using the following Python script:

```sh
python RepoClone.py
```

**Note**: `RepoClone.py` uses [GitPython](https://github.com/gitpython-developers/GitPython). That requires [Git](https://git-scm.com/) being installed on the system, and accessible via the system's PATH.

The following repositories are cloned using this Python script:

#### Free spoken digit dataset (FFDD)

A free audio dataset of spoken digits. Think MNIST for audio - https://github.com/Jakobovski/free-spoken-digit-dataset

#### Frequency Encoder

A custom frequency encoder for the HTM - https://github.com/marionleborgne/frequency-encoder

### Alternative datasets

Disregarding restrictive licensed datasets, e.g. TIDIGITS, the following are a few alternative datasets that can be considered:

#### Speech Commands dataset

Consists of over 105,000 WAVE audio files (v0.02) of people saying thirty different words. This data was collected by Google and released under a Creative Commons BY 4.0 license.

> Twenty core command words were recorded, with most speakers saying each of them five times. The core words are "Yes", "No", "Up", "Down", "Left", "Right", "On", "Off", "Stop", "Go", "Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", and "Nine". To help distinguish unrecognized words, there are also ten auxiliary words, which most speakers only said once. These include "Bed", "Bird", "Cat", "Dog", "Happy", "House", "Marvin", "Sheila", "Tree", and "Wow".

Install Tensorflow. For example, on Mac OSX:

```bash
$ pip install tensorflow
$ git clone https://github.com/tensorflow/tensorflow.git
```

Train the speech commands example:

```bash
$ cd tensorflow/tensorflow/examples/speech_commands
$ python train.py

I0701 17:15:32.307061 4568024512 train.py:235] Step #1: rate 0.001000, accuracy 9.0%, cross entropy 2.569139
...
I0701 17:32:42.993186 4568024512 train.py:263] Step 400: Validation accuracy = 27.4% (N=4445)
...
I0701 18:19:14.371365 4568024512 train.py:235] Step #1501: rate 0.001000, accuracy 50.0%, cross entropy 1.462428
...
I0701 18:23:57.855741 4568024512 train.py:263] Step 1600: Validation accuracy = 59.2% (N=4445)
...
I0702 00:21:14.057275 4568024512 train.py:235] Step #10000: rate 0.001000, accuracy 82.0%, cross entropy 0.539936
I0702 00:21:50.334923 4568024512 train.py:263] Step 10000: Validation accuracy = 87.0% (N=4445)
...
I0702 17:09:18.322210 4699891136 train.py:263] Step 18000: Validation accuracy = 89.1% (N=4445)
I0702 17:09:58.091881 4699891136 train.py:295] Final test accuracy = 88.0% (N=4890)
```

Freezing and testing the trained model:

```bash
$ python freeze.py --start_checkpoint=/tmp/speech_commands_train/conv.ckpt-18000 --output_file=/tmp/my_frozen_graph.pb
...
I0702 17:11:52.593321 4498675136 freeze.py:144] Saved frozen graph to /tmp/my_frozen_graph.pb

$ python label_wav.py --graph=/tmp/my_frozen_graph.pb --labels=/tmp/speech_commands_train/conv_labels.txt --wav=/tmp/speech_dataset/left/25e95412_nohash_2.wav
left (score = 0.77347)
right (score = 0.16540)
_unknown_ (score = 0.04902)
```

Refs:
- [Simple Audio Recognition](https://www.tensorflow.org/tutorials/sequences/audio_recognition) - TensorFlow Tutorial
- [Speech Commands: A Dataset for Limited-Vocabulary Speech Recognition](https://arxiv.org/abs/1804.03209)
- https://petewarden.com/2018/04/11/speech-commands-is-now-larger-and-cleaner/
- https://ai.googleblog.com/2017/08/launching-speech-commands-dataset.html

#### ISOLET dataset

The database consists of 7800 spoken letters, 2 productions of each letter by 150 speakers - https://archive.ics.uci.edu/ml/datasets/isolet

## Future Work

### Cochlear Nucleus

> The mammalian cochlear nucleus (CN) consists of a diverse set of neurons both physiologically and morphologically that are involved in processing different aspects of the sound signal.  
>
> Source: [Response patterns to sound associated with labeled globular/bushy cells in cat](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2518325/)

> - Bushy cells preserve or sharpen information in the firing patterns of auditory nerve fibers that conveys the fine structure of sounds, including phase locking at low frequencies.  
> - Octopus cells detect the coincident firing of large groups of auditory nerve fibers, signaling the presence of onsets and broadband transients.  
> - Individual T-Stellate cells detect the amplitude of sounds over a narrow frequency range and as a population they detect the ongoing spectrum of sounds impinging on the ear.  
> - D-Stellate cells detect coincident firing from many auditory nerve fibers but the temporal and spatial summation of inputs obscures temporal fine structure.  
>
> Source: [The Cochlear Nuclei: Synaptic Plasticity in Circuits and Synapses in the Ventral Cochlear Nuclei](https://www.oxfordhandbooks.com/view/10.1093/oxfordhb/9780190849061.001.0001/oxfordhb-9780190849061-e-4)

[Signal integration at spherical bushy cells enhances representation of temporal structure but limits its range.](https://elifesciences.org/articles/29639)
eLife 2017;6:e29639 DOI: 10.7554/eLife.29639

TODO: https://github.com/mrkrd/cochlear_nucleus - A young repo that looks too limited in it's potential usage in this example.


### CNModel

> Abstract: Models of the auditory brainstem have been an invaluable tool for testing hypotheses about auditory information processing and for highlighting the most important gaps in the experimental literature. Due to the complexity of the auditory brainstem, and indeed most brain circuits, the dynamic behavior of the system may be difficult to predict without a detailed, biologically realistic computational model. Despite the sensitivity of models to their exact construction and parameters, most prior models of the cochlear nucleus have incorporated only a small subset of the known biological properties. This confounds the interpretation of modelling results and also limits the potential future uses of these models, which require a large effort to develop. To address these issues, we have developed a general purpose, biophysically detailed model of the cochlear nucleus for use both in testing hypotheses about cochlear nucleus function and also as an input to models of downstream auditory nuclei. The model implements conductance-based Hodgkin-Huxley representations of cells using a Python-based interface to the NEURON simulator. Our model incorporates most of the quantitatively characterized intrinsic cell properties, synaptic properties, and connectivity available in the literature, and also aims to reproduce the known response properties of the canonical cochlear nucleus cell types. Although we currently lack the empirical data to completely constrain this model, our intent is for the model to continue to incorporate new experimental results as they become available.
>
> Source: Paul B. Manis, Luke Campagnola, A biophysical modelling platform of the cochlear nucleus and other auditory circuits: From channels to networks, Hearing Research, Volume 360, 2018, Pages 76-91, ISSN 0378-5955, https://doi.org/10.1016/j.heares.2017.12.017.
>
> Github: https://github.com/cnmodel/cnmodel - Neuron support library.

