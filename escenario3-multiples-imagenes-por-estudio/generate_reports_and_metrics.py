import pandas as pd
import argparse
import os
from tqdm import tqdm
from PIL import Image
from loguru import logger
import traceback
import random
from src.utils.config import config
from src.utils.gemini import GeminiClient
from src.utils.html_handling import clean_html
from src.system_instructions.escenario1_baseline import (
    system_instruction_text_to_text_comparison,
    system_instruction_text_json_normalizer,
    system_instruction_jsons_comparison,
)

from src.system_instructions.escenario1_baseline import (
    system_instruction_report_generator as system_instruction_report_generator_escenario1
)

from src.system_instructions.escenario3_multiples_imagenes_por_estudio import (
    system_instruction_report_generator
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
    logger.info(f"One random image: {args.one_random_image}")

    # Preprocess text
    dataset_metadata["cleaned_text"] = dataset_metadata["field_value"].apply(clean_html)

    logger.info(f"Initializing Gemini Client with model: {config['GEMINI_MODEL']}")
    gemini = GeminiClient(config["GEMINI_API_KEY"], config["GEMINI_MODEL"])

    # For loop para generar reporte, y calcular metricas
    dataset_metadata["generated_report"] = None
    use_metric1 = args.metrics == "all" or args.metrics == "metric1"
    use_metric2 = args.metrics == "all" or args.metrics == "metric2"
    resulting_df = {"report_id": [], "generated_report": [], "cleaned_text": []}
    if use_metric1:
        logger.info("Metric 1 enabled")
        resulting_df["metric1_json_generated"] = []
        resulting_df["metric1_json_real"] = []
        resulting_df["metric1_json_result"] = []

    if use_metric2:
        logger.info("Metric 2 enabled")
        resulting_df["metric2_json_result"] = []

    logger.info("Starting processing loop...")
    progress_bar = tqdm(dataset_metadata.groupby("report_id"), total=len(dataset_metadata["report_id"].unique()))
    for j, (report_id, report_rows) in enumerate(progress_bar):
        progress_bar.set_description(f"Processing Case {report_id}")
        cleaned_text = report_rows.iloc[0]["cleaned_text"]
        all_images_paths = report_rows["file_url"].apply(lambda x: os.path.join(args.images_path, x.replace("dcm", "jpg"))).tolist()
        try:
            if not all(os.path.exists(image_path) for image_path in all_images_paths):
                logger.warning(
                    f"Image not found at {all_images_paths}, skipping case {report_id}"
                )
                continue
            images = [Image.open(image_path) for image_path in all_images_paths]
            images = [random.choice(images)] if args.one_random_image else images
            study_prompt = f"STUDY NAME: {report_rows.iloc[0]['study_description']}"

            # Generate report
            progress_bar.set_description(f"Case {report_id}: Generating Report")
            if args.one_random_image:
                generated_report = gemini.predict(
                    system_instruction_report_generator_escenario1,
                    study_prompt,
                    args.temperature,
                    images[0],
                )
            else:
                generated_report = gemini.predict_multiple_images(
                    system_instruction_report_generator,
                    study_prompt,
                    args.temperature,
                    images,
            )
            resulting_df["generated_report"].append(generated_report)
            resulting_df["cleaned_text"].append(cleaned_text)
            resulting_df["report_id"].append(report_id)

            if use_metric1:
                progress_bar.set_description(f"Case {report_id}: Calculating Metric 1")
                metric1_json_generated = gemini.predict(
                    system_instruction_text_json_normalizer,
                    generated_report,
                    args.temperature,
                    None,
                )
                metric1_json_real = gemini.predict(
                    system_instruction_text_json_normalizer,
                    cleaned_text,
                    args.temperature,
                    None,
                )
                metric1_prompt = metric1_prompt_merge(
                    metric1_json_real,
                    metric1_json_generated,
                )
                metric1_json_result = gemini.predict(
                    system_instruction_jsons_comparison,
                    metric1_prompt,
                    args.temperature,
                    None,
                )
                resulting_df["metric1_json_generated"].append(metric1_json_generated)
                resulting_df["metric1_json_real"].append(metric1_json_real)
                resulting_df["metric1_json_result"].append(metric1_json_result)

            if use_metric2:
                progress_bar.set_description(f"Case {report_id}: Calculating Metric 2")
                metric2_prompt = metric2_prompt_merge(
                    cleaned_text, generated_report
                )
                metric2_json_result = gemini.predict(
                    system_instruction_text_to_text_comparison,
                    metric2_prompt,
                    args.temperature,
                    None,
                )
                resulting_df["metric2_json_result"].append(metric2_json_result)

        except Exception as e:
            logger.error(f"Error processing case {report_id}: {e}")
            traceback.print_exc()
            continue

    logger.info(f"Saving results to {args.output_path}")
    pd.DataFrame(resulting_df).to_csv(args.output_path, index=False)
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
    parser.add_argument("--one-random-image", action="store_true", default=False, help="Use one random image")
    args = parser.parse_args()

    main(args)
