import sys
import os

# Add project root and GUI directory to sys.path so all imports resolve
project_root = os.path.dirname(os.path.abspath(__file__))
gui_dir = os.path.join(project_root, "GUI")
sys.path.insert(0, project_root)
sys.path.insert(0, gui_dir)

from PyQt5.QtWidgets import QApplication
from GUI.welcome_screen import WelcomeScreen


def main():
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
