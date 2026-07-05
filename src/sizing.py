# src/sizing.py

EOL_OS_LIST = ["Windows Server 2008", "Windows Server 2008 R2", "Windows Server 2012",
               "Windows 8", "Windows 8.1", "Windows XP", "Windows 7"]

def check_os_support(os_name: str) -> dict:
    if os_name == "N/A":
        return {"supported": True, "note": "No OS dependency (SaaS/managed service candidate)."}
    is_eol = any(eol in os_name for eol in EOL_OS_LIST)
    if is_eol:
        return {
            "supported": False,
            "note": f"{os_name} is end-of-life. Requires OS upgrade during migration, "
                    f"or use Extended Security Updates (ESU) as a stopgap — factor ESU cost into pricing."
        }
    return {"supported": True, "note": f"{os_name} is currently supported."}

def recommend_hosting(system: dict) -> dict:
    workload = system["workload_type"]
    os_check = check_os_support(system["os"])

    if workload == "commodity":
        return {
            "hosting": "SaaS",
            "reason": "Commodity function — evaluate replacing with a SaaS product instead of migrating infrastructure at all.",
            "os_check": os_check
        }
    elif workload == "stateless" and os_check["supported"]:
        return {
            "hosting": "Kubernetes",
            "reason": "Stateless workload on a supported OS — good containerization candidate.",
            "os_check": os_check
        }
    else:
        return {
            "hosting": "VM",
            "reason": "Stateful workload or unsupported OS — needs a VM, not a container, at least initially.",
            "os_check": os_check
        }

def recommend_machine_size(cpu_cores: int, memory_gb: int) -> str:
    # Simple tiering — replace with real cloud provider SKU tables later
    if cpu_cores <= 2 and memory_gb <= 8:
        return "Small (2 vCPU / 8GB) — e.g., AWS t3.large, Azure B2ms, GCP e2-standard-2"
    elif cpu_cores <= 4 and memory_gb <= 16:
        return "Medium (4 vCPU / 16GB) — e.g., AWS m5.xlarge, Azure D4s_v5, GCP n2-standard-4"
    else:
        return "Large (8+ vCPU / 32GB+) — e.g., AWS m5.2xlarge, Azure D8s_v5, GCP n2-standard-8"