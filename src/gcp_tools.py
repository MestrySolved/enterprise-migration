# src/gcp_tools.py

GCP_TOOL_MAP = {
    "SaaS": {
        "migration_tool": "N/A — evaluate Google Workspace or a 3rd-party SaaS replacement instead.",
        "pricing_calculator": "https://workspace.google.com/pricing.html",
        "process": [
            "1. Identify SaaS equivalent (e.g., Workspace, Zendesk, Salesforce).",
            "2. Export data from legacy system.",
            "3. Migrate data via vendor's import tool or API.",
            "4. Decommission legacy system after parallel-run validation."
        ]
    },
    "Kubernetes": {
        "migration_tool": "Migrate to Containers (part of Google Cloud Migration Center)",
        "pricing_calculator": "https://cloud.google.com/products/calculator",
        "process": [
            "1. Containerize the app (Docker) if not already.",
            "2. Use 'Migrate to Containers' to auto-generate a K8s deployment from a VM image.",
            "3. Deploy to GKE Autopilot (simplest) or GKE Standard (more control).",
            "4. Set up Cloud Load Balancing + Cloud Armor if internet-facing."
        ]
    },
    "VM": {
        "migration_tool": "Migrate to Virtual Machines (formerly Migrate for Compute Engine)",
        "pricing_calculator": "https://cloud.google.com/products/calculator",
        "process": [
            "1. Install the Migrate to VMs connector against your source (VMware/AWS/on-prem).",
            "2. Replicate the VM disk to GCP.",
            "3. Test-clone the VM in an isolated GCP network before cutover.",
            "4. Cutover and validate; keep source VM as rollback for a defined window."
        ]
    }
}

def get_gcp_recommendation(hosting_type: str) -> dict:
    return GCP_TOOL_MAP.get(hosting_type, {"migration_tool": "Unknown hosting type"})