from ollama import chat

from retrieval import find_graph_evidence, find_text_evidence


def ask_model(model, prompt, keep_alive):
    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0, "num_predict": 100},
        keep_alive=keep_alive,
    )
    return response.message.content


def run_question(facts, film, question, needs_album, model):
    composers, albums, evidence = find_graph_evidence(facts, film, needs_album)
    print("Музика од:", composers)
    print("Албуми:", albums)

    print()
    print("Докази:")
    for line in evidence:
        print(line)

    instruction = "Одговори на македонски во една реченица. Ако не можеш да одговориш, кажи дека немаш доволно информации."
    evidence_rule = "Користи ги само дадените докази. Ако во нив нема одговор, напиши: Немам доволно информации."

    prompt_without_additional_context = f"{instruction}\n\nПрашање: {question}"
    without_context = ask_model(model, prompt_without_additional_context, "1m")

    print()
    print("Одговор без дополнителен контекст:")
    print(without_context)

    evidence_text = "\n".join(evidence)
    prompt_with_graph = f"{instruction}\n{evidence_rule}\n\nДокази:\n{evidence_text}\n\nПрашање: {question}"
    graph_answer = ask_model(model, prompt_with_graph, "1m")

    print()
    print("Одговор со граф:")
    print(graph_answer)

    text_matches = find_text_evidence(facts, film)

    print()
    print("Докази од текстуалното пребарување:")
    for sentence in text_matches:
        print(sentence)

    text_evidence = "\n".join(text_matches)
    prompt_with_text_search = f"{instruction}\n{evidence_rule}\n\nДокази:\n{text_evidence}\n\nПрашање: {question}"
    text_answer = ask_model(model, prompt_with_text_search, 0)

    print()
    print("Одговор со текстуално пребарување:")
    print(text_answer)

    return {
        "without_context": without_context,
        "graph_evidence": evidence,
        "graph_answer": graph_answer,
        "text_evidence": text_matches,
        "text_answer": text_answer,
    }
