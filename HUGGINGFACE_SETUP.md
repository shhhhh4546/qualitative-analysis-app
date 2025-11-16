# Hugging Face Models Setup Guide

The app now supports both **OpenAI** and **Hugging Face** models! Using Hugging Face gives you:
- ✅ **Free** (no API costs)
- ✅ **Privacy** (data stays on your machine)
- ✅ **No rate limits**
- ✅ **More human-like, rich outputs**
- ✅ **Full control** over the model

## Quick Setup

### 1. Install Dependencies

```bash
cd "/Users/shrutichandra/Qualitative Analysis App"
source venv/bin/activate
pip install -r requirements.txt
```

This installs:
- `transformers` - Hugging Face library
- `torch` - PyTorch for model inference
- `accelerate` - Efficient model loading
- `sentencepiece` - Tokenization support

### 2. Configure Environment

Create or update your `.env` file:

```bash
# Choose your provider: "openai" or "huggingface"
LLM_PROVIDER=huggingface

# Hugging Face model (see recommendations below)
HUGGINGFACE_MODEL=microsoft/Phi-3-mini-4k-instruct

# Optional: If using OpenAI
# OPENAI_API_KEY=your_key_here
# OPENAI_MODEL=gpt-4-turbo-preview
```

### 3. Recommended Models

#### Best for Quality (Larger Models)
1. **microsoft/Phi-3-mini-4k-instruct** (3.8B) ⭐ Recommended
   - Great balance of quality and speed
   - Instruction-tuned for structured outputs
   - ~8GB RAM needed

2. **mistralai/Mistral-7B-Instruct-v0.2** (7B)
   - Excellent quality, more human-like
   - ~16GB RAM needed

3. **meta-llama/Llama-2-7b-chat-hf** (7B)
   - High quality, conversational
   - Requires Hugging Face approval
   - ~16GB RAM needed

#### Faster/Smaller Models (Good Quality)
4. **TinyLlama/TinyLlama-1.1B-Chat-v1.0** (1.1B)
   - Fast, lightweight
   - ~4GB RAM needed
   - Good for quick analysis

5. **microsoft/DialoGPT-medium** (345M)
   - Very fast
   - ~2GB RAM needed
   - Lower quality but good for testing

### 4. First Run

On first run, the model will be downloaded from Hugging Face (can take a few minutes). Subsequent runs will be instant.

```bash
cd backend
python main.py
```

You'll see:
```
Loading Hugging Face model: microsoft/Phi-3-mini-4k-instruct on cpu
Model microsoft/Phi-3-mini-4k-instruct loaded successfully!
```

### 5. GPU Support (Optional but Recommended)

For faster analysis, use a GPU:

```bash
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# If True, models will automatically use GPU
```

Models will automatically use GPU if available.

## Performance Tips

1. **Batch Processing**: Analyze multiple conversations in one batch for efficiency
2. **Model Size**: Start with smaller models to test, then upgrade to larger ones for production
3. **GPU**: Use GPU for 5-10x faster inference
4. **Memory**: Close other applications if you run out of RAM

## Switching Between Providers

Just change `LLM_PROVIDER` in your `.env`:

```bash
# Use Hugging Face
LLM_PROVIDER=huggingface

# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## Troubleshooting

### "Out of memory" error
- Use a smaller model (TinyLlama or DialoGPT)
- Or use OpenAI API instead

### Model download fails
- Check internet connection
- Some models require Hugging Face account (sign up at huggingface.co)
- Accept model terms on the Hugging Face website

### Slow inference
- Use GPU if available
- Use smaller models
- Process in smaller batches

### JSON parsing errors
The app handles this automatically, but if issues persist:
- Try a different model (instruction-tuned models work better)
- Models like Phi-3 and Mistral are better at JSON formatting

## Example .env File

```bash
# LLM Configuration
LLM_PROVIDER=huggingface
HUGGINGFACE_MODEL=microsoft/Phi-3-mini-4k-instruct

# Database
DATABASE_URL=sqlite:///./qualitative_analysis.db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
```

## Recommended Setup for Production

For analyzing 20,000+ conversations:

1. **Model**: `microsoft/Phi-3-mini-4k-instruct` or `mistralai/Mistral-7B-Instruct-v0.2`
2. **Hardware**: GPU recommended (8GB+ VRAM)
3. **Batch Size**: Process 50-100 conversations at a time
4. **Monitoring**: Track analysis progress and handle failures gracefully

The app is designed to handle this scale efficiently!

