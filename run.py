#!/usr/bin/env python3
import os
import sys

try:
    import gradio as gr
except ImportError:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    candidate_pythons = [
        os.path.join(ROOT_DIR, "hypergcn", "hypergcn_venv", "bin", "python"),
        os.path.join(ROOT_DIR, "hypergcn", "hypergcn_venv", "Scripts", "python.exe"),
        os.path.join(ROOT_DIR, "opengait", "opengait_venv", "bin", "python"),
        os.path.join(ROOT_DIR, "opengait", "opengait_venv", "Scripts", "python.exe"),
    ]
    reexec_python = None
    for py in candidate_pythons:
        if os.path.exists(py):
            reexec_python = py
            break

    if reexec_python and os.environ.get("AUTO_REEXEC_DONE") != "1":
        os.environ["AUTO_REEXEC_DONE"] = "1"
        os.execv(reexec_python, [reexec_python] + sys.argv)

    else:
        print("[Launcher] Error: 'gradio' module not found.")
        print("Please install gradio (`pip install gradio`) or setup submodules' venvs.")
        sys.exit(1)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

from launcher import ensure_services_running

if __name__ == "__main__":
    print("=" * 60)
    print("  Starting HyperGCN & OpenGait")
    print("=" * 60)

    h_ok, g_ok = ensure_services_running(ROOT_DIR)
    print(f"[Status] Hyper-GCN on port 1234: {'RUNNING' if h_ok else 'FAILED TO START'}")
    print(f"[Status] OpenGait on port 7860: {'RUNNING' if g_ok else 'FAILED TO START'}")

    from app import master_demo
    master_demo.launch(server_name="127.0.0.1", server_port=7800, share=False)