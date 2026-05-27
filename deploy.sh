#!/data/data/com.termux/files/usr/bin/bash

echo "================================"
echo "   CODEFINDER AUTO DEPLOY"
echo "================================"

# Go to project folder
cd ~/codefinder || exit

# Add all changes
git add .

# Commit with auto message
git commit -m "auto deploy update $(date)"

# Push to GitHub
git push

echo ""
echo "================================"
echo "   DEPLOY SENT TO GITHUB ✅"
echo "================================"

