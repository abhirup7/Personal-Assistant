# Personal-Assistant

This repository contains a script for a virtual assistant that uses the Groq API for chat completions. The assistant can remember user inputs by storing them in a text file and retrieve these memories to provide context in future conversations.

## Requirements

- Python 3.7 or later
- `dotenv` library
- `groq` library
- A `.env` file with your Groq API key

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/groq-virtual-assistant.git
    cd groq-virtual-assistant
    ```

2. Install the required libraries:

    ```bash
    pip install python-dotenv groq
    ```

3. Create a `.env` file in the root directory of your project and add your Groq API key:

    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

## Usage

The script provides two main functions: `store` and `retrieve`, as well as a `run_conversation` function to handle the chat with the virtual assistant.

### Functions

- **store(input):** Stores user input in `memory.txt`.

- **retrieve():** Retrieves stored user inputs from `memory.txt`.

- **run_conversation(user_prompt):** Runs a conversation with the virtual assistant using the provided user prompt.

### Running the Script

To run the script, provide a user prompt as an argument:

```bash
python personal_assistant.py remember my hugging face token hf_getyourownhftoken
I have stored your hugging face token - hf_getyourownhftoken. Is there anything else you need help with?

python personal_assistant.py what is my hf token
Your hf token is hf_getyourownhftoken
```
