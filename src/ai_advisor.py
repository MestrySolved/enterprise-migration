import requests

def get_ai_rationale(name: str, info: dict, rule_based_decision: str) -> str:
    prompt = f"""A company is migrating this system to the cloud.
System: {name}
Depends on: {info['depends_on']}
Criticality: {info['criticality']}
A rule-based system suggested: {rule_based_decision}

In 2-3 sentences, confirm or challenge this recommendation using the 7Rs
framework (Rehost, Replatform, Refactor, Repurchase, Retire, Retain, Relocate).
Be specific and practical."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"]

if __name__ == "__main__":
    from discovery import load_systems, build_dependency_graph
    from strategy import classify

    systems = load_systems("data/sample_input.json")
    graph = build_dependency_graph(systems)

    for name, info in graph.items():
        info["has_dependents"] = False
        rule_result = classify(name, info)
        ai_opinion = get_ai_rationale(name, info, rule_result["decision"])
        print(f"\n{name} — rule says: {rule_result['decision']}")
        print(f"AI says: {ai_opinion}")