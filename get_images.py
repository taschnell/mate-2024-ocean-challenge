import json
import os
import requests
import time


def download_image(url, filename, image_dir=r"src\images"):
    """
    Returns true if the image is downloaded
    """
    filepath = os.path.join(image_dir, filename)

    # Check if the file already exists
    if os.path.isfile(filepath):
        print(f"Image already exists: {filepath} (Skipped)")
        return False

    # Proceed with download if not found
    os.makedirs(image_dir, exist_ok=True)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        extension = response.headers.get("Content-Type", "").split("/")[-1]

        filename = f"{filename}.{extension}"
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        print(f"Image downloaded: {filepath}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

def anotate_image(filename, boxes, annotations_dir=r"src\annotations"):
    filename = f"{filename[:-4]}.json"

    filepath = os.path.join(annotations_dir, filename)

    if os.path.isfile(filepath):
        print(f"Annotation already exists: {filepath} (Skipped)")
        return False
    
    os.makedirs(annotations_dir, exist_ok=True)

    filename = f"{filename}.json"

    with open(filepath, "w") as f:
        json.dump(boxes, f, indent=4)  
    
    return True


with open("data\Ophiuroidea.json", "r") as f:
    data = json.load(f)

# Expect 2687 Images this will take a while depending on internet speed ~13 minutes for me
if __name__ == "__main__":
    start = time.time()
    i = 0
    for item in data:
        i += 1
        image_url = item["url"]
        filename = item["url"].split("/")[-1]
        boxes = item["boundingBoxes"]

        print(f"{i}/2687 | ", end="")
        # Call download_image and handle the return value
        download_image(image_url, filename)
        anotate_image(filename, boxes)

    print(f"Download Completed after {round((time.time()-start)/60,2)} minutes")
