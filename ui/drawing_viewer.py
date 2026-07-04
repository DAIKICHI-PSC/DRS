from PySide6.QtWidgets import QDialog, QVBoxLayout
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap, QPainter, QWheelEvent


class DrawingViewer(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = QPixmap()
        self._zoom_scale = 1.0
        self._offset = QPointF(0, 0)
        self._is_dragging = False
        self._drag_start = QPointF(0, 0)
        self._drag_offset_start = QPointF(0, 0)
        self.setMouseTracking(True)
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("図面")
        self.resize(800, 600)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def set_pixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        self._zoom_scale = 1.0
        self._offset = QPointF(0, 0)
        self.update()

    def clear_image(self):
        self._pixmap = QPixmap()
        self._zoom_scale = 1.0
        self._offset = QPointF(0, 0)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_start = event.position()
            self._drag_offset_start = self._offset

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            delta = event.position() - self._drag_start
            self._offset = self._drag_offset_start + delta
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            scaled = self._pixmap.scaled(
                int(self.width() * self._zoom_scale),
                int(self.height() * self._zoom_scale),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            x = (self.width() - scaled.width()) / 2 + self._offset.x()
            y = (self.height() - scaled.height()) / 2 + self._offset.y()
            painter.drawPixmap(x, y, scaled)
            painter.end()

    def wheelEvent(self, event: QWheelEvent):
        if self._pixmap.isNull():
            return

        mouse_pos = event.position()
        center = QPointF(self.width() / 2, self.height() / 2)
        mouse_offset = mouse_pos - center
        old_scale = self._zoom_scale

        if event.angleDelta().y() > 0:
            self._zoom_scale *= 1.1
        else:
            self._zoom_scale /= 1.1
        self._zoom_scale = max(0.1, min(5.0, self._zoom_scale))

        ratio = self._zoom_scale / old_scale
        self._offset = self._offset * ratio + mouse_offset * (1 - ratio)
        self.update()
