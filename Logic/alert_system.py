import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtCore import QThread, pyqtSignal
import yfinance as yf


class AlertChecker(QThread):
    alert_triggered = pyqtSignal(str, float, float, str)  # ticker, current, target, condition

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.running  = True

    def run(self):
        import time
        from Database.db_manager import Database_Manager
        db = Database_Manager()

        while self.running:
            try:
                alerts = db.get_alerts(self.username)
                for alert in alerts:
                    alert_id, username, ticker, target, condition, active = alert
                    try:
                        data = yf.Ticker(ticker)
                        price = data.fast_info["last_price"]
                        if price is None:
                            continue
                        if condition == "above" and price >= target:
                            self.alert_triggered.emit(ticker, price, target, condition)
                            db.delete_alert(alert_id)
                        elif condition == "below" and price <= target:
                            self.alert_triggered.emit(ticker, price, target, condition)
                            db.delete_alert(alert_id)
                    except Exception:
                        continue
            except Exception:
                pass
            time.sleep(60)    # check every 60 seconds

    def stop(self):
        self.running = False