# Finance & Legal SME Backend (v1.1.2)

A high-performance Subject Matter Expert (SME) plugin for Indian financial and legal analysis, optimized for a **5-10 second response time**.

## Features

- ⚖️ **Legal Expert**: Comprehensive Indian criminal, civil, and corporate law analysis.
- 🏦 **Finance & Banking**: RBI/SEBI compliant analysis for banking and investments.
- 📈 **Market Predictions**: Integrated ML models for stock movement forecasting.
- 🚀 **Ultrafast Inference**: Uses Gemini 2.0 Flash Lite with connection pooling.
- 🔗 **Smart Citations**: Automatic extraction and reference listing for all expert claims.

## Performance Optimizations
- **Parallel processing** of domain detection and AI reasoning.
- **`requests.Session` pooling** to reduce network latency to OpenRouter.
- **Context truncation** (2000 chars) to prevent prompt bloat.
- **BackgroundTasks** for non-blocking database/Firebase syncing.

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install requests fastapi uvicorn pymongo firebase-admin joblib python-dotenv
   ```

2. **Run Server**:
   ```bash
   python api/index.py
   ```

3. **API Access**:
   POST requests to `/chat` with JSON body:
   ```json
   {
     "message": "What is the rule of law in India?",
     "session_id": "test_session",
     "user_id": "user_123",
     "context": ""
   }
   ```

## File Structure

- `complete_system.py`: Core `HotSwappableSMEPlugin` logic.
- `api_server.py`: FastAPI server and background tasks.
- `stock_predictor.py`: ML Technical analysis logic.
- `core/`: Expertise domain strategy classes.

## License
MIT License
