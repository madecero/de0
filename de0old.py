# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 14:03:12 2023

@author: madec
"""

import openai
import json
import os
import pinecone

#Change to a local directory
os.chdir(r'C:\Users\madec\Documents\de0project\openAI')

#connect to Pinecone
with open("pineconekey.txt", "r") as credsfile:
    creds = json.load(credsfile)
    pp_key = creds["key"]
    pp_env = creds["env"]
credsfile.close()

pinecone.init(api_key=pp_key, environment=pp_env)

#get openAI key
with open("oaikey.txt", "r") as credsfile:
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
        temperature = 0.1
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
            if user_input.lower() == "end":
                break
    
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
        
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()