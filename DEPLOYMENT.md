# GitHub Deployment Guide

## Method 1: Local Development

1. **Clone Repository**:
```bash
git clone https://github.com/yourusername/kpi-dashboard.git
cd kpi-dashboard
```

2. **Install Dependencies**:
```bash
pip install -r requirements_github.txt
```

3. **Run Application**:
```bash
streamlit run app.py
```

## Method 2: Streamlit Cloud (Recommended)

1. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push all files to your repository

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Choose `app.py` as the main file
   - Deploy automatically

3. **Configuration**:
   - Streamlit Cloud will automatically use `requirements_github.txt`
   - Your app will be available at: `https://yourapp.streamlit.app`

## Method 3: Other Platforms

### Heroku
- Add a `Procfile` with: `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- Use `requirements_github.txt` for dependencies

### Railway/Render
- Use `requirements_github.txt` for dependencies
- Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## Files to Include on GitHub

Essential files for GitHub deployment:
- `app.py` (main application)
- `sample_kpi_data.py` (sample data generator)
- `sample_kpi_data.xlsx` (sample Excel file)
- `requirements_github.txt` (dependencies)
- `README.md` (documentation)
- `.gitignore` (ignore unnecessary files)
- `DEPLOYMENT.md` (this file)

## Environment Variables

No special environment variables needed - the app runs with default settings.

## Notes

- The app works entirely in-memory with uploaded Excel files
- No database setup required
- All dependencies are standard Python packages
- Compatible with Python 3.8+