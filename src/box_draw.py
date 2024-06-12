import cv2
import json
import os

def draw_boxes(image_path, annotation_path, color=(0, 255, 0), thickness=2):

  # Read the image
  image = cv2.imread(image_path)

  # Check if image is read
  if image is None:
    print(f"Error: Could not read image from {image_path}")
    return

  # Read the annotations from the JSON file
  try:
    with open(annotation_path, 'r') as f:
      annotations = json.load(f)
  except FileNotFoundError:
    print(f"Error: Annotation file not found at {annotation_path}")
    return
  except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in annotation file {annotation_path}")
    return

  # Draw boxes for each annotation
  for annotation in annotations:
    x = annotation['x']
    y = annotation['y']
    width = annotation['width']
    height = annotation['height']
    concept = annotation['concept']

    # Ensure coordinates and dimensions are within image bounds
    if x < 0 or y < 0 or x + width > image.shape[1] or y + height > image.shape[0]:
      print(f"Warning: Skipping annotation with invalid coordinates or dimensions ({x}, {y}, {width}, {height})")
      continue

    # Draw the bounding box
    top_left = (x, y)
    bottom_right = (x + width, y + height)
    cv2.rectangle(image, top_left, bottom_right, color, thickness)
    cv2.putText(image, concept, (x, y - 10), fontFace=1, fontScale=1.0, color=color)

  # Display the image with drawn boxes
  cv2.imshow('Image with Boxes', image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

# Get image and annotation directory paths (modify as needed)
image_dir = "images"
annotation_dir = "annotations"

# Iterate through all image files
for image_filename in os.listdir(image_dir):
  # Construct image and annotation paths
  image_path = os.path.join(image_dir, image_filename)
  annotation_path = os.path.join(annotation_dir, os.path.splitext(image_filename)[0] + ".json")

  # Draw boxes on the current image
  draw_boxes(image_path, annotation_path)

print("Finished processing all images!")