# SIEM Home Lab

This lab demonstrates building a home SIEM environment using **Microsoft Sentinel** and simulated attack data. It covers setup, data ingestion, detection engineering, and automated response workflows — showcasing practical cloud security engineering skills.

---

## Objectives
- Build a functional SIEM using Microsoft Sentinel  
- Ingest Windows and network logs via Log Analytics  
- Create custom KQL detections for common attack patterns  
- Automate incident response with Logic Apps  

---

## Tools Used
- Microsoft Sentinel  
- Azure Log Analytics  
- Sysmon  
- Microsoft Defender for Endpoint  
- Logic Apps  
- PowerShell / KQL  

---

## Architecture Overview
A simplified architecture diagram should illustrate:
- Data sources (Sysmon, Azure VMs, network logs)  
- Log Analytics workspace  
- Sentinel dashboards and playbooks  
- Automated response flow  

---

## Setup Steps
1. Deploy an **Azure Log Analytics workspace**  
2. Connect data sources (Sysmon, Defender, etc.)  
3. Enable **Microsoft Sentinel** and create analytic rules  
4. Configure alert automation using Logic Apps  

---

## Detection Engineering
Example KQL query for failed logons:
```kql
SecurityEvent
| where EventID == 4625
| summarize FailedLogons = count() by Account
