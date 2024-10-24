
from PIL import Image
from stegano import lsb
import random
import base64
import quopri

def decode(image_path):
    # Extract the hidden message from the image (num_encode + encoded password)
    hidden_message = lsb.reveal(image_path)
    
    if hidden_message is None:
        print("No hidden message found in the image.")
        return None
    
    # Separate the num_encode and the encoded password
    num_encode, encoded_password = hidden_message.split(":", 1)
    
    # Decode the password based on num_encode
    decoded_password = decode_pass(encoded_password, num_encode)
    
    return decoded_password

import functools

def decode_pass(encoded_password: str, numcode):
    # Iterate through the numcode to decode the password
    #  fns = [functools.partial(encoded_password.encode, "latin1")]
    for num in reversed(numcode):
        if   num == '0':
            encoded_password = encoded_password.encode('latin1').decode('utf-8')
        elif num == '1':
            encoded_password = encoded_password.encode('latin1').decode('utf-16')
        elif num == '2':
             encoded_password = encoded_password.encode('latin1').decode('utf-16')
        elif num == '3':
            encoded_password = encoded_password.encode('latin1').decode('iso-8859-1')
        elif num == '4':
            encoded_password = base64.b64decode(encoded_password.encode('latin1')).decode('utf-8')
        elif num == '5':
            encoded_password = bytes.fromhex(encoded_password).decode('utf-8')
        elif num == '6':
            encoded_password = quopri.decodestring(encoded_password.encode('latin1')).decode('utf-8')
        elif num == '7':
            encoded_password = encoded_password.encode('latin1').decode('iso-8859-1')
        elif num == '8':
            encoded_password = encoded_password.encode('latin1').decode('utf-16')
        elif num == '9':
            encoded_password = encoded_password.encode('latin1').decode('utf-16')

    return encoded_password


