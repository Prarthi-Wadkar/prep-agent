import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()  # reads GROQ_API_KEY from a local .env file if present

MODEL = "openai/gpt-oss-120b"

_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not set. Get a free key at https://console.groq.com/keys "
                "and run: export GROQ_API_KEY=your-key-here"
            )
        _client = Groq(api_key=api_key)
    return _client


def _call_json(prompt: str, temperature: float = 0.5) -> dict:
    """Shared helper: call Groq, strip any markdown fencing, parse JSON.
    Centralizing this means one place to harden parsing if the model
    ever wraps its output in ```json fences despite instructions."""
    resp = _get_client().chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    text = resp.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


def generate_question(topic: str, category: str, difficulty: str = "medium") -> dict:
    prompt = f"""You are a strict placement-exam question setter for Indian campus
placements (TCS NQT / Infosys / aptitude style).
Generate ONE {difficulty}-difficulty question on the topic "{topic}" (category: {category}).
Respond ONLY with JSON, no markdown, no preamble:
{{"question": "...", "answer": "...", "explanation": "..."}}"""
    return _call_json(prompt, temperature=0.7)


def grade_answer(question: str, correct_answer: str, user_answer: str) -> dict:
    prompt = f"""Question: {question}
Correct answer: {correct_answer}
Student's answer: {user_answer}

Is the student's answer correct? Allow for minor rounding/formatting differences
(e.g. "42" and "42.0" and "the answer is 42" all count as correct).
Respond ONLY with JSON:
{{"correct": true or false, "feedback": "one short sentence"}}"""
    return _call_json(prompt, temperature=0)


def extract_topic_update(topic: str, recent_results: list[dict]) -> dict:
    """recent_results: list of {"correct": bool, "time_taken_seconds": float}
    for this topic's attempts in the current session."""
    prompt = f"""A student just attempted questions on the topic "{topic}".
Recent results: {json.dumps(recent_results)}

Based on accuracy and speed, classify their current status on this topic.
Respond ONLY with JSON:
{{"status": "weak" or "solid", "note": "one short sentence, e.g. 'missed 2/3, slow on last attempt'"}}"""
    return _call_json(prompt, temperature=0)