# ScriptWriter Chatbot

### Project Info

Streamlit App that utilizes the OpenAI's GPT-4 model to generate scripts for YouTube and SnapChat channels. The generated scripts have a balance of information and entertainment, keeping viewers engaged.

There are 4 types of scripts that could be generated:
* **List Script for YouTube** (e.g. "10 Famous American Motorcyclists") - about 5K words
* **Story Script for YouTube** (e.g. "What really happened at Pablo Escobar’s funeral?") - about 5K words
* **List Script for SnapChat** (e.g. "Top 10 movie scenes that became internet memes")- about 750 words
* **Story Script for SnapChat** (e.g. "The man who transformed himself into a dog") - about 750 words

### Demo
https://www.loom.com/share/8aab1482c03a4cdfbf338f66cb7a64f7?sid=56705dea-2481-472b-acc3-156fbc20b21a 



### How to use

1. Set environment variables (OpenAI API key) in .env

```
cp .env-template .env
```

2. Install requirements

```
pip install -r requirements.txt
```

3. Run streamlit

```
streamlit run script_bot.py
```
