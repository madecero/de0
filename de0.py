# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 14:40:29 2023

@author: madec
"""

version = 'v0.0.1'

import json
import os
import uuid
import openai
import pinecone
import spacy
import numpy as np
from datetime import datetime
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

print ('---------------------------------------------------------------------')

#Change to a local directory
os.chdir(r'C:\Users\madec\Documents\de0project\openAI')

# Bueller?!
user_name = 'Mike'
system_name = 'de0'

#set llm, index, nlp model, and initial messages
chat_model = 'gpt-3.5-turbo'
index_name = 'de0'
nlp = spacy.load("en_core_web_lg")
session_start = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
dimensions = 1024
temperature = 0.0
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
    memory = ConversationSummaryMemory(llm = llm))


def search_memory(prompt):
    'Function to call similarity search in pinecone'
    
    #convert user input to a spaCy Doc object and vectorize it to query pinceone membory vectors
    doc = nlp(prompt)
    word_vectors = [token.vector for token in doc]
    averaged_vector = np.mean(word_vectors, axis = 0)
    
    if len(averaged_vector) < dimensions:
        normalized_vector = np.pad(averaged_vector, (0, dimensions - len(averaged_vector)))
        normalized_vector = np.ndarray.tolist(normalized_vector)
    else:
        normalized_vector = averaged_vector[:dimensions]
        normalized_vector = np.ndarray.tolist(normalized_vector)
        
    query_response = index.query(normalized_vector, top_k = 1, include_metadata=True)
    
    if query_response == None:
        conversation(system_message)
    else:
        conversation(query_response['matches'][0]['metadata']['text'])

def chat(chain, query):
    'Function to have interactive chat with bot'
    response = chain.run(query)
    return response

# Define the main function to interact with the user
def main():
    
    #start memory session
    conversation_uuid = str(uuid.uuid4())
    conversation_history = {
        "id": conversation_uuid,
        "messages": []
        }
    
    print (system_name + ": What can I do for you today? ")
    print ('\n')
    
    # Start the conversation loop
    while True:
        try:
                        
            # Get user input
            user_input = input(user_name + ": ")
            
            if user_input.lower() == "end":
                break
            
            #record time we have an interaction
            query_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            #query vector store for similar past conversations and add response as context
            search_memory(user_input)
            
            # Generate a response from the GPT-3 model
            response = chat(conversation, user_input)
            response_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print ('\n')
            print (system_name + ": " + str(response))
            print ('\n')
            print(conversation.memory.buffer)
            
            #store the query and response in conversation_history 
            conversation_history["messages"].append(
                {
                "timestamp": query_timestamp,
                "role": user_name,
                "text": user_input
                }
                )
            
            conversation_history["messages"].append(
                {
                "timestamp": response_timestamp,
                "role": system_name,
                "text": str(response)
                }
                )
        
        except KeyboardInterrupt:
            break
        
    #tokenize the conversation_history, transform vectors to consistent dimensionality, and upsert to pinecone index
    vectors = []
    
    #convert conversation_summary to spaCy Doc object
    text = conversation.memory.buffer
    doc = nlp(text)
        
    #extract the word vector for each token in the Doc object
    word_vectors = [token.vector for token in doc]
    
    #average the word vectors to get a single vector representation
    averaged_vector = np.mean(word_vectors, axis = 0)
    
    #pad or truncate the averaged vector to dimensionality 768
    if len(averaged_vector) < dimensions:
        normalized_vector = np.pad(averaged_vector, (0, dimensions - len(averaged_vector)))
        normalized_vector = np.ndarray.tolist(normalized_vector)
    else:
        normalized_vector = averaged_vector[:dimensions]
        normalized_vector = np.ndarray.tolist(normalized_vector)
    
    #append normalized vectors + an id to a list of dictionaries in order to upsert to pinecone
    vectors.append(
        {
        "id": session_start,
        "values": normalized_vector,
        "metadata": {
            "text": text
            }
        }
        )
    
    #index.upsert(vectors=vectors)

if __name__ == '__main__':
    main()