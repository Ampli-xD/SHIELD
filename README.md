# SHIELD: System for Harmful explicit-content Identification and Evaluation through LLM-Driven approach

A content analysis pipeline with vector‐based similarity scoring and LLM‐based classification.  
It ingests text, image, audio and video data, assigns serial IDs, checks for corruption, scores content across 15 sensitive categories, and visualizes results in a Streamlit dashboard.

## Features

- Scrape or upload files (images, audio, video, text).
- Integrity checks via [`Engine/Spare/Corruption.py`](Engine/Spare/Corruption.py).
- Preprocessing of audio/video in [`Engine/PreProcessors`](Engine/PreProcessors/).
- LLM scoring via [`Engine/LLMHandler/MultiSetLLMScoring.py`](Engine/LLMHandler/MultiSetLLMScoring.py).
- Vector scoring via [`Engine/VectorHandler/VectorScoring.py`](Engine/VectorHandler/VectorScoring.py).
- Combine LLM & vector results in [`Engine/Launcher/LauncherMain.py`](Engine/Launcher/LauncherMain.py).
- Interactive Streamlit dashboard in [`Engine/Launcher/StreamLitLauncher.py`](Engine/Launcher/StreamLitLauncher.py).

## Installation

```sh
pip install .
```

## Quick Start

0. Firstly, setup ChromaDB HTTP server & and use the collection creator in [`Engine/VectorHandler/`](Engine/VectorHandler/) to create the collection to be used for semantic searching.
1. Prepare your data folder or use file uploader in Streamlit.
2. Run the dashboard:
    ```sh
    streamlit run Engine/Launcher/StreamLitLauncher.py
    ```
3. Upload files or process a folder, then click **Start Analysis**.

## Documentation

See the [docs](docs/) folder for architecture, module reference, usage examples, and contribution guidelines.

### Files in `docs` folder

- [`docs/Architecture.md`](docs/architecture.md)
- [`docs/ModuleReference.md`](docs/modules.md)
- [`docs/UsageExamples.md`](docs/usage.md)
- [`docs/ContributionGuidelines.md`](CONTRIBUTING.md)
