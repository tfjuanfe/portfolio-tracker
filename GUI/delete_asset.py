from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame,
                              QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))                
from Database.db_manager import Database_Manager


class DeleteAsset(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db = Database_Manager()
        self.setWindowTitle("bipo")
        self.setFixedSize(600, 440)
        self.setup_ui()

    def combo_style(self):
        return """
            QComboBox {
                background-color: #F0F0F0;
                border: none;
                border-radius: 18px;
                padding: 0px 15px;
                font-size: 13px;
                color: #333333;
                height: 40px;
            }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox::down-arrow { image: none; border: none; }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #FFE0E0;
                color: #333333;
            }
        """

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

        # ── White card ──
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 20px; }")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 25, 40, 35)
        card_layout.setSpacing(0)

        # ── Header ──
        header_row = QHBoxLayout()
        header_row.setSpacing(15)

        icon_box = QFrame()
        icon_box.setFixedSize(55, 55)
        icon_box.setStyleSheet("background-color: #FFF3CC; border-radius: 12px;")
        icon_layout = QVBoxLayout()
        icon_label = QLabel("🗑")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 22px; background: transparent;")
        icon_layout.addWidget(icon_label)
        icon_box.setLayout(icon_layout)

        header_text = QVBoxLayout()
        header_text.setSpacing(2)
        sub_label = QLabel("Delete Asset")
        sub_label.setFont(QFont("Arial", 11))
        sub_label.setStyleSheet("color: #888888; background: transparent;")

        logo_row = QHBoxLayout()
        logo_row.setSpacing(6)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 14px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 14, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()

        tagline = QLabel("Intelligent Investing. Simplified.")
        tagline.setStyleSheet("color: #888888; font-size: 10px; background: transparent;")
        title = QLabel("Asset Manager")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #1A1A2E; background: transparent;")

        header_text.addLayout(logo_row)
        header_text.addWidget(tagline)
        header_text.addWidget(title)

        header_row.addWidget(icon_box)
        header_row.addWidget(sub_label)
        header_row.addStretch()
        header_row.addLayout(header_text)
        card_layout.addLayout(header_row)

        card_layout.addSpacing(25)

        # ── Select asset ──
        select_label = QLabel("Select the asset you want to delete")
        select_label.setFont(QFont("Arial", 12, QFont.Bold))
        select_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(select_label)

        card_layout.addSpacing(10)

        self.asset_combo = QComboBox()
        self.asset_combo.setFixedHeight(40)
        self.asset_combo.setStyleSheet(self.combo_style())
        self.load_assets_into_combo()
        card_layout.addWidget(self.asset_combo)

        card_layout.addSpacing(35)

        # ── Delete button ──
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        delete_btn = QPushButton("Delete Asset")
        delete_btn.setFixedSize(180, 45)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #F28B82;
                color: white;
                border: none;
                border-radius: 22px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E07070; }
            QPushButton:pressed { background-color: #C85050; }
        """)
        delete_btn.clicked.connect(self.handle_delete)
        btn_row.addWidget(delete_btn)
        card_layout.addLayout(btn_row)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def load_assets_into_combo(self):
        self.assets = self.db.get_assets(self.username)
        self.asset_combo.clear()
        if not self.assets:
            self.asset_combo.addItem("No assets found")
        else:
            for asset in self.assets:
                self.asset_combo.addItem(f"{asset[2]} — ${asset[4]:,.2f}", userData=asset[0])

    def handle_delete(self):
        if not self.assets:
            QMessageBox.warning(self, "Error", "No assets to delete")
            return

        asset_id   = self.asset_combo.currentData()
        asset_name = self.assets[self.asset_combo.currentIndex()][2]

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{asset_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db.delete_asset(asset_id)
            QMessageBox.information(self, "Success", f"'{asset_name}' deleted successfully!")
            self.load_assets_into_combo()

    def go_back(self):
        try:
            from asset_manager import AssetManager
            self.manager = AssetManager(self.username)
            self.manager.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeleteAsset("Carlos")
    window.show()
    sys.exit(app.exec_())