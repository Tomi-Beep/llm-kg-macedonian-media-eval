# From Film to Playlist — IIS benchmark scorecard

The benchmark compares three conditions on the same 18 Macedonian questions using Qwen3 4B Instruct through Ollama (`qwen3:4b-instruct-2507-q4_K_M`, temperature 0, up to 100 output tokens). The six direct questions need one film credit. The six two-link questions need a film credit and an album by the credited artist. For the other six, the local catalogue has film credits but lacks an album record for the requested artist. The 32 sourced facts are shared between the two retrieval methods.

## Scoring rules

- **Answer:** On an answerable question, the reply must provide any acceptable answer listed in the benchmark. A refusal misses an answerable question, even when the retrieved context is insufficient. A name can be correct despite minor language errors. On a question with missing catalogue evidence, saying that the available information is insufficient passes.
- **Complete evidence:** For an answerable question, the retrieved facts must contain all the fact IDs for at least one acceptable answer path. This is checked independently of the reply. The question-only condition has no retrieved evidence. The six missing-evidence questions are excluded from this metric.
- **Grounded correct answer:** The reply gives an acceptable answer and its specific answer path is present in the retrieved facts. This metric covers the 12 answerable questions.
- **Unsupported album:** On a missing-evidence question, naming an album absent from the retrieved facts fails even if the reply names the correct composer. The benchmark judges what the supplied catalogue supports.

Answers were assessed manually. Evidence coverage was computed from the saved evidence sentences and their fact IDs in the benchmark. Both retrieval prompts use the same instructions, including a request to abstain when the evidence is insufficient. The question-only prompt allows the model to use what it already knows.

## Results

| Measure | No additional context | Film-title text search | Graph lookup |
| --- | ---: | ---: | ---: |
| Correct answers on direct questions | 0/6 | 6/6 | 6/6 |
| Correct answers on two-link questions | 0/6 | 0/6 | 5/6 |
| Correct answers on answerable questions | 0/12 | 6/12 (50.0%) | 11/12 (91.7%) |
| Complete evidence on direct questions | n/a | 6/6 | 6/6 |
| Complete evidence on two-link questions | n/a | 0/6 | 6/6 |
| Grounded correct answers on answerable questions | n/a | 6/12 (50.0%) | 11/12 (91.7%) |
| Correct abstention on missing-evidence questions | 6/6 | 5/6 | 5/6 |
| Overall task score | 6/18 (33.3%) | 11/18 (61.1%) | 16/18 (88.9%) |

## Worked example

`soundtrack-01` asks who composed the music for „Сестри“. Both searches return the film credit for **Игор Василев – Новоградска**, and both replies give that name. Both have complete evidence and a grounded correct answer. The question-only reply says it lacks information, so it misses the answer. Its “одговорим” is also a language error, scored separately from correctness.

## Per-question scoring

In the evidence columns, **Complete** means the retrieved facts contain an entire acceptable path. **Partial** means the composer credit was retrieved and the album link is missing.

| ID | Film | Expected answer or action | No context | Text evidence | Text answer | Graph evidence | Graph answer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Сестри | Игор Василев – Новоградска | Abstained | Complete | Correct | Complete | Correct |
| 02 | Исцелител | Бранислав Николов, Пеце Трајковски, or Гоце Јованоски | Abstained | Complete | Correct | Complete | Correct |
| 03 | Трето полувреме | Кирил Џајковски | Abstained | Complete | Correct | Complete | Correct |
| 04 | Големата вода | Кирил Џајковски | Abstained | Complete | Correct | Complete | Correct |
| 05 | Стела | Оливер Јосифовски | Abstained | Complete | Correct | Complete | Correct |
| 06 | Медена земја | Фолтин | Abstained | Complete | Correct | Complete | Correct |
| 07 | Врба | Homebound | Abstained | Partial | Abstained | Complete | Correct |
| 08 | Медена земја | LO-LEE-TA-TOO | Abstained | Partial | Abstained | Complete | Correct |
| 09 | До Балчак | Love Is The Way | Abstained | Partial | Abstained | Complete | Correct |
| 10 | Bikini Moon | Sisterhood or Bikini Moon soundtrack album | Abstained | Partial | Abstained | Complete | Correct |
| 11 | Мајки | Sisterhood or Bikini Moon soundtrack album | Abstained | Partial | Abstained | Complete | Correct |
| 12 | Кајмак | Wood Works | Abstained | Partial | Abstained | Complete | Abstained |
| 13 | Господ постои, името ѝ е Петрунија | Abstain | Correct abstention | Partial | Correct abstention | Partial | Correct abstention |
| 14 | Кога денот немаше име | Abstain | Correct abstention | Partial | Correct abstention | Partial | Correct abstention |
| 15 | Домаќинство за почетници | Abstain | Correct abstention | Partial | Correct abstention | Partial | Correct abstention |
| 16 | М | Abstain | Correct abstention | Partial | Unsupported album | Partial | Unsupported album |
| 17 | Снежана на крајот умира | Abstain | Correct abstention | Partial | Correct abstention | Partial | Correct abstention |
| 18 | Vera andrron detin | Abstain | Correct abstention | Partial | Correct abstention | Partial | Correct abstention |

## Interpretation

- **Retrieval failure:** For „Врба“, the title search finds Кирил Џајковски’s credit. The album entry has no mention of the film title. Following the composer link adds *Homebound* and Qwen answers correctly.
- **Answer failure with complete evidence:** For „Кајмак“, the graph retrieves both the Danish String Quartet credit and the *Wood Works* entry. Qwen still abstains. The model's reason for doing so is unknown.
- **Unsupported answer:** For „М“, both searches return only the composer credit. Both replies name *The Music of M*. The supplied credit gives no album information.
- **Language:** The question-only replies repeatedly use “одговорим” instead of “одговорам”. The text-search answer for „Медена земја“ (case 06) starts with the awkward form “Засекој”, while the credited artist is correct. Album and artist names keep their original spelling.

The two retrieval methods are compared with the same catalogue and prompt instructions. The graph follows the relationship needed for a case using its supplied film name and question-type flag. The text method is a single pass for the exact quoted film title. It does not perform a second search for the composer or rank by semantic similarity. These results compare the implemented workflows on a small curated dataset. Case 06 had different wording even though the two retrieval prompts were identical.

[Benchmark and source records](../data/soundtrack-benchmark.json) · [Raw answers and evidence](soundtrack-results.jsonl) · [Script used for the benchmark](../run-benchmark.py)
