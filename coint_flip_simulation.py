"""
Simulate a coin flip
"""

import random

def simulate_coin_flips(num_flips=100, num_simulations=100000):
    """method docstring"""

    streak_count = 0  # Count how many times a streak of 6 or more occurs

    for _ in range(num_simulations):
        flips = [random.choice(['H', 'T']) for _ in range(num_flips)]
        streak = 1

        # Check for streaks of 6 or more
        for i in range(1, num_flips):
            if flips[i] == flips[i - 1]:
                streak += 1
                if streak >= 6:
                    streak_count += 1  # Count the streak immediately when found
                    break
            else:
                streak = 1  # Rest streak counter if the sequence breaks

    return streak_count

NUM_TRIALS = 100000  # Number of simulations
STREAK_OCCURRENCES= simulate_coin_flips(num_simulations=NUM_TRIALS)

print(f"Number of chances of getting a streak of 6 or more in 100 flips (out of {NUM_TRIALS} trials): {STREAK_OCCURRENCES}")
print(f"Probability of getting a streak of 6 or more in 100 flips: {STREAK_OCCURRENCES / NUM_TRIALS:.4f}")

# for _ in range(999):
    