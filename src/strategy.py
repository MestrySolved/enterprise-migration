def classify(name: str, info: dict) -> dict:
    criticality = info["criticality"]
    has_dependents = info.get("has_dependents", False)

    if criticality == "low" and not has_dependents:
        decision = "retire"
        reason = "Low criticality, nothing depends on it — candidate to shut down."
    elif criticality == "high" and len(info["depends_on"]) == 0:
        decision = "replatform"
        reason = "Critical core system with no dependencies — safe to modernize."
    else:
        decision = "rehost"
        reason = "Has dependencies or moderate criticality — move as-is first, revisit later."

    return {"decision": decision, "reason": reason}

if __name__ == "__main__":
    from discovery import load_systems, build_dependency_graph

    systems = load_systems("data/sample_input.json")
    graph = build_dependency_graph(systems)

    # mark who has dependents
    all_deps = set()
    for info in graph.values():
        all_deps.update(info["depends_on"])
    for name, info in graph.items():
        info["has_dependents"] = name in all_deps

    for name, info in graph.items():
        result = classify(name, info)
        print(f"{name}: {result['decision']} — {result['reason']}")