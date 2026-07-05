import argparse
from discovery import load_systems, build_dependency_graph
from strategy import classify
from ai_advisor import get_ai_rationale
from sizing import recommend_hosting, recommend_machine_size
from security import assess_security
from gcp_tools import get_gcp_recommendation


def run_pipeline(input_path: str):
    systems = load_systems(input_path)
    graph = build_dependency_graph(systems)

    # Need full system dicts (not just graph) for the new fields (cpu, memory, os, etc.)
    systems_by_name = {s["name"]: s for s in systems}

    # mark who has dependents
    all_deps = set()
    for info in graph.values():
        all_deps.update(info["depends_on"])
    for name, info in graph.items():
        info["has_dependents"] = name in all_deps

    print("=" * 60)
    print("DEPENDENCY GRAPH")
    print("=" * 60)
    for name, info in graph.items():
        print(f"{name}: depends on {info['depends_on']} (criticality: {info['criticality']})")

    print("\n" + "=" * 60)
    print("MIGRATION RECOMMENDATIONS (7R FRAMEWORK + SIZING + SECURITY)")
    print("=" * 60)

    for name, info in graph.items():
        full_system = systems_by_name[name]  # has os, cpu_cores, memory_gb, etc.

        # 7R decision + AI opinion
        rule_result = classify(name, info)
        ai_opinion = get_ai_rationale(name, info, rule_result["decision"])

        # hosting, sizing, security, GCP tools
        hosting = recommend_hosting(full_system)
        size = recommend_machine_size(
            full_system.get("cpu_cores", 2),
            full_system.get("memory_gb", 8)
        )
        sec = assess_security(full_system)
        gcp = get_gcp_recommendation(hosting["hosting"])

        print(f"\n--- {name} ---")
        print(f"  7R decision (rule-based): {rule_result['decision']}")
        print(f"  Reason: {rule_result['reason']}")
        print(f"  AI assessment: {ai_opinion}")
        print(f"  Recommended hosting: {hosting['hosting']} — {hosting['reason']}")
        print(f"  OS status: {hosting['os_check']['note']}")
        print(f"  Suggested machine size: {size}")
        print(f"  Security flags:")
        for flag in sec["flags"]:
            print(f"    - {flag}")
        print(f"  GCP migration tool: {gcp['migration_tool']}")
        print(f"  Pricing calculator: {gcp['pricing_calculator']}")
        print(f"  Migration steps:")
        for step in gcp["process"]:
            print(f"    {step}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enterprise migration copilot")
    parser.add_argument("--input", default="data/sample_input.json", help="Path to systems JSON file")
    args = parser.parse_args()
    run_pipeline(args.input)