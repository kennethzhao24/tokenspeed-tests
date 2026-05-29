import json
from openai import OpenAI

# 1. Configuration
INPUT_FILE = "/u/yzhao25/tokenspeed/gh200/openai_humaneval.json"   # The path to your dataset file
OUTPUT_FILE = "/u/yzhao25/tokenspeed/gh200/results.jsonl"   # Where to save the model's answers
MODEL_NAME = "openai/gpt-oss-20b"

# 2. Initialize the local client
client = OpenAI(api_key="EMPTY", base_url="http://localhost:8001/v1")

# 3. Load the HumanEval dataset
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

tasks = data.get("details", [])
print(f"Loaded {len(tasks)} tasks from HumanEval.")

# Open the output file in append mode
with open(OUTPUT_FILE, "w") as out_file:
    
    # 4. Iterate through every task
    for i, task in enumerate(tasks):
        task_id = task["task_id"]
        prompt = task["prompt"]
        
        print(f"Processing {i+1}/{len(tasks)}: {task_id}...")
        
        try:
            # Send the request to your local server
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer. Complete the following Python code based on the docstring. Return ONLY the valid Python code to complete the function, without any markdown formatting or explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,     # 512 is usually plenty for HumanEval solutions
                temperature=0.2,    # Use a low temperature (0.1 - 0.2) for code generation
            )
            
            # Extract the generated code
            completion = response.choices[0].message.content
            
            # 5. Save the result in the standard HumanEval JSONL format
            result = {
                "task_id": task_id,
                "completion": completion
            }
            out_file.write(json.dumps(result) + "\n")
            
        except Exception as e:
            print(f"Error processing {task_id}: {e}")

print(f"\nAll tasks completed! Results saved to {OUTPUT_FILE}")