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

messages = [
    {"role": "system", "content": "Your name is de0 and you are Michael DeCero's personal assistant."},
]

model = 'gpt-3.5-turbo'

def chat(prompt):
    response = openai.ChatCompletion.create(
        model = model,
        messages = prompt,
    )
    completiontext = response.choices[0].message.content
    return completiontext

# Define the main function to interact with the user
def main():

    # Start the conversation loop
    while True:
        try:
            
            # Initialize the conversation history
            conversation_history = ""
            
            # Get user input
            user_input = input("You: ")
    
            # Generate a response from the GPT-3 model
            messages = [
                {"role": "system", "content": "Your name is de0 and you are Michael DeCero's personal assistant."},
                {"role": "user", "content": user_input}
            ]

            response = chat(messages)
            
            # Add user input to the conversation history
            conversation_history += "You: " + user_input + "\n"
    
            # Add the response to the conversation history
            conversation_history += "de0: " + str(response) + "\n"
    
            # Print the response
            print("de0: ", response)
            
            #write to history file
            with open("chat_history.txt", "a") as historyfile:
                historyfile.write(conversation_history)
            historyfile.close()
            
            print(messages)
        
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()