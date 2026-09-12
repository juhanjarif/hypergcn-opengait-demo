import os
import sys
import time
import socket
import subprocess
import signal
import atexit

processes = []
tracked_ports = []

def get_venv_python(submodule_dir, venv_name):
    possible_paths = [
        os.path.join(submodule_dir, venv_name, "bin", "python"),
        os.path.join(submodule_dir, venv_name, "Scripts", "python.exe"),
        os.path.join(submodule_dir, "venv", "bin", "python"),
        os.path.join(submodule_dir, ".venv", "bin", "python"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return sys.executable

def is_port_in_use(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def kill_process_on_port(port):
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        pids = [pid.strip() for pid in result.stdout.strip().split("\n") if pid.strip()]
        for pid in pids:
            try:
                os.kill(int(pid), signal.SIGTERM)
                print(f"[Cleanup] Killed process {pid} on port {port}")
            except ProcessLookupError:
                pass
            except Exception as e:
                print(f"[Cleanup] Error killing PID {pid}: {e}")
    except Exception as e:
        print(f"[Cleanup] Error finding process on port {port}: {e}")

def cleanup_subprocesses():
    print("\n[Cleanup] Shutting down submodule services")

    for proc in processes:
        if proc.poll() is None:
            try:
                proc.terminate()
                proc.wait(timeout=2)
                print(f"[Cleanup] Terminated subprocess PID {proc.pid}")
            except Exception:
                try:
                    proc.kill()
                    print(f"[Cleanup] Killed subprocess PID {proc.pid}")
                except Exception:
                    pass

    for port in tracked_ports:
        if is_port_in_use(port):
            kill_process_on_port(port)

    print("[Cleanup] Done.")

def signal_handler(signum, frame):
    cleanup_subprocesses()
    sys.exit(0)

atexit.register(cleanup_subprocesses)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def launch_submodule(name, script_path, target_port, default_venv):
    submodule_dir = os.path.dirname(script_path)

    if is_port_in_use(target_port):
        print(f"[{name}] Already running on port {target_port}.")
        tracked_ports.append(target_port)
        return True

    python_bin = get_venv_python(submodule_dir, default_venv)
    print(f"[{name}] Starting via Python ({python_bin}) on port {target_port}...")

    try:
        proc = subprocess.Popen(
            [python_bin, os.path.basename(script_path)],
            cwd=submodule_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        processes.append(proc)
        tracked_ports.append(target_port)

        for _ in range(30):
            time.sleep(0.5)
            if is_port_in_use(target_port):
                print(f"[{name}] Successfully started on http://127.0.0.1:{target_port}")
                return True
            if proc.poll() is not None:
                out, _ = proc.communicate()
                print(f"[{name}] Process exited prematurely with code {proc.returncode}.\nOutput:\n{out[:500] if out else ''}")
                tracked_ports.remove(target_port)
                processes.remove(proc)
                return False

        print(f"[{name}] Warning: Process started but port {target_port} isn't responding yet. Will continue loading UI.")
        return True

    except Exception as e:
        print(f"[{name}] Error starting subprocess: {e}")
        return False

def ensure_services_running(root_dir=None):
    if root_dir is None:
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    hypergcn_script = os.path.join(root_dir, "hypergcn", "app.py")
    opengait_script = os.path.join(root_dir, "opengait", "app.py")

    print("\n--- Initializing Submodule Services ---")
    hypergcn_ok = launch_submodule("HyperGCN", hypergcn_script, 1234, "hypergcn_venv")
    opengait_ok = launch_submodule("OpenGait", opengait_script, 7860, "opengait_venv")
    print("----------------------------------------\n")

    return hypergcn_ok, opengait_ok

if __name__ == "__main__":
    ensure_services_running()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup_subprocesses()