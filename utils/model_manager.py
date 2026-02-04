"""
Model management utilities for FastMLAPI integration.
"""

import subprocess
import socket
import json
import requests
import time
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


def find_free_port(start_port: int = 8000, max_attempts: int = 100) -> Optional[int]:
    """Find an available port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return None


def save_model_file(uploaded_file, custom_name: Optional[str] = None) -> Path:
    """
    Save uploaded .pkl file to models directory.

    Args:
        uploaded_file: Streamlit UploadedFile object
        custom_name: Optional custom name (without extension)

    Returns:
        Path to saved model file
    """
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    if custom_name:
        filename = f"{custom_name}.pkl"
    else:
        filename = uploaded_file.name

    model_path = models_dir / filename

    # Seek to beginning in case file was read before
    uploaded_file.seek(0)

    # Write binary data
    with open(model_path, 'wb') as f:
        f.write(uploaded_file.read())

    return model_path


def save_server_script(uploaded_file, model_name: str) -> Path:
    """
    Save uploaded server script to models/servers directory.

    Args:
        uploaded_file: Streamlit UploadedFile object
        model_name: Model name (without .pkl extension)

    Returns:
        Path to saved server script
    """
    models_dir = Path("models")
    servers_dir = models_dir / "servers"
    servers_dir.mkdir(parents=True, exist_ok=True)

    server_filename = f"model_{model_name}_server.py"
    server_path = servers_dir / server_filename

    with open(server_path, 'w', encoding='utf-8') as f:
        f.write(uploaded_file.getvalue().decode('utf-8'))

    return server_path


def save_base_request(uploaded_file, model_name: str) -> Path:
    """
    Save uploaded base request JSON to models/requests directory.

    Args:
        uploaded_file: Streamlit UploadedFile object
        model_name: Model name (without .pkl extension)

    Returns:
        Path to saved base request file
    """
    models_dir = Path("models")
    requests_dir = models_dir / "requests"
    requests_dir.mkdir(parents=True, exist_ok=True)

    request_filename = f"model_{model_name}_base_request.json"
    request_path = requests_dir / request_filename

    with open(request_path, 'w', encoding='utf-8') as f:
        f.write(uploaded_file.getvalue().decode('utf-8'))

    return request_path


def start_model_server(model_name: str, port: int) -> Tuple[Optional[int], bool, str]:
    """
    Start FastMLAPI server for a model.

    Args:
        model_name: Model name (without .pkl extension)
        port: Port to run server on

    Returns:
        Tuple of (process_id, success, error_message)
    """
    models_dir = Path("models")
    server_path = models_dir / "servers" / f"model_{model_name}_server.py"

    if not server_path.exists():
        return None, False, f"Server script not found: {server_path}"

    try:
        import os
        import sys

        # Set environment variable for port
        env = os.environ.copy()
        env['MODEL_PORT'] = str(port)
        env['MODEL_NAME'] = model_name

        # Create logs directory
        logs_dir = models_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

        log_file = logs_dir / f"model_{model_name}_{port}.log"
        error_log_file = logs_dir / f"model_{model_name}_{port}_error.log"

        # Open log files (don't close them - subprocess will write to them)
        stdout_log = open(log_file, 'w', buffering=1)  # Line buffered
        stderr_log = open(error_log_file, 'w', buffering=1)  # Line buffered

        # Start process in background without console window
        try:
            if hasattr(subprocess, 'CREATE_NO_WINDOW'):
                # Windows - hide console
                process = subprocess.Popen(
                    [sys.executable, str(server_path.absolute())],
                    stdout=stdout_log,
                    stderr=stderr_log,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    env=env,
                    cwd=str(models_dir.parent.absolute())
                )
            else:
                # Unix-like or fallback
                process = subprocess.Popen(
                    [sys.executable, str(server_path.absolute())],
                    stdout=stdout_log,
                    stderr=stderr_log,
                    env=env,
                    cwd=str(models_dir.parent.absolute())
                )
        except Exception as e:
            stdout_log.close()
            stderr_log.close()
            raise

        # Wait for server to start (check /health endpoint)
        max_retries = 20
        for i in range(max_retries):
            time.sleep(1)

            # Flush logs to ensure they're written
            stdout_log.flush()
            stderr_log.flush()

            try:
                response = requests.get(f"http://127.0.0.1:{port}/health", timeout=2)
                if response.status_code == 200:
                    # Keep log files open - the process is still writing to them
                    return process.pid, True, "Server started successfully"
            except requests.exceptions.RequestException:
                # Check if process is still alive
                if process.poll() is not None:
                    # Process died, flush and close logs, then read error log
                    stdout_log.flush()
                    stderr_log.flush()
                    stdout_log.close()
                    stderr_log.close()

                    time.sleep(0.5)  # Give filesystem time to sync

                    with open(error_log_file, 'r') as f:
                        error_content = f.read()
                    return process.pid, False, f"Process died. Error log:\n{error_content}"

                if i < max_retries - 1:
                    continue

        # Timeout - flush, close and read logs
        stdout_log.flush()
        stderr_log.flush()
        stdout_log.close()
        stderr_log.close()

        time.sleep(0.5)  # Give filesystem time to sync

        with open(error_log_file, 'r') as f:
            error_content = f.read()

        error_msg = f"Server failed to respond after {max_retries} seconds.\n"
        error_msg += f"Log file: {log_file}\n"
        error_msg += f"Error log: {error_log_file}\n"
        if error_content:
            error_msg += f"Errors:\n{error_content}"
        else:
            error_msg += "No errors in log (server may be starting slowly)"

        return process.pid, False, error_msg

    except Exception as e:
        return None, False, f"Exception starting server: {str(e)}"


def stop_model_server(pid: int) -> bool:
    """
    Stop a running model server.

    Args:
        pid: Process ID

    Returns:
        True if successfully stopped
    """
    try:
        import psutil
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=3)
        return True
    except Exception:
        return False


def check_server_health(port: int) -> bool:
    """
    Check if server is running and healthy.

    Args:
        port: Port to check

    Returns:
        True if server is healthy
    """
    try:
        response = requests.get(f"http://127.0.0.1:{port}/health", timeout=1)
        return response.status_code == 200
    except:
        return False


def make_prediction(port: int, base_request_path: Path, custom_data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Make a prediction request to the model server.

    Args:
        port: Server port
        base_request_path: Path to base request JSON
        custom_data: Optional custom data to override base request

    Returns:
        Response dictionary
    """
    try:
        # Load base request
        with open(base_request_path, 'r') as f:
            payload = json.load(f)

        # Override with custom data if provided
        if custom_data:
            payload.update(custom_data)

        # Make request
        url = f"http://127.0.0.1:{port}/predict"
        response = requests.post(url, json=payload, timeout=10)

        return {
            'success': response.status_code == 200,
            'status_code': response.status_code,
            'data': response.json() if response.status_code == 200 else None,
            'error': response.text if response.status_code != 200 else None
        }

    except Exception as e:
        return {
            'success': False,
            'status_code': None,
            'data': None,
            'error': str(e)
        }


def update_base_request(model_name: str, new_data: Dict) -> bool:
    """
    Update base request JSON file.

    Args:
        model_name: Model name
        new_data: New request data

    Returns:
        True if successful
    """
    try:
        request_path = Path("models") / "requests" / f"model_{model_name}_base_request.json"
        with open(request_path, 'w') as f:
            json.dump(new_data, f, indent=2)
        return True
    except Exception:
        return False


def delete_model(model_name: str, pid: Optional[int] = None) -> bool:
    """
    Delete model and all associated files.

    Args:
        model_name: Model name
        pid: Optional process ID to stop

    Returns:
        True if successful
    """
    try:
        # Stop server if running
        if pid:
            stop_model_server(pid)

        # Delete files
        models_dir = Path("models")
        files_to_delete = [
            models_dir / f"{model_name}.pkl",
            models_dir / "servers" / f"model_{model_name}_server.py",
            models_dir / "requests" / f"model_{model_name}_base_request.json"
        ]

        for file_path in files_to_delete:
            if file_path.exists():
                file_path.unlink()

        return True

    except Exception:
        return False


def get_available_models() -> list:
    """
    Get list of available models.

    Returns:
        List of model names (without .pkl extension)
    """
    models_dir = Path("models")
    if not models_dir.exists():
        return []

    pkl_files = models_dir.glob("*.pkl")
    # Filter out models that start with "model_" (those are generated)
    return [f.stem for f in pkl_files if not f.stem.startswith("model_")]


def get_model_logs(model_name: str, port: int) -> Dict[str, str]:
    """
    Get stdout and stderr logs for a model.

    Args:
        model_name: Model name
        port: Port the model is/was running on

    Returns:
        Dictionary with 'stdout' and 'stderr' keys
    """
    models_dir = Path("models")
    logs_dir = models_dir / "logs"

    log_file = logs_dir / f"model_{model_name}_{port}.log"
    error_log_file = logs_dir / f"model_{model_name}_{port}_error.log"

    result = {
        'stdout': '',
        'stderr': '',
        'stdout_exists': log_file.exists(),
        'stderr_exists': error_log_file.exists()
    }

    if log_file.exists():
        with open(log_file, 'r') as f:
            result['stdout'] = f.read()

    if error_log_file.exists():
        with open(error_log_file, 'r') as f:
            result['stderr'] = f.read()

    return result


__all__ = [
    'find_free_port',
    'save_model_file',
    'save_server_script',
    'save_base_request',
    'start_model_server',
    'stop_model_server',
    'check_server_health',
    'make_prediction',
    'update_base_request',
    'delete_model',
    'get_available_models',
    'get_model_logs',
]

