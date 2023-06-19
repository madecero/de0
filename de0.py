# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:40:29 2023

@author: madec
"""

import openai
import json
import os
import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory

print ('\n')
print ('     1             00000   ')
print ('     1            0     0  ')
print ('     1    1111   0  0 0  0 ')
print (' 11111   1    1  0  0 0  0 ')
print (' 1   1   11111   0  0 0  0 ')
print (' 1   1   1        0     0  ')
print (' 11111    11111    00000   ')
print ('\n')

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
with open("oaikey4.txt", "r") as credsfile:
    openai.api_key = credsfile.read().strip()
credsfile.close()

#initialize llm
llm = ChatOpenAI(
    temperature = 0.1,
    openai_api_key = openai.api_key,
    model_name = 'gpt-3.5-turbo'
    )

conversation = ConversationChain(
    llm = llm,
    memory = ConversationSummaryMemory(llm = llm))

def chat(chain, query):
    response = chain.run(query)
    return response

# Define the main function to interact with the user
def main():

    # Initialize the system message
    conversation("Your name is de0 and you are Michael DeCero's personal assistant.")
    
    # Start the conversation loop
    while True:
        try:            
            # Get user input
            user_input = input("You: ")
            if user_input.lower() == "end":
                break
    
            # Generate a response from the GPT-3 model
            response = chat(conversation, user_input)
            print ('\n')
            print ('de0: ' + str(response))
            print ('\n')
        
        except KeyboardInterrupt:
            break

# messages = [
#     {"role": "system", "content": "Your name is de0 and you are Michael DeCero's personal assistant."},
# ]

# model = 'gpt-3.5-turbo'

# def chat(prompt):
#     response = openai.ChatCompletion.create(
#         model = model,
#         messages = prompt,
#     )
#     completiontext = response.choices[0].message.content
#     return completiontext

# # Define the main function to interact with the user
# def main():

#     # Start the conversation loop
#     while True:
#         try:
            
#             # Initialize the conversation history
#             conversation_history = ""
            
#             # Get user input
#             user_input = input("You: ")
#             if user_input.lower() == "end":
#                 break
    
#             # Generate a response from the GPT-3 model
#             messages = [
#                 {"role": "system", "content": "Your name is de0 and you are Michael DeCero's personal assistant."},
#                 {"role": "user", "content": user_input}
#             ]

#             response = chat(messages)
            
#             # Add user input to the conversation history
#             conversation_history += "You: " + user_input + "\n"
    
#             # Add the response to the conversation history
#             conversation_history += "de0: " + str(response) + "\n"
    
#             # Print the response
#             print("de0: ", response)
            
#             #write to history file
#             with open("chat_history.txt", "a") as historyfile:
#                 historyfile.write(conversation_history)
#             historyfile.close()
        
#         except KeyboardInterrupt:
#             break

if __name__ == '__main__':
    main()