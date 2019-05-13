# Speech Recognition

The aim of this example is to:

- Test the ability of NuPIC unsupervised online learning, along with a supervised trained SDR Classifier, to recognize spoken digits.
- To test traditional Fourier Analysis approaches to encoding and simulated biological spike encoding.
- Compare recognition ability with existing ML Neural Networks, particularly and _importantly_, with regards to added background noise and other speakers.

A number of existing ML based examples can be used to compare with this example. For example:

1. [Speech Classification Using Neural Networks: The Basics](https://towardsdatascience.com/speech-classification-using-neural-networks-the-basics-e5b08d6928b7)
1. [Audio Classification using FastAI and On-the-Fly Frequency Transforms](https://towardsdatascience.com/audio-classification-using-fastai-and-on-the-fly-frequency-transforms-4dbe1b540f89)
1. [Using CNNs and RNNs for Music Genre Recognition](https://towardsdatascience.com/using-cnns-and-rnns-for-music-genre-recognition-2435fb2ed6af)

Further information on audio signal processing can be found here: Stanford's Center for Computer Research in Music and Acoustics (CCRMA) - [SPECTRAL AUDIO SIGNAL PROCESSING](https://ccrma.stanford.edu/~jos/sasp/)

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

Also:
> Offset adaptation is only implemented in Zilany’s phenomenological model. Offset adaptation can be very important for further neuronal processing. Therefore, if modelled ANF spike trains are used as input to neurons in the brainstem (or even higher), one should consider the Zilany et al. (2014) model.

Another advantage of using the [cochlea](https://github.com/mrkrd/cochlea) Zilany model implementation, over the Frequency Encoder, is that an entire sample can be input into it, and it returns a convenient [pandas](https://pandas.pydata.org/) data frame. No need to segment/chunk the data and apply a window function.

One disadvantage is that the Zilany model has a lower frequency bound of 125 Hz.

1. Rudnicki M., Schoppe O., Isik M., Völk F. and Hemmert W. (2015). Modeling auditory coding: from sound to spikes. Cell and Tissue Research, Springer Nature, 361, 159—175. http://link.springer.com/article/10.1007/s00441-015-2202-z
1. Zilany MSA, Bruce IC, Nelson PC, Carney LH (2009) A phenomenological model of the synapse between the inner hair cell and auditory nerve: Long-term adaptation with power-law dynamics. J Acoust Soc Am 126(5):2390
1. Zilany MSA, Bruce IC, Carney LH (2014) Updated parameters and expanded simulation options for a model of the auditory periphery. J Acoust Soc Am 135(1):283–286

The output of the CochleaEncoder is a neurogram (an image of neural activity). The following figure shows a [SciPy Chirp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.chirp.html), starting at 300 Hz and ramp up to 3000 Hz. With the output neurogram as the central graph, and the bottom graph is a binary representation of the neurogram.

<img src="./docs/sine_spike_encoding.png" alt="Chirp spike encoding" style="width: 400px;"/>

The following shows an input speech signal (the spoken word 'Zero'), with the same central neurogram, and binary representation of the neurogram at the bottom.

<img src="./docs/wav_spike_encoding.png" alt="Wav spike encoding" style="width: 400px;"/>

The following shows the amount of bit sparsity in the binary neurogram of the speech signal (spoken word 'Zero').

<img src="./docs/wav_spike_sparsity.png" alt="Wav spike sparsity" style="width: 400px;"/>

### Resampling speech data

The [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) has been recorded using an 8000 Hz sampling rate. With each mono sample typically around one second long. Samples can be up-sampled using a Python package called [resampy](https://github.com/bmcfee/resampy).

Other resampling methods can be used in Python. Refer to this blog post for an overview: http://signalsprocessed.blogspot.com/2016/08/audio-resampling-in-python.html

### Batch encoding

The Zilany inner ear simulation used in the CochleaEncoder can take quite a while to process an entire sample.

Once the [Free Spoken Digit Dataset](https://github.com/Jakobovski/free-spoken-digit-dataset) (FSDD) repository has been cloned (see below, `RepoClone.py`), the `batch_encode.py` Python script can be used to run the CochleaEncoder on all the FSDD wav files, and produce corresponding NumPy data files.

The CochleaEncoder default entry function is the `encodeIntoNeurogram` that returns the 2-dimensional NumPy neurogram array, that is then saved out.

## Network setup

Spoken digit speech is first encoded (using the Cochlea or Frequency encoder), and sparse distributed representations (SDR) are passed into a Spatial Encoder (SP). The output of the SP is an array of active column indicies that is passed into a Temporal Memory (TM). The output of the TM is an array of active cells that is passed into the SDR Classifier (CL). Which outputs 1-step ahead classification predictions for each digit shown to the network.

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

The following graph shows the progress of the classifier when presenting the four speech samples (random order) twice, four, eight, sixteen, and thirty two times. The classifier is tested with the spoken "One" speech sample. The classifier achieves a 92% prediction accuracy when it sees the four speech samples thirty two times. And as expected, the prediction of the other speech samples diminishes.

<img src="./classifier_performance.png" alt="Classifier performance" style="width: 400px;"/>

## Testing

Training using four speech samples (spoken words "Zero", "One", "Two", and "Three"). 16 times randomly, i.e. 64 speech samples total.

Testing with one **heard** spoken word "One", achieves 74% prediction accuracy:
<img src="./results_16x.png" alt="Classifier predictions" style="width: 400px;"/>

Testing with one **unheard** spoken word "One", achieves 59% accuracy:
<img src="./results_16x_un.png" alt="Classifier predictions" style="width: 400px;"/>

TODO: Mix in background noise data:  
http://soundbible.com/641-Urban-Traffic.html  
http://soundbible.com/1265-Shopping-Mall-Ambiance.html  

## Dataset, Git clones, and Python packages

Dependant python packages can be install using the following command:

```sh
pip install -r requirements.txt
```

### Repository cloning (`RepoClone.py`)

Dependant Git repositories can be cloned using the following Python script:

```sh
python RepoClone.py
```

**Note**: `RepoClone.py` uses [GitPython](https://github.com/gitpython-developers/GitPython). That requires [Git](https://git-scm.com/) being installed on the system, and accessible via the system's PATH.

The following repositories are cloned using this Python script:

#### Free spoken digit dataset (FFDD)

A free audio dataset of spoken digits. Think MNIST for audio - https://github.com/Jakobovski/free-spoken-digit-dataset

#### Frequency Encoder

A custom frequency encoder for the HTM - https://github.com/marionleborgne/frequency-encoder

#### ISOLET dataset

This dataset is optional and is **not** cloned as part of the `RepoClone.py` Python script. The database consists of 7800 spoken letters, 2 productions of each letter by 150 speakers - https://archive.ics.uci.edu/ml/datasets/isolet

## Future Work

### Ventral Cochlear Nucleus

> The mammalian cochlear nucleus (CN) consists of a diverse set of neurons both physiologically and morphologically that are involved in processing different aspects of the sound signal. One class of CN neurons that is located near the entrance of the auditory nerve (AN) to the CN has an oval soma with an eccentric nucleus and a short-bushy dendritic tree and is called a globular/bushy cell (GBC). They contact the principal cells of the medial nucleus of the trapezoid body (MNTB) with the very large calyx of Held that is one of the most secure synapses in the brain.  
Source: [Response patterns to sound associated with labeled globular/bushy cells in cat](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2518325/)

TODO: https://github.com/mrkrd/cochlear_nucleus
