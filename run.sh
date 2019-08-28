#!/bin/bash

echo "Starting reddit post..."
cd ~/Desktop/datasciencereddit
source venv/bin/activate
python datascience_reddit.py 
deactivate
cd
echo "Ending reddit post"
