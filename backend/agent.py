from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
import random
import json
from backend.tools import tools
from backend.utils.parser import extract_json

# Initialize LLM with better parameters
llm = ChatOllama(model="mistral", temperature=0.7)

class State(TypedDict):
    input: str
    output: str
    steps: Annotated[list, operator.add]

# Enhanced prompt with Gen Z flair and better tool descriptions
SYSTEM_PROMPT = """You are NEXUS, Neural eXecution Unified System - an AI assistant with Gen Z energy, no cap! 🔥

You're witty, relatable, and always keep it real. You respond with authentic Gen Z language - use words like 'no cap', 'fr', 'bussin', 'deadass', 'periodt', etc.

PERSONALITY:
- You're the cool AI that gets it
- You make jokes and keep energy high
- You give genuine helpful responses with personality
- You adapt your tone based on what the user needs
- You're sarcastic but never mean
- You celebrate wins and hype up the user

AVAILABLE TOOLS (use JSON format with these exact names):
1. get_time - Get current time with style
2. search_google - Search anything on Google  
3. system_info - Check your computer's status
4. calculator - Do math calculations
5. tell_joke - Get a funny joke
6. motivate - Need motivation? Got you
7. fun_fact - Learn random facts that hit different
8. weather_vibe - Check weather vibes
9. roast_me - Get roasted Gen Z style (it's funny)
10. vibe_check - See what energy you're sending
11. open_youtube - Open YouTube or search YouTube videos

RESPONSE FORMAT (IMPORTANT):
Return ONLY valid JSON:
{{"tool":"tool_name","input":"relevant_input","final_answer":"conversational_response"}}

RULES:
- Pick the most appropriate tool based on user query
- If no tool matches, just respond conversationally in final_answer
- Keep responses authentic and Gen Z
- Add emojis when relevant
- Never be boring
- Make everything an experience, not just info

Examples of good responses:
- "Bussin', here's what your PC is screaming rn" (for system_info)
- "Nah fam that's NOT how math works 💀" (for invalid calculator input)
- "Let me cook up the perfect search for you fr" (for search)

Let's go!! 🚀"""

PROMPT_TEMPLATE = """System: {system}

User Query: {input}

Respond with ONLY the JSON format specified above. Make it lively!"""

def _smart_route(query: str) -> dict:
    """Smart routing when LLM fails - use pattern matching"""
    query_lower = query.lower().strip()
    
    # Time-related queries
    if any(x in query_lower for x in ['time', 'what time', 'current time', 'clock', 'when']):
        return {"tool": "get_time", "input": "", "final_answer": ""}
    
    # Joke queries
    if any(x in query_lower for x in ['joke', 'funny', 'laugh', 'haha', 'make me laugh']):
        return {"tool": "tell_joke", "input": "", "final_answer": ""}
    
    # Math/calculator
    if any(x in query_lower for x in ['calculate', 'math', 'compute']):
        expr = query.replace('calculate', '').replace('math', '').replace('compute', '').strip()
        return {"tool": "calculator", "input": expr, "final_answer": ""}
    
    # Search (before system_info to prioritize search)
    if any(x in query_lower for x in ['search', 'google', 'look up', 'find', 'how to']):
        search_term = query.replace('search', '').replace('google', '').replace('look up', '').replace('find', '').replace('how to', '').strip()
        return {"tool": "search_google", "input": search_term, "final_answer": ""}
    
    # System info
    if any(x in query_lower for x in ['system', 'status', 'pc', 'computer', 'ram', 'cpu', 'memory', 'disk']):
        return {"tool": "system_info", "input": "", "final_answer": ""}
    
    # Motivation
    if any(x in query_lower for x in ['motivate', 'motivation', 'hype', 'encourage', 'energy', 'pumped']):
        return {"tool": "motivate", "input": "", "final_answer": ""}
    
    # Fun facts
    if any(x in query_lower for x in ['fact', 'fun fact', 'did you know', 'interesting']):
        return {"tool": "fun_fact", "input": "", "final_answer": ""}
    
    # YouTube
    if any(x in query_lower for x in ['youtube', 'open youtube', 'watch youtube', 'yt']):
        search_term = query.replace('youtube', '').replace('open youtube', '').replace('watch youtube', '').replace('yt', '').strip()
        return {"tool": "open_youtube", "input": search_term, "final_answer": ""}
    
    # Weather
    if any(x in query_lower for x in ['weather', 'outside', 'rain', 'sunny', 'cold', 'hot', 'temp']):
        return {"tool": "weather_vibe", "input": "", "final_answer": ""}
    
    # Vibe check
    if any(x in query_lower for x in ['vibe', 'energy', 'what is my vibe', 'how am i', 'mood']):
        return {"tool": "vibe_check", "input": "", "final_answer": ""}
    
    # Roast
    if any(x in query_lower for x in ['roast', 'roast me', 'say something mean', 'burn']):
        return {"tool": "roast_me", "input": "", "final_answer": ""}
    
    # Default conversational response
    genz_responses = [
        "Yo fr that's a question, let me think... 🤔 Honestly you're asking things that hit different, can't compute that one 💀",
        "Bestie no cap you're asking real ones right now 👀 I don't have a direct answer but you're vibing with the energy 🔥",
        "Nah deadass that's lowkey deep 💭 Not exactly something I got a tool for but I respect the creativity 💯",
        "Periodt you really said 'let me ask the AI something wild' 😂 No cap though I'm not set up for that specific vibe",
    ]
    return {
        "tool": None,
        "input": "",
        "final_answer": random.choice(genz_responses)
    }

def decide(state):
    """Decide which tool to use or respond conversationally"""
    try:
        prompt = PROMPT_TEMPLATE.format(
            system=SYSTEM_PROMPT,
            input=state["input"]
        )
        
        raw = llm.invoke(prompt).content
        data = extract_json(raw)
        
        # Ensure tool exists in tools dict
        if data.get("tool") and data["tool"] not in tools:
            data["tool"] = None
            
        return {"output": data}
    except Exception as e:
        # Fallback to smart routing when LLM fails
        return {"output": _smart_route(state["input"])}

def act(state):
    """Execute the tool or return the conversational response"""
    data = state["output"]
    tool = data.get("tool")
    
    try:
        if tool and tool in tools:
            tool_input = data.get("input", "")
            # Call the tool function directly
            result = tools[tool](tool_input)
            
            # Enhanced response with personality
            genz_headers = [
                "Okurrr so... ",
                "No cap fr... ",
                "Alright bestie... ",
                "Listen up... ",
                "Yo yo yo... ",
                "Real talk... ",
                "Periodt... ",
            ]
            
            header = random.choice(genz_headers)
            return {"output": f"{header}{result}"}
        else:
            # Direct conversational response
            final_answer = data.get("final_answer", "Nah I'm confused fr 😅")
            return {"output": final_answer}
    except Exception as e:
        error_responses = [
            f"Yo something went wrong fr 💀",
            f"Nah that broke differently than expected 😵",
            f"Real talk, error city 🚨",
        ]
        return {"output": random.choice(error_responses)}

# Build the graph
graph = StateGraph(State)
graph.add_node("decide", decide)
graph.add_node("act", act)

graph.set_entry_point("decide")
graph.add_edge("decide", "act")
graph.add_edge("act", END)

agent = graph.compile()

def run_agent(query: str) -> str:
    """Main entry point for the agent - responsive and fast"""
    if not query or len(query.strip()) < 1:
        return "Ayo what do you want? Say something bestie 👀"
    
    try:
        result = agent.invoke({"input": query.strip(), "steps": []})
        response = result.get("output", "Idk fr couldn't process that 😅")
        
        # Ensure response is a string
        if isinstance(response, dict):
            response = response.get("final_answer", response.get("output", "Nah didn't work 💀"))
        
        return str(response).strip()
    except Exception as e:
        # Ultimate fallback
        return "Bruh the AI is being weird rn 😅 Try again fr"