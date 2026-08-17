# Enterprise LLM Orchestrator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![SDK: Google GenAI](https://img.shields.io/badge/SDK-Google%20GenAI-blue.svg)](https://pypi.org/project/google-genai/)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)

An open-source CLI framework and LLM orchestration wrapper built with Python and the Google GenAI SDK. It executes deterministic prompt schemas, enforces schema validation, and manages context windows for enterprise workflows.

---

## Project Structure

```text
enterprise-llm-orchestrator/
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── main.py
├── requirements.txt
├── engines/
│   ├── analyzer.md
│   ├── goal.md
│   ├── mimic.md
│   └── perfection.md
└── utilities/
    ├── handoff.md
    └── system_hotpatch.md
