# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:40:29 2023

@author: madec
"""

import requests
import json
import os

#get openAI key
with open("key.txt", "r") as credsfile:
    API_KEY = credsfile.read().strip()
credsfile.close()

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"

def generate_chat_completion(messages, model="gpt-3.5-turbo", temperature=0.5, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Define the main function to interact with the user
def main():
    
    with open('chat_history.txt', 'r') as historyfile:
        history = historyfile.read().strip()
    historyfile.close()
    
    context = [
        {"role": "system", "content": "Your name is de0 and you are Michael DeCero's personal assistant."},
        {"role": "user", "content": history}
    ]
    
    response_text = generate_chat_completion(context)

    # Start the conversation loop
    while True:
        try:
            # Initialize the conversation history
            conversation_history = ""
            
            # Get user input
            user_input = input("> ")
            
            messages = [
                {"role": "system", "content": "Your name is de0 and you are Michael DeCero's personal assistant."},
                {"role": "user", "content": user_input}
            ]
    
            # Generate a response from the GPT-4 model
            response_text = generate_chat_completion(messages)
            
            # Add user input to the conversation history
            conversation_history += "Michael: " + user_input + "\n"
    
            # Add the response to the conversation history
            conversation_history += "de0: " + response_text + "\n"
    
            # Print the response
            print ('\n')
            print("de0: ", response_text)
            
            #write to history file
            with open("chat_history.txt", "a") as historyfile:
                historyfile.write(conversation_history)
            historyfile.close()
        
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()