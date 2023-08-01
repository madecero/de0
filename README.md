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

## Demo 🖥️

<h2 align="center"> Ask de0 to help me with a programming problem on July 20th, 2023 </h2>

![de0capture](https://github.com/madecero/de0/assets/59320522/226c36d5-9bfe-4872-87c0-88233691b3f7)

Cool. I know de0 will remember this list, so I moved on to other things that day.

<h2 align="center"> A few days later, I asked de0 for birthday ideas for my wife, Haley </h2>

![de0capture1](https://github.com/madecero/de0/assets/59320522/8c6e2b56-f6c9-4fa8-ae42-68c3d4d26836)

de0 responds with something relevant. I know it will remember this too, so I will come back to that another time.

<h2 align="center"> A week later, I want to revist my speech to text programming problem </h2>

![de0capture2](https://github.com/madecero/de0/assets/59320522/d0a410e2-26e1-427e-badc-d208fd272fc0)

Nice job, de0! You remembered the relevant instructions for my programming solution, and excluded irrelevant details about the birthday gift.

I can handle the birthday gift. I know my wife better than you ;)
<hr/>

## Execution ⌨️

You can start using de0 via your local terminal today! Just follow these instructions:

### 📋 Requirements

  - Python 3.10 or later (instructions: [for Windows](https://www.tutorialspoint.com/how-to-install-python-in-windows))
  - OpenAI API access [documentation](https://platform.openai.com/docs/api-reference/introduction)
  - Pinecone API access [link](https://app.pinecone.io/)
  - SpaCy en_core_web_lg trained pipeline [documentation](https://spacy.io/usage/models)

_NOTE:_ The SpaCy large pipeline model is 560 MBs. You can also replace the _lg model with the _sm model (12 MBs) or the _md model (40 MBs), but the performance has not been tested with these sizes. Documentation on SpaCy english models can be found here:
https://spacy.io/models/en

Other languages can also be tokenzied using SpaCy models. See the list of options here:
https://spacy.io/usage/models

### 🗝️ API Keys

**OpenAI** 🤖

You must have an OpenAI developer account in order to run de0: [link](https://platform.openai.com/signup)

Once you have that set up, you can get your API key here: [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)

![image](https://github.com/madecero/de0/assets/59320522/4ade5c2b-8879-4c49-9f78-b2568cb7d77d)

For OpenAI API key to work, set up paid account at OpenAI API > Billing

![image](https://github.com/madecero/de0/assets/59320522/db51251a-7d3b-4b45-a1f4-5f0782ea924b)

**Pinecone** 💾

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

Install the SpaCy en_core_web_lg model (replace _lg with either _sm or _md if you want to use a smaller model)

```python -m spacy download en_core_web_lg```

Now, open the ```api_keys.txt``` file in your directory and update your open api key, pincecone key, and pinecone environment accordingly (from the 🗝️ API Keys section above)

![image](https://github.com/madecero/de0/assets/59320522/9e70500c-d924-49e5-99fa-64e532a5b83f)

Run de0.py:

```python de0.py```


![image](https://github.com/madecero/de0/assets/59320522/4fff141a-8cf4-48b5-9d18-aa4dabf88987)

<hr/>

## Disclaimer ⚠️

It's highly recommended that you keep track of your API costs on [the Usage page](https://platform.openai.com/account/usage).
    You can also set limits on how much you spend on [the Usage limits page](https://platform.openai.com/account/billing/limits).

I use de0 regularly, and my cost tends to be less than $2 a month. That said, as a best practice, you should monitor your API usage costs closely.

Hope you enjoy de0. Forgive my print statements on top of the program. You can remove those. I am just having fun :)
