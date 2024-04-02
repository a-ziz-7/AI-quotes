import google.generativeai as palm
import keys
import requests
import random
import os


palm.configure(api_key=keys.api_key_ai)



model_id = "models/text-bison-001"
prompt = "Generate 1 sentence - unique philosophical quote."


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


if False:
    completion = generate_text(prompt)

    candidates = [i['output'] for i in completion.candidates]
    for i in candidates:
        print(i)


def get_random_image():
    url = f'https://api.unsplash.com/photos/random/?client_id={keys.api_key_unsplash}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        return image_url
    else:
        print(f"Failed to fetch image. Error: {response.status_code}")
        return None
    
def download_image(image_url, folder='images'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = os.path.join(folder, f'image_{random.randint(1, 10000)}.jpg')  # Generate a random filename
    with open(filename, 'wb') as f:
        response = requests.get(image_url)
        f.write(response.content)
    return filename

def main():
    random_image = get_random_image()
    image_filename = download_image(random_image)
    print("Random Image URL:", random_image)

if __name__ == "__main__":
    main()