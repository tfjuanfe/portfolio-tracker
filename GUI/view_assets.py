from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                              QPushButton, QVBoxLayout, QHBoxLayout,
                              QFrame, QMessageBox, QTableWidget,
                              QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))                
from Database.db_manager import Database_Manager


class ViewAssets(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db = Database_Manager()
        self.setWindowTitle("bipo")
        self.setFixedSize(700, 560)
        self.setup_ui()

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
        card_layout.setContentsMargins(35, 25, 35, 30)
        card_layout.setSpacing(0)

        # ── Header ──
        header_row = QHBoxLayout()
        header_row.setSpacing(15)

        icon_box = QFrame()
        icon_box.setFixedSize(55, 55)
        icon_box.setStyleSheet("background-color: #FFF3CC; border-radius: 12px;")
        icon_layout = QVBoxLayout()
        icon_label = QLabel("👁")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 22px; background: transparent;")
        icon_layout.addWidget(icon_label)
        icon_box.setLayout(icon_layout)

        header_text = QVBoxLayout()
        header_text.setSpacing(2)
        sub_label = QLabel("View Asset")
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

        card_layout.addSpacing(20)

        # ── Search row ──
        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name...")
        self.search_input.setFixedHeight(38)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #F0F0F0;
                border: none;
                border-radius: 19px;
                padding: 0px 15px;
                font-size: 12px;
                color: #333333;
            }
        """)
        self.search_input.textChanged.connect(self.filter_assets)

        sort_btn = QPushButton("Sort by Value")
        sort_btn.setFixedHeight(38)
        sort_btn.setFixedWidth(130)
        sort_btn.setCursor(Qt.PointingHandCursor)
        sort_btn.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                color: #1A1A2E;
                border: none;
                border-radius: 19px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0E0E0; }
        """)
        sort_btn.clicked.connect(self.sort_by_value)

        search_row.addWidget(self.search_input)
        search_row.addWidget(sort_btn)
        card_layout.addLayout(search_row)

        card_layout.addSpacing(15)

        # ── Assets table ──
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Type", "Value ($)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FAFAFA;
                border: none;
                border-radius: 10px;
                gridline-color: #F0F0F0;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                color: #333333;
            }
            QTableWidget::item:selected {
                background-color: #FFF3CC;
                color: #1A1A2E;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                color: #1A1A2E;
                font-weight: bold;
                font-size: 12px;
                padding: 8px;
                border: none;
            }
        """)
        card_layout.addWidget(self.table)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)
        outer_layout.addStretch()
        self.setLayout(outer_layout)

        self.load_assets()

    def load_assets(self):
        self.all_assets = self.db.get_assets(self.username)
        self.display_assets(self.all_assets)

    def display_assets(self, assets):
        self.table.setRowCount(0)
        for row_data in assets:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row, 2, QTableWidgetItem(str(row_data[3])))
            self.table.setItem(row, 3, QTableWidgetItem(f"${row_data[4]:,.2f}"))

    def filter_assets(self):
        query = self.search_input.text().lower()
        filtered = [a for a in self.all_assets if query in a[2].lower()]
        self.display_assets(filtered)

    def sort_by_value(self):
        sorted_assets = sorted(self.all_assets, key=lambda x: x[4], reverse=True)
        self.display_assets(sorted_assets)

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
    window = ViewAssets("Carlos")
    window.show()
    sys.exit(app.exec_())