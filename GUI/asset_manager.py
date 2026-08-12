from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame, QGridLayout,
                              QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class AssetManager(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("bipo")
        self.setFixedSize(650, 550)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(40, 30, 40, 30)
        outer_layout.setSpacing(20)

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
        card_layout.setSpacing(15)

        # ── Header ──
        logo_row = QHBoxLayout()
        logo_row.setSpacing(6)
        logo_row.setAlignment(Qt.AlignCenter)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 18px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 18, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)
        card_layout.addLayout(logo_row)

        tagline = QLabel("Intelligent Investing. Simplified.")
        tagline.setAlignment(Qt.AlignCenter)
        tagline.setStyleSheet("color: #888888; font-size: 11px; background: transparent;")
        card_layout.addWidget(tagline)

        title = QLabel("Asset Manager")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(title)

        card_layout.addSpacing(10)

        # ── 2x2 Grid of feature cards ──
        grid = QGridLayout()
        grid.setSpacing(15)

        features = [
            ("👁", "View Asset",   self.open_view),
            ("✏️", "Modify Asset", self.open_modify),
            ("➕", "Add Asset",    self.open_add),
            ("🗑", "Delete Asset", self.open_delete),
        ]

        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for (row, col), (icon, label, handler) in zip(positions, features):
            btn_card = self.make_card(icon, label, handler)
            grid.addWidget(btn_card, row, col)

        card_layout.addLayout(grid)
        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def make_card(self, icon, label, handler):
        card = QFrame()
        card.setFixedSize(220, 110)
        card.setCursor(Qt.PointingHandCursor)
        card.setStyleSheet("""
            QFrame {
                background-color: #FFF8E1;
                border-radius: 15px;
            }
            QFrame:hover {
                background-color: #FFF3CC;
            }
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignCenter)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 28px; background: transparent;")

        text_label = QLabel(label)
        text_label.setFont(QFont("Arial", 12, QFont.Bold))
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: #1A1A2E; background: transparent;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        card.setLayout(layout)
        card.mousePressEvent = lambda event: handler()
        return card

    def go_back(self):
        try:
            from GUI.dashboard import Dashboard
            self.dashboard = Dashboard(self.username)
            self.dashboard.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def open_view(self):
        from view_assets import ViewAssets
        self.view = ViewAssets(self.username)
        self.view.show()
        self.close()

    def open_modify(self):
        from modify_asset import ModifyAsset
        self.modify = ModifyAsset(self.username)
        self.modify.show()
        self.close()

    def open_add(self):
        from add_asset import AddAsset
        self.add = AddAsset(self.username)
        self.add.show()
        self.close()

    def open_delete(self):
        from delete_asset import DeleteAsset
        self.delete = DeleteAsset(self.username)
        self.delete.show()
        self.close()

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
    window = AssetManager("Carlos")
    window.show()
    sys.exit(app.exec_())