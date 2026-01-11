import pandas as pd
import argparse
from tqdm import tqdm
from PIL import Image
from loguru import logger
import traceback
import json
from src.utils.config import config
from src.utils.gemini import GeminiClient
from src.utils.html_handling import clean_html
from src.system_instructions.escenario2_personalizacion_por_medico import (
    system_instruction_compare_two_medics,
)


def main(args):
    logger.info(f"Starting report generation with args: {args}")

    logger.info(f"Loading dataset from {args.metadata_path}")
    dataset_metadata = pd.read_csv(args.metadata_path)
    logger.info(f"Dataset loaded. Total records: {len(dataset_metadata)}")

    # Preprocess text
    dataset_metadata["cleaned_text"] = dataset_metadata["field_value"].apply(clean_html)

    logger.info(f"Initializing Gemini Client with model: {config['GEMINI_MODEL']}")
    gemini = GeminiClient(config["GEMINI_API_KEY"], config["GEMINI_MODEL"])

    # For loop para generar reporte, y calcular metricas
    results_matrix = {}
    logger.info("Starting processing loop...")
    progress_bar = tqdm(dataset_metadata.iterrows(), total=len(dataset_metadata))
    for case_id, case_row in progress_bar:
        progress_bar2 = tqdm(
            dataset_metadata.loc[dataset_metadata.index[case_id::]].iterrows(),
            total=len(dataset_metadata),
            leave=False,
        )
        progress_bar.set_description(f"Processing Case {case_id}")
        clean_text1 = case_row["cleaned_text"]
        for case_id2, case_row2 in progress_bar2:
            progress_bar2.set_description(f"Processing Case {case_id2}")
            if case_id == case_id2:
                continue
            clean_text2 = case_row2["cleaned_text"]
            try:
                prompt = f"MEDIC A:\n{clean_text1}\nMEDIC B:\n{clean_text2}\n"
                result = gemini.predict(
                    system_instruction_compare_two_medics,
                    prompt,
                    args.temperature,
                    None,
                )
                results_matrix[f"{case_id}_{case_id2}"] = result
            except Exception as e:
                logger.error(f"Error processing case {case_id}: {e}")
                traceback.print_exc()
                continue

    logger.info(f"Saving results to {args.output_path}")
    with open(args.output_path, "w") as f:
        json.dump(results_matrix, f)
    logger.success("Process finished successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate report")
    parser.add_argument(
        "--metadata-path", type=str, required=True, help="Path to metadata"
    )
    parser.add_argument("--output-path", type=str, required=True, help="Path to output")
    parser.add_argument(
        "--temperature", type=float, default=0.0, help="Temperature for Gemini"
    )
    args = parser.parse_args()

    main(args)
