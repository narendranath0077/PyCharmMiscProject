import datetime
import math
import re
import random

import psutil
import webbrowser

def _fmt(b):
    """Format bytes to GB"""
    return f"{b / 1024**3:.1f} GB"

# ─────────────────────────────── Gen Z Responses ─────────────────────────────
GENZ_GREETINGS = [
    "Yo, what's good! 🔥",
    "Ayo, I'm here fr fr no cap 💯",
    "What's poppin'! Let's get it 🚀",
    "No cap, I'm ready to help bestie ✨",
    "Skibidi, I'm here to assist 😎",
    "Nah fr this is about to go hard 🔥",
]

GENZ_AFFIRMATIONS = [
    "That's lowkey fire 🔥",
    "Nah that's bussin fr 💯",
    "Honestly that slaps ✨",
    "No cap, that's crazy good",
    "Yo that's absolutely unhinged (in a good way) 😄",
    "Periodt, that's it 💅",
]

DAD_JOKES = [
    "Why don't scientists trust atoms? Because they make up everything! 😂",
    "I'm reading a book on the history of glue – can't put it down! 📚",
    "Why did the scarecrow win an award? He was outstanding in his field! 🌾",
    "What do you call a fake noodle? An impasta! 🍝",
    "Why don't eggs tell jokes? They'd crack each other up! 🥚",
    "I used to hate facial hair, but then it grew on me! 💇",
    "What did one wall say to the other wall? I'll meet you at the corner! 📐",
    "Why did the coffee file a police report? It got mugged! ☕",
    "I'm terrified of elevators, so I'm taking steps to avoid them! 🚶",
    "Did you hear about the restaurant on the moon? Good food, no atmosphere! 🌙",
]

MOTIVATIONAL_QUOTES = [
    "You're doing amazing, sweetie! 💖",
    "No cap, you're literally the main character energy ✨",
    "Bet on yourself king/queen 👑",
    "Your vibe attracts your tribe, keep shining 🌟",
    "Real ones know it's grind time, no time to waste 💪",
    "You're serving looks AND energy 💅",
    "Not you doubting yourself, bestie – you got this! 🔥",
    "This is your era, own it 🎯",
]

FUN_FACTS = [
    "Did you know? Honey never spoils – archaeologists found 3000-year-old honey in Egyptian tombs! 🍯",
    "Did you know? Octopuses have three hearts and blue blood! 🐙",
    "Did you know? Wombats have cube-shaped poop! 💩",
    "Did you know? Bananas are berries but strawberries aren't! 🍌🍓",
    "Did you know? A group of flamingos is called a 'flamboyance'! 🦩",
    "Did you know? Sloths only defecate once a week! 🦥",
    "Did you know? Otters hold hands while sleeping so they don't drift apart! 🦦",
    "Did you know? Cows have best friends and get stressed when separated! 🐄",
]

# ─────────────────────────────── Core Tools ─────────────────────────────────
def get_time(q: str = "") -> str:
    """Get current time with Gen Z flair"""
    now = datetime.datetime.now()
    time_str = now.strftime('%I:%M %p, %A')
    greeting = random.choice(GENZ_GREETINGS)
    return f"{greeting} It's {time_str} fr no cap ⏰"

def search_google(q: str) -> str:
    """Search Google for anything - we gotchu covered"""
    if not q or len(q.strip()) < 2:
        return "Bruh, give me something to search for 😅"
    webbrowser.open(f"https://google.com/search?q={q}")
    affirmation = random.choice(GENZ_AFFIRMATIONS)
    return f"🔍 Searching '{q}' rn... {affirmation}"

def open_youtube(q: str) -> str:
    """Open YouTube - watch time activated 🎬"""
    if q and len(q.strip()) > 1:
        webbrowser.open(f"https://youtube.com/search?q={q}")
        return f"🎬 Searching YouTube for '{q}' - let's gooo! 🔥"
    else:
        webbrowser.open("https://youtube.com")
        return "🎬 YouTube is open bestie! Time to vibe check on some content 🎥✨"

def system_info(q: str = "") -> str:
    """Check system status - let's see what we're working with"""
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        battery = psutil.sensors_battery()
        
        cpu_status = "🔥 MAXED OUT" if cpu > 80 else "🟢 CHILLIN'" if cpu < 30 else "🟡 VIBIN'"
        ram_status = "🔥 LOW-KEY FULL" if ram.percent > 80 else "✨ SPACIOUS" if ram.percent < 40 else "📊 MID"
        
        result = f"""
╔════════════════════════════════════╗
║     SYSTEM STATUS LOOKIN' CRAZY    ║
╠════════════════════════════════════╣
║ CPU:  {cpu:.0f}% {cpu_status}
║ RAM:  {ram.percent:.0f}% ({_fmt(ram.used)}/{_fmt(ram.total)}) {ram_status}
║ DISK: {disk.percent:.0f}% ({_fmt(disk.used)}/{_fmt(disk.total)})
║ BATTERY: {battery.percent:.0f}% {'🔌 PLUGGED IN' if battery.power_plugged else '⚡ LIVING ON EDGE'}
╚════════════════════════════════════╝
"""
        return result
    except Exception as e:
        return f"Yikes, couldn't get system info: {str(e)} 😭"

def calculator(expr: str) -> str:
    """Calculate anything - we're math nerds fr 🤓"""
    if not expr or len(expr.strip()) < 1:
        return "Bro what calculation? Put in an expression 💀"
    
    # Clean the expression first
    expr = expr.replace(' ', '')
    
    if not re.match(r'^[\d\+\-\*\/\.\(\)]+$', expr):
        return "Nah fam, only numbers and basic math operators allowed (+-*/) 🚫"
    
    try:
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        result = eval(expr, {"__builtins__": None}, allowed)
        affirmation = random.choice(GENZ_AFFIRMATIONS)
        return f"The answer is {result} - no cap! 🧮 {affirmation}"
    except Exception:
        return "That math didn't work out fr 😩"

def tell_joke(q: str = "") -> str:
    """Tell a joke - we got comedy skills"""
    joke = random.choice(DAD_JOKES)
    return f"Joke time! 🎭\n{joke}\n\n(I know it's mid but it's kinda funny 😂)"

def motivate(q: str = "") -> str:
    """Get motivation when you're feeling some type of way"""
    quote = random.choice(MOTIVATIONAL_QUOTES)
    return f"💪 {quote}\n\nYou're literally unstoppable! Keep that energy!! 🔥"

def fun_fact(q: str = "") -> str:
    """Learn random facts that hit different"""
    fact = random.choice(FUN_FACTS)
    return f"{fact}\n\nThat's insane no cap 🤯"

def weather_vibe(q: str = "") -> str:
    """Check weather vibes"""
    try:
        import requests
        response = requests.get(f"https://wttr.in/?format=j1", timeout=5)
        data = response.json()
        current = data['current_condition'][0]
        temp = current['temp_C']
        condition = current['weatherDesc'][0]['value']
        
        if temp > 25:
            vibe = "HOT GIRL/BOY SUMMER ENERGY 🔥"
        elif temp > 15:
            vibe = "Main character autumn walk vibes 🍂"
        else:
            vibe = "Stay cozy bestie, it's giving winter hibernation 🧊"
        
        return f"🌤️ {condition} | {temp}°C\n{vibe}"
    except:
        return "Couldn't check the weather fr but the vibes outside are immaculate ✨"

def roast_me(q: str = "") -> str:
    """Get roasted in the most Gen Z way possible"""
    roasts = [
        "You're giving basic but make it iconic 💀",
        "girl/Boy you're really out here being yourself - the audacity 😤",
        "Nah bestie your energy is unmatched... in a concerning way 💅",
        "You're not just any flavor of confused, you're limited edition 🎨",
        "The way you move through life is absolutely foul 💀",
        "Ma'am/Sir you're giving catastrophe but making it fashion 👗",
    ]
    return f"Alright alright alright... {random.choice(roasts)} nah I'm just playin' you're fire 🔥 (no cap)"

def vibe_check(q: str = "") -> str:
    """Check what kind of energy you're sending"""
    vibes = [
        "Your vibe is UNHINGED and we're here for it 🎢",
        "Bestie you're giving 'chaotic good' energy and I respect it 🌪️",
        "Nah your energy is cosmic - literally out of this world ✨🌌",
        "Girl/Boy you're sending 'main character' vibrations, keep it up 👑",
        "Your aura is BUSSIN - it's the soft glow energy for me 💫",
        "Periodt, your essence is absolutely serving ✨💅",
    ]
    return f"{random.choice(vibes)}"

# ─────────────────────────────── Tools Registry ─────────────────────────────
# Simple dict of tool functions (not langchain wrapped)
tools = {
    "get_time": get_time,
    "search_google": search_google,
    "system_info": system_info,
    "calculator": calculator,
    "tell_joke": tell_joke,
    "motivate": motivate,
    "fun_fact": fun_fact,
    "weather_vibe": weather_vibe,
    "roast_me": roast_me,
    "vibe_check": vibe_check,
    "open_youtube": open_youtube,
}