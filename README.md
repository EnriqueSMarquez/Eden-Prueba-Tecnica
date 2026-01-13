# Eden Prueba Tecnica

Este README fue generado usando el asistente de Antigravity

Para información detallada, chain of thought, etc, ver el reporte pdf en la raiz de este repositorio

## Start of README

This repository contains the code for the Eden Technical Test, focusing on evaluating Google's Gemini models for generating medical reports from medical images (converted from DICOM to JPG).

The project is structured into three main scenarios, each testing different capabilities:
1.  **Baseline**: Standard report generation.
2.  **Personalization**: Adapting reports to specific doctor styles.
3.  **Multiple Images**: Generating reports from studies with multiple images.

## Setup

This project uses `uv` for dependency management and execution.

### Prerequisites

-   Install [uv](https://github.com/astral-sh/uv).

### Installation

1.  **Sync dependencies**:
    ```bash
    uv sync
    ```

2.  **Install the package in editable mode**:
    ```bash
    uv pip install -e .
    ```

    Alternatively, you can run the provided setup script:
    ```bash
    ./setup.sh
    ```

### Configuration (.env)

You **must** create a `.env` file in the root directory of the project. This file is used to store your API keys and configuration.

Reference variables:
```env
GEMINI_API_KEY=<your_gemini_api_key>
GEMINI_MODEL=gemini-2.0-flash-exp
```

> **Note**: The code expects `GEMINI_MODEL` to be defined in your `.env` file as well.

## Project Structure

-   `src/`: Core Python package containing:
    -   `system_instructions/`: Prompts and system instructions for Gemini.
    -   `utils/`: Helper modules (Gemini client, configuration, text processing).
-   `escenario1-baseline/`: Code for the baseline scenario.
-   `escenario2-personalizacion-por-medico/`: Code for doctor-specific personalization.
-   `escenario3-multiples-imagenes-por-estudio/`: Code for multi-image studies.

## Usage

You can execute the scripts using `uv run`. Below are the details for each scenario.

### Escenario 1: Baseline

Located in `escenario1-baseline/`.

**Scripts:**

-   `generate_reports_and_metrics.py`: Generates medical reports for the dataset and calculates metrics (JSON structure match and text similarity).

    **Usage:**
    ```bash
    uv run escenario1-baseline/generate_reports_and_metrics.py \
      --images-path /path/to/images \
      --metadata-path /path/to/metadata.csv \
      --output-path /path/to/output.csv \
      [--metrics all|metric1|metric2] \
      [--temperature 0.0]
    ```

**Notebooks:**
-   `notebooks/general-notebook.ipynb`: Jupyter notebook for dataset derivation and result analysis.

### Escenario 2: Personalization (Style Transfer)

Located in `escenario2-personalizacion-por-medico/`.

**Scripts:**

-   `generate_reports_and_metrics.py`: Generates reports that attempt to mimic the style and preferences extracted from the ground truth.

    **Usage:**
    ```bash
    uv run escenario2-personalizacion-por-medico/generate_reports_and_metrics.py \
      --images-path /path/to/images \
      --metadata-path /path/to/metadata.csv \
      --output-path /path/to/output.csv \
      [--metrics all|metric1|metric2]
    ```

-   `generate_difference_in_reports.py`: Compares reports pairwise to identify differences in style or content between different "medics" (cases).

    **Usage:**
    ```bash
    uv run escenario2-personalizacion-por-medico/generate_difference_in_reports.py \
      --metadata-path /path/to/metadata.csv \
      --output-path /path/to/output.json
    ```

**Notebooks:**
-   `notebooks/general-notebook.ipynb`: Jupyter notebook for dataset derivation and result analysis.

### Escenario 3: Multiple Images

Located in `escenario3-multiples-imagenes-por-estudio/`.

**Scripts:**

-   `generate_reports_and_metrics.py`: Generates reports for studies that contain multiple images. It groups the input metadata by `report_id`.

    **Usage:**
    ```bash
    uv run escenario3-multiples-imagenes-por-estudio/generate_reports_and_metrics.py \
      --images-path /path/to/images \
      --metadata-path /path/to/metadata.csv \
      --output-path /path/to/output.csv \
      [--one-random-image]
    ```
    -   `--one-random-image`: If set, selects only one random image from the study instead of using all valid images.

**Notebooks:**
-   `notebooks/general-notebook.ipynb`: Jupyter notebook for dataset derivation and result analysis.

## Development

-   **Adding Dependencies**: Use `uv add <package>`.
-   **Running Notebooks**:
    ```bash
    uv run jupyter notebook
    ```
    Ensure you are in the root directory so the `src` package is correctly resolved (as configured in `pyproject.toml`).
