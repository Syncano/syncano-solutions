from syncano.models import Object
from qrcode import *
import syncano
import StringIO

syncano.connect(api_key="YOUR_API_KEY_HERE")

# Get Unique Data for solution from ARGs
# Unique data can be any String
data = ARGS.get("data", None)
if data is None:
    raise ValueError("You did not pass any data for the QRCode")

# version is size, read more on parameters here
# https://pypi.python.org/pypi/qrcode
qr = QRCode(version=5, error_correction=ERROR_CORRECT_L)  # Generate QRCode object
qr.add_data(data)  # Adds QR code data 

qr.make() # Generate the QRCode itself

# Generate and save image as StringIO file
image = qr.make_image() 
output = StringIO.StringIO()
image.save(output)
contents = output.getvalue()
output.close()

# Save QRCode image to Syncano class "qrcode"
Object.please.create(instance_name="YOUR_INSTANCE_NAME_HERE",
                     class_name="qrcode",
                     image=contents,
                     data=data)


# SYNTAX TO RUN THIS CODEBOX FROM THE PYTHON LIBRARY
'''
from syncano.models.base import *
import syncano

syncano.connect(api_key='your_api_key')

data = "Username: Sansa Stark"
CodeBox.please.run(id=CODEBOX_ID,
                   instance_name=INSTANCE_NAME,
                   payload={'data': 'House Stark'})
'''