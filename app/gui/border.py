from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt


class CustomDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()  # Save the current painter state

        # Handle the background color manually
        background_color = index.data(Qt.BackgroundRole)
        if background_color:
            background_rect = option.rect
            painter.fillRect(background_rect, background_color)

        # Draw the item text and decorations (default behavior)
        super().paint(painter, option, index)

        # Set up a consistent thin black pen
        thin_pen = QPen(QColor(0, 0, 0), 1)  # 1-pixel black border
        thin_pen.setCosmetic(True)  # Ensure consistent thickness across DPI
        painter.setPen(thin_pen)

        # Draw the bottom border
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        # Draw the top border
        painter.drawLine(option.rect.topLeft(), option.rect.topRight())

        # Draw the column borders
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())  # Right column border
        painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())  # Left column border

        painter.restore()  # Restore the painter state
