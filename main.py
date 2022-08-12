import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine(QUrl("qml/Main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())