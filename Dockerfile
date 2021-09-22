FROM arm64v8/python:3

# Default powerline10k theme, no plugins installed
# RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.1/zsh-in-docker.sh)"
RUN sudo apt-get install git-all python3-dev python3-pip python3-setuptools cmake build-essential
RUN python3 -m pip install couchbase