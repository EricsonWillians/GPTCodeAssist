# GPT Code Assistant

GPT Code Assistant is a powerful tool that leverages OpenAI's GPT-3.5-turbo engine to provide code suggestions, improvements, and insights based on the context of a given codebase. It reads and processes files from your codebase, calculates the token count, estimates the cost of the API call, and prompts the user for a query.

## Features

- Supports various programming languages by reading file extensions from an external JSON file
- Recursively processes all supported files within the codebase directory
- Uses tiktoken to count tokens and estimate the cost of the API call
- Prompts the user for confirmation before proceeding with the API call, considering the cost
- Queries the GPT-3.5-turbo model to generate code suggestions based on the codebase context

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/gpt-code-assistant.git
```

2. Change into the cloned directory:

```
cd gpt-code-assistant
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Set the OpenAI API key as an environment variable:

```
export OPEN_AI_API_KEY=your_api_key_here
```

## Usage

1. Update the `supported_extensions.json` file to include the desired file extensions for the programming languages you wish to support.

2. Run the GPT Code Assistant script with the path to your codebase as an argument:

```
python gpt_code_assistant.py /path/to/your/codebase
```

3. The script will process the codebase, count the tokens, and estimate the cost of the API call. If you wish to proceed, type `yes` when prompted.

4. Enter your query when prompted, and the GPT-3.5-turbo model will generate a response based on the context of your codebase.

## Example

```
python gpt_code_assistant.py /path/to/your/codebase
```

Output:

```
The codebase context contains 12345 tokens.
Estimated cost per API call: $0.03
Do you want to proceed? (yes/no): yes
Enter your prompt: How can I optimize this function?
```

Response:

```
To optimize this function, you can ...
```

## License

This project is licensed under the MIT License.
