# Mark 57 -> Android SPIKE #1
# Goal: prove that a PySide6 (Qt) window with QPainter drawing - the same kind of UI
# Mark 57 uses on the PC - builds into an APK and runs on the phone.
# No Mark 57 code, no keys, no personal data in here.
import math
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


def probe(name):
    try:
        __import__(name)
        return f"OK    {name}"
    except Exception as e:  # noqa: BLE001
        return f"FAIL  {name}: {type(e).__name__}"


class Reactor(QWidget):
    def __init__(self):
        super().__init__()
        self.t = 0.0
        timer = QTimer(self)
        timer.timeout.connect(self.tick)
        timer.start(33)

    def tick(self):
        self.t += 0.04
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(), QColor(5, 10, 20))
        cx, cy = self.width() / 2, self.height() / 2
        r0 = min(self.width(), self.height()) * 0.38
        for i in range(5):
            r = r0 * (1 - i * 0.17)
            pen = QPen(QColor(0, 200 - i * 25, 255, 220))
            pen.setWidth(3)
            p.setPen(pen)
            start = int((self.t * 60 * (1 if i % 2 else -1) + i * 70) * 16)
            p.drawArc(int(cx - r), int(cy - r), int(2 * r), int(2 * r), start, 220 * 16)
        pulse = 0.5 + 0.5 * math.sin(self.t * 2)
        p.setPen(Qt.NoPen)
        p.setBrush(QColor(0, 220, 255, int(120 + 120 * pulse)))
        rc = r0 * 0.18
        p.drawEllipse(int(cx - rc), int(cy - rc), int(2 * rc), int(2 * rc))


app = QApplication(sys.argv)
win = QWidget()
win.setStyleSheet("background:#050a14;color:#7fe8ff;")
lay = QVBoxLayout(win)
title = QLabel("MARK 57 - PySide6 spike OK")
title.setAlignment(Qt.AlignCenter)
title.setStyleSheet("font-size:22px;font-weight:bold;")
info = QLabel(
    "Python " + sys.version.split()[0] + "\n"
    + probe("PySide6.QtMultimedia") + "\n"
    + probe("PySide6.QtNetwork") + "\n"
    + probe("PySide6.QtWebSockets")
)
info.setStyleSheet("font-size:14px;")
lay.addWidget(title)
lay.addWidget(Reactor(), 1)
lay.addWidget(info)
win.showFullScreen()
sys.exit(app.exec())
