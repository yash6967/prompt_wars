import anthropic
from backend.config import settings

def get_anthropic_client():
    key = settings.ANTHROPIC_API_KEY
    if not key or key == "sk-ant-..." or "your" in key.lower():
        return None
    try:
        return anthropic.Anthropic(api_key=key)
    except Exception:
        return None

def generate_story(student_name: str, exam_target: str, mood_score: int) -> str:
    client = get_anthropic_client()
    
    mood_str = "struggling" if mood_score <= 4 else "doing okay" if mood_score <= 7 else "motivated"
    fallback_text = (
        f"Chapter 1: The Choice\n"
        f"{student_name} stared at the study desk, the shadow of the upcoming {exam_target} exam looming large. "
        f"Lately, they felt {mood_str}. The books seemed taller, the nights shorter.\n\n"
        f"Chapter 2: The Breakthrough\n"
        f"One evening, instead of pushing through the fatigue, {student_name} took a 10-minute break to breathe. "
        f"They realized that preparation is a marathon, not a sprint. Step by step, the confidence returned.\n\n"
        f"Chapter 3: The Path Ahead\n"
        f"With a structured daily routine, tracking their moods, and staying connected, "
        f"{student_name} was ready to face the challenges. The {exam_target} exam was no longer an adversary, but a stepping stone."
    )
    
    if not client:
        return fallback_text
        
    try:
        prompt = (
            f"Write a relatable, inspiring 3-chapter short story about a student named {student_name} "
            f"preparing for {exam_target} who is currently feeling {mood_str} (mood score: {mood_score}/10). "
            f"Make it encouraging and highlight the importance of balancing mental wellness and study."
        )
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception:
        return fallback_text

def chat_with_student(history: list, student_name: str) -> str:
    client = get_anthropic_client()
    
    safety_info = (
        "\n\n[Safety Notice: If you are experiencing overwhelming stress, please reach out to AASRA (91-9820466726) "
        "or Kiran Mental Health Helpline (1800-599-0019) for 24/7 confidential support.]"
    )
    
    last_user_message = ""
    for msg in reversed(history):
        if msg["role"] == "user":
            last_user_message = msg["content"].lower()
            break
            
    fallback_text = (
        f"Hey {student_name}, I hear you. Preparing for exams is tough, and it's completely normal to feel "
        f"stressed or overwhelmed. Remember to take small, frequent breaks, stay hydrated, and talk to your loved ones. "
        f"What's one small thing we can focus on right now?"
    )
    
    if "stress" in last_user_message or "anxious" in last_user_message or "panic" in last_user_message:
        fallback_text = (
            f"I understand you are feeling a lot of pressure, {student_name}. Please take a deep breath. "
            f"Inhale for 4 seconds, hold for 4, exhale for 4. You are more than any exam score. "
            f"Please remember to take regular breaks, do some light exercise, and check in with people you trust."
        )
    elif "sad" in last_user_message or "depressed" in last_user_message or "kill" in last_user_message or "die" in last_user_message or "suicide" in last_user_message:
        fallback_text = (
            f"I'm really sorry you're feeling this way, {student_name}. Your life and well-being are incredibly important. "
            f"Please consider talking to a professional, a parent, or a teacher who can support you. "
            f"You don't have to carry this alone."
        )
        
    fallback_text += safety_info
    
    if not client:
        return fallback_text
        
    try:
        system_prompt = (
            f"You are Saathi, an empathetic AI mental wellness co-pilot for a student named {student_name}. "
            f"Provide supportive, non-clinical listening. "
            f"CRITICAL: If the student exhibits extreme distress, self-harm, or suicidal ideation, "
            f"you must provide safety helpline information: AASRA (91-9820466726) and Kiran (1800-599-0019) immediately."
        )
        
        formatted_messages = []
        for h in history:
            formatted_messages.append({"role": h["role"], "content": h["content"]})
            
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            temperature=0.7,
            system=system_prompt,
            messages=formatted_messages
        )
        return message.content[0].text
    except Exception:
        return fallback_text

def generate_subtle_ally_nudge(student_name: str, avg_mood: float, avg_energy: float, recent_note: str) -> str:
    client = get_anthropic_client()
    
    mood_desc = "elevated stress levels" if avg_mood < 5 else "moderate stress" if avg_mood < 7 else "generally stable emotional state"
    energy_desc = "low energy" if avg_energy < 5 else "moderate energy" if avg_energy < 7 else "good energy"
    
    fallback_text = (
        f"Dear Guardian/Educator,\n\n"
        f"Based on recent patterns, {student_name} seems to be experiencing {mood_desc} and {energy_desc} "
        f"during their exam preparation. They noted some pressure recently.\n\n"
        f"Actionable Tips:\n"
        f"1. Encourage a gentle conversation about balancing studies with relaxation without focusing on exam outcome.\n"
        f"2. Ensure they take adequate sleep (at least 7-8 hours) and have healthy meals.\n"
        f"3. Offer reassurance that their effort and health are valued above all else."
    )
    
    if not client:
        return fallback_text
        
    try:
        prompt = (
            f"Create a subtle, non-alarmist, privacy-first nudge/tip card for the parent or teacher of a student named {student_name}. "
            f"The student's current average mood score is {avg_mood}/10 ({mood_desc}) and energy level is {avg_energy}/10 ({energy_desc}). "
            f"Do NOT mention any specific numerical scores or share private journals. "
            f"Provide exactly 2-3 supportive, concrete actions the adult can take to support the student's well-being."
        )
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception:
        return fallback_text
