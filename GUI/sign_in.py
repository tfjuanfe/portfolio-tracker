from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                              QPushButton, QVBoxLayout, QHBoxLayout,
                              QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Database.db_manager import Database_Manager


class SignIn(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database_Manager()
        self.setWindowTitle("bipo")
        self.setFixedSize(500, 550)
        self.setup_ui()

    def field_style(self):
        return """
            QLineEdit {
                background-color: #F0F0F0;
                border: none;
                border-radius: 21px;
                padding: 0px 18px;
                font-size: 13px;
                color: #333333;
            }
            QLineEdit:focus {
                background-color: #E8E8E8;
            }
        """

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(30, 20, 30, 30)
        outer_layout.setSpacing(10)

        # ── Go Back button top right ──
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        go_back_btn = QPushButton("← Go Back")
        go_back_btn.setFixedSize(100, 35)
        go_back_btn.setCursor(Qt.PointingHandCursor)
        go_back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 17px;
                font-size: 13px;
                color: #333333;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        go_back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(go_back_btn)
        outer_layout.addLayout(top_bar)

        # ── White card ──
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 20px; }")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 30, 40, 40)
        card_layout.setSpacing(0)

        # ── Header: icon + logo + info ──
        header_row = QHBoxLayout()
        login_icon = QLabel("→]")
        login_icon.setStyleSheet("color: #555555; font-size: 18px; background: transparent;")

        logo_row = QHBoxLayout()
        logo_row.setSpacing(6)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 16px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 18, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)

        info_icon = QLabel("i")
        info_icon.setFixedSize(22, 22)
        info_icon.setAlignment(Qt.AlignCenter)
        info_icon.setStyleSheet("""
            color: #555555;
            font-size: 12px;
            font-weight: bold;
            border: 2px solid #555555;
            border-radius: 11px;
            background: transparent;
        """)

        header_row.addWidget(login_icon)
        header_row.addStretch()
        header_row.addLayout(logo_row)
        header_row.addStretch()
        header_row.addWidget(info_icon)
        card_layout.addLayout(header_row)

        card_layout.addSpacing(4)

        # ── Tagline ──
        tagline = QLabel("Intelligent Investing. Simplified.")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        card_layout.addWidget(tagline)

        card_layout.addSpacing(12)

        # ── Main heading ──
        heading = QLabel("Create your account")
        heading.setFont(QFont("Arial", 20, QFont.Bold))
        heading.setAlignment(Qt.AlignCenter)
        heading.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(heading)

        card_layout.addSpacing(4)

        subtitle = QLabel("Start managing your investments with confidence")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(20)

        # ── Username ──
        user_label = QLabel("Username")
        user_label.setFont(QFont("Arial", 10, QFont.Bold))
        user_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(user_label)

        card_layout.addSpacing(5)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        self.username_input.setFixedHeight(42)
        self.username_input.setStyleSheet(self.field_style())
        card_layout.addWidget(self.username_input)

        card_layout.addSpacing(14)

        # ── Password ──
        pass_label = QLabel("Password")
        pass_label.setFont(QFont("Arial", 10, QFont.Bold))
        pass_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(pass_label)

        card_layout.addSpacing(5)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Choose a password")
        self.password_input.setFixedHeight(42)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.field_style())
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(14)

        # ── Confirm Password ──
        confirm_label = QLabel("Confirm Password")
        confirm_label.setFont(QFont("Arial", 10, QFont.Bold))
        confirm_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(confirm_label)

        card_layout.addSpacing(5)

        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password")
        self.confirm_input.setFixedHeight(42)
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setStyleSheet(self.field_style())
        card_layout.addWidget(self.confirm_input)

        card_layout.addSpacing(24)

        # ── Sign-Up button ──
        self.signup_button = QPushButton("Sign-Up")
        self.signup_button.setFixedHeight(45)
        self.signup_button.setCursor(Qt.PointingHandCursor)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #F5C518;
                color: #1A1A2E;
                border: none;
                border-radius: 22px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0B200; }
            QPushButton:pressed { background-color: #C9A000; }
        """)
        self.signup_button.clicked.connect(self.handle_signup)
        card_layout.addWidget(self.signup_button)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def handle_signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm  = self.confirm_input.text().strip()

        if not username or not password or not confirm:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return

        if self.db.register_user(username, password):
            QMessageBox.information(self, "Success", "Account created! You can now log in.")
            self.go_back()
        else:
            QMessageBox.warning(self, "Error", "Username already exists")

    def go_back(self):
        try:
            from login_window import LoginWindow
            self.login = LoginWindow()
            self.login.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignIn()
    window.show()
    sys.exit(app.exec_())