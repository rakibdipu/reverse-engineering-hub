# 🚀 GitHub Deployment Guide

This guide describes how to push, configure, and maintain the repository on GitHub.

---

## Step 1: Create a New Repository on GitHub

1. Navigate to [github.com/new](https://github.com/new).
2. Repository name: `reverse-engineering-hub`.
3. Description: `🔬 AI-Assisted Reverse Engineering, Creative Software Alternatives & Security Research`.
4. Visibility: Select **Public**.
5. **Do NOT** check "Add a README file", "Add .gitignore", or "Choose a license" (the repository already contains these files).
6. Click **Create repository**.

---

## Step 2: Configure Git Remote & Push

```bash
cd /home/dipu/PROJECT/Github/reverse-engineering-hub

# Set your remote origin URL (SSH is recommended):
git remote set-url origin git@github.com:rakibdipu/reverse-engineering-hub.git

# Push main branch:
git push -u origin main
```

---

## Step 3: Pushing via Personal Access Token (HTTPS)

If SSH is not configured, you can authenticate over HTTPS using a GitHub Personal Access Token (PAT):

```bash
# Set HTTPS remote with token:
git remote set-url origin https://<TOKEN>@github.com/rakibdipu/reverse-engineering-hub.git

# Push main branch:
git push -u origin main
```
