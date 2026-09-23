# Email Sender Trust Framework

## Overview
The Email Sender Trust Framework is a modular Python-based system for evaluating the trustworthiness of email senders using DNS validation, WHOIS domain age, IP reputation intelligence, and behavioral heuristics. It provides transparent, scriptable scoring logic that helps analysts identify suspicious senders, misconfigured domains, and potential phishing attempts.

## Architecture
- Input: Raw `.eml` files  
- Core Modules:
  - Email parsing  
  - DNS validation (SPF, MX)  
  - WHOIS domain age lookup  
  - AbuseIPDB IP reputation scoring  
  - Behavioral heuristics  
- Output: Composite trust score (0–100) with Low, Medium, or High risk classification

## Features
- SPF record validation  
- MX record presence check  
- Domain age calculation via WHOIS  
- IP reputation scoring using AbuseIPDB  
- Detection of suspicious sender names  
- Detection of risky domain patterns (uncommon TLDs, long domains)  
- Fully modular and extensible Python design

## Scoring Model
| Factor | Condition | Penalty |
|--------|-----------|---------|
| SPF | Missing or invalid | -30 |
| AbuseIPDB score >50 | -50 |
| AbuseIPDB score >20 | -20 |
| Domain age <30 days | -25 |
| Domain age 30–180 days | -10 |
| MX record missing | -25 |
| Suspicious sender name | -20 |
| Risky TLD or long domain | -15 |

**Risk Levels:**  
- Low Risk: >80  
- Medium Risk: 51–80  
- High Risk: ≤50

## Example Outputs

### Medium Risk Example
Sender: `"Access Log: #NYKDNJNWW" <rqgoq@sneezekey.ru>`  
Score: **55**  
Reason: Suspicious display name and `.ru` TLD.

### Low Risk Example
Sender: `CompTIA <noreplies@comptia.org>`  
Score: **100**  
Reason: Long-established domain, clean reputation, valid SPF/MX.

## Folder Structure
