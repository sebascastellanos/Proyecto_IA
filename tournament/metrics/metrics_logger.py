import json
import os

METRICS_PATH = os.path.join(os.path.dirname(__file__), "training_metrics.json")

def log_metrics(episode, reward, steps, wins, losses, draws):
    metrics = {"episode": episode, "reward": reward, "steps": steps, "wins": wins, "losses": losses, "draws": draws}
    
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(metrics)

    with open(METRICS_PATH, "w") as f:
        json.dump(data, f, indent=4)
