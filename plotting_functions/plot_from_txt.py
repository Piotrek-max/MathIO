import io
import os
import uuid
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

def _normalize_text(text: str) -> str:
    cleaned = []
    for line in text.splitlines():
        if "," in line and (" " not in line and "\t" not in line):
            line = line.replace(",", " ")
        cleaned.append(line)
    return "\n".join(cleaned)


def parse_xy_from_text(raw_bytes: bytes, filename: str) -> tuple[np.ndarray, np.ndarray, str]:
    try:
        text = raw_bytes.decode("utf-8", errors="ignore")
    except Exception:
        raise ValueError("Can`t decode as UTF-8.")

    text = _normalize_text(text)

    try:
        data = np.loadtxt(io.StringIO(text))
    except Exception:
        raise ValueError("Wrong format of data in the file.")

    if data.ndim == 1:
        y = data.astype(float)
        x = np.arange(len(y), dtype=float)
    elif data.ndim == 2 and data.shape[1] >= 2:
        x = data[:, 0].astype(float)
        y = data[:, 1].astype(float)
    else:
        raise ValueError("Expected 1 (y) or 2 (x y) columns.")

    if len(x) < 2:
        raise ValueError("To small amount of data points.")

    title = filename or "Plot"
    return x, y, title


def save_plot_png(x: np.ndarray, y: np.ndarray, title: str, out_dir: str) -> str:
    os.makedirs(out_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, y, linewidth=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()

    out_name = f"{uuid.uuid4().hex}.png"
    out_path = os.path.join(out_dir, out_name)

    fig.savefig(out_path, format="png", dpi=150)
    plt.close(fig)

    return out_name
