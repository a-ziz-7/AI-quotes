import google.generativeai as palm
import keys
import requests
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


palm.configure(api_key=keys.api_key_ai)


model_id = "models/text-bison-001"
prompt = "Generate 1 short sentence - unique philosophical motivatonal quote"


def generate_text(prompt):
    completion = palm.generate_text(
        # max_output_tokens=1000,
        model=model_id, 
        prompt=prompt,
        temperature=0.7,
        candidate_count=2,
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
    if answer == "":
        answer = sentence
    splited = answer.split(" ")
    max_len = 44
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
    ret = ((max_len-len(ret1))/2)*" "+ret1+((max_len-len(ret2))/2)*" "+ret2
    punctuation = ["!", "?", ";", ":", "*"]
    for i in punctuation:
        ret = ret.replace(i, "")
    ret = ret.strip()[:-1]
    return ret


def get_random_image(width=1704, height=2272):
    url = f'https://api.unsplash.com/photos/random/?client_id={keys.api_key_unsplash}&w={width}&h={height}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        return image_url
    else:
        print(f"Failed to fetch image. Error: {response.status_code}")
        return None
    

def download_image(image_url, output_path="my_images/", width=1704, height=2272):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = Image.open(BytesIO(response.content))
            image_resized = image_data.resize((width, height), Image.LANCZOS)
            output_path = os.path.join(output_path, f"image_{random.randint(1, 10000)}.jpg")
            image_resized.save(output_path)
            return output_path
        else:
            print(f"Failed to download image from {image_url}. Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Failed to resize image. Error: {e}")
        return None


def write_text_on_image(image_path, text, output_path):
    try:
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font_size = 85
        font = ImageFont.load_default()
        font = font.font_variant(size=font_size)
        draw.text((0, 2000), text, fill="white", font=font)
        output_path += "/quote_"+image_path.split("_")[-1]
        image.save(output_path)
    except:
        print("Failed to write text on image.")


def main():
    output_path = "my_quotes"

    completion = generate_text(prompt)

    candidates = [i['output'] for i in completion.candidates]
    for i in candidates:
        random_image = get_random_image()
        image_filename = download_image(random_image)
        print(chopchop(i))
        write_text_on_image(image_filename, chopchop(i), output_path)
    

if __name__ == "__main__":
    main()