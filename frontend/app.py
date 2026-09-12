import os
import sys
import socket

try:
    import gradio as gr
except ImportError:
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from launcher import ensure_services_running

HYPERGCN_PORT = 1234
OPENGAIT_PORT = 7860

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');

body, html, .gradio-container, .dark {
    background-color: #0b0f19 !important;
    font-family: 'Montserrat', sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    max-width: 100% !important;
    overflow-x: hidden;
    color: #ffffff !important;
}

footer, .footer, .show-api, [class*="footer"], a[href*="gradio.app"], a[href*="/api"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
}

.gradio-container .main, .block, .contain {
    max-width: 100% !important;
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
    background-color: transparent !important;
}

.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 10px 24px;
    background: transparent;
}

.top-bar .brand {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.02em;
}

.tabs {
    border-bottom: 1px solid rgba(255, 255, 255, 0.15) !important;
    padding-left: 10px !important;
    background: transparent !important;
}

button[role="tab"] {
    font-family: 'Montserrat', sans-serif !important;
    color: #94a3b8 !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 12px 24px !important;
    border-radius: 0 !important;
    transition: all 0.2s ease !important;
}

button[role="tab"]:hover {
    color: #e2e8f0 !important;
}

button[role="tab"][aria-selected="true"] {
    background: transparent !important;
    color: #4f46e5 !important;
    border-bottom: 3px solid #4f46e5 !important;
    font-weight: 700 !important;
}

.iframe-container {
    width: 100% !important;
    height: calc(100vh - 120px);
    min-height: 850px;
    border: 1px solid #1e293b;
    border-radius: 12px;
    background: #111827;
    display: block;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    margin-top: 10px;
}
"""

def create_iframe_html(port, path=""):
    url = f"http://127.0.0.1:{port}{path}"
    return f"""
    <iframe src="{url}" class="iframe-container"></iframe>
    """

og_theme = gr.themes.Default(
    primary_hue="indigo",
    secondary_hue="slate",
    font=gr.themes.GoogleFont("Montserrat"),
).set(
    body_background_fill="#0b0f19",
    body_text_color="#ffffff",
    block_background_fill="#111827",
    block_border_color="#1e293b",
)

try:
    master_demo = gr.Blocks(theme=og_theme, title="HyperGCN & OpenGait", css=custom_css, fill_width=True)
except TypeError:
    try:
        master_demo = gr.Blocks(theme=og_theme, title="HyperGCN & OpenGait", css=custom_css)
    except TypeError:
        master_demo = gr.Blocks(theme=og_theme, title="HyperGCN & OpenGait")

with master_demo:
    with gr.Column(elem_classes=["full-width-col"]):
        gr.HTML("""
        <div class="top-bar">
            <div class="brand">HyperGCN &amp; OpenGait Dashboard</div>
        </div>
        """)

        with gr.Tabs(selected=0) as tabs:
            with gr.TabItem("Hyper-GCN Action Recognition", id=0):
                gr.HTML(create_iframe_html(HYPERGCN_PORT))

            with gr.TabItem("OpenGait Gait Analysis", id=1):
                gr.HTML(create_iframe_html(OPENGAIT_PORT))

if __name__ == "__main__":
    print("Launching Submodule Background Services...")
    h_ok, g_ok = ensure_services_running(ROOT_DIR)
    print(f"[Status] Hyper-GCN on port {HYPERGCN_PORT}: {'RUNNING' if h_ok else 'FAILED TO START'}")
    print(f"[Status] OpenGait on port {OPENGAIT_PORT}: {'RUNNING' if g_ok else 'FAILED TO START'}")

    print("Starting main dashboard on http://127.0.0.1:7800")
    try:
        master_demo.launch(server_name="127.0.0.1", server_port=7800, share=False, css=custom_css, show_api=False)
    except TypeError:
        master_demo.launch(server_name="127.0.0.1", server_port=7800, share=False, show_api=False)