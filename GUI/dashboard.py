from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
                              QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class Dashboard(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("bipo")
        self.setFixedSize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 30, 40, 30)
        outer_layout.setSpacing(30)

        # ════════════════════════════
        #         TOP BAR
        # ════════════════════════════
        top_bar = QHBoxLayout()
        top_bar.setSpacing(0)

        # ── Logo ──
        logo_row = QHBoxLayout()
        logo_row.setSpacing(8)
        logo_row.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 22px;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 20, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)

        # ── Welcome message ──
        welcome_label = QLabel(f"Welcome Back, {self.username}.")
        welcome_label.setFont(QFont("Arial", 26, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: #1A1A2E;")

        # ── Log-Out button ──
        logout_btn = QPushButton("Log-Out")
        logout_btn.setFixedSize(100, 35)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1A1A2E;
                border: none;
                border-radius: 17px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
            QPushButton:pressed { background-color: #e0e0e0; }
        """)
        logout_btn.clicked.connect(self.handle_logout)

        top_bar.addLayout(logo_row)
        top_bar.addStretch()
        top_bar.addWidget(welcome_label)
        top_bar.addStretch()
        top_bar.addWidget(logout_btn)
        outer_layout.addLayout(top_bar)

        # ════════════════════════════
        #       FEATURE CARDS GRID
        # ════════════════════════════
        grid = QGridLayout()
        grid.setSpacing(20)

        cards = [
            ("📊", "Asset Manager",
             "Manage all your assets! Add, delete, modify,\nand change your assets here!",
             self.open_asset_manager),
            ("📰", "Financial News",
             "Stay up-to-date by seeing the latest\nfinancial news here!",
             self.open_news),
            ("💡", "Portfolio Insights",
             "Analytics, charts, graphs, and portfolio\nreturns can be consulted here.",
             self.open_portfolio),
            ("📈", "Trading and Analytics",
             "Set up automated trading rules and\nanalyze market trends.",
             self.open_trading),
        ]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for (row, col), (icon, title, desc, handler) in zip(positions, cards):
            card = self.make_feature_card(icon, title, desc, handler)
            grid.addWidget(card, row, col)

        outer_layout.addLayout(grid)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

# ── Start alert checker in background ──
        from Logic.alert_system import AlertChecker
        self.alert_checker = AlertChecker(self.username)
        self.alert_checker.alert_triggered.connect(self.show_alert_notification)
        self.alert_checker.start()
    
    def show_alert_notification(self, ticker, current, target, condition):
        try:
            from plyer import notification
            notification.notify(
                title    = f"🚨 BIPO PRICE ALERT — {ticker}",
                message  = (f"{ticker} has gone {condition} your target!\n"
                            f"Target: ${target:,.2f}\n"
                            f"Current: ${current:,.2f}"),
                app_name = "bipo",
                timeout  = 10
            )
        except Exception:
            pass

        QMessageBox.warning(
            self,
            f"🚨 Price Alert — {ticker}",
            f"{ticker} is now ${current:,.2f}\n"
            f"Your target was {condition} ${target:,.2f}"
        )

    def make_feature_card(self, icon, title, desc, handler):
        card = QFrame()
        card.setFixedSize(380, 180)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
            }
            QFrame:hover {
                background-color: #FAFAFA;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(10)

        # ── Icon in yellow circle ──
        icon_label = QLabel(icon)
        icon_label.setFixedSize(55, 55)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            background-color: #FFF3CC;
            border-radius: 27px;
            font-size: 24px;
        """)

        # ── Title ──
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #1A1A2E; background: transparent;")

        # ── Description ──
        desc_label = QLabel(desc)
        desc_label.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        desc_label.setWordWrap(True)

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addStretch()
        card.setLayout(layout)

        # ── Make whole card clickable ──
        card.mousePressEvent = lambda event: handler()

        return card

    def handle_logout(self):
        reply = QMessageBox.question(
            self, "Log Out",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                from welcome_screen import WelcomeScreen
                self.welcome = WelcomeScreen()
                self.welcome.show()
                self.close()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def open_asset_manager(self):
        try:
            from asset_manager import AssetManager
            self.asset_manager = AssetManager(self.username)
            self.asset_manager.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_news(self):
        try:
            from news_tab import NewsTab
            self.news = NewsTab(self.username)
            self.news.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_portfolio(self):
        try:
            from portfolio_insights import PortfolioInsights
            self.portfolio = PortfolioInsights(self.username)
            self.portfolio.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_trading(self):
        try:
            from Auto_trading import AutoTrading
            self.trading = AutoTrading(self.username)
            self.trading.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard("Carlos")
    window.show()
    sys.exit(app.exec_())