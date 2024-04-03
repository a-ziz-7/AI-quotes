import keys
import requests
import random
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def get_random_image(width=1080, height=1920):
    url = f'https://api.unsplash.com/photos/random/?client_id={keys.api_key_unsplash}&w={width}&h={height}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data['urls']['regular']
        
        # Check if the image dimensions match the specified width and height
        if data['width'] == width and data['height'] == height:
            return image_url
        else:
            print("Fetched image does not match the specified dimensions. Fetching another image...")
            return get_random_image(width, height)  # Fetch another random image
    else:
        print(f"Failed to fetch image. Error: {response.status_code}")
        return None
    

def download_image(image_url, folder='my_images'):
    try:
        filename = os.path.join(folder, f'image_{random.randint(1, 10000)}.jpg')  # Generate a random filename
        with open(filename, 'wb') as f:
            response = requests.get(image_url)
            f.write(response.content)
        return filename
    except Exception as e:
        print(f"Failed to download image. Error: {e}")
        return None


def main():
    for i in range(1000):
        random_image = get_random_image()
        image_filename = download_image(random_image)
    

if __name__ == "__main__":
    main()