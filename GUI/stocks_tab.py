from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame, QComboBox,
                              QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── Background thread for fetching chart data ──
class ChartFetcher(QThread):
    data_ready = pyqtSignal(object, str)
    error = pyqtSignal(str)

    def __init__(self, ticker, period):
        super().__init__()
        self.ticker = ticker
        self.period = period

    def run(self):
        try:
            import yfinance as yf
            data = yf.download(self.ticker, period=self.period, interval=self.get_interval(), progress=False)
            if data.empty:
                self.error.emit(f"No data found for '{self.ticker}'. Check the ticker symbol.")
            else:
                self.data_ready.emit(data, self.ticker)
        except Exception as e:
            self.error.emit(str(e))

    def get_interval(self):
        return {"1d": "5m", "5d": "15m", "1mo": "1d",
                "3mo": "1d", "6mo": "1wk", "1y": "1wk"}.get(self.period, "1d")


class StocksTab(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("bipo")
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.fetch_chart("AAPL", "1mo")  # default chart on open

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

        title = QLabel("Live Charts")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1A1A2E; background: transparent;")

        header_layout.addLayout(logo_row)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_card.setLayout(header_layout)
        outer_layout.addWidget(header_card)

        # ── Search bar ──
        search_card = QFrame()
        search_card.setStyleSheet("QFrame { background-color: white; border-radius: 12px; }")
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(15, 10, 15, 10)
        search_layout.setSpacing(10)

        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("Enter ticker (e.g. AAPL, BTC-USD, TSLA...)")
        self.ticker_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #E0E0E0; border-radius: 8px;
                padding: 6px 12px; font-size: 13px; color: #1A1A2E;
                background: #F9F9F9;
            }
            QLineEdit:focus { border-color: #F5C518; }
        """)
        self.ticker_input.returnPressed.connect(self.on_search)

        # ── Period selector ──
        self.period_combo = QComboBox()
        self.period_combo.addItems(["1d", "5d", "1mo", "3mo", "6mo", "1y"])
        self.period_combo.setCurrentText("1mo")
        self.period_combo.setFixedWidth(70)
        self.period_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #E0E0E0; border-radius: 8px;
                padding: 6px 10px; font-size: 12px;
                background: #F9F9F9; color: #1A1A2E;
            }
            QComboBox:focus { border-color: #F5C518; }
        """)

        search_btn = QPushButton("Search")
        search_btn.setFixedSize(80, 36)
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5C518; color: #1A1A2E;
                border: none; border-radius: 8px;
                font-size: 13px; font-weight: bold;
            }
            QPushButton:hover { background-color: #E0B200; }
        """)
        search_btn.clicked.connect(self.on_search)

        search_layout.addWidget(self.ticker_input)
        search_layout.addWidget(self.period_combo)
        search_layout.addWidget(search_btn)
        search_card.setLayout(search_layout)
        outer_layout.addWidget(search_card)

        # ── Quick picks ──
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(8)
        for ticker in ["AAPL", "TSLA", "MSFT", "BTC-USD", "ETH-USD", "NVDA"]:
            btn = QPushButton(ticker)
            btn.setFixedHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white; color: #1A1A2E;
                    border: 2px solid #E0E0E0; border-radius: 14px;
                    font-size: 11px; font-weight: bold; padding: 0 12px;
                }
                QPushButton:hover { border-color: #F5C518; color: #F5C518; }
            """)
            btn.clicked.connect(lambda _, t=ticker: self.fetch_chart(t, self.period_combo.currentText()))
            quick_layout.addWidget(btn)
        quick_layout.addStretch()
        outer_layout.addLayout(quick_layout)

        # ── Status label ──
        self.status_label = QLabel("Loading chart...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #888888; font-size: 12px;")
        outer_layout.addWidget(self.status_label)

        # ── Chart ──
        chart_frame = QFrame()
        chart_frame.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        chart_frame_layout = QVBoxLayout()
        chart_frame_layout.setContentsMargins(10, 10, 10, 10)

        self.figure = Figure(figsize=(7, 3), facecolor="white")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")

        chart_frame_layout.addWidget(self.canvas)
        chart_frame.setLayout(chart_frame_layout)
        outer_layout.addWidget(chart_frame)

        self.setLayout(outer_layout)

    def on_search(self):
        ticker = self.ticker_input.text().strip().upper()
        if ticker:
            self.fetch_chart(ticker, self.period_combo.currentText())

    def fetch_chart(self, ticker, period):
        self.status_label.setText(f"Loading {ticker}...")
        self.thread = ChartFetcher(ticker, period)
        self.thread.data_ready.connect(self.draw_chart)
        self.thread.error.connect(self.show_error)
        self.thread.start()

    def draw_chart(self, data, ticker):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        close = data["Close"].squeeze()
        dates = close.index
        prices = close.values

        # Color green if price went up, red if down
        color = "#26A69A" if prices[-1] >= prices[0] else "#EF5350"

        ax.plot(dates, prices, color=color, linewidth=2)
        ax.fill_between(dates, prices, prices.min(), alpha=0.1, color=color)

        # Styling
        ax.set_facecolor("white")
        ax.tick_params(colors="#888888", labelsize=8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.figure.autofmt_xdate(rotation=30)
        for spine in ax.spines.values():
            spine.set_edgecolor("#E0E0E0")

        ax.set_title(ticker, color="#1A1A2E", fontsize=13, fontweight="bold", pad=10)
        ax.set_ylabel("Price (USD)", color="#888888", fontsize=9)

        self.canvas.draw()
        self.status_label.setText(
            f"{ticker}  |  Current: ${prices[-1]:.2f}  |  "
            f"{'▲' if prices[-1] >= prices[0] else '▼'} "
            f"{abs(((prices[-1]-prices[0])/prices[0])*100):.2f}%"
        )

    def show_error(self, msg):
        self.status_label.setText(f"Error: {msg}")

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
    window = StocksTab("Carlos")
    window.show()
    sys.exit(app.exec_())