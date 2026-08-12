from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FAQ(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("bipo")
        self.setFixedSize(750, 550)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 30, 40, 30)
        outer_layout.setSpacing(20)

        # ── Top row: logo + Go Back ──
        top_row = QHBoxLayout()

        logo_row = QHBoxLayout()
        logo_row.setSpacing(6)
        logo_row.setAlignment(Qt.AlignLeft)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 18px;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 16, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)

        top_row.addLayout(logo_row)
        top_row.addStretch()

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
        top_row.addWidget(go_back_btn)
        outer_layout.addLayout(top_row)

        # ── Header card ──
        header_card = QFrame()
        header_card.setFixedHeight(80)
        header_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
            }
        """)
        header_card_layout = QHBoxLayout()
        header_card_layout.setContentsMargins(25, 15, 25, 15)

        header_text_layout = QVBoxLayout()
        header_text_layout.setSpacing(4)

        faq_title = QLabel("Frequently Asked Questions")
        faq_title.setFont(QFont("Arial", 16, QFont.Bold))
        faq_title.setStyleSheet("color: #1A1A2E; background: transparent;")
        header_text_layout.addWidget(faq_title)

        faq_subtitle = QLabel("Have a question about Bipo? Take a look at our FAQ.")
        faq_subtitle.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        header_text_layout.addWidget(faq_subtitle)

        question_icon = QLabel("?")
        question_icon.setFont(QFont("Arial", 36, QFont.Bold))
        question_icon.setStyleSheet("color: #CCCCCC; background: transparent;")
        question_icon.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_card_layout.addLayout(header_text_layout)
        header_card_layout.addStretch()
        header_card_layout.addWidget(question_icon)
        header_card.setLayout(header_card_layout)
        outer_layout.addWidget(header_card)

        # ── FAQ content card with scroll ──
        content_card = QFrame()
        content_card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
            }
        """)
        content_card_layout = QVBoxLayout()
        content_card_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #F0F0F0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 4px;
            }
        """)

        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(25, 20, 25, 20)
        scroll_layout.setSpacing(0)

        faqs = [
            (
                "What is Bipo?",
                "Bipo is a centralized investment and asset manager designed to help you visualize "
                "and keep track of your entire financial portfolio in one place. Whether you have "
                "stocks, cryptocurrency, real estate, or other personal assets, Bipo consolidates "
                "everything into a single, easy-to-use platform."
            ),
            (
                "Does Bipo offer automated trading features?",
                "Yes! Bipo includes an automated buy-and-sell system that helps you execute trades "
                "efficiently without relying on quick reaction times. This feature is designed to "
                "help you capitalize on market opportunities even when you're not actively "
                "monitoring your portfolio."
            ),
            (
                "Is my financial data secure on Bipo?",
                "Absolutely. Bipo implements a secure log-in system to protect your account and "
                "sensitive financial data. We understand that you're managing valuable and personal "
                "information, and security is our top priority."
            ),
            (
                "What types of assets can I track on Bipo?",
                "Bipo supports a wide range of asset types including stocks, cryptocurrency, "
                "real estate, and personal belongings. This allows you to get a complete picture "
                "of your total net worth all in one place."
            ),
            (
                "Where does Bipo get its financial data?",
                "Bipo fetches live stock and crypto prices from trusted financial data providers, "
                "ensuring that your portfolio value is always up to date. News is also sourced "
                "from reliable financial outlets to help you make informed decisions."
            ),
            (
                "Can I add assets that are not on a stock exchange?",
                "Yes. Bipo allows you to manually add personal assets such as real estate, "
                "vehicles, or other valuables. These are factored into your overall portfolio "
                "value alongside your traded assets."
            ),
            (
                "How do I get started with Bipo?",
                "Simply click 'Start Investing' on the welcome screen, create your account, "
                "and log in. From there you can start adding your assets, viewing your portfolio "
                "dashboard, and setting up automated trading preferences."
            ),
        ]

        for i, (question, answer) in enumerate(faqs):
            self.add_faq_item(scroll_layout, question, answer)
            if i < len(faqs) - 1:
                # ── Divider line ──
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setStyleSheet("color: #F0F0F0; background-color: #F0F0F0;")
                line.setFixedHeight(1)
                scroll_layout.addSpacing(12)
                scroll_layout.addWidget(line)
                scroll_layout.addSpacing(12)

        scroll_layout.addStretch()
        scroll_content.setLayout(scroll_layout)
        scroll.setWidget(scroll_content)

        content_card_layout.addWidget(scroll)
        content_card.setLayout(content_card_layout)
        outer_layout.addWidget(content_card)

        self.setLayout(outer_layout)

    def add_faq_item(self, layout, question, answer):
        question_label = QLabel(question)
        question_label.setFont(QFont("Arial", 11, QFont.Bold))
        question_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        question_label.setWordWrap(True)
        layout.addWidget(question_label)

        layout.addSpacing(5)

        answer_label = QLabel(answer)
        answer_label.setStyleSheet("color: #555555; font-size: 11px; background: transparent;")
        answer_label.setWordWrap(True)
        layout.addWidget(answer_label)

    def go_back(self):
        try:
            from GUI.welcome_screen import WelcomeScreen
            self.welcome = WelcomeScreen()
            self.welcome.show()
            self.close()
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FAQ()
    window.show()
    sys.exit(app.exec_())