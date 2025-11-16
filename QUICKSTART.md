# Quick Start Guide

## 1. Initial Setup (One-time)

### Backend Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Frontend Setup
```bash
cd frontend
npm install
cd ..
```

## 2. Start the Application

### Terminal 1 - Backend
```bash
source venv/bin/activate  # If not already activated
cd backend
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

## 3. Access the App

Open your browser and go to: `http://localhost:3000`

## 4. Test with Sample Data

1. Go to the "Upload Data" tab
2. Select source: "gong" (or any)
3. Select file type: "CSV"
4. Upload `sample_data.csv` from the project root
5. Click "Upload File"

## 5. Run Analysis

1. Go to the "Analyze" tab
2. Leave source empty (or select one)
3. Set limit to 10 (for testing)
4. Click "Start Analysis"
5. Wait for analysis to complete (may take 1-2 minutes)

## 6. View Insights

1. Go to the "Insights" tab
2. View aggregated pain points, media consumption, and compelling points
3. Explore the charts and detailed lists

## Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure you created `.env` file
- Add your OpenAI API key: `OPENAI_API_KEY=sk-...`

### Frontend can't connect to backend
- Make sure backend is running on port 8000
- Check terminal 1 for any errors

### Import errors
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

## Next Steps

- Upload your real data files (CSV or JSON)
- Run batch analysis on larger datasets
- Explore insights and export results
- Customize the analysis prompts in `backend/services/analyzer.py`

