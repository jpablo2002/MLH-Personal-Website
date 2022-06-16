#!/bin/bash

tmux kill-server || echo "There was no tmux server to kill"

cd ~/project-boisterous-baboons/

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install -r requirements.txt

tmux new -d -s my-portfolio 'source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'
