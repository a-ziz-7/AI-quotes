import keys
import requests
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


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


def main():
    for i in range(1):
        random_image = get_random_image()
        image_filename = download_image(random_image)
    

if __name__ == "__main__":
    main()