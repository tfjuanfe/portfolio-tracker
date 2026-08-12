from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                              QVBoxLayout, QHBoxLayout, QFrame, QComboBox,
                              QCheckBox, QScrollArea, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import sys
import os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ASSET_COLORS = [
    "#F5C518", "#26A69A", "#EF5350", "#7E57C2",
    "#42A5F5", "#FF7043", "#66BB6A", "#EC407A"
]

# ── Ticker validator ──────────────────────────────────────────────
KNOWN_TICKERS = {
    "AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
    "NFLX", "AMD", "INTC", "BTC-USD", "ETH-USD", "BNB-USD",
    "SOL-USD", "XRP-USD", "ADA-USD", "DOGE-USD", "SPY", "QQQ"
}

def is_tradeable(asset_name, asset_type):
    name = asset_name.upper()
    if asset_type.lower() in ("stock", "crypto", "etf"):
        return True
    if name in KNOWN_TICKERS:
        return True
    return False


# ── Background thread ─────────────────────────────────────────────
class PortfolioFetcher(QThread):
    result_ready = pyqtSignal(dict)
    error        = pyqtSignal(str)

    def __init__(self, assets, period):
        super().__init__()
        self.assets = assets   # list of (id, username, name, type, value)
        self.period = period

    def get_interval(self):
        return {"1mo": "1d", "3mo": "1d", "6mo": "1wk", "1y": "1wk"}.get(self.period, "1d")

    def run(self):
        try:
            import pandas as pd
            import yfinance as yf
            from sklearn.linear_model import LinearRegression

            results = {}   # asset_name → {dates, values, predicted_dates, predicted_values, current_value, change_pct}

            for asset in self.assets:
                _, _, name, atype, stored_value = asset
                ticker_sym = name.upper()

                if is_tradeable(name, atype):
                    try:
                        ticker = yf.Ticker(ticker_sym)
                        hist = ticker.history(period=self.period, interval=self.get_interval())

                        if hist.empty:
                            raise ValueError("No data")

                        close = hist["Close"].squeeze()
                        purchase_price = float(close.iloc[0])
                        shares = stored_value / purchase_price if purchase_price > 0 else 0
                        values = (close * shares).values
                        dates  = close.index.to_pydatetime()

                        # ── Linear regression prediction ──
                        x = np.arange(len(values)).reshape(-1, 1)
                        model = LinearRegression().fit(x, values)
                        future_steps = 30
                        x_future = np.arange(len(values), len(values) + future_steps).reshape(-1, 1)
                        predicted_values = model.predict(x_future)

                        # Generate future dates
                        last_date = dates[-1]
                        future_dates = pd.date_range(start=last_date, periods=future_steps + 1, freq="D")[1:]
                        future_dates = future_dates.to_pydatetime()

                        current_val  = float(values[-1])
                        start_val    = float(values[0])
                        change_pct   = ((current_val - start_val) / start_val * 100) if start_val > 0 else 0

                        results[name] = {
                            "dates":            dates,
                            "values":           values,
                            "predicted_dates":  future_dates,
                            "predicted_values": predicted_values,
                            "current_value":    current_val,
                            "change_pct":       change_pct,
                            "tradeable":        True
                        }
                    except Exception:
                        # Fall back to flat line
                        results[name] = self._flat_asset(name, stored_value)
                else:
                    results[name] = self._flat_asset(name, stored_value)

            self.result_ready.emit(results)

        except Exception as e:
            self.error.emit(str(e))

    def _flat_asset(self, name, value):
        import pandas as pd
        dates = pd.date_range(end=pd.Timestamp.today(), periods=60, freq="D").to_pydatetime()
        values = np.full(len(dates), value)
        return {
            "dates":            dates,
            "values":           values,
            "predicted_dates":  [],
            "predicted_values": [],
            "current_value":    value,
            "change_pct":       0.0,
            "tradeable":        False
        }


# ── Main widget ───────────────────────────────────────────────────
class PortfolioInsights(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username   = username
        self.asset_data = {}
        self.checkboxes = {}
        self.setWindowTitle("bipo")
        self.setFixedSize(900, 680)
        self.setup_ui()
        self.load_and_fetch()

    def setup_ui(self):
        self.setStyleSheet("background-color: #E8E6F0;")
        outer = QVBoxLayout()
        outer.setContentsMargins(30, 20, 30, 20)
        outer.setSpacing(12)

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
        outer.addLayout(top_bar)

        # ── Header ──
        header = QFrame()
        header.setFixedHeight(75)
        header.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        hl = QHBoxLayout()
        hl.setContentsMargins(25, 15, 25, 15)

        logo_row = QHBoxLayout()
        logo_row.setSpacing(6)
        bar_icon = QLabel("▌▌▌")
        bar_icon.setStyleSheet("color: #F5C518; font-size: 16px; background: transparent;")
        logo_text = QLabel("bipo")
        logo_text.setFont(QFont("Arial", 16, QFont.Bold))
        logo_text.setStyleSheet("color: #1A1A2E; background: transparent;")
        logo_row.addWidget(bar_icon)
        logo_row.addWidget(logo_text)

        title = QLabel("Portfolio Insights")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1A1A2E; background: transparent;")

        self.total_label = QLabel("Total: —")
        self.total_label.setFont(QFont("Arial", 13, QFont.Bold))
        self.total_label.setStyleSheet("color: #26A69A; background: transparent;")

        hl.addLayout(logo_row)
        hl.addStretch()
        hl.addWidget(title)
        hl.addStretch()
        hl.addWidget(self.total_label)
        header.setLayout(hl)
        outer.addWidget(header)

        # ── Controls row ──
        ctrl = QHBoxLayout()
        ctrl.setSpacing(10)

        self.period_combo = QComboBox()
        self.period_combo.addItems(["1mo", "3mo", "6mo", "1y"])
        self.period_combo.setCurrentText("3mo")
        self.period_combo.setFixedWidth(80)
        self.period_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #E0E0E0; border-radius: 8px;
                padding: 5px 10px; font-size: 12px;
                background: white; color: #1A1A2E;
            }
        """)
        self.period_combo.currentTextChanged.connect(self.load_and_fetch)

        self.show_prediction_btn = QPushButton("🔮 Show Prediction")
        self.show_prediction_btn.setCheckable(True)
        self.show_prediction_btn.setChecked(True)
        self.show_prediction_btn.setFixedHeight(34)
        self.show_prediction_btn.setCursor(Qt.PointingHandCursor)
        self.show_prediction_btn.setStyleSheet("""
            QPushButton {
                background-color: #7E57C2; color: white;
                border: none; border-radius: 8px;
                font-size: 12px; font-weight: bold; padding: 0 14px;
            }
            QPushButton:checked { background-color: #5E35B1; }
            QPushButton:hover   { background-color: #9575CD; }
        """)
        self.show_prediction_btn.clicked.connect(self.redraw)

        self.show_total_btn = QPushButton("📊 Show Total")
        self.show_total_btn.setCheckable(True)
        self.show_total_btn.setChecked(True)
        self.show_total_btn.setFixedHeight(34)
        self.show_total_btn.setCursor(Qt.PointingHandCursor)
        self.show_total_btn.setStyleSheet("""
            QPushButton {
                background-color: #F5C518; color: #1A1A2E;
                border: none; border-radius: 8px;
                font-size: 12px; font-weight: bold; padding: 0 14px;
            }
            QPushButton:checked { background-color: #E0B200; }
            QPushButton:hover   { background-color: #FFD740; }
        """)
        self.show_total_btn.clicked.connect(self.redraw)

        self.status_label = QLabel("Loading portfolio data...")
        self.status_label.setStyleSheet("color: #888888; font-size: 12px;")

        ctrl.addWidget(QLabel("Period:"))
        ctrl.addWidget(self.period_combo)
        ctrl.addWidget(self.show_prediction_btn)
        ctrl.addWidget(self.show_total_btn)
        ctrl.addStretch()
        ctrl.addWidget(self.status_label)
        outer.addLayout(ctrl)

        # ── Main content: chart + asset list side by side ──
        content = QHBoxLayout()
        content.setSpacing(12)

        # Chart
        chart_frame = QFrame()
        chart_frame.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        chart_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        cf_layout = QVBoxLayout()
        cf_layout.setContentsMargins(10, 10, 10, 10)
        self.figure = Figure(facecolor="white")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: transparent;")
        cf_layout.addWidget(self.canvas)
        chart_frame.setLayout(cf_layout)
        content.addWidget(chart_frame, stretch=3)

        # Asset list panel
        panel = QFrame()
        panel.setFixedWidth(210)
        panel.setStyleSheet("QFrame { background-color: white; border-radius: 15px; }")
        panel_layout = QVBoxLayout()
        panel_layout.setContentsMargins(12, 12, 12, 12)
        panel_layout.setSpacing(8)

        panel_title = QLabel("Assets")
        panel_title.setFont(QFont("Arial", 12, QFont.Bold))
        panel_title.setStyleSheet("color: #1A1A2E;")
        panel_layout.addWidget(panel_title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; border: none; }")
        self.asset_list_widget = QWidget()
        self.asset_list_widget.setStyleSheet("background: transparent;")
        self.asset_list_layout = QVBoxLayout()
        self.asset_list_layout.setSpacing(6)
        self.asset_list_layout.setContentsMargins(0, 0, 0, 0)
        self.asset_list_widget.setLayout(self.asset_list_layout)
        scroll.setWidget(self.asset_list_widget)
        panel_layout.addWidget(scroll)
        panel.setLayout(panel_layout)
        content.addWidget(panel, stretch=1)

        outer.addLayout(content)
        self.setLayout(outer)

    # ── Data loading ──────────────────────────────────────────────
    def load_and_fetch(self):
        from Database.db_manager import Database_Manager
        db = Database_Manager()
        assets = db.get_assets(self.username)
        if not assets:
            self.status_label.setText("No assets found. Add some assets first.")
            return
        self.assets = assets
        self.status_label.setText("Fetching live data...")
        self.thread = PortfolioFetcher(assets, self.period_combo.currentText())
        self.thread.result_ready.connect(self.on_data_ready)
        self.thread.error.connect(lambda e: self.status_label.setText(f"Error: {e}"))
        self.thread.start()

    def on_data_ready(self, data):
        self.asset_data = data
        self.build_asset_list()
        self.redraw()
        total = sum(v["current_value"] for v in data.values())
        self.total_label.setText(f"Total: ${total:,.2f}")
        self.status_label.setText(f"{len(data)} assets loaded")

    # ── Asset checkboxes ──────────────────────────────────────────
    def build_asset_list(self):
        # Clear old
        while self.asset_list_layout.count():
            child = self.asset_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        self.checkboxes.clear()

        for i, (name, info) in enumerate(self.asset_data.items()):
            color = ASSET_COLORS[i % len(ASSET_COLORS)]
            row = QHBoxLayout()
            row.setSpacing(6)

            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 14px;")
            dot.setFixedWidth(18)

            cb = QCheckBox(name)
            cb.setChecked(True)
            cb.setStyleSheet(f"""
                QCheckBox {{ color: #1A1A2E; font-size: 11px; font-weight: bold; }}
                QCheckBox::indicator {{ width: 14px; height: 14px; border-radius: 3px;
                    border: 2px solid {color}; background: white; }}
                QCheckBox::indicator:checked {{ background: {color}; }}
            """)
            cb.stateChanged.connect(self.redraw)
            self.checkboxes[name] = cb

            val_label = QLabel(f"${info['current_value']:,.0f}")
            val_label.setStyleSheet("color: #888; font-size: 10px;")

            chg = info["change_pct"]
            chg_label = QLabel(f"{'▲' if chg >= 0 else '▼'}{abs(chg):.1f}%")
            chg_label.setStyleSheet(f"color: {'#26A69A' if chg >= 0 else '#EF5350'}; font-size: 10px; font-weight: bold;")

            col_layout = QVBoxLayout()
            col_layout.setSpacing(1)
            top_row = QHBoxLayout()
            top_row.addWidget(dot)
            top_row.addWidget(cb)
            top_row.addStretch()
            col_layout.addLayout(top_row)
            bottom_row = QHBoxLayout()
            bottom_row.addSpacing(24)
            bottom_row.addWidget(val_label)
            bottom_row.addWidget(chg_label)
            bottom_row.addStretch()
            col_layout.addLayout(bottom_row)

            wrapper = QWidget()
            wrapper.setStyleSheet("background: transparent;")
            wrapper.setLayout(col_layout)
            self.asset_list_layout.addWidget(wrapper)

        self.asset_list_layout.addStretch()

    # ── Chart drawing ─────────────────────────────────────────────
    def redraw(self):
        if not self.asset_data:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("white")
        ax.tick_params(colors="#888888", labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor("#E0E0E0")

        show_pred  = self.show_prediction_btn.isChecked()
        show_total = self.show_total_btn.isChecked()

        total_dates  = None
        total_values = None

        for i, (name, info) in enumerate(self.asset_data.items()):
            if name not in self.checkboxes or not self.checkboxes[name].isChecked():
                continue

            color  = ASSET_COLORS[i % len(ASSET_COLORS)]
            dates  = info["dates"]
            values = info["values"]

            ax.plot(dates, values, color=color, linewidth=2, label=name, zorder=3)

            # Prediction
            if show_pred and len(info["predicted_dates"]) > 0:
                pd_dates = list(dates[-1:]) + list(info["predicted_dates"])
                pd_vals  = [values[-1]] + list(info["predicted_values"])
                ax.plot(pd_dates, pd_vals, color=color, linewidth=1.5,
                        linestyle="--", alpha=0.6, zorder=2)
                ax.fill_between(pd_dates, pd_vals, alpha=0.05, color=color)

            # Accumulate total
            if show_total:
                if total_dates is None:
                    total_dates  = dates
                    total_values = np.array(values, dtype=float)
                else:
                    # align by interpolation if lengths differ
                    min_len = min(len(total_values), len(values))
                    total_values = total_values[:min_len] + np.array(values[:min_len], dtype=float)
                    total_dates  = total_dates[:min_len]

        # Total portfolio line
        if show_total and total_dates is not None and len(total_dates) > 1:
            ax.plot(total_dates, total_values, color="#1A1A2E",
                    linewidth=2.5, linestyle="-.", label="Total", zorder=4)

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.figure.autofmt_xdate(rotation=30)
        ax.set_ylabel("Value (USD)", color="#888888", fontsize=9)
        ax.set_title("Portfolio Value Over Time", color="#1A1A2E",
                     fontsize=13, fontweight="bold", pad=10)
        ax.legend(fontsize=8, framealpha=0.5, loc="upper left")
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"${x:,.0f}")
        )

        self.canvas.draw()

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
    window = PortfolioInsights("Carlos")
    window.show()
    sys.exit(app.exec_())