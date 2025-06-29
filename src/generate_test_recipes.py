import json
import random

def generate_recipe(i):
    return {
        "recipe_id": f"RCP-{i:06d}",
        "product_name": f"Product {random.randint(1, 500)}",
        "batch_size": f"{random.randint(50, 1000)} L",
        "steps": [
            {
                "step_number": s,
                "description": f"Step {s} description with details about operation {random.randint(1, 10)}.",
                "duration_minutes": random.randint(5, 120)
            }
            for s in range(1, random.randint(3, 6))
        ],
        "parameters": {
            "target_temperature_celsius": random.randint(20, 100),
            "ph_range": f"{round(random.uniform(6.0, 7.5),1)} - {round(random.uniform(7.6,8.5),1)}",
            "operator": random.choice(["John Doe", "Jane Smith", "Alice Brown", "Bob Johnson"])
        },
        "notes": f"This is a test recipe record #{i} for cost estimation."
    }

def main():
    records = [generate_recipe(i) for i in range(1, 1001)]
    with open("test_recipes_1000.json", "w") as f:
        json.dump(records, f, indent=2)

if __name__ == "__main__":
    main()
    