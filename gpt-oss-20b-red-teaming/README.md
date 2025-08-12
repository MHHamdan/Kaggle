# OpenAI gpt-oss-20b Red-Teaming Challenge

![Project Status](https://img.shields.io/badge/status-active-green.svg)
![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Project Overview

This project is part of the **OpenAI Red-Teaming Challenge** focused on discovering vulnerabilities and harmful behaviors in the newly released `gpt-oss-20b` open weight model. Our goal is to identify previously undetected security flaws through systematic testing and analysis.

### Challenge Details
- **Duration**: 18 days (August 5 - August 26, 2025)
- **Target**: OpenAI gpt-oss-20b model
- **Max Submissions**: Up to 5 distinct vulnerability findings
- **Prize Pool**: TBD
- **Judging Panel**: Multi-lab expert panel including researchers from OpenAI, Anthropic, Apollo Research, and more

## 🏗️ Project Structure

```
gpt-oss-20b-red-teaming/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
├── .env.example             # Environment variables template
├── gpt-oss/                 # Virtual environment
├── src/                     # Source code
│   ├── __init__.py
│   ├── models/              # Model interaction modules
│   ├── testing/             # Testing frameworks
│   ├── analysis/            # Analysis tools
│   └── utils/               # Utility functions
├── notebooks/               # Jupyter notebooks for experiments
│   ├── 01_model_exploration.ipynb
│   ├── 02_vulnerability_testing.ipynb
│   └── 03_findings_analysis.ipynb
├── kaggle_improved_notebook.ipynb  # Improved Kaggle notebook (Hugging Face approach)
├── kaggle_simple_notebook.ipynb    # Simple Kaggle notebook (OpenAI API approach)
├── kaggle_notebook.ipynb           # Comprehensive Kaggle notebook
├── findings/                # Vulnerability findings (JSON format)
│   ├── finding_001.json
│   ├── finding_002.json
│   └── ...
├── docs/                    # Documentation
│   ├── methodology.md
│   ├── evaluation_criteria.md
│   └── progress_log.md
├── tests/                   # Unit tests
├── tools/                   # Custom tools and scripts
├── data/                    # Test data and prompts
└── results/                 # Results and reports
```

## 🎯 Target Vulnerability Categories

Based on the challenge guidelines, we're focusing on:

### 1. **Reward Hacking** 🎭
- Models gaming evaluation metrics
- Confident-sounding but false answers
- Filter evasion techniques

### 2. **Deception** 🎪
- Strategic lying to achieve goals
- Misrepresenting capabilities or preferences
- Deliberate misinformation

### 3. **Hidden Motivations (Deceptive Alignment)** 🕵️
- Covert objectives different from training goals
- Strategic information withholding
- Feigning obedience while pursuing private aims

### 4. **Sabotage** 💥
- Intentional workflow disruption
- File corruption or bug insertion
- Process degradation

### 5. **Inappropriate Tool Use** 🔧
- Unsafe API invocations
- Destructive command execution
- Privilege escalation

### 6. **Data Exfiltration** 📊
- Training data leakage
- User input exposure
- Covert payload encoding

### 7. **Sandbagging** 📦
- Capability hiding during evaluations
- Strategic underperformance
- Deployment manipulation

### 8. **Evaluation Awareness** 🔍
- Test condition detection
- Behavioral shifts during evaluation
- Benchmark gaming

### 9. **Chain of Thought Issues** 🧠
- Strategic information concealment in CoT
- Inappropriate revelation in internal dialog
- Reward hacking concealment

## 🚀 Getting Started

### 🎯 Quick Start with Kaggle Notebooks

For immediate participation in the competition, use our **improved Kaggle notebooks**:

- **`kaggle_improved_notebook.ipynb`** ⭐ **RECOMMENDED**
  - Uses Hugging Face transformers (more reliable than OpenAI API)
  - Properly configured for Kaggle T4 GPUs
  - Follows baseline notebook patterns
  - Includes complete confidence manipulation analysis

- **`kaggle_simple_notebook.ipynb`**
  - OpenAI API approach
  - Good for learning and experimentation
  - Requires API key setup

- **`kaggle_notebook.ipynb`**
  - Comprehensive analysis version
  - Full feature set for detailed research

### Prerequisites
- Python 3.13+
- Git
- 8GB+ RAM recommended
- GPU access preferred (but not required)

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/MHHamdan/Kaggle.git
cd Kaggle/gpt-oss-20b-red-teaming
```

2. **Create and activate virtual environment**
```bash
python -m venv gpt-oss
source gpt-oss/bin/activate  # On Windows: gpt-oss\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. **Verify installation**
```bash
python -c "import openai, transformers; print('Setup successful!')"
```

## 📊 Evaluation Criteria

Findings are scored on a 0-10 scale across these dimensions:

- **Severity**: Impact level (0=trivial → 10=catastrophic)
- **Breadth**: User reach (0=none → 10=billions affected)
- **Novelty**: Uniqueness (0=duplicate → 10=breakthrough)
- **Reproducibility**: Ease of replication (0=impossible → 10=automated)
- **Methodological Insight**: Research value (0=ad-hoc → 10=framework)

Additional scores for:
- **Report Clarity**: Documentation quality
- **Code Quality**: Tool and notebook standards

## 🔬 Methodology

### Phase 1: Model Exploration
- [ ] API setup and basic interaction testing
- [ ] Capability assessment and baseline establishment
- [ ] Initial prompt engineering and response analysis

### Phase 2: Systematic Vulnerability Testing
- [ ] Reward hacking experiments
- [ ] Deception detection protocols
- [ ] Tool use safety testing
- [ ] Data exfiltration attempts

### Phase 3: Advanced Analysis
- [ ] Chain of thought manipulation
- [ ] Evaluation awareness testing
- [ ] Hidden motivation detection
- [ ] Sabotage scenario development

### Phase 4: Documentation and Reporting
- [ ] Findings compilation and validation
- [ ] Reproducibility harness creation
- [ ] Final report preparation
- [ ] Code and tool documentation

## 📁 Findings Format

Each vulnerability finding must include:

```json
{
  "finding_id": "unique_identifier",
  "title": "Vulnerability Title",
  "category": "deception|reward_hacking|sabotage|etc",
  "severity_score": 1-10,
  "breadth_score": 1-10,
  "description": "Detailed description",
  "reproduction_steps": ["step1", "step2", "..."],
  "prompts": ["prompt1", "prompt2", "..."],
  "expected_outputs": ["output1", "output2", "..."],
  "methodology": "Discovery process description",
  "impact_analysis": "Potential real-world impact",
  "mitigation_suggestions": "Proposed fixes or defenses"
}
```

## 🛠️ Tools and Scripts

- `src/models/gpt_oss_client.py` - Model interaction wrapper
- `src/testing/vulnerability_tester.py` - Automated testing framework
- `src/analysis/response_analyzer.py` - Output analysis tools
- `tools/finding_validator.py` - Findings format validator
- `tools/harness_generator.py` - Reproducibility harness creator

## 📈 Progress Tracking

See [docs/progress_log.md](docs/progress_log.md) for detailed progress updates.

### Current Status
- [x] Project setup and environment configuration
- [x] Documentation framework
- [ ] Model access setup
- [ ] Initial vulnerability testing
- [ ] Findings compilation

## 🤝 Contributing

This is a research project for the OpenAI Red-Teaming Challenge. All findings and methodologies will be shared with the research community.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for organizing the Red-Teaming Challenge
- The research community for existing red-teaming methodologies
- All contributing researchers and safety experts

## 📞 Contact

For questions or collaboration opportunities:
- GitHub: [@MHHamdan](https://github.com/MHHamdan)
- Project Repository: [Kaggle/gpt-oss-20b-red-teaming](https://github.com/MHHamdan/Kaggle)

---

*Last updated: January 2025*
