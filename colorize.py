import requests
import os
from pdb import set_trace as stx
from tqdm import tqdm

url = "http://127.0.0.1:8080/upload"

file_path_dir = "test_images"
output_dir = "output"
os.makedirs("output", exist_ok=True)

# get all files in the test_images folder
files = os.listdir(file_path_dir)

total = len(files)

for i, file_path in enumerate(tqdm(files)):
    print(f"Processing: {file_path}")
    # Open the image file
    with open(f"{file_path_dir}/{file_path}", "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)

    # Get original image name
    file_name = os.path.basename(file_path)
    # Colorized file name should be like img_1_colorized.jpg
    file_name = file_name.split(".")[0] + "_colorized.jpg"

    if response.status_code == 200:
        with open(f"output/{file_name}", "wb") as file:
            file.write(response.content)
        print("Image saved successfully")
    else:
        print("Error:", response.text)
