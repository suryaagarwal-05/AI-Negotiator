# AI-Negotiator

Agentic AI based buyer seller negotiator.

## Getting Started

Follow these steps to set up and run the AI-Negotiator project:

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- A Groq API key

### Installation

1. **Clone the repository**
   git clone <repository-url>
   cd AI-Negotiator

2. **Install dependencies**
   This will install all packages specified in `pyproject.toml`.
   uv sync

3. **Set up environment variables**

- Create a `.env` file in the project root directory
- Add your Groq API key:
  ```
  GROQ_API_KEY=your_groq_api_key_here
  ```

4. **Run the application**
   python app.py

### Configuration

Make sure to replace `your_groq_api_key_here` with your actual Groq API key. You can obtain a Groq API key by signing up at [Groq's website](https://groq.com/).

### Project Structure

The project uses `pyproject.toml` for dependency management and requires a Groq API connection to function properly.

**Note**: Ensure all dependencies are properly installed and your API key is valid before running the application.
