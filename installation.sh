#!/bin/sh
conda install pip

pip install -r requirements.txt
pip install -U bitsandbytes
pip install -U git+https://github.com/huggingface/transformers.git
pip install -U git+https://github.com/huggingface/accelerate.git
pip install -q datasets loralib sentencepiece

mkdir ./DataGeneration/logs
mkdir ./Data
touch ./DataGeneration/hf_token.txt