# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainQBtZgL.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QLabel,
    QListView, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1085, 605)
        MainWindow.setStyleSheet(u"QPushButton{\n"
"	width: 100\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.team_data_btn = QPushButton(self.centralwidget)
        self.team_data_btn.setObjectName(u"team_data_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.team_data_btn.sizePolicy().hasHeightForWidth())
        self.team_data_btn.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.team_data_btn, 0, 4, 1, 1)

        self.run_btn = QPushButton(self.centralwidget)
        self.run_btn.setObjectName(u"run_btn")
        sizePolicy.setHeightForWidth(self.run_btn.sizePolicy().hasHeightForWidth())
        self.run_btn.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.run_btn, 0, 2, 1, 1)

        self.path_lbl = QLabel(self.centralwidget)
        self.path_lbl.setObjectName(u"path_lbl")

        self.gridLayout.addWidget(self.path_lbl, 0, 0, 1, 1)

        self.result_list = QListView(self.centralwidget)
        self.result_list.setObjectName(u"result_list")

        self.gridLayout.addWidget(self.result_list, 1, 0, 1, 5)

        self.team_list = QComboBox(self.centralwidget)
        self.team_list.setObjectName(u"team_list")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.team_list.sizePolicy().hasHeightForWidth())
        self.team_list.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.team_list, 0, 3, 1, 1)

        self.browse_btn = QPushButton(self.centralwidget)
        self.browse_btn.setObjectName(u"browse_btn")
        sizePolicy.setHeightForWidth(self.browse_btn.sizePolicy().hasHeightForWidth())
        self.browse_btn.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.browse_btn, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sauna-Maraton", None))
        self.team_data_btn.setText(QCoreApplication.translate("MainWindow", u"See Team Data", None))
        self.run_btn.setText(QCoreApplication.translate("MainWindow", u"Run File", None))
        self.path_lbl.setText("")
        self.team_list.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pick Team..", None))
        self.browse_btn.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
    # retranslateUi

