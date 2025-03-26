import re
import os
import subprocess
import sys

# Extract Python code block from a LLM response
def extract_code(text):
    try:
        match = re.search(r"```python(.*?)```", text, re.DOTALL)
        if match:
            code = match.group(0).strip()
        else:
            code = ""
            print("No matching code block found.")
        return code.replace("```python\n", "").replace("```", "")
    except Exception as e:
        print(f"Code extraction error: {e}")
        raise

# Extract file path from a code string that uses os.path.join()
def extract_file_path(code_str):
    try:
        match = re.search(r'os\.path\.join\(\s*["\'](.+?)["\']\s*,\s*["\'](.+?)["\']\s*\)', code_str)
        if match:
            folder = match.group(1)
            filename = match.group(2)
            return os.path.join(folder, filename)
        print("No file path found.")
        return None
    except Exception as e:
        print(f"File path extraction error: {e}")
        raise

# Execute extracted Python code in a subprocess using the given interpreter
def execute_code_in_virtualenv(text, python_interpreter=sys.executable):
    if not python_interpreter:
        raise EnvironmentError("Python interpreter not found.")

    code_str = extract_code(text)
    command = [python_interpreter, "-c", code_str]

    try:
        print("✅ Running script:", command)
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        file_path = extract_file_path(code_str)
        print("✅ Extracted file path:", file_path)
        return file_path
    except subprocess.CalledProcessError as e:
        return (f"Execution error:\n{e.stderr.strip()}", None)
