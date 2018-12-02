# Speech Recognition

The aim of this example is:

- Test the ability of NuPIC unsupervised learning, alongside a supervised trained SDR Classifier, to recognize spoken digits.
- To test traditional Fourier Analysis approaches to encoding, with a simulated biological spike encoding.
- To compare recognition with existing ML Neural Networks, particularly and _importantly_ with regards to added background noise and other speakers.

A number of existing ML based examples can be used to contrast with this example, such as:
1. https://towardsdatascience.com/speech-classification-using-neural-networks-the-basics-e5b08d6928b7
1. https://towardsdatascience.com/audio-classification-using-fastai-and-on-the-fly-frequency-transforms-4dbe1b540f89

## Encoding

### Frequency Encoding

### Spike Encoding

## Network setup

### Spatial Pooler

### Temporal Memory

### SDR Classifier

http://hopding.com/sdr-classifier

> The purpose of the SDR Classifier is identical to that of the older CLA Classifier: learn associations between a given state of the Temporal Memory at time t, and the value that is to be fed into the Encoder at time t+n (where n is the number of steps into the future you want to predict. t+1, t+5, t+2 - or all three!).
> You can also think of it as mapping activation patterns (vector of Temporal Memory’s active cells) to probability distributions (for the possible encoder buckets).

## Training

### Classifier training

## Testing

Background noise data:  
http://soundbible.com/641-Urban-Traffic.html  
http://soundbible.com/1265-Shopping-Mall-Ambiance.html  

## Dataset and Python packages

Dependant python packages can be install using the following command:

```sh
pip install -r requirements.txt
```

Dependant Git repositories can be cloned using the following Python script:

```sh
python RepoClone.py
```

**Note**: RepoClone.py uses [GitPython](https://github.com/gitpython-developers/GitPython). It requires [Git](https://git-scm.com/) being installed on the system, and accessible via the system's PATH.

### Repository cloning (RepoClone.py)

#### Free spoken digit dataset (FFDD)

A free audio dataset of spoken digits. Think MNIST for audio. -  https://github.com/Jakobovski/free-spoken-digit-dataset

#### Frequency Encoder

A custom frequency encoder for the HTM. - https://github.com/marionleborgne/frequency-encoder

#### ISOLET dataset

The database consists of 7800 spoken letters, 2 productions of each letter by 150 speakers - https://archive.ics.uci.edu/ml/datasets/isolet

