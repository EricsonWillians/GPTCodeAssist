import os
import sys
import json
import openai
from pathlib import Path
import tiktoken

openai.api_key = os.environ["OPEN_AI_API_KEY"]


def read_supported_files(directory, extensions):
    for entry in directory.iterdir():
        if entry.is_file() and entry.suffix in extensions:
            try:
                with open(entry, "r", encoding="utf-8", errors="ignore") as f:
                    yield f.read()
            except UnicodeDecodeError:
                print(f"Warning: Ignoring file with encoding issues: {entry}")
        elif entry.is_dir():
            yield from read_supported_files(entry, extensions)


def count_tokens(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def main():
    if len(sys.argv) != 2:
        print("Usage: python gpt_code_assistant.py <path/to/your/codebase>")
        sys.exit(1)

    codebase_directory = Path(sys.argv[1])

    with open("supported_extensions.json", "r") as f:
        supported_extensions_data = json.load(f)
        supported_extensions = set(supported_extensions_data["extensions"])

    codebase_context = "\n".join(read_supported_files(
        codebase_directory, supported_extensions))
    token_count = count_tokens(codebase_context)
    cost_per_token = 0.002 / 1000
    estimated_cost = token_count * cost_per_token

    print(f"The codebase context contains {token_count} tokens.")
    print(f"Estimated cost per API call: ${estimated_cost:.2f}")

    proceed = input("Do you want to proceed? (yes/no): ").lower()

    if proceed == "yes":
        prompt = input("Enter your prompt: ")
        model_engine = "gpt-3.5-turbo"

        response = openai.Completion.create(
            engine=model_engine,
            prompt=codebase_context + "\n" + prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.8,
        )

        print(response.choices[0].text.strip())
    else:
        print("Operation aborted.")


if __name__ == "__main__":
    main()
