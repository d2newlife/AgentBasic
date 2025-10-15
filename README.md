# AgentBasic

This project is designed to build AI agents using the Langchain framework and Google Generative AI models. The primary goal is to create intelligent agents that can interact with various tools and perform complex tasks.

## Architecture Overview

- **`main.py`**: This file is intended to be the entry point for defining and running the Langchain agent. It will handle the setup of the Language Model (LLM), integrate tools, and orchestrate the agent's execution flow.
- **`util/tools.py`**: This file is designated for defining custom tools that the AI agent can utilize. These tools can encapsulate specific functionalities, API calls, or data processing logic that the agent needs to interact with the external environment.
- **`requirements.txt`**: Lists all Python dependencies, including `langchain`, `wikipedia`, `langchain-community`, `langchain-openai`, `langchain-google`, `pydantic`, `python-dotenv`, and `google-genai`.

## Key Components and Data Flows

1.  **Language Model (LLM)**: The project uses Google Generative AI models (e.g., Gemini) via `google-genai` and `langchain-google` for natural language understanding and generation.
2.  **Langchain Agent**: The core of the AI agent will be built using Langchain, which provides the framework for chaining LLM calls, tool usage, and memory management.
3.  **Tools**: Custom tools defined in `util/tools.py` (or potentially external tools like Wikipedia via `wikipedia` and `langchain-community`) will extend the agent's capabilities.
4.  **Environment Variables**: Sensitive information and API keys are expected to be loaded from a `.env` file using `python-dotenv`.

## Developer Workflows

### Setting up the Environment

1.  **Install Dependencies**: Ensure all required Python packages are installed:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Variables**: Create a `.env` file in the project root and populate it with necessary API keys (e.g., `GOOGLE_API_KEY`).

### Running the Agent

Once the agent logic is implemented in `main.py`, it can be run directly:

```bash
python main.py
```

## Project-Specific Conventions

-   **Tool Definition**: Custom tools should be defined as functions or classes in `util/tools.py` and integrated into the Langchain agent.
-   **LLM Integration**: The `google.genai` client should be initialized and used to interact with Google's Generative AI models.

## Integration Points and External Dependencies

-   **Google Generative AI**: The project relies heavily on Google's Generative AI services for its core intelligence.
-   **Wikipedia**: The `wikipedia` library is included for potential integration as a search tool for the agent.
-   **Langchain**: This framework is central to the agent's architecture, providing abstractions for LLMs, tools, and agents.
