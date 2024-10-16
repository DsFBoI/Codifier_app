from stegano import lsb

def decode(encoded_image_path):
    # Reveal the hidden message (password) from the image
    password = lsb.reveal(encoded_image_path)
    
    return password

