import json
import asyncio
from openai import AsyncOpenAI

# 1. Configuration
INPUT_FILE = "/u/yzhao25/tokenspeed/gh200/prompts/openai_humaneval.json"   # The path to your dataset file
OUTPUT_FILE = "/u/yzhao25/tokenspeed/gh200/outputs/results_qwen3.jsonl"   # Where to save the model's answers
MODEL_NAME = "Qwen/Qwen3-32B"
PORT = 8003

MAX_CONCURRENT_REQUESTS = 16  # Adjust this based on your GPU memory/batch size

# 2. Initialize the ASYNC client
client = AsyncOpenAI(api_key="EMPTY", base_url=f"http://localhost:{PORT}/v1")

async def process_task(task, semaphore):
    """Processes a single task asynchronously, gated by a semaphore."""
    task_id = task["task_id"]
    prompt = task["prompt"]
    
    # Wait until a slot opens up in the semaphore
    async with semaphore:
        print(f"Starting {task_id}...")
        try:
            response = await client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert Python developer. Complete the following Python code based on the docstring. Return ONLY the valid Python code to complete the function, without any markdown formatting or explanations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.2,
            )
            completion = response.choices[0].message.content
            print(f"Finished {task_id}!")
            
            return {
                "task_id": task_id,
                "completion": completion
            }
        except Exception as e:
            print(f"Error on {task_id}: {e}")
            return None

async def main():
    # 3. Load the dataset
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    
    tasks = data.get("details", [])
    print(f"Loaded {len(tasks)} tasks. Starting concurrent execution...\n")
    
    # 4. Create a semaphore to limit concurrency
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    # 5. Build a list of background tasks
    coroutines = [process_task(task, semaphore) for task in tasks]
    
    # 6. Run them all concurrently and wait for all to finish
    results = await asyncio.gather(*coroutines)
    
    # 7. Write all successful results to the JSONL file
    successful_results = [res for res in results if res is not None]
    
    with open(OUTPUT_FILE, "w") as out_file:
        for res in successful_results:
            out_file.write(json.dumps(res) + "\n")
            
    print(f"\nAll tasks completed! Saved {len(successful_results)} results to {OUTPUT_FILE}")

# Run the async event loop
if __name__ == "__main__":
    asyncio.run(main())