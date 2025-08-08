# Project Links and Resources

## GitHub Repository
**Main Project**: https://github.com/MHHamdan/Kaggle/tree/main/gpt-oss-20b-red-teaming

## Project Structure
```
gpt-oss-20b-red-teaming/
├── src/                    # Core framework code
│   ├── models/            # GPT-OSS client implementation
│   └── submission/        # Kaggle submission tools
├── findings/              # Vulnerability findings (JSON)
├── docs/                  # Documentation and writeups
├── notebooks/             # Jupyter analysis notebooks
├── tests/                 # Test suites
└── tools/                 # Red-teaming utilities
```

## Key Components

### 🔧 Automated Testing Framework
- **GPT-OSS Client**: `src/models/gpt_oss_client.py`
- **Submission System**: `src/submission/kaggle_submitter.py`
- **Direct Submit Tool**: `direct_submit.py`

### 📊 Analysis Notebooks
- **Model Exploration**: `notebooks/01_model_exploration.ipynb`
- **Vulnerability Testing**: Interactive testing environment
- **Results Analysis**: Automated evaluation and scoring

### 🔍 Findings and Evidence
- **JSON Findings**: Structured vulnerability reports
- **Reproduction Scripts**: Automated verification tools
- **Evidence Files**: Supporting data and logs

## Reproducibility
All findings can be reproduced using:
```bash
python direct_submit.py --check-status
python quick_test.py
```

## Dependencies
See `requirements.txt` for complete Python environment setup.

## Contact
Mohammed Hamdan - AI/ML Engineer
GitHub: @MHHamdan
