# Unified Frontend for HyperGCN & OpenGait

This directory contains the unified Gradio dashboard for both `hypergcn` and `opengait` submodules.

## Setup Instructions

### 1. Install dashboard UI Requirements & Run
Install requirements for the frontend dashboard UI:

```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the unified interface from the root directory:

```bash
python run.py
```

### How It Works
- The background launcher (`frontend/launcher.py`) automatically detects `hypergcn/hypergcn_venv` and `opengait/opengait_venv`.
- It starts `hypergcn/app.py` on `http://127.0.0.1:1234` and `opengait/app.py` on `http://127.0.0.1:7860` in background processes.
- It opens the dashboard Gradio UI on `http://127.0.0.1:7800`.