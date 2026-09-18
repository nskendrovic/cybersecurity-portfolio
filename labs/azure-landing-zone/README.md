# Azure Landing Zone Lab

## Overview
This lab demonstrates the design and deployment of a **Cloud Adoption Framework (CAF)–aligned Azure Landing Zone** for enterprise security and governance.  
It serves as a practical portfolio project showcasing cloud security architecture, identity management, and monitoring integration.

---

## Current Progress

| CAF Pillar | Status | Notes |
|-------------|---------|-------|
| **Management & Governance** | ✅ Complete | Root, Platform, Prod, and NonProd management groups created. Resource groups structured and tagging policy applied. |
| **Identity & Access** | ✅ Complete | Two break-glass accounts configured with diagnostic logging to Log Analytics. Conditional Access baseline applied. |
| **Networking** | ⚙️ In Progress (~70%) | Hub VNet created. Firewall and policy deployed (later removed to prevent cost). Route tables and peering planned next. |
| **Security** | ⚙️ In Progress (~80%) | Governance policy, Defender integration, and audit logging configured. Security score and compliance policies next. |
| **Monitoring** | ⚙️ In Progress (~80%) | Log Analytics workspace created and connected to identity logs. Expanding to resource and network diagnostics. |
| **Automation (IaC)** | 🚧 Planned | Terraform/Bicep templates to automate Landing Zone deployment. |

**Overall Completion:** ~75%

---

## Key Components Implemented
- **Management Groups:** Root → Platform → Prod / NonProd hierarchy  
- **Resource Groups:** `rg-network-hub`, `rg-logging`, `rg-security`, `rg-shared`  
- **Hub VNet:** Created with `AzureFirewallSubnet`  
- **Firewall Policy:** Deployed and tested, later removed to reduce cost  
- **Governance:** Tag enforcement and baseline policies applied  
- **Log Analytics Workspace:** Centralized logging for sign-in and audit events  
- **Break-Glass Accounts:** Configured with diagnostic settings and monitoring  
- **Diagnostic Settings:** Forwarded to Log Analytics for visibility and audit trail  

---

## Next Steps
1. Rebuild cost-optimized **Firewall and route tables**  
2. Add **spoke VNets** and **peering**  
3. Expand **Defender for Cloud** and **Sentinel integration**  
4. Begin **Terraform automation** for repeatable deployment  
5. Document architecture diagrams and security controls  

---

## Learning Objectives
- Apply **Azure CAF principles** for governance and security  
- Implement **Zero Trust** identity and access controls  
- Configure **centralized monitoring and diagnostics**  
- Build a **portfolio-ready cloud security architecture**

---
  
## Architecture Diagram
This diagram shows the current state of the Azure Landing Zone, including management groups, subscriptions, resource groups, and core networking/logging components.

---

```mermaid
flowchart TB
    tenant["Tenant Root"]
    mg_root["Management Groups"]
    mg_platform["Platform MG"]
    mg_prod["Prod MG"]
    mg_nonprod["NonProd MG"]

    sub_platform["Platform Subscription"]
    rg_hub["rg-network-hub"]
    vnet_hub["vnet-hub"]
    fw_subnet["AzureFirewallSubnet – planned"]
    rg_logging["rg-logging"]
    law["Log Analytics Workspace"]
    rg_security["rg-security"]
    sec_tools["Defender / Sentinel – planned"]
    rg_shared["rg-shared"]

    tenant --> mg_root
    mg_root --> mg_platform
    mg_root --> mg_prod
    mg_root --> mg_nonprod

    mg_platform --> sub_platform
    sub_platform --> rg_hub
    rg_hub --> vnet_hub
    vnet_hub --> fw_subnet

    sub_platform --> rg_logging
    rg_logging --> law

    sub_platform --> rg_security
    rg_security --> sec_tools

    sub_platform --> rg_shared
```
---

## IAM Flow Diagram
This diagram shows how identity authentication events move through Entra ID, Conditional Access, logging, and alerting within the Landing Zone. It includes break‑glass accounts, baseline CA policies, diagnostic settings, and Log Analytics integration.

```mermaid
flowchart TB
    user["User / Break‑Glass Account"]
    sign_in["Entra ID Sign‑In"]
    ca["Conditional Access Policies"]
    decision["Access Decision (Allow / Block / MFA)"]
    logs["Sign‑In Logs"]
    diag["Diagnostic Settings"]
    law["Log Analytics Workspace"]
    alert["Break‑Glass Alert Rule"]
    notify["Notification / Incident"]

    user --> sign_in
    sign_in --> ca
    ca --> decision
    decision --> logs
    logs --> diag
    diag --> law
    law --> alert
    alert --> notify
```


---

## Author
**Nikola Skendrovic**  
Security Analyst | Cloud Security Engineer  
CCSP Certified | GSEC, GCIH | CompTIA Net+ Sec+ | WGU Cybersecurity Student  

