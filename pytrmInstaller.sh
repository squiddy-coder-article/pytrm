#!/bin/bash
# pytrm 1.0.0 Cloud Deployment Engine

# 1. Enforce root privileges so the script can write to /usr/local/bin
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run this installer with sudo permissions:"
    echo "sudo ./pytrmInstaller.sh"
    exit 1
fi

echo "Initializing pytrm cloud deployment framework..."
echo "Fetching latest production source code directly from GitHub..."

# 2. Stream the raw text application logic directly into the global binary tree path
sudo curl -sL "https://raw.githubusercontent.com/squiddy-coder-article/pytrm/main/pytrm.py" -o /usr/local/bin/pytrm

# 3. Verify if the network download completed successfully and wrote data
if [ $? -eq 0 ] && [ -s /usr/local/bin/pytrm ]; then
    # 4. Make the downloaded file a globally executable system binary tool
    sudo chmod +x /usr/local/bin/pytrm
    echo "--------------------------------------------------------"
    echo "SUCCESS: pytrm 1.0.0 has been downloaded and deployed!"
    echo "You can now run it from any folder by typing: pytrm"
    echo "--------------------------------------------------------"
else
    echo "Error: Installation failed during network download phase."
    echo "Please check your internet connection or verify your GitHub repository path URL."
    # Clean up empty file markers if the fetch failed
    rm -f /usr/local/bin/pytrm
    exit 1
fi
