# How to Access the App

## Quick Steps to Run:

### 1. Setup Backend (First Time Only)

Open Terminal and run:
```bash
cd "/Users/shrutichandra/Qualitative Analysis App"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your_api_key_here" > .env
echo "DATABASE_URL=sqlite:///./qualitative_analysis.db" >> .env
```

**Important:** Replace `your_api_key_here` with your actual OpenAI API key!

### 2. Setup Frontend (First Time Only)

In the same terminal or a new one:
```bash
cd "/Users/shrutichandra/Qualitative Analysis App/frontend"
npm install
```

### 3. Start Backend Server

Open Terminal 1:
```bash
cd "/Users/shrutichandra/Qualitative Analysis App"
source venv/bin/activate
cd backend
python main.py
```

You should see: `Uvicorn running on http://0.0.0.0:8000`

### 4. Start Frontend Server

Open Terminal 2 (new terminal window):
```bash
cd "/Users/shrutichandra/Qualitative Analysis App/frontend"
npm run dev
```

You should see: `Local: http://localhost:3000`

### 5. Access the App

Open your web browser and go to:
**http://localhost:3000**

That's it! The app should be running.

---

## Quick Test:

1. Go to "Upload Data" tab
2. Upload `sample_data.csv` (from project root)
3. Go to "Analyze" tab and click "Start Analysis"
4. Go to "Insights" tab to see results

