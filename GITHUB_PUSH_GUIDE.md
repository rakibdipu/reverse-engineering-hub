# 🚀 GitHub-এ Upload করার গাইড

## ধাপ ১: GitHub-এ নতুন Repository তৈরি করুন

1. [github.com/new](https://github.com/new) যান
2. Repository name: `reverse-engineering-hub`
3. Description: `🔬 AI-Assisted RE Hub: REA Tool + Adobe Creative Alternatives + Security Research`
4. Public রাখুন
5. **"Add a README file" checkbox টিক দেবেন না** (আমাদের নিজের README আছে)
6. Create repository ক্লিক করুন

## ধাপ ২: Remote যোগ করুন এবং Push করুন

```bash
cd /home/dipu/PROJECT/Github/reverse-engineering-hub

# আপনার GitHub username দিয়ে replace করুন
git remote add origin https://github.com/YOUR_USERNAME/reverse-engineering-hub.git

# Push করুন
git push -u origin main
```

## ধাপ ৩: GitHub Token (যদি password না চলে)

```bash
# GitHub Personal Access Token তৈরি করুন:
# Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
# Scope: repo (full control)

# Token দিয়ে push:
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/reverse-engineering-hub.git
git push -u origin main
```
