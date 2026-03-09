# PlugMind 🚀
**HackX 4.0 Project by Team Innoventures**

PlugMind is a high-performance, AI-powered financial and legal Subject Matter Expert (SME) plugin. It provides expert-grade analysis, real-time compliance checks, and market predictions with industry-leading response times.

## ⚡ Performance: The 5-10s Goal
PlugMind (v1.1.2) is engineered for speed without compromising depth. We've achieved a **5-10 second response time** for complex expert queries through:
- **Parallel AI Pipeline**: Simultaneous domain detection and LLM processing.
- **Gemini 2.0 Flash Lite**: Integration with the fastest next-gen inference models via OpenRouter.
- **Connection Pooling**: `requests.Session` link pooling to eliminate TLS handshake overhead.
- **Context Truncation**: Smart history management to prevent prompt bloat.

## 🏦 SME Plugin Capabilities
- **⚖️ Legal Expert**: Deep expertise in Indian Law (IPC, CrPC, IT Act, SEBI).
- **🏦 Banking & Finance**: RBI guidelines, loan analysis, and regulatory compliance.
- **📈 Stock Market**: Real-time market sentiment and ML-based movement predictions.
- **🛡️ Ethical AI**: Built-in frameworks for transparency and unbiased reasoning.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python), ThreadPoolExecutor, OpenRouter API.
- **Frontend**: React, Lucide-React for premium aesthetics.
- **Database**: MongoDB (Chat History), Firebase (Real-time syncing).
- **Inference**: Google Gemini 2.0 Flash Lite.

## 🚀 Quick Start

### Backend Setup
1. Navigate to directory: `cd Backend`
2. Install dependencies: `pip install -r requirements.txt` (or `pip install requests fastapi uvicorn pymongo firebase-admin joblib python-dotenv`)
3. Set environment variables in `.env`:
   ```
   OPENROUTER_API_KEY=your_key
   MONGODB_URI=your_db_uri
   ```
4. Run server: `python api/index.py`

### Frontend Setup
1. Navigate to directory: `cd Frontend`
2. Install: `npm install`
3. Start: `npm run dev`

## 📂 Project Structure
- `Backend/`: FastAPI server and `HotSwappableSMEPlugin` core logic.
- `Frontend/`: Modern, responsive user interface.
- `TrainTestCompare/`: ML model training and comparison scripts.

---
*Built with ❤️ for HackX 4.0*
