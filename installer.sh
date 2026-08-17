#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Privilege escalation required. Elevating to root..."
    exec sudo bash "$0" "$@"
fi

echo "Deploying pytrm globally to /usr/local/bin..."

#THE MAJOR FIX IS BELOW:
curl -sL "https://tinyurl.com/pytrm" -o /usr/local/bin/pytrm

if [ $? -eq 0 ] && [ -s /usr/local/bin/pytrm ]; then
    chmod +x /usr/local/bin/pytrm
    echo "--------------------------------------------------------"
    echo "SUCCESS: pytrm installed globally. Run by typing: pytrm"
    echo "--------------------------------------------------------"
else
    echo "Error: Installation failed during network file transfer."
    rm -f /usr/local/bin/pytrm
    exit 1
fi
