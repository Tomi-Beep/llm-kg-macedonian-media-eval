# Evaluation of LLM with KG on Macedonian Media

Can a knowledge graph help an LLM answer questions in Macedonian about film music? I tested this with 18 questions and a catalogue of 32 facts drawn from film credits and discographies. For example, to name an album by the composer of the music for „Врба“, the graph follows two links from the film to Кирил Џајковски and then to *Homebound*.

I ran the same Qwen3 4B Instruct model in three ways. The overall score was **6/18** with the question alone, **11/18** with exact film-title text search, and **16/18** with graph lookup. On the six questions that needed two links, graph lookup found all the needed facts and Qwen answered five correctly. Film-title search found the credits, and its answers missed all six. The overall score includes correctly saying when there was too little information to answer.

[Benchmark questions and sources](data/soundtrack-benchmark.json) · [Scoring notes](results/soundtrack-scoring.md) · [Saved results](results/soundtrack-results.jsonl)

## Run the benchmark

With Python 3 installed and Ollama running, open a terminal in the project folder and run these commands. Use `python3` if that’s how your system runs Python.

```sh
ollama pull qwen3:4b-instruct-2507-q4_K_M
python -m pip install -r requirements.txt
python run-benchmark.py
```

The script prints the evidence and answers for all 18 questions and saves the new run to `results/latest-run.jsonl`. The [original benchmark run](results/soundtrack-results.jsonl) is saved separately.
