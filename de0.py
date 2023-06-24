# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:40:29 2023

@author: madec
"""

version = 'v0.0.1'

import json
import os
import openai
import pinecone
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
from langchain.embeddings.openai import OpenAIEmbeddings

print ('\n')
print ('     1             00000   ')
print ('     1            0     0  ')
print ('     1    1111   0  0 0  0 ')
print (' 11111   1    1  0  0 0  0 ')
print (' 1   1   11111   0  0 0  0 ')
print (' 1   1   1        0     0  ')
print (' 11111    11111    00000   ')
print ('\n')

print ('---------------------------------------------------------------------')

#Change to a local directory
os.chdir(r'C:\Users\madec\Documents\de0project\openAI')

# Bueller?!
user_name = 'Mike'
system_name = 'de0'

#set llm, index, and initial messages
chat_model = 'gpt-3.5-turbo'
embed_model = 'text-embedding-ada-002'
index_name = 'de0'
session_start = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
system_message = "Your name is " + str(system_name) + " and you are " + str(user_name) + "'s personal assistant. This conversation started at " + session_start

print ("Welcome to your personal assistant, " + system_name + ' ' + version)
print ("This conversation will be logged with the following date and time: " + str(session_start))
print ("To end your conversation, type 'end'")
print ('---------------------------------------------------------------------')
print ('\n')

#connect to apis

#get openAI key
with open("oaikey.txt", "r") as credsfile:
    openai.api_key = credsfile.read().strip()
credsfile.close()

#connect to Pinecone
with open("pineconekey.txt", "r") as credsfile:
    creds = json.load(credsfile)
    pp_key = creds["key"]
    pp_env = creds["env"]
credsfile.close()

pinecone.init(api_key=pp_key, environment=pp_env)

#initialize embedding model
embed = OpenAIEmbeddings(
    openai_api_key=openai.api_key
)
embed_dimension = 768

#connect to index
index = pinecone.Index(index_name)

#initialize llm
llm = ChatOpenAI(
    temperature = 0,
    openai_api_key = openai.api_key,
    model_name = chat_model
    )

#let's talk

conversation = ConversationChain(
    llm = llm,
    memory = ConversationSummaryMemory(llm = llm))

def chat(chain, query):
    response = chain.run(query)
    return response

# Define the main function to interact with the user
def main():
    
    # system initiation
    conversation(system_message)
    
    #start memory session
    memory_start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    memory = {session_start: {memory_start_time: {'system' : system_message}}}
    memory_path = session_start + ".json"
    
    print ("de0: What can I do for you today? ")
    print ('\n')
    
    # Start the conversation loop
    while True:
        try:
                        
            # Get user input
            user_input = input("You: ")
            if user_input.lower() == "end":
                break
            
            #record time we have an interaction
            interaction_moment = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Generate a response from the GPT-3 model
            response = chat(conversation, user_input)
            print ('\n')
            print ('de0: ' + str(response))
            print ('\n')
            
            #store the query and response in memory dictionary
            memory[session_start][interaction_moment] = {user_name: user_input, system_name: response}
            
            #print to memory file
            os.chdir(r'C:\Users\madec\Documents\de0project\openAI\memory_log')
            with open(memory_path, 'a') as json_file:
                json.dump(memory, json_file)
            os.chdir(r'C:\Users\madec\Documents\de0project\openAI')
        
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()