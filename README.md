# 🎨 Sketch Maker App (Flask + OpenCV)

This app lets users upload an image and converts it into a pencil sketch using OpenCV.

---

## 🚀 Deploy Options

### Option A — Quick Deploy (Render)
1. Push code to GitHub (with `app.py`, `templates/`, `static/`, `requirements.txt`, `Procfile`).
2. In [Render](https://render.com):
   - Create **Web Service** → connect GitHub repo.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
3. Add environment variables in Render dashboard:
   - `FLASK_SECRET` = some-random-secret
4. Open your Render URL.  
⚠️ **Uploads are ephemeral** on free Render — they reset on redeploy. For persistence, use Render Disks or cloud storage (AWS S3 / GCS).

---

### Option B — Production Deploy (Google Cloud Run)
1. Install gcloud CLI and authenticate:
   ```sh
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
