"""Homework 2, Problem 1: Number and parse Python source files."""

import ast
import io
import os
import pprint
import tokenize


def line_number(input_filename: str, output_filename: str) -> None:
    """Write a copy of a file with each line prefixed by its line number."""
    try:
        with open(input_filename, "r", encoding="utf-8") as input_file:
            lines = input_file.readlines()

        with open(output_filename, "w", encoding="utf-8") as output_file:
            for number, line in enumerate(lines, start=1):
                output_file.write("{}. {}".format(number, line))

    except (OSError, UnicodeError) as error:
        print("Could not number the lines in the file:", error)
        raise


def parse_functions(
        filename: str) -> tuple[tuple[int, str, str, str], ...]:
    """Return information about the top-level functions in a Python file.

    Each tuple contains the definition line number, function name, formal
    argument list, and original function code with comments and empty lines
    removed. The result is sorted alphabetically by function name.
    """
    try:
        with open(filename, "r", encoding="utf-8") as source_file:
            source = source_file.read()

        tree = ast.parse(source)
        functions = []

        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_code = ast.get_source_segment(source, node)
                reader = io.StringIO(function_code).readline
                tokens = [
                    token
                    for token in tokenize.generate_tokens(reader)
                    if token.type != tokenize.COMMENT
                ]
                code_without_comments = tokenize.untokenize(tokens)
                code_lines = [
                    line.rstrip()
                    for line in code_without_comments.splitlines()
                    if line.strip()
                ]
                cleaned_code = "\n".join(code_lines) + "\n"
                arguments = ast.unparse(node.args)
                functions.append(
                    (node.lineno, node.name, arguments, cleaned_code)
                )

        functions.sort(key=lambda function: function[1])
        return tuple(functions)

    except (OSError, UnicodeError, SyntaxError, tokenize.TokenError) as error:
        print("Could not parse the Python file:", error)
        raise


def main() -> None:
    """Test line_number and parse_functions on this source file."""
    source_filename = os.path.abspath(__file__)
    numbered_filename = source_filename + ".txt"

    line_number(source_filename, numbered_filename)
    functions = parse_functions(source_filename)

    print("Emir Koyuncu")
    print("Numbered file created:", numbered_filename)
    print("Functions found in", os.path.basename(source_filename))
    pprint.pprint(functions, width=120)


if __name__ == "__main__":
    main()
