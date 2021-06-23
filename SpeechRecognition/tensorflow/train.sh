#!/bin/sh -

# python organize_data.py

python train.py --data_url=  --data_dir=./data \
    --wanted_word=zero,one,two,three \
    --background_volume=0.0 --silence_percentage=0 --unknown_percentage=0 \
    --sample_rate=8000 --how_many_training_steps=400,100 \
    --train_dir=./data_train