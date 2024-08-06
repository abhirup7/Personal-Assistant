import json
import os
import sys

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

MODEL = 'llama3-groq-70b-8192-tool-use-preview'

def store(input):
    """Store what the user wants in a text file"""
    try:
        with open("memory.txt", "a") as file:
            file.write(input + "\n")
        return json.dumps({"stored": input})
    except:
        return json.dumps({"error storing info"})

def retrieve():
    """Retreive what the user wants from memory"""
    try:
        with open("memory.txt", "r") as file:
            memory = file.read().replace('\n', '')
            return memory
    except:
        return json.dumps({"error retrieving info"})
def run_conversation(user_prompt):
    chat_history = retrieve()
    messages=[
        {
            "role": "system",
            "content": f"""You are a virtual assistant. Use the store function to remember what the user wants, 
            use the chat history to answer questions from the user if answer doesn't exist here answer with what 
            you know but don't make up stuff
            {chat_history}"""
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "store",
                "description": "store what the user wants to be remembered",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "The input to be stored",
                        }
                    },
                    "required": ["input"],
                },
            },
        },
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "store": store,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                input=function_args.get("input")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return second_response.choices[0].message.content
    else:
        return response_message.content

# user_prompt = "Remember that my name is Abhirup Sahoo"
user_prompt = " ".join(sys.argv[1:])
print(run_conversation(user_prompt))
