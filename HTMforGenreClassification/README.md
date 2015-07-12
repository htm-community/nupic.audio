# HTM for Musical Genre Classification

Tied to issue #14 https://github.com/nupic-community/nupic.audio/issues/14

George Tzanetakis, Georg Essl, and Perry Cook produced the paper "Musical Genre Classification of Audio Signals" (http://webhome.csc.uvic.ca/~gtzan/output/tsap02gtzan.pdf and http://ismir2001.ismir.net/pdf/tzanetakis.pdf). They create feature vectors from a variety of statistics over short-time frame analysis windows, and longer texture windows containing groups of analysis windows (either whole-file or real-time streaming). The creation and description of these feature vectors I think is an important way of showing HTM SDR creation for audio signals.

Over time a large dataset has been collected, found here http://marsyas.info/ and https://github.com/marsyas/marsyas The main GTZAN dataset consists of 1000 audio tracks each 30 seconds long. It contains 10 genres, each represented by 100 tracks. The tracks are all 22050Hz Mono 16-bit audio files in .wav format, contained in a 1.6GB tar.gz file. A separate dataset exists (~250MB) for music and speech.

As a comparison from supervised learning; in 2010 Philippe Hamel and Douglas Eck detailed "Learning features from music audio with deep belief networks" http://musicweb.ucsd.edu/~sdubnov/Mu270d/DeepLearning/FeaturesAudioEck.pdf

This idea for a new HTM showpiece is to implement the statistical analysis inside a fork of nupic.critic and from there, with the GTZAN dataset, **investigate the unsupervised recognition of musical genres**. An alternative is to train with musical styles rather than genre. With potential to expand into composition later on. Or adopt an Inner Hair Cell model that can reproduce the irregular spiking of auditory nerve fibers, with an investigation of the integrative effects of bushy cells in the Cochlear Nucleus.
