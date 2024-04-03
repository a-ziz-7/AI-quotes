import google.generativeai as palm
import keys
import requests
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


palm.configure(api_key=keys.api_key_ai)


model_id = "models/text-bison-001"
prompt = "Generate 1 sentence - unique motivatonal quote"


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
    answer = ""
    state = False
    for i in range(len(sentence)):
        if sentence[i] == "\"":
            state = not state
            continue
        if state:
            answer += sentence[i]
    splited = answer.split(" ")
    max_len = 32
    ret1 = ""
    ret2 = ""
    state = True
    for i in splited:
        if state:
            if len(ret1) + len(i) + 1 <= max_len:
                ret1 += i + " "
            else:
                ret1 += "\n"
                ret2 += i + " "
                state = False
        else:
            ret2 += i + " "
    # print(ret1+ret2)
    ret = (max_len-len(ret1))*" "+ret1+(max_len-len(ret2))*" "+ret2
    punctuation = [".", "!", "?", ";", ":"]
    for i in punctuation:
        ret = ret.replace(i, "")
    return ret


def get_random_image(width=1080, height=1920):
    url = f'https://api.unsplash.com/photos/random/?client_id={keys.api_key_unsplash}&w={width}&h={height}'
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


def write_text_on_image(image_path, text, output_path):
    # print(image_path)
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font_size = 75
    font = ImageFont.load_default()
    font = font.font_variant(size=font_size)
    draw.text((30, 1350), text, fill="white", font=font)
    output_path += "/quote_"+image_path.split("_")[-1]
    image.save(output_path)


def main():
    output_path = "quotes"

    completion = generate_text(prompt)

    candidates = [i['output'] for i in completion.candidates]
    for i in candidates:
        random_image = get_random_image()
        image_filename = download_image(random_image)
        print(chopchop(i))
        write_text_on_image(image_filename, chopchop(i), output_path)
    

if __name__ == "__main__":
    main()