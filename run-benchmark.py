import json
from pathlib import Path

from question_answering import run_question

project_folder = Path(__file__).parent
model = "qwen3:4b-instruct-2507-q4_K_M"

with open(project_folder / "data" / "soundtrack-benchmark.json", encoding="utf-8") as benchmark_file:
    benchmark = json.load(benchmark_file)

facts = []
for fact in benchmark["facts"]:
    facts.append((fact["subject"], fact["relation"], fact["target"]))

cases = benchmark["cases"]
results_path = project_folder / "results" / "latest-run.jsonl"

with open(results_path, "w", encoding="utf-8") as results_file:
    for case in cases:
        print()
        print("Прашање:", case["question"])

        result = {"case": case, "model": model}
        result.update(
            run_question(facts, case["film"], case["question"], case["needs_album"], model)
        )
        results_file.write(json.dumps(result, ensure_ascii=False) + "\n")
        results_file.flush()
