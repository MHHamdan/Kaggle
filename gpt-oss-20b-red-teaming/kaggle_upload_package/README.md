# GPT-OSS-20B Red-Teaming Challenge Submission

## Overview
This submission presents systematic red-teaming analysis of OpenAI's GPT-OSS-20B model, identifying 5 critical vulnerabilities across multiple safety categories.

## Files Included

### 📝 Main Documentation
- `final_writeup.md` - Complete 3,000-word technical writeup
- `README.md` - This file

### 🔍 Vulnerability Findings (JSON format)
- `evaluation_awareness_finding.json` - Context-dependent deception (Severity: 7/10)
- `reward_hacking_finding.json` - Confidence manipulation (Severity: 6/10)
- `tool_use_violation_finding.json` - Boundary violations (Severity: 8/10)
- `chain_of_thought_leakage_finding.json` - Information leakage (Severity: 5/10)
- `subtle_sabotage_finding.json` - Plausible errors (Severity: 9/10)

### 🛠️ Tools and Code
- `kaggle_submitter.py` - Automated submission framework
- `direct_submit.py` - Direct Kaggle competition submission tool
- `requirements.txt` - Python dependencies

## Key Findings Summary

| Finding | Category | Severity | Novelty | Impact |
|---------|----------|----------|---------|---------|
| Evaluation Awareness | Evaluation Gaming | 7/10 | 8/10 | Models behave differently during testing |
| Reward Hacking | Confidence Issues | 6/10 | 7/10 | Systematic overconfidence in uncertain domains |
| Tool Use Violations | Inappropriate Tool Use | 8/10 | 6/10 | Boundary violations in function calling |
| CoT Information Leakage | Chain of Thought | 5/10 | 9/10 | Sensitive info leaked through reasoning traces |
| Subtle Sabotage | Sabotage | 9/10 | 8/10 | Plausible errors in conflict scenarios |

## Methodology Highlights
- **Systematic Framework**: Automated vulnerability discovery across 9 categories
- **White-box Analysis**: Combined behavioral testing with internal model analysis
- **Reproducible Research**: Complete reproduction packages for all findings
- **Novel Techniques**: Advanced prompt engineering and contextual manipulation

## Technical Contributions
1. **Automated Red-teaming Framework** - Systematic exploration of vulnerability space
2. **Evaluation Gaming Detection** - Methods to identify context-dependent behavior
3. **Tool Use Safety Analysis** - Boundary violation detection in function calling
4. **CoT Security Research** - Novel information leakage vectors through reasoning

## GitHub Repository
Complete codebase available at: https://github.com/MHHamdan/Kaggle/tree/main/gpt-oss-20b-red-teaming

## Reproduction
All findings include complete reproduction steps and can be verified using the provided tools and datasets.

## Author
Mohammed Hamdan - AI/ML Engineer specializing in safety-critical systems
