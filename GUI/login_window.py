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


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database_Manager()
        self.setWindowTitle("bipo")
        self.setFixedSize(500, 560)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(30, 20, 30, 30)
        outer_layout.setSpacing(10)

        # ── Go Back button ──
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
        card_layout.setSpacing(12)

        # ── Header row ──
        header_row = QHBoxLayout()
        login_icon = QLabel("→]")
        login_icon.setStyleSheet("color: #555555; font-size: 18px; background: transparent;")
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(6)
        bar_icon = QLabel("▐█▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 20px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 18, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        logo_layout.addWidget(bar_icon)
        logo_layout.addWidget(logo_text)
        info_icon = QLabel("ⓘ")
        info_icon.setStyleSheet("color: #555555; font-size: 18px; background: transparent;")
        header_row.addWidget(login_icon)
        header_row.addStretch()
        header_row.addLayout(logo_layout)
        header_row.addStretch()
        header_row.addWidget(info_icon)
        card_layout.addLayout(header_row)

        # ── Tagline ──
        tagline = QLabel("Intelligent Investing. Simplified.")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        card_layout.addWidget(tagline)

        card_layout.addSpacing(10)

        # ── Welcome Back ──
        welcome = QLabel("Welcome Back!")
        welcome.setFont(QFont("Arial", 22, QFont.Bold))
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(welcome)

        subtitle = QLabel("Log-in to access your investment portfolio.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(15)

        # ── Username ──
        user_label = QLabel("Username:")
        user_label.setFont(QFont("Arial", 11, QFont.Bold))
        user_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(user_label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedHeight(42)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: none;
                border-radius: 21px;
                padding: 0px 18px;
                font-size: 13px;
                color: #333333;
            }
            QLineEdit:focus { background-color: #E8E8E8; }
        """)
        card_layout.addWidget(self.username_input)

        card_layout.addSpacing(5)

        # ── Password ──
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 11, QFont.Bold))
        password_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(42)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: none;
                border-radius: 21px;
                padding: 0px 18px;
                font-size: 13px;
                color: #333333;
            }
            QLineEdit:focus { background-color: #E8E8E8; }
        """)
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(20)

        # ── Log-In button ──
        self.login_button = QPushButton("Log-In")
        self.login_button.setFixedHeight(45)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_button)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if self.db.login_user(username, password):
            self.open_dashboard(username)
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def go_back(self):
        try:
            from welcome_screen import WelcomeScreen
            self.welcome = WelcomeScreen()
            self.welcome.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_dashboard(self, username):
        from dashboard import Dashboard
        self.dashboard = Dashboard(username)
        self.dashboard.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())