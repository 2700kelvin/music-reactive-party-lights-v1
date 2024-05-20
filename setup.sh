#!/usr/bin/env bash
set +e

xcode-select --install
set -e
# brew install numpy 
# May need to do sudo pip3 install numpy --compile --pre
sudo pip3 install -r requirements.txt
