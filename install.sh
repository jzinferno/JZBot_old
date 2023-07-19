#!/bin/sh

git clone --recurse --depth=1 https://github.com/jzinferno/JZBot.git
cd JZBot
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
find . -name "requirements.txt" -exec pip3 install -r {} \;
