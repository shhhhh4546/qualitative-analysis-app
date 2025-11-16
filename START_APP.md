# How to Run the App

## Quick Start (Both Servers)

### Option 1: Use the Startup Scripts

**Terminal 1 - Backend:**
```bash
cd "/Users/shrutichandra/Qualitative Analysis App"
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd "/Users/shrutichandra/Qualitative Analysis App"
./start_frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd "/Users/shrutichandra/Qualitative Analysis App"
source venv/bin/activate
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
```

**Terminal 2 - Frontend:**
```bash
cd "/Users/shrutichandra/Qualitative Analysis App/frontend"
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### Step 2: Access the App

Open your web browser and go to:
**http://localhost:3000**

### Step 3: Upload Data

1. Go to **"Upload Data"** tab
2. Select **Source**: "tulip" (or any name)
3. Select **File Type**: "CSV"
4. Click the upload area or drag and drop `sample_data.csv`
5. Click **"Upload File"**

You should see: "Successfully uploaded 25 conversations!"

### Step 4: Run Analysis

1. Go to **"Analyze"** tab
2. Leave source empty (or select one)
3. Set **Number of Conversations**: 25 (or leave default)
4. Click **"Start Analysis"**

⚠️ **Note**: First analysis will download the Hugging Face model (if using Hugging Face). This can take 2-5 minutes depending on your internet speed.

### Step 5: View Insights

1. Go to **"Insights"** tab
2. View aggregated:
   - Top Pain Points
   - Media Consumption
   - Compelling Points

## Troubleshooting

### Backend won't start
- Make sure virtual environment is activated: `source venv/bin/activate`
- Check if port 8000 is already in use
- Verify `.env` file exists with `LLM_PROVIDER` set

### Frontend won't start
- Run `npm install` in the frontend directory first
- Check if port 3000 is already in use

### "No conversations found"
- Upload data first (Step 3)
- Check backend logs for errors
- Verify database file exists in backend directory

### Upload takes too long
- The optimized version should be fast now (< 2 seconds for 25 conversations)
- Check backend logs if it's still slow

### Analysis fails
- Make sure `.env` has `LLM_PROVIDER` set (huggingface or openai)
- If using Hugging Face, first run will download the model
- Check backend logs for specific errors

## Stopping the Servers

Press `CTRL+C` in each terminal to stop the servers.

