pip install -U bitsandbytes
pip install -U git+https://github.com/huggingface/transformers.git
pip install -U git+https://github.com/huggingface/accelerate.git
pip install -q datasets loralib sentencepiece

mkdir ./DataGeneration/logs
mkdir ./Data
mkdir ./Data/Storage_Llama
touch ./DataGeneration/hf_token.txt