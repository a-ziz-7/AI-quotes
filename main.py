import google.generativeai as palm
api_key = "AIzaSyC_Kvq8rIPjHMuVOCqXc5ywq57Ju57LhpI"
palm.configure(api_key=api_key)

# models = [_ for _ in palm.list_models()]
# for i in models:
#     print(i.name)

# Text
model_id = "models/text-bison-001"
prompt = input("Enter your prompt: ")
# prompt = " " # Give me 10 best boooks of all time.

completion = palm.generate_text(
    model=model_id, 
    prompt=prompt,
    temperature=0.99,
    max_output_tokens=800,
    candidate_count=1
)

# while prompt != "exit":
#    prompt = input("Enter your prompt: ")
res = completion.candidates[0]['output']
print(res)