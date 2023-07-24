# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:40:29 2023

@author: madec
"""

version = 'v0.0.1'

import json
import os
import sys
import openai
import pinecone
import spacy
import numpy as np
from datetime import datetime
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory

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

#set llm, index, nlp model, and initial messages
chat_model = 'gpt-3.5-turbo'
index_name = 'de0-memory'
dimensions = 300
temperature = 0.0
nlp = spacy.load("en_core_web_lg")
session_start = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
system_message = "Your name is " + str(system_name) + " and you are " + str(user_name) + "'s personal assistant. This conversation started at " + session_start

print ("Welcome to your personal assistant, " + system_name + ' ' + version)
print ("This conversation will be logged with the following date and time: " + str(session_start))
print ("To end your conversation, type 'end'")
print ('---------------------------------------------------------------------')
print ('\n')

#connect to apis

#get openAI key, Pinecone key, and Pinecone Environment
with open("api_keys.txt", "r") as api_keys:
    keys = json.load(api_keys)
    openai.api_key = keys["open_ai_key"]
    pinecone_key = keys["pinecone_key"]
    pinecone_env = keys["pinecone_env"]
api_keys.close()

pinecone.init(api_key=pinecone_key, environment=pinecone_env)

#connect to index
index = pinecone.Index(index_name)

#initialize llm
llm = ChatOpenAI(
    temperature = temperature,
    openai_api_key = openai.api_key,
    model_name = chat_model
    )

#let's talk

conversation = ConversationChain(
    llm = llm,
    memory = ConversationBufferMemory()
    )

def normalize_vector(prompt):
    'Function to vectorize a prompt and normalize it in order to upsert to and/or query pinecone vectorstore'
    
    #convert user input to a spaCy Doc object and vectorize it to upsert to and/or query pinceone memory vectors
    doc = nlp(prompt)
    word_vectors = [token.vector for token in doc]
    averaged_vector = np.mean(word_vectors, axis = 0)
    
    if len(averaged_vector) < dimensions:
        normalized_vector = np.pad(averaged_vector, (0, dimensions - len(averaged_vector)))
        normalized_vector = np.ndarray.tolist(normalized_vector)
    else:
        normalized_vector = averaged_vector[:dimensions]
        normalized_vector = np.ndarray.tolist(normalized_vector)
    
    return normalized_vector

def search_memory(prompt):
    'Function to call similarity search in pinecone'
    
    #obtain the normalized vector representing the prompt text and query pinecone vectorstore
    normalized_vector = normalize_vector(prompt)    
    query_response = index.query(normalized_vector, top_k = 1, include_metadata=True)
    
    #if there is a response from pinecone, set the conversation with context. if not, initialize new conversation
    if (query_response["matches"][0]["score"]) < 0.85:
        conversation(system_message)
    else:
        conversation(query_response["matches"][0]["metadata"]["text"])
        
    print (query_response)

def chat(chain, query):
    'Function to have interactive chat with bot'
    
    response = chain.run(query)
    return response

def upsert_to_memory(conversation_history):
    'Function to upsert conversation to Pinecone for future similarity search'
    
    #tokenize the conversation_history, transform vectors to consistent dimensionality, and upsert to pinecone index
    vectors = []
    normalized_vector = normalize_vector(conversation_history)
    
    #append normalized vectors + an id to a list of dictionaries in order to upsert to pinecone
    vectors.append(
        {
        "id": session_start,
        "values": normalized_vector,
        "metadata": {
            "text": conversation_history
            }
        }
        )
    
    index.upsert(vectors=vectors)
    print (vectors)

# Define the main function to interact with the user
def main():
    
    #have the ai start the conversation by asking the user what they need    
    print (system_name + ": What can I do for you today? ")
    print ('\n')
    
    #initial input from user
    user_input = input(user_name + ": ")
    
    if user_input.lower() == "end":
        sys.exit()
    
    #query vector store for similar past conversations and add response as context
    search_memory(user_input)
    
    # Generate a response from LLM
    response = chat(conversation, user_input)
    print ('\n')
    print (system_name + ": " + str(response))
    print ('\n')
    
    # Start the conversation loop after initial conversation started
    while True:
        try:
            # Get user input
            user_input = input(user_name + ": ")
            
            if user_input.lower() == "end":
                break
            
            # Generate a response from LLM
            response = chat(conversation, user_input)
            print ('\n')
            print (system_name + ": " + str(response))
            print ('\n')
                    
        except KeyboardInterrupt:
            break

    #upsert new conversation history to pinecone
    text = conversation.memory.buffer
    upsert_to_memory(text)

if __name__ == '__main__':
    main()