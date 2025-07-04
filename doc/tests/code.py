import re
path = '../'
from apsimNGpy import *
import re
import textwrap


def run_rst_code_blocks(rst_path):
    """
    Parses and executes Python code blocks from an .rst file.

    Parameters:
        rst_path (str): Path to the .rst file.

    Returns:
        List[dict]: A list of dictionaries with 'code' and 'output' or 'error'.
    """
    results = []
    inside_block = False
    collecting = False
    code_lines = []

    with open(rst_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith(".. code-block:: python"):
            inside_block = True
            collecting = False
            code_lines = []
            continue

        # Code blocks in reStructuredText start on next indented line(s)
        if inside_block:
            if line.strip() == "":
                continue
            if line.startswith("    "):  # must be at least 4 spaces indented
                collecting = True
                code_lines.append(line)
            elif collecting and not line.startswith("    "):
                # end of code block
                code = textwrap.dedent("".join(code_lines))
                results.append(execute_code_block(code))
                inside_block = False
                collecting = False
                code_lines = []

    # Catch final code block if file ends
    if code_lines:
        code = str(textwrap.dedent("".join(code_lines)))
        print(code)
        results.append(execute_code_block(code))

    return results


def execute_code_block(code):
    try:
        local_vars = {}
        x= eval(code, globals(), local_vars)
        print(x)
        return {"code": code, "output": "Executed successfully."}
    except Exception as e:
        return {"code": code, "error": str(e)}

results = run_rst_code_blocks("../OPT.rst")

for i, result in enumerate(results):
    print(f"\n\033[94m--- Code Block {i+1} ---\033[0m")
    print(result["code"])
    print("✓ Output:" if "output" in result else "✗ Error:", result.get("output", result.get("error")))
