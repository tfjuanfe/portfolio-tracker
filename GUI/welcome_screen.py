from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("bipo")
        self.setFixedSize(850, 500)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(50, 40, 40, 40)
        main_layout.setSpacing(40)

        # ════════════════════════════
        #         LEFT SIDE
        # ════════════════════════════
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        left_layout.setAlignment(Qt.AlignTop)

        logo_row = QHBoxLayout()
        logo_row.setSpacing(8)
        logo_row.setAlignment(Qt.AlignLeft)
        bar_icon = QLabel("▐█▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 26px;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 20, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        left_layout.addLayout(logo_row)

        heading1 = QLabel("Intelligent investing.")
        heading1.setFont(QFont("Arial", 28, QFont.Bold))
        heading1.setStyleSheet("color: #1A1A2E;")
        left_layout.addWidget(heading1)

        heading2 = QLabel("Simplified.")
        heading2.setFont(QFont("Arial", 28, QFont.Bold))
        heading2.setStyleSheet("color: #F5C518;")
        left_layout.addWidget(heading2)

        desc = QLabel(
            "A simplified asset manager for high-level\n"
            "investing powered by data-driven analytics.\n"
            "Build wealth with confidence."
        )
        desc.setStyleSheet("color: #444444; font-size: 12px;")
        desc.setWordWrap(True)
        left_layout.addWidget(desc)

        left_layout.addSpacing(20)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(15)
        btn_row.setAlignment(Qt.AlignLeft)

        start_btn = QPushButton("Start Investing")
        start_btn.setFixedSize(160, 45)
        start_btn.setCursor(Qt.PointingHandCursor)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #444444; }
        """)
        start_btn.clicked.connect(self.go_to_signup)

        learn_btn = QPushButton("Learn More")
        learn_btn.setFixedSize(140, 45)
        learn_btn.setCursor(Qt.PointingHandCursor)
        learn_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0DDF0;
                color: #1A1A2E;
                border: none;
                border-radius: 22px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #D0CCE8; }
        """)
        learn_btn.clicked.connect(self.go_to_faq)

        btn_row.addWidget(start_btn)
        btn_row.addWidget(learn_btn)
        left_layout.addLayout(btn_row)
        left_layout.addStretch()

        # ════════════════════════════
        #         RIGHT SIDE
        # ════════════════════════════
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        right_layout.setAlignment(Qt.AlignTop)

        login_row = QHBoxLayout()
        login_row.addStretch()
        login_btn = QPushButton("Log-In")
        login_btn.setFixedSize(90, 35)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1A1A2E;
                border: none;
                border-radius: 17px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        login_btn.clicked.connect(self.go_to_login)
        login_row.addWidget(login_btn)
        right_layout.addLayout(login_row)

        cards_top = QHBoxLayout()
        cards_top.setSpacing(10)
        cards_top.addWidget(self.make_feature_card(
            "📈", "Visualization of asset portfolio value through easy-to-read graphs."
        ))
        cards_top.addWidget(self.make_feature_card(
            "🎯", "Target trade-value setting made by buy-and-sell thresholds customized by the user."
        ))
        right_layout.addLayout(cards_top)

        cards_bottom = QHBoxLayout()
        cards_bottom.setSpacing(10)
        cards_bottom.addWidget(self.make_feature_card(
            "🧠", "Make smart investing decisions by getting relevant up-to-date information."
        ))
        cards_bottom.addWidget(self.make_feature_card(
            "🏠", "Include real-estate assets onto your overall portfolio value."
        ))
        right_layout.addLayout(cards_bottom)
        right_layout.addStretch()

        main_layout.addLayout(left_layout, 55)
        main_layout.addLayout(right_layout, 45)
        self.setLayout(main_layout)

    def make_feature_card(self, icon, text):
        card = QFrame()
        card.setFixedSize(170, 120)
        card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 22px; background: transparent;")
        layout.addWidget(icon_label)
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #444444; font-size: 10px; background: transparent;")
        layout.addWidget(text_label)
        card.setLayout(layout)
        return card

    def go_to_login(self):
        from login_window import LoginWindow
        self.login = LoginWindow()
        self.login.show()
        self.close()

    def go_to_signup(self):
        from sign_in import SignIn
        self.signup = SignIn()
        self.signup.show()
        self.close()

    def go_to_faq(self):
        from FAQ import FAQ
        self.faq = FAQ()
        self.faq.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec_())