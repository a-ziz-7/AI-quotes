import google.generativeai as palm
import keys
import requests
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def generate_text(prompt):
    model_id = "models/text-bison-001"
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
            state = not state # !state 
            continue
        if state:
            answer += sentence[i]
    if answer == "":
        answer = sentence
    splited = answer.split(" ")
    max_len = 40 # might need to change
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
    ret = ret1 + ret2
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


def write_text_on_image(num, run, image_path, text, output_path):
    try:
        width = 1704
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font_size = 110
        color = 1
        font = ImageFont.truetype("AmericanCaptain-MdEY.otf", size=font_size)
        text_split = text.split("\n")
        text_long = text_split[0] if len(text_split)==1 else text_split[0] if len(text_split[0]) >= len(text_split[1]) else text_split[1]
        font_width, font_height = font.font.getsize(text_long)
        font_width = font_width[0]
        new_width = (width - font_width) // 2
        draw.text((new_width, 2000), text, fill="white", font=font, spacing=30, align="center")
        output_path1 = f"{output_path}quote_{num}{run}{color}.jpg"
        image.save(output_path1)
        
        # 2nd color

        # image = Image.open(image_path)
        # draw = ImageDraw.Draw(image)
        # font = ImageFont.truetype("AmericanCaptain-MdEY.otf", size=font_size)
        # draw.text((new_width, 2000), text, fill="black", font=font, spacing=30, align="center")
        # color += 1
        # output_path2 = f"{output_path}quote_{num}{run}{color}.jpg"
        # image.save(output_path2)

    except:
        print("Failed to write text on image.")


def main():
    palm.configure(api_key=keys.api_key_ai)

    prompt = "Generate 1 short sentence - unique philosophical motivatonal quote"

    f = open("all_quotes/number.txt", "r")
    num = int(f.read())
    path = f"all_quotes/quotes_{num}/"
    os.mkdir(path) 
    output_path = path
    num_images = 3
    

    completion = generate_text(prompt)

    candidates = [i['output'] for i in completion.candidates]
    for i in range(len(candidates)):
        for j in range(num_images):
            random_image = get_random_image()
            image_filename = download_image(random_image)
            write_text_on_image(i+1, j+1, image_filename, chopchop(candidates[i]), output_path)
    
    w = open("all_quotes/number.txt", "w")  
    w.write(str(num+1))  
    f.close()
    w.close()

    
if __name__ == "__main__":
    main()