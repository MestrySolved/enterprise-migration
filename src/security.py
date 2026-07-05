# src/security.py

def assess_security(system: dict) -> dict:
    flags = []

    if system.get("internet_facing"):
        flags.append("Internet-facing: requires Cloud Armor (WAF) and a Load Balancer with TLS.")

    if system.get("compliance"):
        for framework in system["compliance"]:
            flags.append(f"{framework} compliance: requires CMEK (customer-managed encryption keys) "
                         f"and audit logging via Cloud Audit Logs.")

    if system.get("workload_type") == "stateful":
        flags.append("Stateful workload: enable automated backups (Persistent Disk snapshots or Cloud SQL backups).")

    os_name = system.get("os", "N/A")
    if os_name != "N/A" and any(eol in os_name for eol in
                                  ["2008", "2012", "Windows 8", "Windows 7", "XP"]):
        flags.append("EOL operating system: no vendor security patches — isolate in its own VPC/subnet "
                     "with restricted firewall rules until upgraded.")

    if not flags:
        flags.append("No special security considerations flagged — apply standard IAM least-privilege and VPC firewall rules.")

    return {"flags": flags}