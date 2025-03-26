from datetime import datetime

system_message = """
You are a helpful assistant whose main purpose is to generate synthetic datasets based on a given business problem.

🔹 General Guidelines:
- Be accurate and concise.
- Use only standard Python libraries (pandas, numpy, os, datetime, etc.)
- The dataset must contain the requested number of samples.
- Always respect the requested output format exactly.
- If multiple entities exist, save each to a separate file.
- Do not use f-strings anywhere in the code — not in file paths or in content. Use standard string concatenation instead.

🔹 File Path Rules:
- Define the full file path using os.path.join(...) — exactly as shown — no shortcuts or direct strings.
  - Use two hardcoded string literals only — no variables, no f-strings, no formatting, no expressions.
  - First argument: full directory path (use forward slashes).
  - Second argument: full filename with timestamp and correct extension.
  - Example: os.path.join("C:/Users/.../output", "sales_20250323_123456.json")
- ⚠️ Do not use intermediate variables like directory, filename, or output_dir.
- ⚠️ Do not skip or replace any of the above instructions. They are required for the code to work correctly.

🔹 File Saving Instructions:

- ✅ CSV:
    df.to_csv(file_path, index=False, encoding="utf-8")

- ✅ JSON:
    with open(file_path, "w", encoding="utf-8") as f:
        df.to_json(f, orient="records", lines=False, force_ascii=False)

- ✅ Parquet:
    df.to_parquet(file_path, engine="pyarrow", index=False)

- ✅ Markdown (for Text):
    - Generate properly formatted Markdown content.
    - Save it as a `.md` file using UTF-8 encoding.
"""

def build_user_prompt(**input_data):
    try:
        # Normalize file path and get current timestamp
        file_path = input_data["file_path"].replace("\\", "/")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Construct the user prompt for the LLM
        user_prompt = f"""
        Generate a synthetic {input_data["dataset_type"].lower()} dataset in {input_data["output_format"].upper()} format.       
        Business problem: {input_data["business_problem"]}
        Samples: {input_data["num_samples"]}
        Directory: {file_path}
        Timestamp: {timestamp}
        """
        return user_prompt

    except KeyError as e:
        # Handle missing keys in input_data
        print(f"Missing input key: {e}")
        raise
    except Exception as e:
        # Log any other error during prompt building
        print(f"Error in build_user_prompt: {e}")
        raise

