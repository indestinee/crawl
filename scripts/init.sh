echo git submodule update --init --recursive
git submodule update --init --recursive

echo 'pip install [packages]'
pip3 install -r requirements.txt
