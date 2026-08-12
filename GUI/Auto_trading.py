from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                              QPushButton, QVBoxLayout, QHBoxLayout,
                              QFrame, QMessageBox, QComboBox,
                              QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Database.db_manager import Database_Manager


class AutoTrading(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.db = Database_Manager()
        self.setWindowTitle("bipo")
        self.setFixedSize(700, 580)
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
                height: 40px;
            }
            QComboBox::drop-down { border: none; width: 30px; }
            QComboBox::down-arrow { image: none; border: none; }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #FFF3CC;
                color: #333333;
            }
        """

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(35, 20, 35, 25)
        outer_layout.setSpacing(12)

        # ── Top bar: Stocks button + Go Back ──
        top_bar = QHBoxLayout()

        stocks_btn = QPushButton("📈 Live Charts")
        stocks_btn.setFixedSize(130, 35)
        stocks_btn.setCursor(Qt.PointingHandCursor)
        stocks_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5C518; border: none;
                border-radius: 17px; font-size: 13px;
                color: #1A1A2E; font-weight: bold;
            }
            QPushButton:hover { background-color: #E0B200; }
        """)
        stocks_btn.clicked.connect(self.open_stocks_tab)
        top_bar.addWidget(stocks_btn)

        top_bar.addStretch()
        go_back_btn = QPushButton("← Go Back")
        go_back_btn.setFixedSize(100, 35)
        go_back_btn.setCursor(Qt.PointingHandCursor)
        go_back_btn.setStyleSheet("""
            QPushButton {
                background-color: white; border: none;
                border-radius: 17px; font-size: 13px;
                color: #333333; font-weight: bold;
            }
            QPushButton:hover { background-color: #f0f0f0; }
        """)
        go_back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(go_back_btn)
        outer_layout.addLayout(top_bar)

        # ── Header ──
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        hl = QHBoxLayout()
        hl.setContentsMargins(25, 15, 25, 15)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 16px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 16, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        title = QLabel("Price Alerts")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1A1A2E; background: transparent;")
        hl.addWidget(bar_icon)
        hl.addWidget(logo_text)
        hl.addStretch()
        hl.addWidget(title)
        hl.addStretch()
        header.setLayout(hl)
        outer_layout.addWidget(header)

        # ── White card: add new alert ──
        card = QFrame()
        card.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(25, 20, 25, 20)
        card_layout.setSpacing(12)

        card_title = QLabel("Set New Alert")
        card_title.setFont(QFont("Arial", 13, QFont.Bold))
        card_title.setStyleSheet("color: #1A1A2E; background: transparent;")
        card_layout.addWidget(card_title)

        # ── Row: ticker + condition + price ──
        row = QHBoxLayout()
        row.setSpacing(12)

        # Ticker input
        ticker_col = QVBoxLayout()
        ticker_col.setSpacing(5)
        ticker_label = QLabel("Ticker")
        ticker_label.setFont(QFont("Arial", 10, QFont.Bold))
        ticker_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("e.g. AAPL, BTC-USD")
        self.ticker_input.setFixedHeight(40)
        self.ticker_input.setStyleSheet(self.field_style())
        ticker_col.addWidget(ticker_label)
        ticker_col.addWidget(self.ticker_input)

        # Condition dropdown
        cond_col = QVBoxLayout()
        cond_col.setSpacing(5)
        cond_label = QLabel("Condition")
        cond_label.setFont(QFont("Arial", 10, QFont.Bold))
        cond_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        self.condition_combo = QComboBox()
        self.condition_combo.addItems(["above", "below"])
        self.condition_combo.setFixedHeight(40)
        self.condition_combo.setStyleSheet(self.combo_style())
        cond_col.addWidget(cond_label)
        cond_col.addWidget(self.condition_combo)

        # Target price input
        price_col = QVBoxLayout()
        price_col.setSpacing(5)
        price_label = QLabel("Target Price ($)")
        price_label.setFont(QFont("Arial", 10, QFont.Bold))
        price_label.setStyleSheet("color: #1A1A2E; background: transparent;")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("e.g. 200.00")
        self.price_input.setFixedHeight(40)
        self.price_input.setStyleSheet(self.field_style())
        price_col.addWidget(price_label)
        price_col.addWidget(self.price_input)

        row.addLayout(ticker_col, 2)
        row.addLayout(cond_col, 1)
        row.addLayout(price_col, 2)
        card_layout.addLayout(row)

        # ── Add Alert button ──
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignRight)
        add_btn = QPushButton("＋ Add Alert")
        add_btn.setFixedSize(140, 40)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5C518; color: #1A1A2E;
                border: none; border-radius: 20px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #E0B200; }
        """)
        add_btn.clicked.connect(self.handle_add_alert)
        btn_row.addWidget(add_btn)
        card_layout.addLayout(btn_row)

        card.setLayout(card_layout)
        outer_layout.addWidget(card)

        # ── Active alerts table ──
        table_label = QLabel("Active Alerts")
        table_label.setFont(QFont("Arial", 13, QFont.Bold))
        table_label.setStyleSheet("color: #1A1A2E;")
        outer_layout.addWidget(table_label)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Ticker", "Condition", "Target Price", "Delete"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 12px;
                gridline-color: #F0F0F0;
                font-size: 12px;
            }
            QTableWidget::item { padding: 8px; color: #333333; }
            QTableWidget::item:selected {
                background-color: #FFF3CC; color: #1A1A2E;
            }
            QHeaderView::section {
                background-color: #F5F5F5; color: #1A1A2E;
                font-weight: bold; font-size: 12px;
                padding: 8px; border: none;
            }
        """)
        outer_layout.addWidget(self.table)

        self.setLayout(outer_layout)
        self.load_alerts()

    def handle_add_alert(self):
        ticker    = self.ticker_input.text().strip().upper()
        condition = self.condition_combo.currentText()
        price     = self.price_input.text().strip()

        if not ticker or not price:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            price_float = float(price)
        except ValueError:
            QMessageBox.warning(self, "Error", "Price must be a number")
            return

        self.db.add_alert(self.username, ticker, price_float, condition)
        QMessageBox.information(self, "Alert Set",
            f"Alert set: notify me when {ticker} goes {condition} ${price_float:,.2f}")
        self.ticker_input.clear()
        self.price_input.clear()
        self.load_alerts()

    def load_alerts(self):
        self.table.setRowCount(0)
        alerts = self.db.get_alerts(self.username)
        for alert in alerts:
            alert_id, username, ticker, target, condition, active = alert
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(alert_id)))
            self.table.setItem(row, 1, QTableWidgetItem(ticker))
            self.table.setItem(row, 2, QTableWidgetItem(condition))
            self.table.setItem(row, 3, QTableWidgetItem(f"${target:,.2f}"))

            # ── Delete button inside table ──
            del_btn = QPushButton("✕ Delete")
            del_btn.setCursor(Qt.PointingHandCursor)
            del_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F28B82; color: white;
                    border: none; border-radius: 8px;
                    font-size: 11px; font-weight: bold;
                    padding: 4px 10px;
                }
                QPushButton:hover { background-color: #E07070; }
            """)
            del_btn.clicked.connect(lambda _, aid=alert_id: self.delete_alert(aid))
            self.table.setCellWidget(row, 4, del_btn)

    def delete_alert(self, alert_id):
        self.db.delete_alert(alert_id)
        self.load_alerts()

    def open_stocks_tab(self):
        try:
            from stocks_tab import StocksTab
            self.stocks_window = StocksTab(self.username)
            self.stocks_window.show()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

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
    window = AutoTrading("Carlos")
    window.show()
    sys.exit(app.exec_())