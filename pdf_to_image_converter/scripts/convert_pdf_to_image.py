from syncano.models import Object
from tempfile import *
import syncano
import requests
import zipfile
import tempfile
import os

syncano.connect(api_key="SYNCANO ACCOUNT KEY")

file_url = ARGS.get('file_url', None)
if file_url is None:
    raise ValueError("You didn't pass file_url to your CodeBox Execution")

# gets pdf file from url
pdf_file = requests.get(file_url)

# set up temporary directory and save the pdf file in it
temp_directory = tempfile.mkdtemp()
pdf_file_name = temp_directory + "/pdf_file.pdf"
f = open(pdf_file_name, "wb")
f.write(pdf_file.content)
f.close()


# make request for conversion and then save contents to zip
headers = {
    # Get your mashape api key here, make sure to sign up for a mashape account
    # first. Replace username in the link below with your mashape username
    # and get your key!
    # https://www.mashape.com/YOUR_USERNAME/applications/default-application
    "X-Mashape-Key": "PLACE API KEY HERE",
}
data = {
    'OutputFormat': 'jpg'
}
files = {
  'File': open(pdf_file_name, "r")  # open("pdf_file.pdf", mode="r")
}

# You also need an api key from convertapi
# sign up for an account and get it here!
# http://www.convertapi.com/a
# It should look something like this: 199769741
convertapi_api_key = 'PLACE API KEY HERE'
url = "https://convertapi-pdf2image.p.mashape.com/?ApiKey="+convertapi_api_key
# We receive converted images in a zip file
converted_zip_file = requests.post(url=url,
                                   headers=headers,
                                   data=data,
                                   files=files)

# Save zip file to temp directory so that we can unzip it later
image_zip_file_name_and_location = temp_directory + "/images.zip"
with open(image_zip_file_name_and_location, "wb") as zippyfile:
    zippyfile.write(converted_zip_file.content)

# Unzip the file we placed in the temp directory
extracted_location = temp_directory + "/image_file"
with zipfile.ZipFile(image_zip_file_name_and_location, "r") as z:
    z.extractall(extracted_location)

# Get and save individual images to Syncano
page_number = 1
for image in files:
    print image
    image_path = extracted_location + "/" + image
    image_file = open(image_path, "r")
    Object.please.create(instance_name="dry-sunset-9045",
                         class_name="image",
                         image=image_file,
                         page_number=page_number,
                         file_url=file_url
                         )
    page_number += 1
    image_file.close()

'''
For this solution, you will need an api key from here

https://www.mashape.com/YOUR_USERNAME/applications/default-application
Insert it into line 32 where it says 'PLACE API KEY HERE'

and from here

http://www.convertapi.com/a
Insert it into line 45 where it says 'PLACE API KEY HERE'


This solution will save the images under a class called image
If you want to filter and get objects for only a certain pdf file url,
You can later do it like so

images = Object.please.list(instance_name="INSTANCE_NAME",
                            class_name="image").filter(file_url__eq=URL_OF_FILE)

Replace URL_OF_FILE with the pdf file name you want to retrieve by

For further customizeablity in converting PDFs, check out
http://www.convertapi.com/pdf-image-api


##### python code example #####

from syncano.models.base import *
import syncano

syncano.connect(api_key=ACCOUNT_KEY)

CodeBox.please.run(id=CODEBOX_ID,
                   instance_name=INSTANCE_NAME,
                   payload={'file_url': 'http://www.pdfwatermarkremover.com/PDF-Watermark-Sample.pdf'})
'''