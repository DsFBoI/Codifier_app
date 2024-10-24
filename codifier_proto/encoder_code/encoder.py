from PIL import Image
from stegano import lsb
import random
import base64
import quopri

def encode(image_path, password, output_image_path):
    # Generate a random numcode (6-digit random number)
    num_encode = str(random.randrange(100000, 999999))
    
    # Encode the password based on numcode
    encoded_password = encode_pass(password, num_encode)
    
    # Combine num_encode and the encoded password as a single string
    secret_message = num_encode + ":" + encoded_password
    
    # Hide the combined secret (num_encode + encoded password) inside the image
    secret_image = lsb.hide(image_path, secret_message)
    
    # Save the output image with the hidden secret
    secret_image.save(output_image_path)
    print(encoded_password)
    print(num_encode)
    print(f"Password embedded and image saved as {output_image_path}")

def encode_pass(password, numcode):
    # Iterate through the numcode to encode the password
    for num in numcode:
        if num == '0':
            password = password.encode('utf-8').decode('latin1')
        elif num == '1':
            password = password.encode('utf-16').decode('latin1')
        elif num == '2':
            password = password.encode('utf-16').decode('latin1')
        elif num == '3':
            password = password.encode('iso-8859-1').decode('latin1')
        elif num == '4':
            password = base64.b64encode(password.encode()).decode('latin1')
        elif num == '5':
            password = password.encode().hex()
        elif num == '6':
            password = quopri.encodestring(password.encode()).decode('latin1')
        elif num == '7':
            password = password.encode('iso-8859-1').decode('latin1')
        elif num == '8':
            password = password.encode('utf-16').decode('latin1')
        elif num == '9':
            password = password.encode('utf-16').decode('latin1')

    return password







