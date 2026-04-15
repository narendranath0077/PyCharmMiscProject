# NEXUS - Voice-Based AI Assistant

NEXUS, short for Neural eXecution Unified System, is a local Python voice assistant with a Streamlit interface, speech recognition, text-to-speech replies, and a LangGraph-powered agent that can route requests to practical tools.

The assistant runs as a local web app. Click the listening button, speak a command, and NEXUS routes the request through an Ollama-backed LLM or a fallback keyword router.

## Features

- Voice input through Whisper and `sounddevice`
- Spoken responses through `pyttsx3`
- Streamlit UI with a status sphere, conversation history, and live system metrics
- LangGraph agent flow with `decide` and `act` stages
- Ollama integration through `langchain-ollama`
- Fallback routing when the LLM call fails
- Tool support for time, search, YouTube, system info, math, jokes, motivation, facts, weather, roasts, and vibe checks

## Project Structure

```text
.
|-- app.py
|-- requirements.txt
|-- backend/
|   |-- agent.py
|   |-- tools.py
|   `-- utils/
|       |-- parser.py
|       |-- speak.py
|       `-- voice.py
`-- frontend/
    `-- voice.py
```

## Requirements

- Python 3.10 or newer
- A working microphone
- Ollama installed locally
- The `mistral` Ollama model, or another model configured in `backend/agent.py`

Install Ollama from:

```text
https://ollama.com
```

Then pull the default model:

```bash
ollama pull mistral
```

## Setup

From the project directory:

```powershell
cd "C:\Users\athot\OneDrive\Desktop\voice based assistant\PyCharmMiscProject"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The voice modules also import `whisper`, `sounddevice`, and `numpy`. If those are not already installed in your environment, install them too:

```powershell
pip install openai-whisper sounddevice numpy
```

## Run The App

Start Ollama in one terminal:

```bash
ollama serve
```

Then start the Streamlit app in another terminal:

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

## How To Use

1. Click `START LISTENING`.
2. Speak your command clearly.
3. Wait while NEXUS transcribes the audio and runs the agent.
4. Read the response in the conversation history and listen for the spoken reply.
5. Click `CLEAR CHAT` to reset the current conversation.

Example commands:

```text
What time is it?
Tell me a joke.
Show system info.
Calculate 25 * 4 - 10.
Search Google for Python Streamlit examples.
Open YouTube.
Open YouTube lo-fi music.
Give me motivation.
Tell me a fun fact.
What is the weather vibe?
Roast me.
Check my vibe.
```

## Tools

| Tool | Purpose |
| --- | --- |
| `get_time` | Returns the current time and day. |
| `search_google` | Opens a Google search in the browser. |
| `open_youtube` | Opens YouTube or searches YouTube. |
| `system_info` | Reports CPU, RAM, disk, and battery status. |
| `calculator` | Evaluates basic math expressions. |
| `tell_joke` | Returns a random joke. |
| `motivate` | Returns a motivational response. |
| `fun_fact` | Returns a random fact. |
| `weather_vibe` | Fetches current weather from `wttr.in`. |
| `roast_me` | Returns a playful roast. |
| `vibe_check` | Returns a random personality-style response. |

## How It Works

`app.py` owns the Streamlit UI, microphone button flow, session state, system metrics, and text-to-speech call.

`frontend/voice.py` records five seconds of microphone audio, ignores very quiet input, and transcribes speech with Whisper.

`backend/agent.py` uses a LangGraph state machine:

```text
decide -> act -> END
```

The `decide` step asks the Ollama model to return JSON that selects a tool. If the model call fails, `_smart_route()` uses keyword matching as a fallback. The `act` step runs the selected function from `backend/tools.py`.

## Changing The Model

Pull another Ollama model:

```bash
ollama pull neural-chat
```

Then update this line in `backend/agent.py`:

```python
llm = ChatOllama(model="mistral", temperature=0.7)
```

For example:

```python
llm = ChatOllama(model="neural-chat", temperature=0.7)
```

## Adding A Tool

Add a function in `backend/tools.py`:

```python
def my_tool(q: str = "") -> str:
    return "Tool response"
```

Register it in the `tools` dictionary:

```python
tools = {
    "my_tool": my_tool,
}
```

Then update the prompt and fallback routing in `backend/agent.py` so the agent knows when to call it.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `ModuleNotFoundError` | Activate the virtual environment and run `pip install -r requirements.txt`. |
| `No module named whisper` | Run `pip install openai-whisper`. |
| Microphone returns no text | Check microphone permissions and speak clearly during the five-second capture window. |
| Ollama connection error | Start Ollama with `ollama serve` and make sure the selected model is pulled. |
| Slow first voice command | Whisper may take time to load the model on first use. |
| Browser search does not open | Check default browser settings and popup restrictions. |
| Weather fails | `weather_vibe` depends on network access to `wttr.in`. |

## Notes

- The app is designed to run locally.
- Some tools open browser tabs as part of their behavior.
- The fallback router keeps basic commands working even when the LLM is unavailable.
- Secrets and local runtime files should stay out of Git; see `.gitignore`.
