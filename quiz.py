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

