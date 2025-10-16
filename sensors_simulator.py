import random, time

def get_simulated_signals():
    """Generate random HRV, typing speed, and EDA values."""
    hrv = random.uniform(50, 90)            # ms
    typing_speed = random.uniform(200, 350) # chars/min
    eda = random.uniform(0.1, 0.6)          # microsiemens
    return {"hrv": hrv, "typing_speed": typing_speed, "eda": eda}

if __name__ == "__main__":
    for _ in range(5):
        print(get_simulated_signals())
        time.sleep(1)
