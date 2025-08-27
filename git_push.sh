#!/bin/bash

# Prompt for a commit message
echo "Enter your commit message:"
read commit_message

# Git commands
git status
git add .
git commit -m "$commit_message"
git push origin main
