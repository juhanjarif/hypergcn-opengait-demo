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

### 2. Initialize submodules

```bash
git submodule update --init --recursive
```

### 3. Create virtual environments and install dependencies

#### HyperGCN

```bash
cd hypergcn
python3 -m venv hypergcn_venv
source hypergcn_venv/bin/activate
pip install -r demo-requirements.txt
deactivate
cd ..
```
(use weights from Google Drive link provided in `hypergcn/README.md` folder)

#### OpenGait

```bash
cd opengait
python3 -m venv opengait_venv
source opengait_venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
```
(use weights from Google Drive link provided in `opengait/README.md` folder)

#### Dashboard

```bash
cd frontend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..
```

---

## Running a Single Submodule

Run only one submodule directly without the unified frontend.

### HyperGCN

```bash
cd hypergcn
source hypergcn_venv/bin/activate
python app.py
deactivate
```

Then open `http://127.0.0.1:1234` in your browser.

### OpenGait

```bash
cd opengait
source opengait_venv/bin/activate
python app.py
deactivate
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

## Team Members

- **[Juhan Ahmed Jarif](https://github.com/juhanjarif)**, 220041214
- **[Aakash Abdullah Siddhartha](https://github.com/Arceus-221)**, 220041221
- **[Tanvir Mahmud Hossain](https://github.com/tamajose)**, 220041253

---