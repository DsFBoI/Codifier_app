
from PIL import Image
from stegano import lsb

def encode(image_path, password, output_image_path):
    # Hide the password inside the image using LSB steganography
    secret_image = lsb.hide(image_path, password)
    
    # Save the output image with the hidden password
    secret_image.save(output_image_path)
    print(f"Password embedded and image saved as {output_image_path}")






