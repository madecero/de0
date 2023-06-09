# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:40:29 2023

@author: madec
"""

import openai
import os

#Change to a local directory
os.chdir(r'<INSERT HERE>')

#get openAI key
with open("key.txt", "r") as credsfile:
    openai.api_key = credsfile.read().strip()
credsfile.close()

model = 'gpt-3.5-turbo'

def chat(conversation_log):
    response = openai.ChatCompletion.create(
        model = model,
        messages = conversation_log
    )
    conversation_log.append({
        'role': response.choices[0].message.role,
        'content': response.choices[0].message.content.strip()
        })
    return conversation_log

conversations = []
conversations.append({'role': 'system', 'content': "Your name is de0 and you are Michael DeCero's personal assistant."})
prompt = chat(conversations)


# Define the main function to interact with the user
def main():

    # Start the conversation loop
    while True:
        try:
            # Initialize the conversation history
            conversation_history = ""
            
            # Get user input
            user_input = input("> ")
    
            # Generate a response from the GPT-3 model
            response = chat(prompt=user_input)
            
            # Add user input to the conversation history
            conversation_history += "You: " + user_input + "\n"
    
            # Add the response to the conversation history
            conversation_history += "de0: " + response + "\n"
    
            # Print the response
            print("de0: ", response)
            
            #write to history file
            with open("chat_history.txt", "a") as historyfile:
                historyfile.write(conversation_history)
            historyfile.close()
        
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()
