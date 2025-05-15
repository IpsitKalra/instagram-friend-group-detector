# Instagram Friend‑Group Detector

## Overview

Instagram Friend‑Group Detector is a command‑line utility that analyses the social graph of a personal Instagram account. It clusters followees into cohesive communities using the Louvain method and identifies bridge accounts through betweenness centrality. The tool runs entirely on the client machine; no data is transmitted to external servers.

## Features

* Authenticates locally; two‑factor verification is required only on the first run.
* Scrapes the first‑order follow graph and stores responses in a SQLite cache to minimise repeated API calls.
* Applies Louvain community detection to discover friend‑group “bubbles”.
* Computes betweenness centrality to pinpoint users who connect multiple communities.
* Produces:

  * `bridges.txt` — human‑readable list of bridge users.
  * `network.gml` — Gephi‑compatible file for visual analysis.

## Prerequisites

| macOS                | Windows                                        |
| -------------------- | ---------------------------------------------- |
| macOS 12 or later    | Windows 10 or 11                               |
| Homebrew             | Python 3.11 from python.org or Microsoft Store |
| Git (for cloning)    | Git (optional)                                 |
| An Instagram account | An Instagram account                           |

## Installation and Setup

### macOS

```bash
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Obtain the source
git clone https://github.com/<user>/instagram-friend-group-detector.git
cd instagram-friend-group-detector

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
# Verify Python installation
python --version   # should report 3.11.x

# Create project directory
cd $HOME\Desktop
mkdir insta-graph
cd insta-graph

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

# Install required packages
pip install instagrapi networkx python-louvain tqdm pillow

# Download the script
Invoke-WebRequest -Uri https://raw.githubusercontent.com/<user>/instagram-friend-group-detector/main/friend_groups.py -OutFile friend_groups.py
```

If `Activate.ps1` is blocked, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

for the current session.

## Usage

```bash
python friend_groups.py
```

During the first run, supply the Instagram username, password, and two‑factor authentication code. Subsequent runs reuse `session.json` and operate unattended.

A typical initial crawl of approximately 1 000 followees completes in 30–45 minutes. Later executions are faster because cached data are reused.

## Configuration

Adjust the following parameters in `friend_groups.py` as needed.

| Parameter                                 | Purpose                                 | Typical Range |
| ----------------------------------------- | --------------------------------------- | ------------- |
| `amount` in `cl.user_following`           | Number of followees sampled per account | 40–100        |
| Betweenness threshold (`if score > 0.05`) | Sensitivity of bridge detection         | 0.03–0.08     |
| Delay between requests (`time.sleep`)     | Rate‑limit protection                   | 2–8 s         |

## Troubleshooting

| Issue                         | Likely Cause                                         | Resolution                                       |
| ----------------------------- | ---------------------------------------------------- | ------------------------------------------------ |
| `FeedbackRequired` exception  | Instagram rate‑limit                                 | Wait 30 minutes, reduce `amount`, increase delay |
| `ModuleNotFoundError: Pillow` | Pillow package not installed                         | `pip install pillow`                             |
| NetworkX import stalls        | Local `networkx` directory shadows installed package | Remove the stray directory; reinstall NetworkX   |

## Contact

Questions and contributions are welcome. Please open an issue or pull request in the repository.
