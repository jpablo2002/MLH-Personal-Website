#!/bin/bash

tmux kill-server

cd /root/project-boisterous-baboons/

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new -d 'source python3-virtualenv/bin/activate; flask run --host=0.0.0.0'
