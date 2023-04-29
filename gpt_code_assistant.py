import os
import sys
import json
import openai
import pathspec
from pathlib import Path
import tiktoken

openai.api_key = os.environ["OPEN_AI_API_KEY"]


def read_supported_files(directory, extensions, gitignore_spec=None):
    for entry in directory.iterdir():
        if gitignore_spec and gitignore_spec.match_file(entry):
            continue

        if entry.is_file() and entry.suffix in extensions:
            try:
                with open(entry, "r", encoding="utf-8", errors="ignore") as f:
                    yield f.read()
            except UnicodeDecodeError:
                print(f"Warning: Ignoring file with encoding issues: {entry}")
        elif entry.is_dir():
            yield from read_supported_files(entry, extensions, gitignore_spec)


def load_gitignore_patterns(directory):
    gitignore_path = directory / ".gitignore"
    if gitignore_path.exists():
        with open(gitignore_path, "r") as f:
            gitignore_content = f.read()
        return pathspec.PathSpec.from_lines("gitwildmatch", gitignore_content.splitlines())
    else:
        return None


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

    gitignore_spec = load_gitignore_patterns(codebase_directory)
    codebase_context = "\n".join(read_supported_files(
        codebase_directory, supported_extensions, gitignore_spec))
    token_count = count_tokens(codebase_context)
    cost_per_token = 0.002 / 1000
    estimated_cost = token_count * cost_per_token

    print(f"The codebase context contains {token_count} tokens.")
    print(f"Estimated cost per API call: ${estimated_cost:.2f}")

    proceed = input("Do you want to proceed? (yes/no): ").lower()

    if proceed == "yes":
        prompt = input("Enter your prompt: ")
        model_engine = "gpt-3.5-turbo"

        # Split the input message into parts of length 4096 tokens
        message_parts = [codebase_context[i:i+4096]
                         for i in range(0, len(codebase_context), 4096)]

        # Make multiple API calls to provide the full data
        response_parts = []
        for part in message_parts:
            response = openai.ChatCompletion.create(
                model=model_engine,
                messages=[
                    {"role": "user", "content": part + "\n" + prompt}
                ]
            )
            if len(response.choices) > 0 and hasattr(response.choices[0], 'message'):
                response_parts.append(response.choices[0].message)

        # Combine the response parts into a single response
        full_response = ""
        i = 1
        for response in response_parts:
            full_response += str(i) + '.: ' + response.content + '\n\n'
            i += 1

        print(full_response.strip())
    else:
        print("Operation aborted.")


if __name__ == "__main__":
    main()
