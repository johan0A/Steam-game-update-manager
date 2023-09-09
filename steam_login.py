import os
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import steam.client


class SteamLoginHandler:
    def __init__(self, sentry_path='sentry.bin'):
        self.steamclient = steam.client.SteamClient()
        self.steamclient.verbose_debug = False
        
        self.sentry_path = sentry_path

        # Set the location where we want to store the sentry file
        self.steamclient.set_credential_location(os.path.dirname(self.sentry_path))

        # Catch the event when a new sentry file is created
        self.steamclient.on('new_login_key', self._save_sentry_file)

    def _save_sentry_file(self, sentry):
        """Save the sentry file when generated."""
        with open(self.sentry_path, 'wb') as f:
            f.write(sentry)

    def login_with_sentry(self):
        """Attempt to login using an existing sentry file."""
        if os.path.exists(self.sentry_path):
            return self.steamclient.relogin()

    def login(self, username, password, two_factor_code=None):
        """Attempt to login to Steam with user credentials."""
        result = self.steamclient.login(username, password, two_factor_code=two_factor_code)
        return result

    def get_client(self):
        """Return the Steam client object."""
        return self.steamclient

    def check_client_validity(self):
        """Placeholder function to check if the client is still valid."""
        # TODO: Implement logic to verify client's validity
        return True


class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.steam_handler = SteamLoginHandler()

        # Check if we can use an existing sentry file to login
        if self.steam_handler.login_with_sentry():
            if self.steam_handler.check_client_validity():
                # Client is valid, no need to show login window
                self.close()
                return

        # UI Elements for login window (will only show if sentry login fails)
        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.two_fa_label = QLabel('2FA Code (if needed):', self)
        self.two_fa_input = QLineEdit(self)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.attempt_login)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.two_fa_label)
        layout.addWidget(self.two_fa_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        two_fa_code = self.two_fa_input.text() or None

        result = self.steam_handler.login(username, password, two_factor_code=two_fa_code)

        if result == steam.enums.EResult.OK:
            QMessageBox.information(self, "Success", "Logged in successfully!")
            self.close()  # This will close the login window
        else:
            QMessageBox.warning(self, "Error", f"Login failed with result: {result}")

    def get_client(self):
        """Return the Steam client object from the handler."""
        return self.steam_handler.get_client()
