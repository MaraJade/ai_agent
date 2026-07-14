import os
import argparse
import sys
# import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from functions.call_function import call_function, available_functions


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No api key found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # Parse arguments passed by the user
    parser = argparse.ArgumentParser(description="Chatbot")

    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]

    for _ in range(20):
        messages = generate_content(client, messages, args.verbose)
        if not messages:
            return

    sys.exit("Error: More than 20 iterations required")


def generate_content(
    client: OpenAI, messages: list, verbose: bool
) -> list | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    # If there are no tool calls, just print the response
    if not message.tool_calls:
        print("Final Response:")
        print(message.content)
        # Return None to let the program know the conversation is over
        return None

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        result_message = call_function(tool_call, verbose)
        messages.append(result_message)
        if not result_message.get("content"):
            raise RuntimeError("Empty function response for " +
                               f"{tool_call.function.name}")
        if verbose:
            print(f"-> {result_message['content']}")

    return messages


if __name__ == "__main__":
    main()
