# Finance & Stock Market Backend

A comprehensive financial analysis system powered by AI with complete responses and proper citations.

## Features

- 🏦 **Finance Expert**: Complete financial analysis with definitions, types, examples
- 📈 **Stock Market Expert**: Market analysis, predictions, and recommendations  
- 🤖 **AI-Powered**: Uses OpenRouter API with Claude-3-Haiku for comprehensive responses
- 📚 **Proper Citations**: Includes references to authoritative financial sources
- ⚡ **Fast Responses**: Optimized for quick, detailed answers

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install requests pyyaml
   ```

2. **Run the Backend**:
   ```bash
   python complete_system.py
   ```

3. **Start Asking Questions**:
   ```
   You > what is a loan?
   You > what is a bear market?
   You > explain portfolio diversification
   ```

## API Configuration

The system uses OpenRouter API with Claude-3-Haiku model. The API key is included in the code.

## File Structure

```
Backend/
├── complete_system.py    # Main backend application
├── config.yaml          # Configuration settings
├── core/                # Core strategy and plugin classes
├── rag/                 # Document retrieval and analysis
├── llms/                # LLM factory and model handling
├── adapters/            # Data adapters
├── docs/                # Sample financial documents
└── stock_predictor.py   # Stock market prediction models
```

## Response Format

All responses include:
- **Comprehensive Analysis**: Detailed explanations with examples
- **Citations**: Proper references to authoritative sources [1], [2], [3]
- **Confidence Rating**: Analysis confidence level
- **Sources Used**: List of data sources and methodologies
- **Disclaimer**: Professional financial advice disclaimer

## Example Response

```
# What is a Bear Market?

A bear market is a prolonged period of declining stock prices, typically characterized by a 20% or more drop in a major stock market index over at least a two-month period [1]...

**Analysis Confidence:** HIGH
**Sources Used:** Stock Market ML Models, Technical Analysis Tools, SEC Financial Regulations
**Citations:** This response includes properly formatted citations [1], [2], [3]
**Disclaimer:** Financial and investment advice should be reviewed with qualified professionals
```

## Dependencies

- Python 3.7+
- requests
- pyyaml
- OpenRouter API access

## License

MIT License
