import time
import llm
import memory

INITIAL_TOPICS = [
    # DSA — needs work
    ("Hashmaps beyond Two Sum", "DSA", "weak"),
    ("Recursion / DP", "DSA", "weak"),
    ("Sorting patterns", "DSA", "weak"),
    ("Two Pointers / Sliding Window", "DSA", "solid"),
    # Quant — solid, tested at high accuracy
    ("Percentages", "Quant", "solid"),
    ("Profit & Loss", "Quant", "solid"),
    ("SI/CI", "Quant", "solid"),
    ("Time & Work", "Quant", "solid"),
    ("Time Speed Distance", "Quant", "solid"),
    ("HCF/LCM", "Quant", "solid"),
    ("Probability", "Quant", "solid"),
    ("Permutation & Combination", "Quant", "solid"),
    ("Mixtures", "Quant", "solid"),
    # Reasoning — solid
    ("Coding-Decoding", "Reasoning", "solid"),
    ("Blood Relations", "Reasoning", "solid"),
    ("Series", "Reasoning", "solid"),
    ("Syllogisms", "Reasoning", "solid"),
    ("Seating Arrangement", "Reasoning", "solid"),
    # Verbal — not started yet, treat as weak until proven otherwise
    ("Grammar / Verbal", "Verbal", "weak"),
]

def pick_next_topic():
    weak = memory.get_weak_topics(limit=1)

    if weak:
        return weak[0]["topic"], weak[0]["category"]
    all_topics = memory.get_all_topics()
    t = all_topics[0]
    return t["topic"], t["category"]


def run_session(num_questions: int = 3):
    print("\n======Placement prep session======\n")
    session_results: dict[str, list[dict]] = {}

    for i in rangve(num_questions):
        topic, category = pick_next_topic()
        print(f"[Q{i + 1}] Topic: {topic} ({category})")
        q = llm.generate_question(topic, category)
        print(f"\n{q['question']}\n")

        start = time.time()
        user_answer = input("Your answer: ")
        elapsed = time.time() - start

        grade = llm.grade_answer(q["question"], q["answer"], user_answer)
        


