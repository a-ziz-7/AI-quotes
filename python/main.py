import google.generativeai as palm
import os
api_key = "AIzaSyC_Kvq8rIPjHMuVOCqXc5ywq57Ju57LhpI"
palm.configure(api_key=api_key)
# personalized meme generator

# models = [_ for _ in palm.list_models()]
# for i in models:
#     print(i.name)

# Text
model_id = "models/text-bison-001"
# prompt = "Generate 1 sentence meme joke related to mountains. Without a question" 
prompt = "Generate 1 sentence - unique philosophical quote."
example = [("prompt","responce")]

def generate_text(prompt):
    completion = palm.generate_text(
        # max_output_tokens=1000,
        model=model_id, 
        prompt=prompt,
        temperature=0.7,
        candidate_count=8,
    )
    if len(completion.candidates) == 0:
        return "Cannot generate text."
    else:
        return completion
    

def chopchop(sentence):
    pass


os.system('clear')
# chatboе
# while prompt != "exit":
#     prompt = input("Enter your prompt: ")
completion = generate_text(prompt)
# completion.reply("promt")

# one case
# candidates = [i['output'] for i in completion.candidates][0]
# print(candidates)

# many case
candidates = [i['output'] for i in completion.candidates]
for i in candidates:
    print(i)