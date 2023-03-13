import requests

# set up the URL and image file path
url = "http://createDatasetInputs.com"
image_path = "Website/Images/rot.png"

# open the image file and read its contents
with open(image_path, 'rb') as f:
    image_data = f.read()

# set up the HTTP headers
headers = {'Content-Type': 'image/png'}

# send the POST request with the image data and headers
response = requests.post(url, data=image_data, headers=headers)

# check the response status code
if response.status_code == 200:
    print("Image uploaded successfully.")
else:
    print("Error uploading image:", response.status_code)
