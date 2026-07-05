import json

def load_systems(path: str) -> list:
    with open(path, "r") as f:
        data = json.load(f)
    return data["systems"]

def build_dependency_graph(systems: list) -> dict:
    graph = {}
    for system in systems:
        graph[system["name"]] = {
            "depends_on": system["depends_on"],
            "criticality": system["criticality"]
        }
    return graph

if __name__ == "__main__":
    systems = load_systems("data/sample_input.json")
    graph = build_dependency_graph(systems)
    for name, info in graph.items():
        print(f"{name}: depends on {info['depends_on']} (criticality: {info['criticality']})")