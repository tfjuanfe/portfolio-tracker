from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame,
                              QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Logic.news_fetcher import get_financial_news

class NewsFetcher(QThread):
    news_ready = pyqtSignal(list)

    def run(self):
        articles = get_financial_news()  
        self.news_ready.emit(articles)


class NewsTab(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("bipo")
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.fetch_news()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 20, 40, 30)
        outer_layout.setSpacing(15)

        # ── Go Back ──
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

        # ── Header card ──
        header_card = QFrame()
        header_card.setFixedHeight(75)
        header_card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(25, 15, 25, 15)

        logo_row = QHBoxLayout()
        logo_row.setSpacing(6)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 16px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 16, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)

        title = QLabel("Financial News")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1A1A2E; background: transparent;")

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setFixedSize(100, 32)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5C518;
                color: #1A1A2E;
                border: none;
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0B200; }
        """)
        refresh_btn.clicked.connect(self.fetch_news)

        header_layout.addLayout(logo_row)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)
        header_card.setLayout(header_layout)
        outer_layout.addWidget(header_card)

        # ── Status label ──
        self.status_label = QLabel("Loading latest news...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #888888; font-size: 12px;")
        outer_layout.addWidget(self.status_label)

        # ── Scroll area for articles ──
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("""
            QScrollArea { background: transparent; border: none; }
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

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.articles_layout = QVBoxLayout()
        self.articles_layout.setSpacing(10)
        self.articles_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_content.setLayout(self.articles_layout)
        self.scroll.setWidget(self.scroll_content)
        outer_layout.addWidget(self.scroll)

        self.setLayout(outer_layout)

    def fetch_news(self):
        self.status_label.setText("Loading latest news...")
        self.clear_articles()
        self.thread = NewsFetcher()
        self.thread.news_ready.connect(self.display_news)
        self.thread.start()

    def clear_articles(self):
        while self.articles_layout.count():
            child = self.articles_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def display_news(self, articles):
        self.clear_articles()

        if not articles:
            self.status_label.setText("Could not load news. Check your API key or internet connection.")
            return

        self.status_label.setText(f"{len(articles)} articles loaded")

        for article in articles:
            card = self.make_article_card(article)
            self.articles_layout.addWidget(card)

        self.articles_layout.addStretch()

    def make_article_card(self, article):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
            QFrame:hover { background-color: #FAFAFA; }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(6)

        # ── Source + date row ──
        meta_row = QHBoxLayout()
        source_label = QLabel(article["source"])
        source_label.setStyleSheet("""
            color: white;
            background-color: #F5C518;
            border-radius: 8px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: bold;
        """)
        source_label.setFixedHeight(20)

        date_label = QLabel(article["publishedAt"])
        date_label.setStyleSheet("color: #AAAAAA; font-size: 10px; background: transparent;")

        meta_row.addWidget(source_label)
        meta_row.addSpacing(8)
        meta_row.addWidget(date_label)
        meta_row.addStretch()
        layout.addLayout(meta_row)

        # ── Title ──
        title_label = QLabel(article["title"])
        title_label.setFont(QFont("Arial", 11, QFont.Bold))
        title_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        # ── Description ──
        if article["description"]:
            desc_label = QLabel(article["description"])
            desc_label.setStyleSheet("color: #666666; font-size: 10px; background: transparent;")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)

        card.setLayout(layout)
        return card

    def go_back(self):
        try:
            from dashboard import Dashboard
            self.dashboard = Dashboard(self.username)
            self.dashboard.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NewsTab("Carlos")
    window.show()
    sys.exit(app.exec_())