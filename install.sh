conda create -n venv python=3.6
source activate venv
#conda install numpy
conda install --file requirements.txt
pip install git+https://github.com/quantopian/zipline.git@b661d075e4a6d00f8da91083ac17ac371b0f0a65
cat requirements.txt | xargs -n 1 pip install
