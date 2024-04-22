import asyncio
import tkinter as tk

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions

# Configure the Gemini API key
GEMINI_API_KEY = "Gemini API Key"

# Configure the API key
genai.configure(api_key=GEMINI_API_KEY)

# Create a Gemini model instance
model = genai.GenerativeModel('gemini-pro')

async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's api key 
        api_key='VIAM API Key',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
        api_key_id='VIAM API Key ID'
    )
    return await RobotClient.at_address('RobotClientAddress', opts)

async def main():
    machine = await connect()

    print('Resources:')
    print(machine.resource_names)
    
    # Close the machine when done
    await machine.close()

    # Tkinter GUI setup
    root = tk.Tk()
    root.title("Chatbot")

    # Create chat log display
    chat_log = tk.Text(root, state=tk.DISABLED, wrap="word")
    chat_log.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
    
    # Insert initial message
    response1 = model.generate_content("Assume that you are a chatbot in Naveen Hospital and you are interacting with a patient. Your task is to collect important information from patient so a doctor can focus on important information and other information should be discarded. Now, act like hospital chatbot and ask me questions.?")
    initial_message = str(response1.text)

    chat_log.config(state=tk.NORMAL)
    chat_log.insert("end", initial_message)
    chat_log.config(state=tk.DISABLED)

    # Create input box
    input_box = tk.Text(root, height=3, wrap="word")
    input_box.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    # Create send button
    send_button = tk.Button(root, text="Send", width=10, command=lambda: send_message(input_box, chat_log))
    send_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

    # Bind Enter key to send message
    root.bind("<Return>", lambda event: send_message(input_box, chat_log))

    # Focus on the input box
    input_box.focus_set()

    # Run the Tkinter event loop
    root.mainloop()

async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace "<API-KEY>" (including brackets) with your machine's api key 
        api_key='VIAM API Key',
        # Replace "<API-KEY-ID>" (including brackets) with your machine's api key id
        api_key_id='VIAM API Key ID'
    )
    return await RobotClient.at_address('RobotClientAddress', opts)

def send_message(input_box, chat_log):
    user_input = input_box.get("1.0", "end").strip()
    input_box.delete("1.0", "end")
    if user_input:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert("end", "You: " + user_input + "\n\n")
        chat_log.see("end")
        
        # Get the chatbot's response using the Gemini API
        response = get_chatbot_response(user_input)
        chat_log.insert("end", "Chatbot: " + str(response) + "\n\n")
        chat_log.config(state=tk.DISABLED)

def get_chatbot_response(user_input):
    try:
        # Use the Gemini API to get the chatbot's response
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return "I'm sorry, there was an error processing your request. Please try again later."

if __name__ == '__main__':
    asyncio.run(main())
