# 🚀 Deployment Guide

This guide covers deploying your Smart Job Parser API to various free platforms.

## 📋 Prerequisites

1. GitHub repository with your code
2. All tests passing locally
3. Docker working locally (optional but recommended)

### Steps:

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Sign up at [render.com](https://render.com)**
   - Use your GitHub account

3. **Create new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose "smart-job-parser" repo

4. **Configure deployment**
   ```
   Name: smart-job-parser
   Runtime: Docker
   Branch: main
   Build Command: (leave empty - using Dockerfile)
   Start Command: (leave empty - using Dockerfile)
   ```

5. **Set Environment Variables**
   ```
   PYTHONPATH=/app
   PORT=8000
   ```

6. **Deploy!**
   - Click "Create Web Service"
   - Wait 3-5 minutes for first deployment
   - Your app will be live at: `https://smart-job-parser.onrender.com`

---
