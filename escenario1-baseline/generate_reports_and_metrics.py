import pandas as pd
import argparse
import os
from tqdm import tqdm
from PIL import Image
from loguru import logger
import traceback
from src.utils.config import config
from src.utils.gemini import GeminiClient
from src.utils.html_handling import clean_html
from src.system_instructions.escenario1_baseline import (
    system_instruction_report_generator,
    system_instruction_text_to_text_comparison,
    system_instruction_text_json_normalizer,
    system_instruction_jsons_comparison,
)


def metric1_prompt_merge(ground_truth, generated):
    return f"""    
    - Ground Truth JSON: 
    {ground_truth}
    - Generated JSON:
    {generated}
    """


def metric2_prompt_merge(ground_truth, generated):
    return f"""    
    - Ground Truth Text: 
    {ground_truth}
    - Generated Text:
    {generated}
    """


def main(args):
    logger.info(f"Starting report generation with args: {args}")

    logger.info(f"Loading dataset from {args.metadata_path}")
    dataset_metadata = pd.read_csv(args.metadata_path)
    logger.info(f"Dataset loaded. Total records: {len(dataset_metadata)}")

    logger.info(f"Loading images from {args.images_path}")

    # Preprocess text
    dataset_metadata["cleaned_text"] = dataset_metadata["field_value"].apply(clean_html)

    logger.info(f"Initializing Gemini Client with model: {config['GEMINI_MODEL']}")
    gemini = GeminiClient(config["GEMINI_API_KEY"], config["GEMINI_MODEL"])

    # For loop para generar reporte, y calcular metricas
    dataset_metadata["generated_report"] = None
    use_metric1 = args.metrics == "all" or args.metrics == "metric1"
    use_metric2 = args.metrics == "all" or args.metrics == "metric2"

    if use_metric1:
        logger.info("Metric 1 enabled")
        dataset_metadata["metric1_json_generated"] = None
        dataset_metadata["metric1_json_real"] = None
        dataset_metadata["metric1_json_result"] = None

    if use_metric2:
        logger.info("Metric 2 enabled")
        dataset_metadata["metric2_json_result"] = None

    logger.info("Starting processing loop...")
    progress_bar = tqdm(dataset_metadata.iterrows(), total=len(dataset_metadata))
    for case_id, case_row in progress_bar:
        progress_bar.set_description(f"Processing Case {case_id}")
        try:
            image_path = os.path.join(
                args.images_path, case_row["file_url"].replace("dcm", "jpg")
            )
            if not os.path.exists(image_path):
                logger.warning(
                    f"Image not found at {image_path}, skipping case {case_id}"
                )
                continue

            image = Image.open(image_path)
            study_description = case_row["study_description"]

            # Generate report
            progress_bar.set_description(f"Case {case_id}: Generating Report")
            generated_report = gemini.predict(
                system_instruction_report_generator,
                study_description,
                args.temperature,
                image,
            )
            dataset_metadata.at[case_id, "generated_report"] = generated_report

            if use_metric1:
                progress_bar.set_description(f"Case {case_id}: Calculating Metric 1")
                dataset_metadata.at[case_id, "metric1_json_generated"] = gemini.predict(
                    system_instruction_text_json_normalizer,
                    generated_report,
                    args.temperature,
                    None,
                )
                dataset_metadata.at[case_id, "metric1_json_real"] = gemini.predict(
                    system_instruction_text_json_normalizer,
                    case_row["cleaned_text"],
                    args.temperature,
                    None,
                )
                metric1_prompt = metric1_prompt_merge(
                    dataset_metadata.at[case_id, "metric1_json_real"],
                    dataset_metadata.at[case_id, "metric1_json_generated"],
                )
                dataset_metadata.at[case_id, "metric1_json_result"] = gemini.predict(
                    system_instruction_jsons_comparison,
                    metric1_prompt,
                    args.temperature,
                    None,
                )

            if use_metric2:
                progress_bar.set_description(f"Case {case_id}: Calculating Metric 2")
                metric2_prompt = metric2_prompt_merge(
                    case_row["cleaned_text"], generated_report
                )
                dataset_metadata.at[case_id, "metric2_json_result"] = gemini.predict(
                    system_instruction_text_to_text_comparison,
                    metric2_prompt,
                    args.temperature,
                    None,
                )

        except Exception as e:
            logger.error(f"Error processing case {case_id}: {e}")
            traceback.print_exc()
            continue

    logger.info(f"Saving results to {args.output_path}")
    dataset_metadata.to_csv(args.output_path, index=False)
    logger.success("Process finished successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate report")
    parser.add_argument(
        "--images-path", type=str, required=True, help="Path to dataset"
    )
    parser.add_argument(
        "--metadata-path", type=str, required=True, help="Path to metadata"
    )
    parser.add_argument(
        "--metrics",
        type=str,
        default="all",
        choices=["all", "metric1", "metric2"],
        help="Metrics to evaluate",
    )
    parser.add_argument("--output-path", type=str, required=True, help="Path to output")
    parser.add_argument(
        "--temperature", type=float, default=0.0, help="Temperature for Gemini"
    )
    args = parser.parse_args()

    main(args)
