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
from langchain.embeddings.openai import OpenAIEmbeddings

#Change to a local directory
os.chdir(r'<INSERT PATH>')

#set llm and index
chat_model = 'gpt-3.5-turbo'
embed_model = 'text-embedding-ada-002'
index_name = 'de0'

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

if __name__ == '__main__':
    main()