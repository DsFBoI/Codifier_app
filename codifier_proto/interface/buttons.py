import sys
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QTextEdit, QFileDialog, QApplication
from PyQt5.QtCore import Qt  # Import Qt for using Qt constants
from PyQt5.QtGui import QIcon
from PIL import Image

# Corrected Absolute path to folder_2 where encoder_code is located
folder_2_dir = r"C:\Users\d.sanchez.ferrari\OneDrive - Accenture\Documents\Tfg\Codifier_app\codifier_proto"

# Add the directory to sys.path
sys.path.append(folder_2_dir)

# Now import your modules
from encoder_code import encoder  # Assuming 'encoder' is a module inside 'encoder_code'
from encoder_code import decoder  # Similarly for 'decoder'

class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drop Image Here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; background-color: #f9f9f9;")  # Styling the drop area
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                selected_image_path = url.toLocalFile()
                if selected_image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    self.parent().display_image(selected_image_path)  # Call the parent method to display the image
                    self.parent().selected_image_path = selected_image_path  # Update the selected image path
                    self.hide()  # Hide the drop area after the image is dropped

class PicPassApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize UI components
        self.init_ui()
        
        # Initialize variables
        self.selected_image_path = None
        self.modified_image_path = None

    def init_ui(self):
        self.setWindowTitle('PicPass')

        # Set application icon (Update the path to your icon image file)
        self.setWindowIcon(QIcon('C:/Users/d.sanchez.ferrari/OneDrive - Accenture/Documents/Tfg/Codifier_app/codifier_proto/images/OIP.png'))

        # Create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Center items vertically

        # Create a text box for input
        self.text_box = QTextEdit(self)
        self.text_box.setFixedHeight(30)
        self.text_box.setFixedWidth(300)  # Set fixed width for consistency
        layout.addWidget(self.text_box, alignment=Qt.AlignCenter)

        # Create a drop label for dropping images
        self.drop_label = DropLabel(self)
        layout.addWidget(self.drop_label, alignment=Qt.AlignCenter)

        # Create a button for uploading images
        upload_button = QPushButton('Upload Image', self)
        upload_button.clicked.connect(self.upload_image)
        layout.addWidget(upload_button, alignment=Qt.AlignCenter)

        # Create a button to send the text and process the image
        send_button = QPushButton('Enviar', self)
        send_button.clicked.connect(self.enviar_texto)
        layout.addWidget(send_button, alignment=Qt.AlignCenter)

        # Create a label to display the image
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Create a button to download the encoded image
        download_button = QPushButton('Download Image', self)
        download_button.clicked.connect(self.download_image)
        layout.addWidget(download_button, alignment=Qt.AlignCenter)

        # Set layout to the main widget
        self.setLayout(layout)

    def enviar_texto(self):
        texto = self.text_box.toPlainText().strip()  # Get the text from the text box
        if texto and self.selected_image_path:  # Only send if there is text and an image selected
            print("Nueva contraseña imagen:", texto)
            self.text_box.clear()  # Clear the text box after sending

            # Path to save the encoded image
            self.modified_image_path = './codifier_proto/images/passimg.png'

            # Encode the image with the text
            encoder.encode(self.selected_image_path, texto, self.modified_image_path)

            # Display the modified encoded image
            self.display_image(self.modified_image_path)

    def upload_image(self):
        # Open a file dialog to select an image
        self.selected_image_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)"
        )
        if self.selected_image_path:
            self.display_image(self.selected_image_path)

    def display_image(self, image_path):
        # Open the image file and get its size
        img = Image.open(image_path)
        original_size = img.size  # Get original size (width, height)

        # Resize the image to fit within the screen while maintaining the aspect ratio
        max_size = 800  # Set a maximum size for display
        img.thumbnail((max_size, max_size))  # Resize image while maintaining aspect ratio

        # Convert the image to a format PyQt can use
        img.save('temp_image.png')  # Save as a temporary file for loading
        pixmap = QtGui.QPixmap('temp_image.png')

        # Update the label size to fit the image
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())  # Set label size to the image size

    def download_image(self):
        if self.modified_image_path:
            # Ask the user where to save the modified image
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save Encoded Image", "", "PNG files (*.png);;JPEG files (*.jpg);;All files (*.*)"
            )
            if save_path:
                # Copy the modified image to the selected path
                img = Image.open(self.modified_image_path)
                img.save(save_path)
                print(f"Image saved to {save_path}")
        else:
            print("No modified image to download.")

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PicPassApp()
    window.show()
    sys.exit(app.exec_())
