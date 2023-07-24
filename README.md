# de0: A "Long-Term Memory" 🧠 Chatbot

de0 is the name I gave to my personal assistant, but you are able to change the name to whatever your heart desires. You can update both the chatbot's name and your name in the #Bueller?! section of [de0.py](https://github.com/madecero/de0/blob/main/de0.py).

![image](https://github.com/madecero/de0/assets/59320522/fec1af71-31b5-4ec9-9919-13ff982fe9d7)

This chatbot runs on the gpt-3.5-turbo model from OpenAI, but you can select a different OpenAI model as well. Other LLMs such as llama2 and bard will be explored in future releases. **Stay Tuned!**

It is important to note that LLMs may not always be accurate. This is an *experiment!*

See more commentary in my blog: *link coming soon*

<hr/>

## Introduction 📜

I use chatGPT nearly every day - mostly (but not exclusively) to help with coding questions/problems. There are times I am working through a complex problem where I need to end my session and call it a night. Then, a few days later, I may be ready to resurrect my problem solving assistant.

But in order to "pick up" where I (and my chatbot) left off, I need to find the relevant session in order to properly "restart" my assistant in helping me solve my problem. Because I use this tool so much, I find it annoying to dig through previous sessions to find the right one that is relevant to a particular task at hand.

This made me think... What if my chatbot had long-term memory? I simply ask it something like "Hey. we were working on problem x a few days ago... Can you remind me where we left off?" and we are right back where we started. No digging through previous sessions.

This is the goal of de0.

<hr/>

## Demo 🤖

<hr/>

## Execution ⌨️

You can start using de0 via your local terminal today! Just follow these instructions:

### 📋 Requirements

  - Python 3.10 or later (instructions: [for Windows](https://www.tutorialspoint.com/how-to-install-python-in-windows))
  - OpenAI API access [documentation](https://platform.openai.com/docs/api-reference/introduction)
  - Pinecone API access [link](https://app.pinecone.io/)

### 🗝️ API Keys

**OpenAI**

You must have an OpenAI developer account in order to run de0: [link](https://platform.openai.com/signup)

Once you have that set up, you can get your API key here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

![image](https://github.com/madecero/de0/assets/59320522/4ade5c2b-8879-4c49-9f78-b2568cb7d77d)

**Pinecone**

Once you have your pinecone account, create an index.

![image](https://github.com/madecero/de0/assets/59320522/0a296b9e-217a-459e-a10f-07881d97c77f)

Once you create the index, you can find the API key and the Environment on the following page. If you have not yet created an API key, click the +Create API Link. This will be important later:

![image](https://github.com/madecero/de0/assets/59320522/7998cf03-75ac-4899-a28d-f491364f8909)


I have named my index "de0-memory." You can name it whatever you like. Just make sure that if you make adjustments to either the name or the dimensions in this setup, you also update the **#set llm, index, nlp model, and initial messages** section of [de0.py](https://github.com/madecero/de0/blob/main/de0.py).

![image](https://github.com/madecero/de0/assets/59320522/f22bb446-3711-4082-adfd-4e2b1cea6e1a)

*Note:* 300 dimensions and the cosine metric are the best options for this use case. I talk about this more in my blog *link coming soon*

### 💻 Run de0

Copy the path here:

![image](https://github.com/madecero/de0/assets/59320522/ecf537ea-17ab-47f2-aa58-fe2628820b19)

Open your terminal window and clone the repo:

```git clone https://github.com/madecero/de0.git```

Change your directory to the de0 folder:

```cd de0```

Install the required packages (must set the permissions as --user):

```pip install -r requirements.txt --user```

Now, open the ```api_keys.txt``` file in your directory and update your open api key, pincecone key, and pinecone environment accordingly (from the 🗝️ API Keys section above)

![image](https://github.com/madecero/de0/assets/59320522/9e70500c-d924-49e5-99fa-64e532a5b83f)

Run de0.py:

```python de0.py```

![image](https://github.com/madecero/de0/assets/59320522/60a19c9b-505b-4d7e-ac6e-c68e2411b486)
