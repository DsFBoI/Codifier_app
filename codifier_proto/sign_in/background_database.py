import sys
import sqlite3
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QFileDialog, QApplication, QLineEdit, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PIL import Image

# Path to your codifier_proto directory
folder_2_dir = r"C:\Users\d.sanchez.ferrari\OneDrive - Accenture\Documents\Tfg\Codifier_app\codifier_proto"
sys.path.append(folder_2_dir)

from encoder_code import decoder  # Assuming 'decoder' is a module inside 'encoder_code'


class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Drop Image Here")
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #aaa; background-color: #f9f9f9;")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                selected_image_path = url.toLocalFile()
                if selected_image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                    self.parent().display_image(selected_image_path)
                    self.parent().selected_image_path = selected_image_path
                    self.hide()  # Hide the drop label after the image is dropped


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # Initialize UI
        self.setWindowTitle('Login with Photo')
        self.setWindowIcon(QIcon('C:/Users/d.sanchez.ferrari/OneDrive - Accenture/Documents/Tfg/Codifier_app/codifier_proto/images/OIP.png'))

        self.selected_image_path = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Create a text field for username
        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        layout.addWidget(self.username_field, alignment=Qt.AlignCenter)

        # Create a drop label for dropping images
        self.drop_label = DropLabel(self)
        layout.addWidget(self.drop_label, alignment=Qt.AlignCenter)

        # Create a button for uploading images
        upload_button = QPushButton('Upload Image', self)
        upload_button.clicked.connect(self.upload_image)
        layout.addWidget(upload_button, alignment=Qt.AlignCenter)

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)  # Fixed size for the image label
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)

        # Create a button for login
        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def upload_image(self):
        # Open a file dialog to select an image
        self.selected_image_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", "", "Image files (*.jpg *.jpeg *.png *.bmp)"
        )
        if self.selected_image_path:
            self.display_image(self.selected_image_path)

    def display_image(self, image_path):
        # Open the image file and resize it for display
        img = Image.open(image_path)
        img.thumbnail((300, 300))  # Resize image to fit within the PyQt window

        # Save as temporary image
        img.save('temp_login_image.png')
        pixmap = QtGui.QPixmap('temp_login_image.png')

        # Display the image
        self.image_label.setPixmap(pixmap)

    def login(self):
        username = self.username_field.text().strip()
        if not username:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter your username.")
            return

        if not self.selected_image_path:
            QtWidgets.QMessageBox.warning(self, "Error", "Please upload or drop an image to login.")
            return

        # Fetch user details from the database
        user = self.get_user_from_db(username)
        if not user:
            QtWidgets.QMessageBox.warning(self, "Error", "Username not found.")
            return

        # Decode the image to extract the hidden password
        decoded_password = decoder.decode(self.selected_image_path)

        # Validate the password
        if decoded_password == user['encoded_password']:
            QtWidgets.QMessageBox.information(self, "Login Successful", f"Welcome, {username}!")
            self.accept()  # Close the login dialog and proceed to the main app
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid password.")

    def get_user_from_db(self, username):
        # Fetch the user information from the database
        conn = sqlite3.connect('user_database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user:
            return {'id': user[0], 'username': user[1], 'encoded_password': user[2]}
        return None


class PicPassApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main App')
        self.setWindowIcon(QIcon('C:/Users/d.sanchez.ferrari/OneDrive - Accenture/Documents/Tfg/Codifier_app/codifier_proto/images/OIP.png'))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to the Main App!"))
        self.setLayout(layout)


def main():
    app = QApplication(sys.argv)
    
    # Create login dialog
    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        # If login is successful, open the main app window
        window = PicPassApp()
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
