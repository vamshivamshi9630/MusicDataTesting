#!/bin/bash

set -e  # Exit if any command fails

read -p "Enter commit message: " msg

git add .
git commit -m "${msg:-Updated albums and JSON}"
git push origin main

echo "✅ Upload complete!"
