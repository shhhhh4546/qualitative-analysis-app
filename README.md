# Qualitative Data Analysis App

A comprehensive application for analyzing large sets of customer conversation data from sources like Gong, Salesforce, and Planhat. The app extracts key insights including pain points, media consumption patterns, and compelling points using AI-powered analysis.

## Features

- **Data Ingestion**: Upload CSV or JSON files with conversation transcripts
- **AI-Powered Analysis**: Automatically extracts:
  - **Pain Points**: Customer problems, challenges, and frustrations
  - **Media Consumption**: Podcasts, blogs, social media, and other media sources customers follow
  - **Compelling Points**: Features, benefits, or aspects that interested customers
- **Batch Processing**: Analyze thousands of conversations efficiently
- **Aggregate Insights**: View aggregated statistics and trends across all analyzed conversations
- **Visualizations**: Interactive charts and graphs for better understanding
- **Multi-Source Support**: Handle data from Gong, Salesforce, Planhat, and other sources

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React with Vite
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **AI Analysis**: OpenAI GPT-4 **or** Hugging Face Models (Phi-3, Mistral, Llama, etc.)
- **Visualization**: Recharts

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 16+
- **For OpenAI**: OpenAI API key (optional)
- **For Hugging Face**: 8GB+ RAM recommended (16GB+ for larger models), GPU optional but recommended

### Backend Setup

1. Navigate to the project root directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```bash
   # Create .env file manually or copy from example
   ```

5. Configure your LLM provider in `.env`:

   **Option A: Use Hugging Face (Recommended - Free, Private)**
   ```
   LLM_PROVIDER=huggingface
   HUGGINGFACE_MODEL=microsoft/Phi-3-mini-4k-instruct
   ```

   **Option B: Use OpenAI**
   ```
   LLM_PROVIDER=openai
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

   See `HUGGINGFACE_SETUP.md` for detailed Hugging Face configuration!

6. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

## Usage

### 1. Upload Data

- Go to the "Upload Data" tab
- Select your data source (Gong, Salesforce, Planhat, etc.)
- Choose file type (CSV or JSON)
- Upload your file

**CSV Format:**
- Must include a `transcript` column
- Optional: `conversation_id` and other metadata columns

**JSON Format:**
- Array of objects or single object
- Must include `transcript`, `text`, or `content` field
- Optional: `conversation_id` and other metadata

### 2. Run Analysis

- Go to the "Analyze" tab
- Select data source (optional - leave empty for all)
- Set the number of conversations to analyze
- Click "Start Analysis"

The system will:
- Analyze each conversation using AI
- Extract pain points, media consumption, and compelling points
- Store results in the database
- Skip conversations that have already been analyzed

### 3. View Insights

- Go to the "Insights" tab
- View aggregate statistics:
  - Top pain points across all conversations
  - Most mentioned media sources
  - Most compelling points
- Filter by data source if needed
- Explore interactive charts and detailed lists

## API Endpoints

### Upload
- `POST /api/upload/csv` - Upload CSV file
- `POST /api/upload/json` - Upload JSON file
- `GET /api/upload/stats` - Get upload statistics

### Analysis
- `POST /api/analysis/analyze/{conversation_id}` - Analyze single conversation
- `POST /api/analysis/analyze-batch` - Analyze multiple conversations
- `GET /api/analysis/status/{conversation_id}` - Check analysis status

### Results
- `GET /api/results/{result_id}` - Get specific analysis result
- `GET /api/results/conversation/{conversation_id}` - Get result by conversation
- `GET /api/results/aggregate/summary` - Get aggregate insights
- `GET /api/results/list/all` - List all results with pagination

## Data Structure

### Conversation
- `id`: Unique identifier
- `source`: Data source (gong, salesforce, planhat, etc.)
- `conversation_id`: Original conversation ID
- `transcript`: Full conversation text
- `metadata`: Additional data (JSON)
- `created_at`: Upload timestamp

### Analysis Result
- `id`: Unique identifier
- `conversation_id`: Reference to conversation
- `pain_points`: Array of pain points with severity
- `media_consumption`: Array of media sources
- `compelling_points`: Array of compelling points
- `summary`: Brief summary
- `confidence_score`: Analysis confidence (0-1)
- `created_at`: Analysis timestamp

## Configuration

Edit `.env` file to configure:
- `LLM_PROVIDER`: Choose "huggingface" or "openai" (default: huggingface)
- **For Hugging Face**:
  - `HUGGINGFACE_MODEL`: Model to use (default: microsoft/Phi-3-mini-4k-instruct)
- **For OpenAI**:
  - `OPENAI_API_KEY`: Your OpenAI API key (required)
  - `OPENAI_MODEL`: Model to use (default: gpt-4-turbo-preview)
- `DATABASE_URL`: Database connection string (default: SQLite)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

## Scaling for Large Datasets

For analyzing 20,000+ conversations:

1. **Use PostgreSQL**: Change `DATABASE_URL` in `.env` to a PostgreSQL connection string
2. **Batch Processing**: Use the batch analysis endpoint with appropriate limits
3. **Background Jobs**: Consider implementing Celery or similar for async processing
4. **Caching**: Implement caching for frequently accessed aggregate results
5. **Rate Limiting**: Be mindful of OpenAI API rate limits

## Troubleshooting

### OpenAI API Errors
- Verify your API key is correct in `.env`
- Check your OpenAI account has sufficient credits
- Monitor rate limits for large batches

### Hugging Face Model Errors
- **Out of Memory**: Use a smaller model (TinyLlama) or increase available RAM
- **Model Download Fails**: Check internet connection, some models require Hugging Face account
- **Slow Inference**: Use GPU if available, or switch to a smaller model
- **JSON Parsing Issues**: Instruction-tuned models (Phi-3, Mistral) work better for structured outputs
- See `HUGGINGFACE_SETUP.md` for detailed troubleshooting

### Database Issues
- Ensure write permissions for SQLite database
- For PostgreSQL, verify connection string format

### Frontend Not Connecting
- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify proxy configuration in `frontend/vite.config.js`

## License

This project is for internal use at Tulip Interfaces.

## Support

For issues or questions, please contact the development team.

