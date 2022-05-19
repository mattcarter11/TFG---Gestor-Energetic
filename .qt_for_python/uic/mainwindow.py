# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QCheckBox,
    QComboBox, QDateTimeEdit, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QStackedWidget, QStatusBar, QTabWidget, QTableView,
    QTextEdit, QVBoxLayout, QWidget)

from QMplWidgets import (MplTwinxWidget, MplWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1082, 770)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1080, 720))
        MainWindow.setStyleSheet(u"QHeaderView::section {\n"
"	background-color: rgb(205, 205, 205);\n"
"    border: 0px transparent;\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QTableView::item {\n"
"	border-top: 0px transparent;\n"
"	border-bottom: 0px transparent;\n"
"}\n"
"\n"
"QHeaderView {\n"
"    qproperty-defaultAlignment: AlignHCenter AlignVCenter;\n"
"}")
        MainWindow.setAnimated(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.options = QVBoxLayout()
        self.options.setObjectName(u"options")
        self.options.setSizeConstraint(QLayout.SetNoConstraint)
        self.options.setContentsMargins(10, -1, 10, -1)
        self.time_options = QVBoxLayout()
        self.time_options.setObjectName(u"time_options")
        self.time_l = QLabel(self.centralwidget)
        self.time_l.setObjectName(u"time_l")
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.time_l.setFont(font)

        self.time_options.addWidget(self.time_l)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.start_date_l = QLabel(self.centralwidget)
        self.start_date_l.setObjectName(u"start_date_l")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.start_date_l)

        self.start_date = QDateTimeEdit(self.centralwidget)
        self.start_date.setObjectName(u"start_date")
        self.start_date.setDateTime(QDateTime(QDate(2022, 2, 2), QTime(7, 0, 0)))

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.start_date)

        self.end_date = QDateTimeEdit(self.centralwidget)
        self.end_date.setObjectName(u"end_date")
        self.end_date.setDateTime(QDateTime(QDate(2000, 2, 2), QTime(17, 0, 0)))

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.end_date)

        self.end_date_l = QLabel(self.centralwidget)
        self.end_date_l.setObjectName(u"end_date_l")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.end_date_l)


        self.time_options.addLayout(self.formLayout_2)


        self.options.addLayout(self.time_options)

        self.algorithm_option = QVBoxLayout()
        self.algorithm_option.setObjectName(u"algorithm_option")
        self.algorithm_l = QLabel(self.centralwidget)
        self.algorithm_l.setObjectName(u"algorithm_l")
        self.algorithm_l.setFont(font)

        self.algorithm_option.addWidget(self.algorithm_l)

        self.algorithm = QComboBox(self.centralwidget)
        self.algorithm.addItem("")
        self.algorithm.addItem("")
        self.algorithm.addItem("")
        self.algorithm.setObjectName(u"algorithm")

        self.algorithm_option.addWidget(self.algorithm)


        self.options.addLayout(self.algorithm_option)

        self.algorithm_options = QStackedWidget(self.centralwidget)
        self.algorithm_options.setObjectName(u"algorithm_options")
        self.algorithm_options.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.algorithm_options.sizePolicy().hasHeightForWidth())
        self.algorithm_options.setSizePolicy(sizePolicy1)
        self.algorithm_options.setMinimumSize(QSize(160, 0))
        self.algorithm_options.setAcceptDrops(False)
        self.algorithm_options.setStyleSheet(u"")
        self.algorithm_options.setFrameShape(QFrame.NoFrame)
        self.algorithm_options.setFrameShadow(QFrame.Plain)
        self.algorithm_options.setLineWidth(1)
        self.algorithm_options.setMidLineWidth(0)
        self.th_options = QWidget()
        self.th_options.setObjectName(u"th_options")
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.th_options.sizePolicy().hasHeightForWidth())
        self.th_options.setSizePolicy(sizePolicy2)
        self.verticalLayout = QVBoxLayout(self.th_options)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 6, 0, 6)
        self.th_l = QLabel(self.th_options)
        self.th_l.setObjectName(u"th_l")
        self.th_l.setFont(font)

        self.verticalLayout.addWidget(self.th_l)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.th_top1 = QSpinBox(self.th_options)
        self.th_top1.setObjectName(u"th_top1")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.th_top1.sizePolicy().hasHeightForWidth())
        self.th_top1.setSizePolicy(sizePolicy3)
        self.th_top1.setMinimum(-99999)
        self.th_top1.setMaximum(99999)
        self.th_top1.setSingleStep(25)
        self.th_top1.setValue(50)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.th_top1)

        self.label_3 = QLabel(self.th_options)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.th_bottom1 = QSpinBox(self.th_options)
        self.th_bottom1.setObjectName(u"th_bottom1")
        sizePolicy3.setHeightForWidth(self.th_bottom1.sizePolicy().hasHeightForWidth())
        self.th_bottom1.setSizePolicy(sizePolicy3)
        self.th_bottom1.setMinimum(-99999)
        self.th_bottom1.setMaximum(99999)
        self.th_bottom1.setSingleStep(25)
        self.th_bottom1.setValue(0)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.th_bottom1)

        self.label_7 = QLabel(self.th_options)
        self.label_7.setObjectName(u"label_7")
        sizePolicy3.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy3)

        self.formLayout_4.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.th_top2 = QSpinBox(self.th_options)
        self.th_top2.setObjectName(u"th_top2")
        sizePolicy3.setHeightForWidth(self.th_top2.sizePolicy().hasHeightForWidth())
        self.th_top2.setSizePolicy(sizePolicy3)
        self.th_top2.setMinimum(-99999)
        self.th_top2.setMaximum(99999)
        self.th_top2.setSingleStep(25)
        self.th_top2.setValue(50)

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.th_top2)

        self.label_8 = QLabel(self.th_options)
        self.label_8.setObjectName(u"label_8")
        sizePolicy2.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy2)

        self.formLayout_4.setWidget(4, QFormLayout.LabelRole, self.label_8)

        self.th_bottom2 = QSpinBox(self.th_options)
        self.th_bottom2.setObjectName(u"th_bottom2")
        sizePolicy3.setHeightForWidth(self.th_bottom2.sizePolicy().hasHeightForWidth())
        self.th_bottom2.setSizePolicy(sizePolicy3)
        self.th_bottom2.setMinimum(-99999)
        self.th_bottom2.setMaximum(99999)
        self.th_bottom2.setSingleStep(25)
        self.th_bottom2.setValue(0)

        self.formLayout_4.setWidget(4, QFormLayout.FieldRole, self.th_bottom2)

        self.label_2 = QLabel(self.th_options)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_2)


        self.verticalLayout.addLayout(self.formLayout_4)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.algorithm_options.addWidget(self.th_options)
        self.arnau_options = QWidget()
        self.arnau_options.setObjectName(u"arnau_options")
        self.verticalLayout_2 = QVBoxLayout(self.arnau_options)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_5 = QLabel(self.arnau_options)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setFont(font)

        self.verticalLayout_2.addWidget(self.label_5, 0, Qt.AlignTop)

        self.time_limit = QSpinBox(self.arnau_options)
        self.time_limit.setObjectName(u"time_limit")
        sizePolicy3.setHeightForWidth(self.time_limit.sizePolicy().hasHeightForWidth())
        self.time_limit.setSizePolicy(sizePolicy3)
        self.time_limit.setMinimum(-99999)
        self.time_limit.setMaximum(99999)
        self.time_limit.setSingleStep(25)
        self.time_limit.setValue(300)

        self.verticalLayout_2.addWidget(self.time_limit)

        self.wh_eq = QLabel(self.arnau_options)
        self.wh_eq.setObjectName(u"wh_eq")

        self.verticalLayout_2.addWidget(self.wh_eq)

        self.verticalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.algorithm_options.addWidget(self.arnau_options)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.predict_final_energy = QCheckBox(self.page)
        self.predict_final_energy.setObjectName(u"predict_final_energy")
        sizePolicy3.setHeightForWidth(self.predict_final_energy.sizePolicy().hasHeightForWidth())
        self.predict_final_energy.setSizePolicy(sizePolicy3)
        self.predict_final_energy.setChecked(True)

        self.verticalLayout_3.addWidget(self.predict_final_energy)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.algorithm_options.addWidget(self.page)

        self.options.addWidget(self.algorithm_options)

        self.base_load_option = QVBoxLayout()
        self.base_load_option.setObjectName(u"base_load_option")
        self.bload_l = QLabel(self.centralwidget)
        self.bload_l.setObjectName(u"bload_l")
        self.bload_l.setFont(font)

        self.base_load_option.addWidget(self.bload_l)

        self.formLayout_5 = QFormLayout()
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.formLayout_5.setWidget(1, QFormLayout.LabelRole, self.label)

        self.base_load = QSpinBox(self.centralwidget)
        self.base_load.setObjectName(u"base_load")
        self.base_load.setMaximum(99999)
        self.base_load.setSingleStep(25)

        self.formLayout_5.setWidget(1, QFormLayout.FieldRole, self.base_load)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_5.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.load1 = QSpinBox(self.centralwidget)
        self.load1.setObjectName(u"load1")
        self.load1.setMaximum(99999)
        self.load1.setSingleStep(25)
        self.load1.setValue(1000)

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.load1)

        self.load2 = QSpinBox(self.centralwidget)
        self.load2.setObjectName(u"load2")
        self.load2.setMaximum(99999)
        self.load2.setSingleStep(25)
        self.load2.setValue(1000)

        self.formLayout_5.setWidget(3, QFormLayout.FieldRole, self.load2)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_5.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.use_data_bl = QCheckBox(self.centralwidget)
        self.use_data_bl.setObjectName(u"use_data_bl")
        self.use_data_bl.setEnabled(True)

        self.formLayout_5.setWidget(0, QFormLayout.SpanningRole, self.use_data_bl)


        self.base_load_option.addLayout(self.formLayout_5)


        self.options.addLayout(self.base_load_option)

        self.simulate = QPushButton(self.centralwidget)
        self.simulate.setObjectName(u"simulate")
        self.simulate.setEnabled(False)
        self.simulate.setAutoDefault(False)
        self.simulate.setFlat(False)

        self.options.addWidget(self.simulate)

        self.results = QPushButton(self.centralwidget)
        self.results.setObjectName(u"results")
        self.results.setEnabled(False)
        self.results.setAutoDefault(False)
        self.results.setFlat(False)

        self.options.addWidget(self.results)

        self.recalc_warn = QLabel(self.centralwidget)
        self.recalc_warn.setObjectName(u"recalc_warn")
        self.recalc_warn.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.recalc_warn.sizePolicy().hasHeightForWidth())
        self.recalc_warn.setSizePolicy(sizePolicy3)

        self.options.addWidget(self.recalc_warn, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.options.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addLayout(self.options)

        self.plots = QVBoxLayout()
        self.plots.setObjectName(u"plots")
        self.Help = QTabWidget(self.centralwidget)
        self.Help.setObjectName(u"Help")
        self.Help.setEnabled(True)
        self.Help.setTabPosition(QTabWidget.North)
        self.Help.setTabShape(QTabWidget.Rounded)
        self.plot_dr = MplTwinxWidget()
        self.plot_dr.setObjectName(u"plot_dr")
        self.horizontalLayout_7 = QHBoxLayout(self.plot_dr)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_10 = QLabel(self.plot_dr)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_7.addWidget(self.label_10)

        self.data_line_style = QLineEdit(self.plot_dr)
        self.data_line_style.setObjectName(u"data_line_style")
        self.data_line_style.setEnabled(False)
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.data_line_style.sizePolicy().hasHeightForWidth())
        self.data_line_style.setSizePolicy(sizePolicy4)
        self.data_line_style.setMaximumSize(QSize(50, 16777215))
        self.data_line_style.setMaxLength(5)
        self.data_line_style.setReadOnly(False)

        self.horizontalLayout_7.addWidget(self.data_line_style)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)

        self.Help.addTab(self.plot_dr, "")
        self.global_results = QWidget()
        self.global_results.setObjectName(u"global_results")
        self.verticalLayout_6 = QVBoxLayout(self.global_results)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.plot_eb_t = MplWidget(self.global_results)
        self.plot_eb_t.setObjectName(u"plot_eb_t")
        sizePolicy3.setHeightForWidth(self.plot_eb_t.sizePolicy().hasHeightForWidth())
        self.plot_eb_t.setSizePolicy(sizePolicy3)

        self.horizontalLayout_8.addWidget(self.plot_eb_t)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.table_loads_aprox = QTableView(self.global_results)
        self.table_loads_aprox.setObjectName(u"table_loads_aprox")
        sizePolicy1.setHeightForWidth(self.table_loads_aprox.sizePolicy().hasHeightForWidth())
        self.table_loads_aprox.setSizePolicy(sizePolicy1)
        self.table_loads_aprox.setMaximumSize(QSize(200, 10000000))
        self.table_loads_aprox.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_loads_aprox.setFrameShape(QFrame.NoFrame)
        self.table_loads_aprox.setFrameShadow(QFrame.Plain)
        self.table_loads_aprox.setLineWidth(0)
        self.table_loads_aprox.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_loads_aprox.setAlternatingRowColors(True)
        self.table_loads_aprox.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_loads_aprox.setTextElideMode(Qt.ElideNone)
        self.table_loads_aprox.setSortingEnabled(False)
        self.table_loads_aprox.setWordWrap(True)
        self.table_loads_aprox.horizontalHeader().setCascadingSectionResizes(False)
        self.table_loads_aprox.horizontalHeader().setStretchLastSection(True)
        self.table_loads_aprox.verticalHeader().setVisible(True)
        self.table_loads_aprox.verticalHeader().setMinimumSectionSize(10)

        self.verticalLayout_5.addWidget(self.table_loads_aprox, 0, Qt.AlignRight)

        self.table_eb_t = QTableView(self.global_results)
        self.table_eb_t.setObjectName(u"table_eb_t")
        sizePolicy1.setHeightForWidth(self.table_eb_t.sizePolicy().hasHeightForWidth())
        self.table_eb_t.setSizePolicy(sizePolicy1)
        self.table_eb_t.setMaximumSize(QSize(350, 10000000))
        self.table_eb_t.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_eb_t.setFrameShape(QFrame.NoFrame)
        self.table_eb_t.setFrameShadow(QFrame.Plain)
        self.table_eb_t.setLineWidth(0)
        self.table_eb_t.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_eb_t.setAlternatingRowColors(True)
        self.table_eb_t.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_eb_t.setTextElideMode(Qt.ElideNone)
        self.table_eb_t.setSortingEnabled(False)
        self.table_eb_t.setWordWrap(True)
        self.table_eb_t.horizontalHeader().setCascadingSectionResizes(False)
        self.table_eb_t.horizontalHeader().setStretchLastSection(True)
        self.table_eb_t.verticalHeader().setVisible(True)
        self.table_eb_t.verticalHeader().setMinimumSectionSize(10)

        self.verticalLayout_5.addWidget(self.table_eb_t, 0, Qt.AlignHCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)


        self.horizontalLayout_8.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.table_t = QTableView(self.global_results)
        self.table_t.setObjectName(u"table_t")
        sizePolicy3.setHeightForWidth(self.table_t.sizePolicy().hasHeightForWidth())
        self.table_t.setSizePolicy(sizePolicy3)
        self.table_t.setMaximumSize(QSize(16777215, 16777215))
        self.table_t.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_t.setFrameShape(QFrame.NoFrame)
        self.table_t.setFrameShadow(QFrame.Plain)
        self.table_t.setLineWidth(0)
        self.table_t.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_t.setAlternatingRowColors(True)
        self.table_t.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_t.setSortingEnabled(False)
        self.table_t.horizontalHeader().setCascadingSectionResizes(False)
        self.table_t.horizontalHeader().setStretchLastSection(True)
        self.table_t.verticalHeader().setVisible(True)

        self.verticalLayout_6.addWidget(self.table_t)

        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.show_values_t = QCheckBox(self.global_results)
        self.show_values_t.setObjectName(u"show_values_t")
        self.show_values_t.setEnabled(False)
        self.show_values_t.setChecked(True)

        self.layout.addWidget(self.show_values_t)

        self.line_10 = QFrame(self.global_results)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShadow(QFrame.Plain)
        self.line_10.setLineWidth(0)
        self.line_10.setFrameShape(QFrame.VLine)

        self.layout.addWidget(self.line_10)

        self.subdivide_t = QCheckBox(self.global_results)
        self.subdivide_t.setObjectName(u"subdivide_t")
        self.subdivide_t.setEnabled(False)
        self.subdivide_t.setChecked(True)

        self.layout.addWidget(self.subdivide_t)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.layout)

        self.Help.addTab(self.global_results, "")
        self.plot_s = MplTwinxWidget()
        self.plot_s.setObjectName(u"plot_s")
        self.horizontalLayout_9 = QHBoxLayout(self.plot_s)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_9 = QLabel(self.plot_s)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_9.addWidget(self.label_9)

        self.sim_line_style = QLineEdit(self.plot_s)
        self.sim_line_style.setObjectName(u"sim_line_style")
        self.sim_line_style.setEnabled(False)
        sizePolicy4.setHeightForWidth(self.sim_line_style.sizePolicy().hasHeightForWidth())
        self.sim_line_style.setSizePolicy(sizePolicy4)
        self.sim_line_style.setMaximumSize(QSize(50, 16777215))
        self.sim_line_style.setMaxLength(5)
        self.sim_line_style.setReadOnly(False)

        self.horizontalLayout_9.addWidget(self.sim_line_style)

        self.line_6 = QFrame(self.plot_s)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Plain)
        self.line_6.setLineWidth(0)
        self.line_6.setFrameShape(QFrame.VLine)

        self.horizontalLayout_9.addWidget(self.line_6)

        self.show_loads_area = QCheckBox(self.plot_s)
        self.show_loads_area.setObjectName(u"show_loads_area")
        self.show_loads_area.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.show_loads_area)

        self.line_4 = QFrame(self.plot_s)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setLineWidth(0)
        self.line_4.setFrameShape(QFrame.VLine)

        self.horizontalLayout_9.addWidget(self.line_4)

        self.energyP_s = QCheckBox(self.plot_s)
        self.energyP_s.setObjectName(u"energyP_s")
        self.energyP_s.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.energyP_s)

        self.line_12 = QFrame(self.plot_s)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShadow(QFrame.Plain)
        self.line_12.setLineWidth(0)
        self.line_12.setFrameShape(QFrame.VLine)

        self.horizontalLayout_9.addWidget(self.line_12)

        self.show_th = QCheckBox(self.plot_s)
        self.show_th.setObjectName(u"show_th")
        self.show_th.setEnabled(False)

        self.horizontalLayout_9.addWidget(self.show_th)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)

        self.Help.addTab(self.plot_s, "")
        self.plot_eb = MplWidget()
        self.plot_eb.setObjectName(u"plot_eb")
        self.horizontalLayout_5 = QHBoxLayout(self.plot_eb)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.show_values_eb = QCheckBox(self.plot_eb)
        self.show_values_eb.setObjectName(u"show_values_eb")
        self.show_values_eb.setEnabled(False)

        self.horizontalLayout_5.addWidget(self.show_values_eb)

        self.line_5 = QFrame(self.plot_eb)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setLineWidth(0)
        self.line_5.setFrameShape(QFrame.VLine)

        self.horizontalLayout_5.addWidget(self.line_5)

        self.subdivide_eb = QCheckBox(self.plot_eb)
        self.subdivide_eb.setObjectName(u"subdivide_eb")
        self.subdivide_eb.setEnabled(False)
        self.subdivide_eb.setChecked(True)

        self.horizontalLayout_5.addWidget(self.subdivide_eb)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.Help.addTab(self.plot_eb, "")
        self.tab3 = QWidget()
        self.tab3.setObjectName(u"tab3")
        self.gridLayout_2 = QGridLayout(self.tab3)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.table_in = QTableView(self.tab3)
        self.table_in.setObjectName(u"table_in")
        self.table_in.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_in.setFrameShape(QFrame.NoFrame)
        self.table_in.setFrameShadow(QFrame.Plain)
        self.table_in.setLineWidth(0)
        self.table_in.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_in.setAlternatingRowColors(True)
        self.table_in.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_in.setSortingEnabled(False)
        self.table_in.horizontalHeader().setCascadingSectionResizes(False)
        self.table_in.horizontalHeader().setStretchLastSection(True)
        self.table_in.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.table_in, 0, 0, 1, 1)

        self.Help.addTab(self.tab3, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_6 = QHBoxLayout(self.tab)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.table_s = QTableView(self.tab)
        self.table_s.setObjectName(u"table_s")
        self.table_s.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_s.setFrameShape(QFrame.NoFrame)
        self.table_s.setFrameShadow(QFrame.Plain)
        self.table_s.setLineWidth(0)
        self.table_s.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_s.setAlternatingRowColors(True)
        self.table_s.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_s.setSortingEnabled(False)
        self.table_s.horizontalHeader().setCascadingSectionResizes(False)
        self.table_s.horizontalHeader().setStretchLastSection(True)
        self.table_s.verticalHeader().setVisible(False)

        self.horizontalLayout_6.addWidget(self.table_s)

        self.Help.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.table_eb = QTableView(self.tab_2)
        self.table_eb.setObjectName(u"table_eb")
        self.table_eb.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_eb.setFrameShape(QFrame.NoFrame)
        self.table_eb.setFrameShadow(QFrame.Plain)
        self.table_eb.setLineWidth(0)
        self.table_eb.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_eb.setAlternatingRowColors(True)
        self.table_eb.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_eb.setSortingEnabled(False)
        self.table_eb.setWordWrap(False)
        self.table_eb.horizontalHeader().setCascadingSectionResizes(False)
        self.table_eb.horizontalHeader().setStretchLastSection(True)
        self.table_eb.verticalHeader().setVisible(False)

        self.verticalLayout_4.addWidget(self.table_eb)

        self.Help.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_3 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.textEdit = QTextEdit(self.tab_3)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setFrameShadow(QFrame.Plain)
        self.textEdit.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.textEdit)

        self.Help.addTab(self.tab_3, "")

        self.plots.addWidget(self.Help)


        self.horizontalLayout_2.addLayout(self.plots)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.data_source = QVBoxLayout()
        self.data_source.setObjectName(u"data_source")
        self.data_source.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.load_file = QPushButton(self.centralwidget)
        self.load_file.setObjectName(u"load_file")

        self.horizontalLayout.addWidget(self.load_file)

        self.file_path = QLineEdit(self.centralwidget)
        self.file_path.setObjectName(u"file_path")
        self.file_path.setEnabled(True)
        self.file_path.setReadOnly(True)

        self.horizontalLayout.addWidget(self.file_path)


        self.data_source.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.sampling_rate = QLabel(self.centralwidget)
        self.sampling_rate.setObjectName(u"sampling_rate")

        self.horizontalLayout_4.addWidget(self.sampling_rate)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.VLine)

        self.horizontalLayout_4.addWidget(self.line)

        self.date_range = QLabel(self.centralwidget)
        self.date_range.setObjectName(u"date_range")

        self.horizontalLayout_4.addWidget(self.date_range)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(0)
        self.line_2.setFrameShape(QFrame.VLine)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.simulation_time = QLabel(self.centralwidget)
        self.simulation_time.setObjectName(u"simulation_time")

        self.horizontalLayout_4.addWidget(self.simulation_time)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setLineWidth(0)
        self.line_3.setFrameShape(QFrame.VLine)

        self.horizontalLayout_4.addWidget(self.line_3)

        self.plotting_time = QLabel(self.centralwidget)
        self.plotting_time.setObjectName(u"plotting_time")

        self.horizontalLayout_4.addWidget(self.plotting_time)

        self.line_11 = QFrame(self.centralwidget)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShadow(QFrame.Plain)
        self.line_11.setLineWidth(0)
        self.line_11.setFrameShape(QFrame.VLine)

        self.horizontalLayout_4.addWidget(self.line_11)

        self.n_samples = QLabel(self.centralwidget)
        self.n_samples.setObjectName(u"n_samples")

        self.horizontalLayout_4.addWidget(self.n_samples)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)


        self.data_source.addLayout(self.horizontalLayout_4)


        self.gridLayout.addLayout(self.data_source, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1082, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.load_file, self.start_date)
        QWidget.setTabOrder(self.start_date, self.end_date)
        QWidget.setTabOrder(self.end_date, self.algorithm)
        QWidget.setTabOrder(self.algorithm, self.th_top1)
        QWidget.setTabOrder(self.th_top1, self.th_bottom1)
        QWidget.setTabOrder(self.th_bottom1, self.th_top2)
        QWidget.setTabOrder(self.th_top2, self.th_bottom2)
        QWidget.setTabOrder(self.th_bottom2, self.use_data_bl)
        QWidget.setTabOrder(self.use_data_bl, self.base_load)
        QWidget.setTabOrder(self.base_load, self.load1)
        QWidget.setTabOrder(self.load1, self.load2)
        QWidget.setTabOrder(self.load2, self.simulate)
        QWidget.setTabOrder(self.simulate, self.results)
        QWidget.setTabOrder(self.results, self.Help)
        QWidget.setTabOrder(self.Help, self.time_limit)
        QWidget.setTabOrder(self.time_limit, self.predict_final_energy)
        QWidget.setTabOrder(self.predict_final_energy, self.data_line_style)
        QWidget.setTabOrder(self.data_line_style, self.table_eb_t)
        QWidget.setTabOrder(self.table_eb_t, self.table_t)
        QWidget.setTabOrder(self.table_t, self.show_values_t)
        QWidget.setTabOrder(self.show_values_t, self.file_path)
        QWidget.setTabOrder(self.file_path, self.sim_line_style)
        QWidget.setTabOrder(self.sim_line_style, self.subdivide_t)
        QWidget.setTabOrder(self.subdivide_t, self.show_loads_area)
        QWidget.setTabOrder(self.show_loads_area, self.energyP_s)
        QWidget.setTabOrder(self.energyP_s, self.show_th)
        QWidget.setTabOrder(self.show_th, self.show_values_eb)
        QWidget.setTabOrder(self.show_values_eb, self.subdivide_eb)
        QWidget.setTabOrder(self.subdivide_eb, self.table_in)
        QWidget.setTabOrder(self.table_in, self.table_s)
        QWidget.setTabOrder(self.table_s, self.table_eb)
        QWidget.setTabOrder(self.table_eb, self.textEdit)

        self.retranslateUi(MainWindow)
        self.algorithm.currentIndexChanged.connect(self.recalc_warn.show)
        self.start_date.dateTimeChanged.connect(self.recalc_warn.show)
        self.simulate.clicked.connect(self.recalc_warn.hide)
        self.file_path.textChanged.connect(self.recalc_warn.show)
        self.end_date.dateTimeChanged.connect(self.recalc_warn.show)
        self.th_top1.valueChanged.connect(self.recalc_warn.show)
        self.th_top2.valueChanged.connect(self.recalc_warn.show)
        self.th_bottom1.valueChanged.connect(self.recalc_warn.show)
        self.base_load.valueChanged.connect(self.recalc_warn.show)
        self.load1.valueChanged.connect(self.recalc_warn.show)
        self.load2.valueChanged.connect(self.recalc_warn.show)
        self.time_limit.valueChanged.connect(self.recalc_warn.show)
        self.predict_final_energy.clicked.connect(self.recalc_warn.show)
        self.algorithm.currentIndexChanged.connect(self.algorithm_options.setCurrentIndex)
        self.use_data_bl.toggled.connect(self.recalc_warn.show)
        self.load_file.clicked.connect(self.recalc_warn.show)

        self.algorithm_options.setCurrentIndex(0)
        self.simulate.setDefault(False)
        self.results.setDefault(False)
        self.Help.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Simulation", None))
#if QT_CONFIG(tooltip)
        self.time_l.setToolTip(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Can also select the dates ranges using the plot: <br />  - Select a date line to move it <br />  - Pres ESC to cancel the move</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.time_l.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Date &amp; Time</p></body></html>", None))
        self.start_date_l.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.start_date.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm", None))
        self.end_date.setDisplayFormat(QCoreApplication.translate("MainWindow", u"yyyy-MM-dd HH:mm", None))
        self.end_date_l.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.algorithm_l.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-weight:700;\">Algorithm</span></p></body></html>", None))
        self.algorithm.setItemText(0, QCoreApplication.translate("MainWindow", u"Hysteresis", None))
        self.algorithm.setItemText(1, QCoreApplication.translate("MainWindow", u"Min On Time (Arnau)", None))
        self.algorithm.setItemText(2, QCoreApplication.translate("MainWindow", u"Time To Consume", None))

        self.th_l.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:700;\">Threshold</span></p></body></html>", None))
        self.th_top1.setSuffix(QCoreApplication.translate("MainWindow", u" Wh", None))
        self.th_top1.setPrefix("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Bottom L1", None))
        self.th_bottom1.setSuffix(QCoreApplication.translate("MainWindow", u" Wh", None))
        self.th_bottom1.setPrefix("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Top L2", None))
        self.th_top2.setSuffix(QCoreApplication.translate("MainWindow", u" Wh", None))
        self.th_top2.setPrefix("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Bottom L2", None))
        self.th_bottom2.setSuffix(QCoreApplication.translate("MainWindow", u" Wh", None))
        self.th_bottom2.setPrefix("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Top L1", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt;\">Time Limit</span></p></body></html>", None))
        self.time_limit.setSuffix(QCoreApplication.translate("MainWindow", u" s", None))
        self.time_limit.setPrefix("")
        self.wh_eq.setText(QCoreApplication.translate("MainWindow", u"= Wh", None))
        self.predict_final_energy.setText(QCoreApplication.translate("MainWindow", u"Predict Final Energy", None))
        self.bload_l.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Loads</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("MainWindow", u"External / Not controled", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Base", None))
        self.base_load.setSuffix(QCoreApplication.translate("MainWindow", u" W", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Load 1", None))
        self.load1.setSuffix(QCoreApplication.translate("MainWindow", u" W", None))
        self.load2.setSuffix(QCoreApplication.translate("MainWindow", u" W", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Load 2", None))
        self.use_data_bl.setText(QCoreApplication.translate("MainWindow", u"Use data Base Load", None))
        self.simulate.setText(QCoreApplication.translate("MainWindow", u"Simulate", None))
        self.results.setText(QCoreApplication.translate("MainWindow", u"Results", None))
        self.recalc_warn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; color:#f4b300;\">\u26a0</span><span style=\" color:#f4b300;\"> Recalculate \u26a0</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Line Style", None))
        self.data_line_style.setInputMask("")
        self.data_line_style.setText("")
        self.Help.setTabText(self.Help.indexOf(self.plot_dr), QCoreApplication.translate("MainWindow", u"\u231a Data Range/In", None))
        self.show_values_t.setText(QCoreApplication.translate("MainWindow", u"Show values (rounded)", None))
        self.subdivide_t.setText(QCoreApplication.translate("MainWindow", u"Subdivide", None))
        self.Help.setTabText(self.Help.indexOf(self.global_results), QCoreApplication.translate("MainWindow", u"\ud83d\udcca\ud83d\udcc5 Summary", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Line Style", None))
        self.sim_line_style.setInputMask("")
        self.sim_line_style.setText("")
        self.show_loads_area.setText(QCoreApplication.translate("MainWindow", u"Power Consumed by Load", None))
        self.energyP_s.setText(QCoreApplication.translate("MainWindow", u"Energy Produced", None))
        self.show_th.setText(QCoreApplication.translate("MainWindow", u"Show Thresholds", None))
        self.Help.setTabText(self.Help.indexOf(self.plot_s), QCoreApplication.translate("MainWindow", u"\ud83d\udcc9 Simulation", None))
        self.show_values_eb.setText(QCoreApplication.translate("MainWindow", u"Show values (rounded)", None))
        self.subdivide_eb.setText(QCoreApplication.translate("MainWindow", u"Subdivide", None))
        self.Help.setTabText(self.Help.indexOf(self.plot_eb), QCoreApplication.translate("MainWindow", u"\ud83d\udcca Enegry Balance", None))
        self.Help.setTabText(self.Help.indexOf(self.tab3), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Data In", None))
        self.Help.setTabText(self.Help.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Simulation", None))
        self.Help.setTabText(self.Help.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Energy Balance", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:11pt; font-weight:700;\">What is this</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">This is a simulator/analyzer of a load manager for a very specific and neash area.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sego"
                        "e UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">In Spain, the energy bill goes as follows. At the end of every hour a energy balance is calculated, </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">energyConsumed - energyGenerated.</span><span style=\" font-family:'Segoe UI','sans-serif';\"> If you have consumed more energy that produced, you must pay that difference. If instead you have produced more that consumed, the company has to pay you.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','s"
                        "ans-serif';\">Thanks to this hour slot system, you can for example consume 1 KWh of energy in the first 10 min and then produce 1KWh during 20 min thus having a net zero consumption and not paying anything.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Segoe UI','sans-serif';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">This project aims to create an intelligent system that manages loads adequately so to achieve or at least get close to a neat zero o even positive income (produce more that consumed) system.\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-"
                        "top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:11pt; font-weight:700;\">Load File</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">Select a .csv file to load the data. If simulating, it must at least have the columns:</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">timestamp -&gt; </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">string of datetime (ex: 2022-02-01 15:57:50)</span> </p>\n"
"<p"
                        " style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">powerG</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> -&gt; float (stands for powerGenerated)</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">If loading it for calculating the results of real data, it must have the previous columns plus:</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p styl"
                        "e=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">energyA -&gt; </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">float (stands for energyAvailable)</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">powerC -&gt; </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">float (stands for powerConsumed)</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">powerL1 -&gt; </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">float (stands for powerLoad1)</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px"
                        "; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">on_offL1 -&gt; </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">[0, 1, -1] (no change, turned on, turned off)</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:11pt; font-weight:700;\">Date &amp; Time</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">Indicates the day and time from where the simulation starts and ends. This values range are limited by the dataset give. </span></p>\n"
"<p style=\" margin-top:"
                        "0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">You can use the scroll wheel to increment/decrement the value. You can also select the dates ranges using the plot in </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">Date Range</span><span style=\" font-family:'Segoe UI','sans-serif';\">: <br />- Select a date line to move it <br />- Pres ESC to cancel the move</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0p"
                        "x;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:11pt; font-weight:700;\">Algorithm</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">You can select what algorithm to simulate and it's associated settings.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Hysteresis</span><span style=\" font-family:'Segoe UI','sans-serif';\"> As the names says, loads are controlled using hysteresis. It allows for up two loads to be managed. Each top and bottom threshold corresponds to the load with the same num"
                        "ber. If the load is 0, the thresholds get disabled.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Min On Use</span><span style=\" font-family:'Segoe UI','sans-serif';\"> Controls only one load, which is turned on when the time it would take to consume the energy accumulated is equal or greater than the time indicated, and will stay on until that time has passed. It's equivalent to having a single threshold (which is also calculated for reference). While the load is on, it keeps doing the check and refreshing the timer.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent"
                        ":0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Time to consume</span><span style=\" font-family:'Segoe UI','sans-serif';\"> Controls only one load, which is turned on when the time it would take to consume the energy accumulated is equal or greater than the time left to end the hour. If the flag </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">predict final energy</span><span style=\" font-family:'Segoe UI','sans-serif';\"> is turned on, it will also predict the energy that it will probably generate during the time it's on. The equation is </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">energyEnd = energyA + timeLeft * powerG / 3600 </span><span style=\" font-family:'Segoe UI','sans-serif';\">in Wh.</span> </p>\n"
""
                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">Because of how energy is calculated, at each hour the load doesn't always turn off. The formula is </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">energyA = ( powerG - powerC ) * Ts / 3600 + energyA, </span><span style=\" font-family:'Segoe UI','sans-serif';\">which means we are supposing/&quot;predicting&quot; that after Ts will have produced</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> energyP = ( powerG - powerC ) * Ts / 3600 </span><span style=\" font-family:'Segoe UI','sans-serif';\">Wh. If we instead did </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style"
                        ":italic;\">energyP = ( powerG(-1) - powerC(-1) ) * Ts / 3600 </span><span style=\" font-family:'Segoe UI','sans-serif';\">and at t=0 </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">energy = 0</span><span style=\" font-family:'Segoe UI','sans-serif';\"> we would not have this prediction. We might think this can be problematic, but in fact is the opposite, since it vastly improves the algorithms by avoiding a lot of possible commutations because of the fact that we don\u2019t start at 0 Wh.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:11pt; font-weight:700;\">Loads</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-l"
                        "eft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">Depending on the number of loads that the algorithm supports, the fields get disabled.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">- </span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Base Load</span><span style=\" font-family:'Segoe UI','sans-serif';\"> represent the constant power draw of a building. It can be 0 if needed to not factor it.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sa"
                        "ns-serif'; font-size:11pt; font-weight:700;\">Tabs</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; text-decoration: underline;\">\u231a</span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\"> Data Range/In</span><span style=\" font-family:'Segoe UI','sans-serif';\"> Used to seeing the input data (power generated) from the .csv and to also easily changing the date and time interval by:</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">- Select a date line to move it <br />- Pres ESC to cancel the move</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</"
                        "span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; font-weight:700;\">\ud83d\udcca</span><span style=\" font-family:'Segoe UI Emoji','sans-serif'; text-decoration: underline;\">\ud83d\udcc5</span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\"> Summary</span><span style=\" font-family:'Segoe UI','sans-serif';\"> After simulating or calculating results, this tab contains the important results. It also has two plot options that are very useful:</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">- Show values</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> displays a label next to each bar/area value.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-"
                        "left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">- </span><span style=\" font-family:'Segoe UI','sans-serif';\">Subdivide</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> each bar is subdivided in its relevant data parts.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; font-weight:700; text-decoration: underline;\">\ud83d\udcc9</span><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; text-decoration: underline;\"> </span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Simulation</span><span style=\" f"
                        "ont-family:'Segoe UI','sans-serif';\"> After  simulating or calculating results, is filled with a plot of the simulated data.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">- Power Consumed by Loads</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> shows the loads plots as a stacked area, this helps see the components of Power Consumed.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">- Power Produced</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> shows all the energy produced which is equal to energyC + energyA.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-"
                        "family:'Segoe UI','sans-serif';\">- Show threshold</span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\"> displays horizontal lines corresponding to each threshold (works in &quot;hysteresis&quot; and in &quot;min on use&quot;).</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; font-weight:700; text-decoration: underline;\">\ud83d\udcca</span><span style=\" font-family:'Segoe UI','sans-serif'; font-weight:700; text-decoration: underline;\"> </span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Energy Balance</span><span style=\" font-family:'Segoe UI','sans-serif';\"> After  simulating or calculating results, conta"
                        "ins the hourly breakdown of the energy balance (the sum of this breakdown is shown in summary). Both plot options in summary are also available here.</span> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; text-decoration: underline;\">\ud83d\udcc5</span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\"> Data In</span><span style=\" font-family:'Segoe UI','sans-serif';\"> After importing the .csv, it shows the table with the document data.</span> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-r"
                        "ight:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; text-decoration: underline;\">\ud83d\udcc5</span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\"> Simulation</span><span style=\" font-family:'Segoe UI','sans-serif';\"> After  simulating or calculating results, it contains the table of all the simulated data (which is plotted at the other simulation tab)</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI Emoji','sans-serif'; text-decoration: underline;\">\ud83d\udcc5</span><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\"> Energy Balance</span><span style=\" font-family:'Seg"
                        "oe UI','sans-serif';\"> After  simulating or calculating results, it shows the table of all the energy balance data (which is plotted at the energy balance tab).</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; font-size:11pt; font-weight:700;\">Plots</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">The plots have the standard </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">maptlotlib</span><span style=\" font-family:'Segoe UI','sans-serif';\"> functionally plus some extra options. </span></p>\n"
"<p style=\""
                        " margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Cross Hair Cursor</span><span style=\" font-family:'Segoe UI','sans-serif';\"> Toggled by selecting the toolbar buttons + it displays a cross hair which snaps to the closest point of the data line. To change the line it snaps, you simply have to select it.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans"
                        "-serif'; text-decoration: underline;\">Line Style</span><span style=\" font-family:'Segoe UI','sans-serif';\"> A input that accepts any </span><span style=\" font-family:'Segoe UI','sans-serif'; font-style:italic;\">matplotlib </span><span style=\" font-family:'Segoe UI','sans-serif';\">line style and marker to apply to the displayed lines.</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif';\">\u00a0</span> </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Segoe UI','sans-serif'; text-decoration: underline;\">Hide lines</span><span style=\" font-family:'Segoe UI','sans-serif';\"> Any line in a plot can be hidden by pressing the lines in the legend. Hidden lines still show in the legend but more transparent.</span> </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top"
                        ":12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.Help.setTabText(self.Help.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u2139 Help", None))
        self.load_file.setText(QCoreApplication.translate("MainWindow", u"Load File", None))
        self.sampling_rate.setText(QCoreApplication.translate("MainWindow", u"Sample Rate", None))
        self.date_range.setText(QCoreApplication.translate("MainWindow", u"Date Range", None))
        self.simulation_time.setText(QCoreApplication.translate("MainWindow", u"Simulation Time", None))
        self.plotting_time.setText(QCoreApplication.translate("MainWindow", u"Plotting Time", None))
        self.n_samples.setText(QCoreApplication.translate("MainWindow", u"N Samples", None))
    # retranslateUi

