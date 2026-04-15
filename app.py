"""
NEXUS - Neural eXecution Unified System
Fixed version with proper voice responses and face expressions
"""

import streamlit as st
import pyttsx3
from threading import Thread
import psutil
import random
import time
from frontend.voice import listen
from backend.agent import run_agent

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="NEXUS",
    layout="wide",
    page_icon="🌐",
    initial_sidebar_state="collapsed"
)

# ═════════════════════════════════════════════════════════════════════════════
# STYLING
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Mono:wght@400;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0a !important;
    color: #d0d0d0 !important;
}

[data-testid="stMainBlockContainer"] {
    background: #0a0a0a !important;
    padding: 0 !important;
}

@keyframes nano-pulse-listen {
    0% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); transform: scale(1); }
    50% { box-shadow: 0 0 50px rgba(212, 175, 55, 0.8); transform: scale(1.08); }
    100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); transform: scale(1); }
}

@keyframes nano-pulse-speak {
    0% { box-shadow: 0 0 30px rgba(212, 175, 55, 0.5); transform: scale(1); }
    20% { box-shadow: 0 0 60px rgba(212, 175, 55, 1); transform: scale(1.1); }
    40% { box-shadow: 0 0 80px rgba(212, 175, 55, 1.2); transform: scale(1.15); }
    60% { box-shadow: 0 0 60px rgba(212, 175, 55, 1); transform: scale(1.1); }
    80% { box-shadow: 0 0 40px rgba(212, 175, 55, 0.7); transform: scale(1.05); }
    100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); transform: scale(1); }
}

@keyframes nano-pulse-idle {
    0% { box-shadow: 0 0 15px rgba(212, 175, 55, 0.2); transform: scale(1); }
    50% { box-shadow: 0 0 30px rgba(212, 175, 55, 0.4); transform: scale(1.03); }
    100% { box-shadow: 0 0 15px rgba(212, 175, 55, 0.2); transform: scale(1); }
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #d4af37 !important;
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.5) !important;
}

button {
    background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%) !important;
    color: #d4af37 !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: bold !important;
    border: 2px solid #d4af37 !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
}

button:hover {
    box-shadow: 0 0 20px rgba(212, 175, 55, 0.6) !important;
}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TEXT-TO-SPEECH ENGINE
# ═════════════════════════════════════════════════════════════════════════════
def speak_response(text):
    """Speak response with proper error handling"""
    try:
        if len(text) > 600:
            text = text[:600]
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 145)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        
        print(f"[VOICE] Speaking: {text[:50]}...")
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[ERROR] Voice failed: {e}")

def speak_async(text):
    """Speak in background without blocking UI"""
    thread = Thread(target=speak_response, args=(text,), daemon=True)
    thread.start()

# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═════════════════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nano_state" not in st.session_state:
    st.session_state.nano_state = "idle"
if "nano_face" not in st.session_state:
    st.session_state.nano_face = "neutral"
if "status_text" not in st.session_state:
    st.session_state.status_text = "READY"

# Face expressions based on emotion/state
FACE_EXPRESSIONS = {
    "neutral": "⚪",
    "thinking": "🤔",
    "happy": "😊",
    "excited": "🤩",
    "listening": "👂",
    "speaking": "🗣️",
    "confused": "😕",
    "proud": "😌",
    "energetic": "⚡",
    "calm": "😌"
}

# ═════════════════════════════════════════════════════════════════════════════
# MAIN UI
# ═════════════════════════════════════════════════════════════════════════════

# Title
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-size: 48px; margin: 0; color: #d4af37;'>NEXUS</h1>
    <p style='color: #606060; letter-spacing: 4px; margin-top: 10px;'>NEURAL EXECUTION UNIFIED SYSTEM</p>
</div>
""", unsafe_allow_html=True)

# Nano-Sphere with Face Expression
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    nano_animation = {
        "idle": "nano-pulse-idle",
        "listening": "nano-pulse-listen",
        "speaking": "nano-pulse-speak"
    }.get(st.session_state.nano_state, "nano-pulse-idle")
    
    face = FACE_EXPRESSIONS.get(st.session_state.nano_face, "⚪")
    status = st.session_state.status_text
    
    st.markdown(f"""
    <div style='text-align: center; margin: 40px 0;'>
        <div style='
            position: relative;
            width: 240px;
            height: 240px;
            margin: 0 auto;
            border-radius: 50%;
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 35%, #0a0a0a 100%);
            border: 3px solid #d4af37;
            animation: {nano_animation} 2s ease-in-out infinite;
            display: flex;
            align-items: center;
            justify-content: center;
        '>
            <div style='font-size: 80px;'>{face}</div>
        </div>
        <p style='color: #d4af37; font-size: 18px; letter-spacing: 3px; margin: 20px 0 0 0; font-weight: bold;'>{status}</p>
    </div>
    """, unsafe_allow_html=True)

# Control Buttons
st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        start_btn = st.button("START LISTENING", key="listen_btn", use_container_width=True)
    with btn_col2:
        clear_btn = st.button("CLEAR CHAT", key="clear_btn", use_container_width=True)
    
    if clear_btn:
        st.session_state.messages = []
        st.session_state.nano_state = "idle"
        st.session_state.nano_face = "neutral"
        st.session_state.status_text = "READY"
        st.rerun()
    
    if start_btn:
        # Update state - LISTENING
        st.session_state.nano_state = "listening"
        st.session_state.nano_face = "listening"
        st.session_state.status_text = "LISTENING..."
        
        # Force rerun to show listening state
        st.rerun()

# Process listening if in listening state
if st.session_state.nano_state == "listening":
    st.markdown("<div style='text-align: center; color: #d4af37; margin-top: 15px;'>", unsafe_allow_html=True)
    st.info("🎤 Listening... Speak now!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # IMPORTANT: This is where we actually listen
    print("[APP] Starting voice capture...")
    user_input = listen()
    
    if user_input and len(user_input.strip()) > 0:
        print(f"[APP] Got input: {user_input}")

        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip()
        })
        
        # Update state - PROCESSING
        st.session_state.nano_state = "speaking"
        st.session_state.nano_face = "thinking"
        st.session_state.status_text = "PROCESSING..."
        st.rerun()
    else:
        print("[APP] No input received")
        st.session_state.nano_state = "idle"
        st.session_state.nano_face = "confused"
        st.session_state.status_text = "No response detected"
        time.sleep(2)
        st.rerun()

# Process response if we have a pending input
if st.session_state.nano_state == "speaking" and len(st.session_state.messages) > 0:
    last_msg = st.session_state.messages[-1] if st.session_state.messages else None
    
    if last_msg and last_msg.get("role") == "user":
        user_text = last_msg.get("content", "")
        
        # Show processing
        st.progress(0.3, text="NEXUS is thinking...")
        
        try:
            # Get agent response
            print(f"[APP] Running agent with: {user_text}")
            response = run_agent(user_text)
            print(f"[APP] Got response: {response}")
            
            # Add to messages
            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })
            
            # Update state - SPEAKING
            st.session_state.nano_state = "speaking"
            st.session_state.nano_face = "speaking"
            st.session_state.status_text = "SPEAKING..."
            
            st.progress(0.7, text="Speaking response...")
            
            # Speak the response
            print(f"[APP] Calling speak_async with: {response[:100]}...")
            speak_async(response)
            
            time.sleep(0.5)
            
            # Return to idle
            st.session_state.nano_state = "idle"
            st.session_state.nano_face = "happy"
            st.session_state.status_text = "READY"
            
        except Exception as e:
            print(f"[APP] Error: {e}")
            error = f"Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error})
            st.error(error)
            speak_async("Sorry, something went wrong!")
            st.session_state.nano_state = "idle"
            st.session_state.nano_face = "confused"
            st.session_state.status_text = "ERROR"
        
        st.rerun()

# System Metrics
st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    cpu = psutil.cpu_percent(interval=0.1)
    st.metric("CPU", f"{cpu:.1f}%")

with col2:
    mem = psutil.virtual_memory()
    st.metric("MEMORY", f"{mem.percent:.1f}%")

with col3:
    disk = psutil.disk_usage('/')
    st.metric("DISK", f"{disk.percent:.1f}%")

with col4:
    battery = psutil.sensors_battery()
    bat_pct = battery.percent if battery else 0
    st.metric("BATTERY", f"{bat_pct:.1f}%")

# Chat History
st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>
    <p style='color: #d4af37; letter-spacing: 2px; font-size: 14px;'>CONVERSATION HISTORY</p>
</div>
""", unsafe_allow_html=True)

if st.session_state.messages:
    for msg in st.session_state.messages[-10:]:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        
        if role == "user":
            st.markdown(f"""
            <div style='background: #1a2a3a; border-left: 4px solid #d4af37; padding: 12px; margin: 8px 0; border-radius: 4px;'>
                <p style='color: #a0c0ff; margin: 0; font-weight: bold; font-size: 12px;'>YOU:</p>
                <p style='color: #d0d0d0; margin: 5px 0 0 0;'>{content}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            display_content = content[:200] + "..." if len(content) > 200 else content
            st.markdown(f"""
            <div style='background: #1a3a2a; border-left: 4px solid #d4af37; padding: 12px; margin: 8px 0; border-radius: 4px;'>
                <p style='color: #a0ffa0; margin: 0; font-weight: bold; font-size: 12px;'>NEXUS:</p>
                <p style='color: #d0d0d0; margin: 5px 0 0 0;'>{display_content}</p>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px; opacity: 0.6;'>
        <p style='color: #606060; font-size: 14px;'>No conversation yet. Click START LISTENING to begin.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; border-top: 1px solid #404040;'>
    <p style='color: #606060; font-size: 12px; margin: 0;'>NEXUS v2.0 | Neural Execution Unified System</p>
    <p style='color: #404040; font-size: 11px; margin: 5px 0 0 0;'>Voice-First AI with Nano-Material Interface</p>
</div>
""", unsafe_allow_html=True)
