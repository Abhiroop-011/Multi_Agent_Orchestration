# 🤖 Declarative Multi-Agent Orchestration Engine

> **"Infrastructure-as-Code" for AI Agents.**
> Define complex multi-agent workflows using simple YAML configuration files—no complex coding required.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📖 Overview

Building multi-agent systems is often brittle and code-heavy. This engine solves that problem by separating **Logic** (Python) from **Configuration** (YAML).

It allows you to spin up teams of AI agents that can work **sequentially**, **in parallel**, or **conditionally** (loops/routing) just by editing a text file. It supports **Tool Use** (running Python code) and **Hierarchical Delegation** (Manager -> Worker) out of the box.

---

## ✨ Key Features

* **📄 Declarative Syntax:** Define agents, roles, and workflows in clean YAML.
* **⚡ Parallel Execution:** Run multiple agents simultaneously using thread pools.
* **🧠 Intelligent Routing:** Agents can dynamically decide to retry tasks or branch to different steps based on output (Conditional Logic).
* **🛠️ Tool-Enabled:** Agents can write and execute **Python code** safely to solve math/logic problems.
* ** hierarchy:** Supports "Manager" agents that can delegate sub-tasks to specialists.
* **🎨 Rich UI:** Enterprise-grade console output with spinners, markdown rendering, and syntax highlighting.
* **✅ Type Safety:** Built on **Pydantic** for strict schema validation—catches config errors before execution.

---

## 🚀 Installation & Setup

### 1. Clone & Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt