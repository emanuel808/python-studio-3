
import ast

MAX_SCRIPT_SIZE = 100_000

def validate_script(code):
    if not isinstance(code, str):
        return False, "Invalid script"

    if len(code.encode("utf-8")) > MAX_SCRIPT_SIZE:
        return False, "Script is too large"

    try:
        ast.parse(code)
    except SyntaxError as exc:
        return False, f"Syntax error: {exc}"

    return True, "Script syntax is valid"
