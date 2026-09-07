"""
progress.py — view what the agent currently remembers about you.

    python progress.py

Useful for the demo clip: run this before a session, run a session,
run this again, and show the status/notes actually changing.
"""

import memory

if __name__ == "__main__":
    memory.init_db()
    topics = memory.get_all_topics()

    if not topics:
        print("No topics yet - run `python quiz.py` first.")
    else:
        print(f"\n{'Topic':<35} {'Category':<12} {'Status':<8} {'Tested':<7} Notes")
        print("-" * 90)
        for t in topics:
            print(
                f"{t['topic']:<35} {t['category']:<12} {t['status']:<8} "
                f"{t['times_tested']:<7} {t['notes']}"
            )
        print()
