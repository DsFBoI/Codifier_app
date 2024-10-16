import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # To display images in tkinter

# Corrected Absolute path to folder_2 where encoder_code is located
folder_2_dir = r"C:\Users\d.sanchez.ferrari\OneDrive - Accenture\Documents\Tfg\Codifier_app"

# Add the directory to sys.path
sys.path.append(folder_2_dir)

# Now import your modules
from encoder_code import encoder  # Assuming 'encoder' is a module inside 'encoder_code'
from encoder_code import decoder  # Similarly for 'decoder'

def enviar_texto(event=None):
    # Obtiene el texto de la caja de texto
    texto = text_box.get("1.0", tk.END).strip()  # Obtener todo el texto y eliminar espacios
    if texto and selected_image_path:  # Solo enviar si hay texto e imagen seleccionada
        print("Nueva contraseña imagen:", texto)
        text_box.delete("1.0", tk.END)  # Borra el texto en la caja después de enviarlo
        
        # Path to save the encoded image
        global modified_image_path
        modified_image_path = './images/passimg.png'

        # Encode the image with the text (assuming 'encoder.encode' modifies the image and saves it)
        encoder.encode(selected_image_path, texto, modified_image_path)  # Pass output path to save the modified image

        # Display the modified encoded image
        display_image(modified_image_path)

    return "break"  # Evita que se inserte una nueva línea

def upload_image():
    global selected_image_path
    # Open a file dialog to select an image
    selected_image_path = filedialog.askopenfilename(
        title="Select an Image", 
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")]
    )
    if selected_image_path:
        display_image(selected_image_path)

def display_image(image_path):
    # Open the image file and resize it for display
    img = Image.open(image_path)
    img = img.resize((300, 300))  # Resize image to fit within the Tkinter window

    # Convert the image to a format Tkinter can use
    img_tk = ImageTk.PhotoImage(img)

    # Display the image in the label
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

def download_image():
    if modified_image_path:
        # Ask the user where to save the modified image
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Save Encoded Image"
        )
        if save_path:
            # Copy the modified image to the selected path
            img = Image.open(modified_image_path)
            img.save(save_path)
            print(f"Image saved to {save_path}")
    else:
        print("No modified image to download.")

# Create the main window
root = tk.Tk()
root.title("PicPass")

# Create a text box for input
text_box = tk.Text(root, height=1, width=40, bg='lightgray', font=('Arial', 12))
text_box.pack(padx=10, pady=10)

# Create a button for uploading images
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Create a button to send the text and process the image
boton_enviar = tk.Button(root, text="Enviar", command=enviar_texto)
boton_enviar.pack(pady=10)

# Create a label to display the image
image_label = tk.Label(root)
image_label.pack(pady=10)

# Create a button to download the encoded image
download_button = tk.Button(root, text="Download Image", command=download_image)
download_button.pack(pady=10)

# Bind the Enter key to the enviar_texto function
text_box.bind("<Return>", enviar_texto)

# Initialize the selected image path
selected_image_path = None
modified_image_path = None  # To store the path of the modified image

# Start the Tkinter main loop
root.mainloop()
