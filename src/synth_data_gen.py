import os
from datetime import datetime
from .prompts import build_user_prompt, system_message
from .models import get_gpt_completion, get_claude_completion
from .utils import execute_code_in_virtualenv

class SynthDataGen:
    def __init__(self, output_dir="output"):
        # Set the default output directory and ensures it's created
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def get_timestamp(self):
        # Return current timestamp for file naming
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate_dataset(self, **input_data):
        try:
            # Add output directory path to input data
            input_data["file_path"] = self.output_dir

            # Build the prompt to send to the LLM
            prompt = build_user_prompt(**input_data)

            # Call the selected LLM based on the model
            if input_data["model"] == "GPT":
                code = get_gpt_completion(prompt, system_message)
            elif input_data["model"] == "Claude":
                code = get_claude_completion(prompt, system_message)
            else:
                raise ValueError("Invalid model selected.")

            # Execute the generated code and return the output file path
            file_path = execute_code_in_virtualenv(code)
            return file_path

        except Exception as e:
            # Log and re-raise any errors
            print(f"Error in generate_dataset: {e}")
            raise


