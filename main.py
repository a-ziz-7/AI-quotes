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
prompt = "Generate meme joke related to sports" # input("Enter your prompt: ")


def generate_text(prompt):
    completion = palm.generate_text(
        model=model_id, 
        prompt=prompt,
        temperature=0.99,
        # max_output_tokens=1000,
        candidate_count=1
    )
    if len(completion.candidates) == 0:
        return "Cannot generate text."
    else:
        return completion.candidates
    

os.system('clear')
# chatbot
# while prompt != "exit":
#     prompt = input("Enter your prompt: ")
completion = generate_text(prompt)
candidates = [i['output'] for i in completion] # [0]
print(candidates)