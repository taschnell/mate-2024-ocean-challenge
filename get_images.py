import json
import os
import requests


def download_image(url, filename, image_dir="images"):
    try:
        os.makedirs(image_dir, exist_ok=True)

        filepath = os.path.join(image_dir, filename)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        extension = response.headers.get("Content-Type", "").split("/")[-1]

        # These should really all be PNG's
        filename = f"{filename}.{extension}" if extension else f"{filename}.jpg"
        
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image downloaded: {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")


with open("data\Ophiuroidea.json", "r") as f:
    data = json.load(f)

# Expect 2687 Images
if __name__ == "__main__":
    i = 0
    for item in data:
        i += 1
        image_url = item["url"]
        filename = item["url"].split("/")[-1]

        print(f"{i} | ", end="")
        download_image(image_url, filename)
