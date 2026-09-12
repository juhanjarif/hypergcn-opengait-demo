# HyperGCN & OpenGait Dashboard

- **HyperGCN**, Human Action Recognition from video streams
- **OpenGait**, Gait Silhouette Extraction, 1-vs-1 Verification, and 1-vs-N Identification

---

## Prerequisites

- Python 3.9+
- `pip` and `venv`
- for macOS/Linux, use `source venv/bin/activate`
- on Windows, use `venv\Scripts\activate`

---

## Setup for the First Time

### 1. Clone the repository

```bash
git clone git@github.com:juhanjarif/hypergcn-opengait-demo.git
```
or,
```bash
git clone https://github.com/juhanjarif/hypergcn-opengait-demo.git
```

then go to the folder.
```bash
cd hypergcn-opengait-demo
```

### 2. Create virtual environments and install dependencies

#### HyperGCN

**macOS/Linux:**
```bash
cd hypergcn
python3 -m venv hypergcn_venv
source hypergcn_venv/bin/activate
pip install -r demo-requirements.txt
deactivate
cd ..
```

**Windows (PowerShell):**
```powershell
cd hypergcn
python -m venv hypergcn_venv
.\hypergcn_venv\Scripts\Activate.ps1
pip install -r demo-requirements.txt
deactivate
cd ..
```

(use weights from Google Drive link provided in `hypergcn/README.md` folder)

#### OpenGait

**macOS/Linux:**
```bash
cd opengait
python3 -m venv opengait_venv
source opengait_venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
```

**Windows (PowerShell):**
```powershell
cd opengait
python -m venv opengait_venv
.\opengait_venv\Scripts\Activate.ps1
pip install -r requirements.txt
deactivate
cd ..
```

(use weights from Google Drive link provided in `opengait/README.md` folder)

#### Dashboard

**macOS/Linux:**
```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
```

**Windows (PowerShell):**
```powershell
cd frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
deactivate
cd ..
```

---

## Running a Single Submodule

Run only one submodule directly without the unified frontend.

### HyperGCN

**macOS/Linux:**
```bash
cd hypergcn
source hypergcn_venv/bin/activate
python app.py
```

**Windows (PowerShell):**
```powershell
cd hypergcn
.\hypergcn_venv\Scripts\Activate.ps1
python app.py
```

Then open `http://127.0.0.1:1234` in your browser.

### OpenGait

**macOS/Linux:**
```bash
cd opengait
source opengait_venv/bin/activate
python app.py
```

**Windows (PowerShell):**
```powershell
cd opengait
.\opengait_venv\Scripts\Activate.ps1
python app.py
```

Then open `http://127.0.0.1:7860` in your browser.

---

## Running the Unified Frontend
From the project root:

```bash
python run.py
```

This starts both submodules in the background and opens the master UI at `http://127.0.0.1:7800`.

---

## Notes

- If PowerShell blocks script execution, run this first:
  ```powershell
  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
  ```
- If you see `python: command not found`, try `py` instead of `python`.
- If ports `1234`, `7860`, or `7800` are already in use, stop the conflicting process or change the port in the respective `app.py` file.

---

## Team Members

- **[Juhan Ahmed Jarif](https://github.com/juhanjarif)**, 220041214
- **[Aakash Abdullah Siddhartha](https://github.com/Arceus-221)**, 220041221
- **[Tanvir Mahmud Hossain](https://github.com/tamajose)**, 220041253

---