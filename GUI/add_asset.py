from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                              QPushButton, QVBoxLayout, QHBoxLayout,
                              QFrame, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))                
from Database.db_manager import Database_Manager


class AddAsset(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db = Database_Manager()
        self.setWindowTitle("bipo")
        self.setFixedSize(600, 520)
        self.setup_ui()

    def field_style(self):
        return """
            QLineEdit {
                background-color: #F0F0F0;
                border: none;
                border-radius: 18px;
                padding: 0px 15px;
                font-size: 13px;
                color: #333333;
            }
            QLineEdit:focus { background-color: #E8E8E8; }
        """

    def combo_style(self):
        return """
            QComboBox {
                background-color: #F0F0F0;
                border: none;
                border-radius: 18px;
                padding: 0px 15px;
                font-size: 13px;
                color: #333333;
                height: 38px;
            }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox::down-arrow { image: none; border: none; }
            QComboBox QAbstractItemView {
                background-color: white;
                border-radius: 10px;
                selection-background-color: #FFF3CC;
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
        icon_label = QLabel("➕")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 22px; background: transparent;")
        icon_layout.addWidget(icon_label)
        icon_box.setLayout(icon_layout)

        header_text = QVBoxLayout()
        header_text.setSpacing(2)
        sub_label = QLabel("Add Asset")
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

        # ── Row 1: Asset Name + Asset Type ──
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        left1 = QVBoxLayout()
        left1.setSpacing(6)
        name_label = QLabel("Asset Name")
        name_label.setFont(QFont("Arial", 11, QFont.Bold))
        name_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. Apple Stock")
        self.name_input.setFixedHeight(40)
        self.name_input.setStyleSheet(self.field_style())
        left1.addWidget(name_label)
        left1.addWidget(self.name_input)

        right1 = QVBoxLayout()
        right1.setSpacing(6)
        type_label = QLabel("Asset Type")
        type_label.setFont(QFont("Arial", 11, QFont.Bold))
        type_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Stock", "Crypto", "Real Estate",
                                  "Personal Belonging", "Other"])
        self.type_combo.setFixedHeight(40)
        self.type_combo.setStyleSheet(self.combo_style())
        right1.addWidget(type_label)
        right1.addWidget(self.type_combo)

        row1.addLayout(left1)
        row1.addLayout(right1)
        card_layout.addLayout(row1)

        card_layout.addSpacing(18)

        # ── Row 2: Value ──
        value_label = QLabel("Value")
        value_label.setFont(QFont("Arial", 11, QFont.Bold))
        value_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(value_label)

        card_layout.addSpacing(6)

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("e.g. 1500.00")
        self.value_input.setFixedHeight(40)
        self.value_input.setFixedWidth(220)
        self.value_input.setStyleSheet(self.field_style())
        card_layout.addWidget(self.value_input)

        card_layout.addSpacing(30)

        # ── Save Changes button ──
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignCenter)
        save_btn = QPushButton("Save Changes")
        save_btn.setFixedSize(180, 45)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5C518;
                color: #1A1A2E;
                border: none;
                border-radius: 22px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0B200; }
            QPushButton:pressed { background-color: #C9A000; }
        """)
        save_btn.clicked.connect(self.handle_save)
        btn_row.addWidget(save_btn)
        card_layout.addLayout(btn_row)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

    def handle_save(self):
        name  = self.name_input.text().strip()
        atype = self.type_combo.currentText()
        value = self.value_input.text().strip()

        if not name or not value:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            value_float = float(value)
        except ValueError:
            QMessageBox.warning(self, "Error", "Value must be a number")
            return

        self.db.add_asset(self.username, name, atype, value_float)
        QMessageBox.information(self, "Success", f"'{name}' added to your portfolio!")
        self.name_input.clear()
        self.value_input.clear()

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
    window = AddAsset("Carlos")
    window.show()
    sys.exit(app.exec_())