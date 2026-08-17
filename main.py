#!/usr/bin/env python3
"""
Enterprise LLM Orchestrator CLI Wrapper
Author: To Cheuk Yui Dexter
Description: CLI wrapper executing deterministic multi-turn meta-prompts via google-genai SDK.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
ENGINES_DIR = BASE_DIR / "engines"
UTILITIES_DIR = BASE_DIR / "utilities"


def load_template(folder: Path, filename: str) -> str:
    file_path = folder / f"{filename}.md"
    if not file_path.exists():
        print(f"Error: Prompt template '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def format_prompt(template: str, user_input: str, flag: str = "/fast") -> str:
    flag_str = flag if flag.startswith("/") else f"/{flag}"
    formatted = template.replace("/fast or /slow", flag_str)

    if "<brain_dump>" in formatted:
        formatted = formatted.replace("[INSERT YOUR CASUAL MESSY WORKFLOW CONCEPT HERE]", user_input)
    elif "<goal>" in formatted:
        formatted = formatted.replace("[INSERT GOAL STATEMENT OR RAW PRESENTATION/STYLE WORKFLOW HERE]", user_input)
        formatted = formatted.replace("[INSERT HIGH-STAKES TASK / WORKFLOW REQUIREMENT HERE]", user_input)
    elif "<user_prompt>" in formatted:
        formatted = formatted.replace("[PASTE TARGET PROMPT HERE, ALONGSIDE OPTIONAL STYLING FLAGS LIKE /perfection OR /mimic]", user_input)
    else:
        formatted += f"\n\n<raw_input_data>\n{user_input}\n</raw_input_data>"

    return formatted


def execute_orchestration(prompt_payload: str, model_name: str, temperature: float = 0.2) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is missing.", file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=0.95,
        max_output_tokens=8192,
    )

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_payload,
            config=config,
        )
        return response.text
    except Exception as e:
        print(f"API Execution Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Enterprise LLM Orchestrator CLI")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--engine", choices=["goal", "mimic", "perfection", "analyzer"])
    group.add_argument("--utility", choices=["handoff", "system_hotpatch"])

    parser.add_argument("--flag", default="fast")
    parser.add_argument("--input", type=str)
    parser.add_argument("--input-file", type=Path)
    parser.add_argument("--model", default=os.getenv("DEFAULT_MODEL", "gemini-2.5-flash"))
    parser.add_argument("--temperature", type=float, default=0.2)

    args = parser.parse_args()

    if args.input_file:
        if not args.input_file.exists():
            print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
            sys.exit(1)
        user_payload = args.input_file.read_text(encoding="utf-8")
    elif args.input:
        user_payload = args.input
    elif not sys.stdin.isatty():
        user_payload = sys.stdin.read()
    else:
        print("Error: No input provided.", file=sys.stderr)
        sys.exit(1)

    if args.engine:
        template_raw = load_template(ENGINES_DIR, args.engine)
    else:
        template_raw = load_template(UTILITIES_DIR, args.utility)

    compiled_prompt = format_prompt(template_raw, user_payload, args.flag)
    output = execute_orchestration(compiled_prompt, args.model, args.temperature)
    print(output)


if __name__ == "__main__":
    main()
