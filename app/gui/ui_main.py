# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'maincfzjxT.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTreeWidget, QTreeWidgetItem, QWidget)

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
        self.result_list = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.result_list.setHeaderItem(__qtreewidgetitem)
        self.result_list.setObjectName(u"result_list")

        self.gridLayout.addWidget(self.result_list, 1, 0, 1, 5)

        self.browse_btn = QPushButton(self.centralwidget)
        self.browse_btn.setObjectName(u"browse_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browse_btn.sizePolicy().hasHeightForWidth())
        self.browse_btn.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.browse_btn, 0, 0, 1, 1)

        self.run_btn = QPushButton(self.centralwidget)
        self.run_btn.setObjectName(u"run_btn")
        sizePolicy.setHeightForWidth(self.run_btn.sizePolicy().hasHeightForWidth())
        self.run_btn.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.run_btn, 0, 1, 1, 1)

        self.team_data_btn = QPushButton(self.centralwidget)
        self.team_data_btn.setObjectName(u"team_data_btn")
        sizePolicy.setHeightForWidth(self.team_data_btn.sizePolicy().hasHeightForWidth())
        self.team_data_btn.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.team_data_btn, 0, 2, 1, 1)

        self.path_lbl = QLabel(self.centralwidget)
        self.path_lbl.setObjectName(u"path_lbl")

        self.gridLayout.addWidget(self.path_lbl, 0, 3, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sauna-Maraton", None))
        self.browse_btn.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.run_btn.setText(QCoreApplication.translate("MainWindow", u"Run File", None))
        self.team_data_btn.setText(QCoreApplication.translate("MainWindow", u"See Team Data", None))
        self.path_lbl.setText("")
    # retranslateUi

