# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
    QComboBox, QDateTimeEdit, QDoubleSpinBox, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QStatusBar, QTabWidget,
    QTableView, QTextEdit, QVBoxLayout, QWidget)

from QMplWidgets import (QMplPlot, QMplPlotterWidget, QMplTwinxPlot)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1508, 843)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
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
"QTableView:item:selected {\n"
"	background-color: #007ac9; \n"
"	color: #FFFFFF;\n"
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
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
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
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.algorithm_options.addWidget(self.page_2)
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
        self.th_top1.setSingleStep(10)
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
        self.th_bottom1.setSingleStep(10)
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
        self.th_top2.setSingleStep(10)
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
        self.th_bottom2.setSingleStep(10)
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
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_5 = QLabel(self.arnau_options)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.time_limit = QSpinBox(self.arnau_options)
        self.time_limit.setObjectName(u"time_limit")
        sizePolicy3.setHeightForWidth(self.time_limit.sizePolicy().hasHeightForWidth())
        self.time_limit.setSizePolicy(sizePolicy3)
        self.time_limit.setMinimum(-99999)
        self.time_limit.setMaximum(99999)
        self.time_limit.setSingleStep(25)
        self.time_limit.setValue(300)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.time_limit)

        self.label_31 = QLabel(self.arnau_options)
        self.label_31.setObjectName(u"label_31")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_31)

        self.mot_mode = QComboBox(self.arnau_options)
        self.mot_mode.addItem("")
        self.mot_mode.addItem("")
        self.mot_mode.addItem("")
        self.mot_mode.setObjectName(u"mot_mode")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.mot_mode)


        self.verticalLayout_2.addLayout(self.formLayout)

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
        self.label_11 = QLabel(self.page)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_3.addWidget(self.label_11)

        self.predict_final_energy = QComboBox(self.page)
        self.predict_final_energy.addItem("")
        self.predict_final_energy.addItem("")
        self.predict_final_energy.addItem("")
        self.predict_final_energy.setObjectName(u"predict_final_energy")

        self.verticalLayout_3.addWidget(self.predict_final_energy)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_18 = QLabel(self.page)
        self.label_18.setObjectName(u"label_18")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.label_18)

        self.ttc_end_at = QSpinBox(self.page)
        self.ttc_end_at.setObjectName(u"ttc_end_at")
        self.ttc_end_at.setMaximum(999)
        self.ttc_end_at.setSingleStep(5)
        self.ttc_end_at.setValue(100)

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.ttc_end_at)

        self.label_19 = QLabel(self.page)
        self.label_19.setObjectName(u"label_19")

        self.formLayout_6.setWidget(1, QFormLayout.LabelRole, self.label_19)

        self.label_20 = QLabel(self.page)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_6.setWidget(2, QFormLayout.LabelRole, self.label_20)

        self.ttc_on_min = QSpinBox(self.page)
        self.ttc_on_min.setObjectName(u"ttc_on_min")
        self.ttc_on_min.setMaximum(9999)
        self.ttc_on_min.setSingleStep(10)
        self.ttc_on_min.setValue(100)

        self.formLayout_6.setWidget(2, QFormLayout.FieldRole, self.ttc_on_min)

        self.ttc_time_factor = QDoubleSpinBox(self.page)
        self.ttc_time_factor.setObjectName(u"ttc_time_factor")
        self.ttc_time_factor.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.ttc_time_factor.setMaximum(1.000000000000000)
        self.ttc_time_factor.setSingleStep(0.100000000000000)
        self.ttc_time_factor.setValue(1.000000000000000)

        self.formLayout_6.setWidget(1, QFormLayout.FieldRole, self.ttc_time_factor)


        self.verticalLayout_3.addLayout(self.formLayout_6)

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
        self.load1.setMinimum(25)
        self.load1.setMaximum(99999)
        self.load1.setSingleStep(25)
        self.load1.setValue(500)

        self.formLayout_5.setWidget(2, QFormLayout.FieldRole, self.load1)

        self.load2 = QSpinBox(self.centralwidget)
        self.load2.setObjectName(u"load2")
        self.load2.setMaximum(99999)
        self.load2.setSingleStep(25)
        self.load2.setValue(500)

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

        self.algorithm_option_2 = QVBoxLayout()
        self.algorithm_option_2.setObjectName(u"algorithm_option_2")
        self.algorithm_l_2 = QLabel(self.centralwidget)
        self.algorithm_l_2.setObjectName(u"algorithm_l_2")
        self.algorithm_l_2.setFont(font)

        self.algorithm_option_2.addWidget(self.algorithm_l_2)

        self.generation_factor = QDoubleSpinBox(self.centralwidget)
        self.generation_factor.setObjectName(u"generation_factor")
        self.generation_factor.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.generation_factor.setMaximum(10.000000000000000)
        self.generation_factor.setSingleStep(0.100000000000000)
        self.generation_factor.setValue(1.000000000000000)

        self.algorithm_option_2.addWidget(self.generation_factor)


        self.options.addLayout(self.algorithm_option_2)

        self.simulate = QPushButton(self.centralwidget)
        self.simulate.setObjectName(u"simulate")
        self.simulate.setEnabled(False)
        self.simulate.setAutoDefault(False)
        self.simulate.setFlat(False)
        self.simulate.setProperty("dataValidEnable", True)

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
        self.recalc_warn.setAlignment(Qt.AlignCenter)

        self.options.addWidget(self.recalc_warn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.options.addItem(self.verticalSpacer)


        self.gridLayout.addLayout(self.options, 0, 0, 1, 1)

        self.data = QVBoxLayout()
        self.data.setObjectName(u"data")
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setEnabled(True)
        self.tabs.setMinimumSize(QSize(1280, 720))
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setTabShape(QTabWidget.Rounded)
        self.tabs.setElideMode(Qt.ElideNone)
        self.daterange_t = QWidget()
        self.daterange_t.setObjectName(u"daterange_t")
        self.daterange_t.setStyleSheet(u"")
        self.horizontalLayout_7 = QHBoxLayout(self.daterange_t)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 1, 0, 0)
        self.tabWidget = QTabWidget(self.daterange_t)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setStyleSheet(u"QTabWidget::pane { /* The tab widget frame */\n"
"	left:-1px;\n"
"	top: -1px;\n"
"    bottom: -3px;\n"
"	right: -3px;\n"
"}")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.plot_dr = QMplTwinxPlot()
        self.plot_dr.setObjectName(u"plot_dr")
        self.horizontalLayout_10 = QHBoxLayout(self.plot_dr)
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(9, 9, 9, 9)
        self.label_10 = QLabel(self.plot_dr)
        self.label_10.setObjectName(u"label_10")
        sizePolicy1.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy1)

        self.horizontalLayout_10.addWidget(self.label_10)

        self.data_line_style = QLineEdit(self.plot_dr)
        self.data_line_style.setObjectName(u"data_line_style")
        self.data_line_style.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.data_line_style.sizePolicy().hasHeightForWidth())
        self.data_line_style.setSizePolicy(sizePolicy4)
        self.data_line_style.setMaximumSize(QSize(50, 16777215))
        self.data_line_style.setMaxLength(5)
        self.data_line_style.setReadOnly(False)

        self.horizontalLayout_10.addWidget(self.data_line_style)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_8)

        self.tabWidget.addTab(self.plot_dr, "")
        self.table_dr_t = QWidget()
        self.table_dr_t.setObjectName(u"table_dr_t")
        self.horizontalLayout_13 = QHBoxLayout(self.table_dr_t)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 2, 0, 0)
        self.table_in = QTableView(self.table_dr_t)
        self.table_in.setObjectName(u"table_in")
        self.table_in.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_in.setFrameShape(QFrame.NoFrame)
        self.table_in.setFrameShadow(QFrame.Plain)
        self.table_in.setLineWidth(0)
        self.table_in.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_in.setAlternatingRowColors(True)
        self.table_in.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_in.setSortingEnabled(False)
        self.table_in.horizontalHeader().setCascadingSectionResizes(False)
        self.table_in.horizontalHeader().setStretchLastSection(False)
        self.table_in.verticalHeader().setVisible(False)
        self.table_in.verticalHeader().setHighlightSections(True)

        self.horizontalLayout_13.addWidget(self.table_in)

        self.tabWidget.addTab(self.table_dr_t, "")

        self.horizontalLayout_7.addWidget(self.tabWidget)

        self.tabs.addTab(self.daterange_t, "")
        self.price_t = QWidget()
        self.price_t.setObjectName(u"price_t")
        self.verticalLayout_4 = QVBoxLayout(self.price_t)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.plot_price = QMplPlotterWidget(self.price_t)
        self.plot_price.setObjectName(u"plot_price")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.plot_price.sizePolicy().hasHeightForWidth())
        self.plot_price.setSizePolicy(sizePolicy5)

        self.verticalLayout_11.addWidget(self.plot_price)

        self.table_price_energy = QTableView(self.price_t)
        self.table_price_energy.setObjectName(u"table_price_energy")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.table_price_energy.sizePolicy().hasHeightForWidth())
        self.table_price_energy.setSizePolicy(sizePolicy6)
        self.table_price_energy.setMaximumSize(QSize(10000000, 1000))
        self.table_price_energy.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_price_energy.setFrameShape(QFrame.NoFrame)
        self.table_price_energy.setFrameShadow(QFrame.Plain)
        self.table_price_energy.setLineWidth(0)
        self.table_price_energy.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_price_energy.setAlternatingRowColors(True)
        self.table_price_energy.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_price_energy.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_price_energy.setTextElideMode(Qt.ElideNone)
        self.table_price_energy.setSortingEnabled(False)
        self.table_price_energy.setWordWrap(True)
        self.table_price_energy.horizontalHeader().setCascadingSectionResizes(False)
        self.table_price_energy.horizontalHeader().setStretchLastSection(False)
        self.table_price_energy.verticalHeader().setVisible(True)
        self.table_price_energy.verticalHeader().setMinimumSectionSize(10)
        self.table_price_energy.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_11.addWidget(self.table_price_energy)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.label_21 = QLabel(self.price_t)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_17.addWidget(self.label_21)

        self.sell_price = QDoubleSpinBox(self.price_t)
        self.sell_price.setObjectName(u"sell_price")
        sizePolicy3.setHeightForWidth(self.sell_price.sizePolicy().hasHeightForWidth())
        self.sell_price.setSizePolicy(sizePolicy3)
        self.sell_price.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.sell_price.setDecimals(5)
        self.sell_price.setMaximum(10.000000000000000)
        self.sell_price.setSingleStep(0.010000000000000)
        self.sell_price.setValue(0.100000000000000)

        self.horizontalLayout_17.addWidget(self.sell_price)

        self.line_13 = QFrame(self.price_t)
        self.line_13.setObjectName(u"line_13")
        self.line_13.setFrameShadow(QFrame.Plain)
        self.line_13.setLineWidth(0)
        self.line_13.setFrameShape(QFrame.VLine)

        self.horizontalLayout_17.addWidget(self.line_13)

        self.label_22 = QLabel(self.price_t)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_17.addWidget(self.label_22)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_6)


        self.verticalLayout_11.addLayout(self.horizontalLayout_17)


        self.verticalLayout_4.addLayout(self.verticalLayout_11)

        self.tabs.addTab(self.price_t, "")
        self.global_results = QWidget()
        self.global_results.setObjectName(u"global_results")
        self.verticalLayout_6 = QVBoxLayout(self.global_results)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(9, 9, 9, 9)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.plot_eb_t = QMplPlot(self.global_results)
        self.plot_eb_t.setObjectName(u"plot_eb_t")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.plot_eb_t.sizePolicy().hasHeightForWidth())
        self.plot_eb_t.setSizePolicy(sizePolicy7)

        self.horizontalLayout_8.addWidget(self.plot_eb_t)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_5 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.table_eb_t = QTableView(self.global_results)
        self.table_eb_t.setObjectName(u"table_eb_t")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.table_eb_t.sizePolicy().hasHeightForWidth())
        self.table_eb_t.setSizePolicy(sizePolicy8)
        self.table_eb_t.setMinimumSize(QSize(350, 0))
        self.table_eb_t.setMaximumSize(QSize(350, 10000000))
        self.table_eb_t.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_eb_t.setFrameShape(QFrame.NoFrame)
        self.table_eb_t.setFrameShadow(QFrame.Plain)
        self.table_eb_t.setLineWidth(0)
        self.table_eb_t.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_eb_t.setAlternatingRowColors(True)
        self.table_eb_t.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_eb_t.setTextElideMode(Qt.ElideNone)
        self.table_eb_t.setSortingEnabled(False)
        self.table_eb_t.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.table_eb_t, 0, Qt.AlignHCenter)

        self.verticalSpacer_6 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)


        self.horizontalLayout_8.addLayout(self.verticalLayout_5)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.table_t = QTableView(self.global_results)
        self.table_t.setObjectName(u"table_t")
        sizePolicy3.setHeightForWidth(self.table_t.sizePolicy().hasHeightForWidth())
        self.table_t.setSizePolicy(sizePolicy3)
        self.table_t.setMaximumSize(QSize(16777215, 16777215))
        self.table_t.setBaseSize(QSize(0, 0))
        self.table_t.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_t.setFrameShape(QFrame.NoFrame)
        self.table_t.setFrameShadow(QFrame.Plain)
        self.table_t.setLineWidth(0)
        self.table_t.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_t.setAlternatingRowColors(True)
        self.table_t.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_t.setSortingEnabled(False)

        self.verticalLayout_6.addWidget(self.table_t)

        self.layout = QHBoxLayout()
        self.layout.setObjectName(u"layout")
        self.show_values_t = QCheckBox(self.global_results)
        self.show_values_t.setObjectName(u"show_values_t")
        self.show_values_t.setEnabled(True)
        self.show_values_t.setChecked(True)

        self.layout.addWidget(self.show_values_t)

        self.line_8 = QFrame(self.global_results)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShadow(QFrame.Plain)
        self.line_8.setLineWidth(0)
        self.line_8.setFrameShape(QFrame.VLine)

        self.layout.addWidget(self.line_8)

        self.show_ecm_t = QCheckBox(self.global_results)
        self.show_ecm_t.setObjectName(u"show_ecm_t")
        self.show_ecm_t.setEnabled(True)

        self.layout.addWidget(self.show_ecm_t)

        self.line_10 = QFrame(self.global_results)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShadow(QFrame.Plain)
        self.line_10.setLineWidth(0)
        self.line_10.setFrameShape(QFrame.VLine)

        self.layout.addWidget(self.line_10)

        self.label_27 = QLabel(self.global_results)
        self.label_27.setObjectName(u"label_27")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy9)

        self.layout.addWidget(self.label_27)

        self.subdivide_t = QComboBox(self.global_results)
        self.subdivide_t.addItem("")
        self.subdivide_t.addItem("")
        self.subdivide_t.addItem("")
        self.subdivide_t.setObjectName(u"subdivide_t")

        self.layout.addWidget(self.subdivide_t)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_6.addLayout(self.layout)

        self.tabs.addTab(self.global_results, "")
        self.simulation_t = QWidget()
        self.simulation_t.setObjectName(u"simulation_t")
        self.horizontalLayout_9 = QHBoxLayout(self.simulation_t)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 1, 0, 0)
        self.tabWidget_2 = QTabWidget(self.simulation_t)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setStyleSheet(u"QTabWidget::pane { /* The tab widget frame */\n"
"	left:-1px;\n"
"	top: -1px;\n"
"    bottom: -3px;\n"
"	right: -3px;\n"
"}")
        self.plot_s = QMplTwinxPlot()
        self.plot_s.setObjectName(u"plot_s")
        self.horizontalLayout_14 = QHBoxLayout(self.plot_s)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(9, -1, -1, -1)
        self.label_9 = QLabel(self.plot_s)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_14.addWidget(self.label_9)

        self.sim_line_style = QLineEdit(self.plot_s)
        self.sim_line_style.setObjectName(u"sim_line_style")
        self.sim_line_style.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.sim_line_style.sizePolicy().hasHeightForWidth())
        self.sim_line_style.setSizePolicy(sizePolicy4)
        self.sim_line_style.setMaximumSize(QSize(50, 16777215))
        self.sim_line_style.setMaxLength(5)
        self.sim_line_style.setReadOnly(False)

        self.horizontalLayout_14.addWidget(self.sim_line_style)

        self.line_6 = QFrame(self.plot_s)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Plain)
        self.line_6.setLineWidth(0)
        self.line_6.setFrameShape(QFrame.VLine)

        self.horizontalLayout_14.addWidget(self.line_6)

        self.show_loads_area = QCheckBox(self.plot_s)
        self.show_loads_area.setObjectName(u"show_loads_area")
        self.show_loads_area.setEnabled(True)

        self.horizontalLayout_14.addWidget(self.show_loads_area)

        self.line_9 = QFrame(self.plot_s)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShadow(QFrame.Plain)
        self.line_9.setFrameShape(QFrame.VLine)

        self.horizontalLayout_14.addWidget(self.line_9)

        self.label_28 = QLabel(self.plot_s)
        self.label_28.setObjectName(u"label_28")

        self.horizontalLayout_14.addWidget(self.label_28)

        self.show_max_cons = QComboBox(self.plot_s)
        self.show_max_cons.addItem("")
        self.show_max_cons.addItem("")
        self.show_max_cons.addItem("")
        self.show_max_cons.addItem("")
        self.show_max_cons.setObjectName(u"show_max_cons")

        self.horizontalLayout_14.addWidget(self.show_max_cons)

        self.line_4 = QFrame(self.plot_s)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setLineWidth(0)
        self.line_4.setFrameShape(QFrame.VLine)

        self.horizontalLayout_14.addWidget(self.line_4)

        self.energyP_s = QCheckBox(self.plot_s)
        self.energyP_s.setObjectName(u"energyP_s")
        self.energyP_s.setEnabled(True)

        self.horizontalLayout_14.addWidget(self.energyP_s)

        self.line_12 = QFrame(self.plot_s)
        self.line_12.setObjectName(u"line_12")
        self.line_12.setFrameShadow(QFrame.Plain)
        self.line_12.setLineWidth(0)
        self.line_12.setFrameShape(QFrame.VLine)

        self.horizontalLayout_14.addWidget(self.line_12)

        self.show_th = QCheckBox(self.plot_s)
        self.show_th.setObjectName(u"show_th")
        self.show_th.setEnabled(True)

        self.horizontalLayout_14.addWidget(self.show_th)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_2)

        self.tabWidget_2.addTab(self.plot_s, "")
        self.table_s_t = QWidget()
        self.table_s_t.setObjectName(u"table_s_t")
        self.horizontalLayout_15 = QHBoxLayout(self.table_s_t)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 2, 0, 0)
        self.table_s = QTableView(self.table_s_t)
        self.table_s.setObjectName(u"table_s")
        self.table_s.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_s.setFrameShape(QFrame.NoFrame)
        self.table_s.setFrameShadow(QFrame.Plain)
        self.table_s.setLineWidth(0)
        self.table_s.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_s.setAlternatingRowColors(True)
        self.table_s.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_s.setSortingEnabled(False)
        self.table_s.horizontalHeader().setStretchLastSection(False)
        self.table_s.verticalHeader().setVisible(False)

        self.horizontalLayout_15.addWidget(self.table_s)

        self.tabWidget_2.addTab(self.table_s_t, "")

        self.horizontalLayout_9.addWidget(self.tabWidget_2)

        self.tabs.addTab(self.simulation_t, "")
        self.resultsH_t = QWidget()
        self.resultsH_t.setObjectName(u"resultsH_t")
        self.horizontalLayout_5 = QHBoxLayout(self.resultsH_t)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 1, 0, 0)
        self.tabWidget_3 = QTabWidget(self.resultsH_t)
        self.tabWidget_3.setObjectName(u"tabWidget_3")
        self.tabWidget_3.setStyleSheet(u"QTabWidget::pane { /* The tab widget frame */\n"
"	left:-1px;\n"
"	top: -1px;\n"
"    bottom: -3px;\n"
"	right: -3px;\n"
"}")
        self.plot_eb = QMplPlot()
        self.plot_eb.setObjectName(u"plot_eb")
        self.horizontalLayout_6 = QHBoxLayout(self.plot_eb)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.show_values_eb = QCheckBox(self.plot_eb)
        self.show_values_eb.setObjectName(u"show_values_eb")
        self.show_values_eb.setEnabled(True)

        self.horizontalLayout_6.addWidget(self.show_values_eb)

        self.line_7 = QFrame(self.plot_eb)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShadow(QFrame.Plain)
        self.line_7.setLineWidth(0)
        self.line_7.setFrameShape(QFrame.VLine)

        self.horizontalLayout_6.addWidget(self.line_7)

        self.show_ecm_eb = QCheckBox(self.plot_eb)
        self.show_ecm_eb.setObjectName(u"show_ecm_eb")
        self.show_ecm_eb.setEnabled(True)

        self.horizontalLayout_6.addWidget(self.show_ecm_eb)

        self.line_5 = QFrame(self.plot_eb)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setLineWidth(0)
        self.line_5.setFrameShape(QFrame.VLine)

        self.horizontalLayout_6.addWidget(self.line_5)

        self.label_26 = QLabel(self.plot_eb)
        self.label_26.setObjectName(u"label_26")

        self.horizontalLayout_6.addWidget(self.label_26)

        self.subdivide_eb = QComboBox(self.plot_eb)
        self.subdivide_eb.addItem("")
        self.subdivide_eb.addItem("")
        self.subdivide_eb.addItem("")
        self.subdivide_eb.setObjectName(u"subdivide_eb")

        self.horizontalLayout_6.addWidget(self.subdivide_eb)

        self.line_14 = QFrame(self.plot_eb)
        self.line_14.setObjectName(u"line_14")
        self.line_14.setFrameShadow(QFrame.Plain)
        self.line_14.setLineWidth(0)
        self.line_14.setFrameShape(QFrame.VLine)

        self.horizontalLayout_6.addWidget(self.line_14)

        self.label_23 = QLabel(self.plot_eb)
        self.label_23.setObjectName(u"label_23")
        sizePolicy4.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy4)

        self.horizontalLayout_6.addWidget(self.label_23)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.tabWidget_3.addTab(self.plot_eb, "")
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.plot_eb), u"\ud83d\udd0b Energy")
        self.eff_t = QWidget()
        self.eff_t.setObjectName(u"eff_t")
        self.verticalLayout_10 = QVBoxLayout(self.eff_t)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.plot_effC = QMplPlot(self.eff_t)
        self.plot_effC.setObjectName(u"plot_effC")
        sizePolicy5.setHeightForWidth(self.plot_effC.sizePolicy().hasHeightForWidth())
        self.plot_effC.setSizePolicy(sizePolicy5)

        self.verticalLayout_10.addWidget(self.plot_effC)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.show_values_effC = QCheckBox(self.eff_t)
        self.show_values_effC.setObjectName(u"show_values_effC")
        sizePolicy10 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.show_values_effC.sizePolicy().hasHeightForWidth())
        self.show_values_effC.setSizePolicy(sizePolicy10)

        self.horizontalLayout_19.addWidget(self.show_values_effC)

        self.line_15 = QFrame(self.eff_t)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setFrameShadow(QFrame.Plain)
        self.line_15.setLineWidth(0)
        self.line_15.setFrameShape(QFrame.VLine)

        self.horizontalLayout_19.addWidget(self.line_15)

        self.label_24 = QLabel(self.eff_t)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_19.addWidget(self.label_24)

        self.horizontalSpacer_9 = QSpacerItem(898, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_9)


        self.verticalLayout_10.addLayout(self.horizontalLayout_19)

        self.plot_effGR = QMplPlot(self.eff_t)
        self.plot_effGR.setObjectName(u"plot_effGR")
        sizePolicy5.setHeightForWidth(self.plot_effGR.sizePolicy().hasHeightForWidth())
        self.plot_effGR.setSizePolicy(sizePolicy5)

        self.verticalLayout_10.addWidget(self.plot_effGR)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.show_values_effGR = QCheckBox(self.eff_t)
        self.show_values_effGR.setObjectName(u"show_values_effGR")
        sizePolicy10.setHeightForWidth(self.show_values_effGR.sizePolicy().hasHeightForWidth())
        self.show_values_effGR.setSizePolicy(sizePolicy10)

        self.horizontalLayout_18.addWidget(self.show_values_effGR)

        self.line_16 = QFrame(self.eff_t)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setFrameShadow(QFrame.Plain)
        self.line_16.setLineWidth(0)
        self.line_16.setFrameShape(QFrame.VLine)

        self.horizontalLayout_18.addWidget(self.line_16)

        self.label_25 = QLabel(self.eff_t)
        self.label_25.setObjectName(u"label_25")

        self.horizontalLayout_18.addWidget(self.label_25)

        self.horizontalSpacer_7 = QSpacerItem(898, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_7)


        self.verticalLayout_10.addLayout(self.horizontalLayout_18)

        self.tabWidget_3.addTab(self.eff_t, "")
        self.bal_com_t = QWidget()
        self.bal_com_t.setObjectName(u"bal_com_t")
        self.verticalLayout_12 = QVBoxLayout(self.bal_com_t)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.plot_balance = QMplPlot(self.bal_com_t)
        self.plot_balance.setObjectName(u"plot_balance")
        sizePolicy5.setHeightForWidth(self.plot_balance.sizePolicy().hasHeightForWidth())
        self.plot_balance.setSizePolicy(sizePolicy5)

        self.verticalLayout_12.addWidget(self.plot_balance)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.show_values_balance = QCheckBox(self.bal_com_t)
        self.show_values_balance.setObjectName(u"show_values_balance")
        sizePolicy10.setHeightForWidth(self.show_values_balance.sizePolicy().hasHeightForWidth())
        self.show_values_balance.setSizePolicy(sizePolicy10)

        self.horizontalLayout_21.addWidget(self.show_values_balance)

        self.line_18 = QFrame(self.bal_com_t)
        self.line_18.setObjectName(u"line_18")
        self.line_18.setFrameShadow(QFrame.Plain)
        self.line_18.setLineWidth(0)
        self.line_18.setFrameShape(QFrame.VLine)

        self.horizontalLayout_21.addWidget(self.line_18)

        self.label_30 = QLabel(self.bal_com_t)
        self.label_30.setObjectName(u"label_30")

        self.horizontalLayout_21.addWidget(self.label_30)

        self.horizontalSpacer_11 = QSpacerItem(898, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_11)


        self.verticalLayout_12.addLayout(self.horizontalLayout_21)

        self.plot_commut = QMplPlot(self.bal_com_t)
        self.plot_commut.setObjectName(u"plot_commut")
        sizePolicy5.setHeightForWidth(self.plot_commut.sizePolicy().hasHeightForWidth())
        self.plot_commut.setSizePolicy(sizePolicy5)

        self.verticalLayout_12.addWidget(self.plot_commut)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.show_values_commut = QCheckBox(self.bal_com_t)
        self.show_values_commut.setObjectName(u"show_values_commut")
        sizePolicy10.setHeightForWidth(self.show_values_commut.sizePolicy().hasHeightForWidth())
        self.show_values_commut.setSizePolicy(sizePolicy10)

        self.horizontalLayout_20.addWidget(self.show_values_commut)

        self.line_17 = QFrame(self.bal_com_t)
        self.line_17.setObjectName(u"line_17")
        self.line_17.setFrameShadow(QFrame.Plain)
        self.line_17.setLineWidth(0)
        self.line_17.setFrameShape(QFrame.VLine)

        self.horizontalLayout_20.addWidget(self.line_17)

        self.label_29 = QLabel(self.bal_com_t)
        self.label_29.setObjectName(u"label_29")

        self.horizontalLayout_20.addWidget(self.label_29)

        self.horizontalSpacer_10 = QSpacerItem(898, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_10)


        self.verticalLayout_12.addLayout(self.horizontalLayout_20)

        self.tabWidget_3.addTab(self.bal_com_t, "")
        self.table_t_2 = QWidget()
        self.table_t_2.setObjectName(u"table_t_2")
        self.horizontalLayout_16 = QHBoxLayout(self.table_t_2)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 2, 0, 0)
        self.table_eb = QTableView(self.table_t_2)
        self.table_eb.setObjectName(u"table_eb")
        sizePolicy5.setHeightForWidth(self.table_eb.sizePolicy().hasHeightForWidth())
        self.table_eb.setSizePolicy(sizePolicy5)
        self.table_eb.setMaximumSize(QSize(16777215, 16777215))
        self.table_eb.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_eb.setFrameShape(QFrame.NoFrame)
        self.table_eb.setFrameShadow(QFrame.Plain)
        self.table_eb.setLineWidth(0)
        self.table_eb.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_eb.setAlternatingRowColors(True)
        self.table_eb.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_eb.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.table_eb.setSortingEnabled(False)
        self.table_eb.setWordWrap(False)
        self.table_eb.horizontalHeader().setCascadingSectionResizes(False)
        self.table_eb.horizontalHeader().setStretchLastSection(False)
        self.table_eb.verticalHeader().setVisible(False)

        self.horizontalLayout_16.addWidget(self.table_eb)

        self.tabWidget_3.addTab(self.table_t_2, "")

        self.horizontalLayout_5.addWidget(self.tabWidget_3)

        self.tabs.addTab(self.resultsH_t, "")
        self.optimise_t = QWidget()
        self.optimise_t.setObjectName(u"optimise_t")
        self.verticalLayout_7 = QVBoxLayout(self.optimise_t)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.op_settings = QHBoxLayout()
        self.op_settings.setObjectName(u"op_settings")
        self.label_14 = QLabel(self.optimise_t)
        self.label_14.setObjectName(u"label_14")
        sizePolicy2.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy2)

        self.op_settings.addWidget(self.label_14)

        self.op_setting = QComboBox(self.optimise_t)
        self.op_setting.setObjectName(u"op_setting")
        self.op_setting.setEnabled(True)
        self.op_setting.setProperty("dataValidEnable", True)

        self.op_settings.addWidget(self.op_setting)

        self.label_12 = QLabel(self.optimise_t)
        self.label_12.setObjectName(u"label_12")
        sizePolicy2.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy2)

        self.op_settings.addWidget(self.label_12)

        self.op_start = QDoubleSpinBox(self.optimise_t)
        self.op_start.setObjectName(u"op_start")
        self.op_start.setEnabled(True)
        self.op_start.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.op_start.setMinimum(-9999.989999999999782)
        self.op_start.setMaximum(9999.989999999999782)

        self.op_settings.addWidget(self.op_start)

        self.label_13 = QLabel(self.optimise_t)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.op_settings.addWidget(self.label_13)

        self.op_end = QDoubleSpinBox(self.optimise_t)
        self.op_end.setObjectName(u"op_end")
        self.op_end.setEnabled(True)
        self.op_end.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.op_end.setMinimum(-9999.989999999999782)
        self.op_end.setMaximum(9999.989999999999782)

        self.op_settings.addWidget(self.op_end)

        self.label_15 = QLabel(self.optimise_t)
        self.label_15.setObjectName(u"label_15")
        sizePolicy2.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy2)

        self.op_settings.addWidget(self.label_15)

        self.op_step = QDoubleSpinBox(self.optimise_t)
        self.op_step.setObjectName(u"op_step")
        self.op_step.setEnabled(True)
        self.op_step.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.op_step.setMaximum(999.990000000000009)

        self.op_settings.addWidget(self.op_step)

        self.op_calculate = QPushButton(self.optimise_t)
        self.op_calculate.setObjectName(u"op_calculate")
        self.op_calculate.setEnabled(False)
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.op_calculate.sizePolicy().hasHeightForWidth())
        self.op_calculate.setSizePolicy(sizePolicy11)
        self.op_calculate.setAutoDefault(False)
        self.op_calculate.setFlat(False)
        self.op_calculate.setProperty("dataValidEnable", True)

        self.op_settings.addWidget(self.op_calculate)

        self.op_recalc_warn = QLabel(self.optimise_t)
        self.op_recalc_warn.setObjectName(u"op_recalc_warn")
        self.op_recalc_warn.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.op_recalc_warn.sizePolicy().hasHeightForWidth())
        self.op_recalc_warn.setSizePolicy(sizePolicy3)
        self.op_recalc_warn.setMinimumSize(QSize(134, 0))
        self.op_recalc_warn.setMaximumSize(QSize(134, 16777215))
        self.op_recalc_warn.setAlignment(Qt.AlignCenter)

        self.op_settings.addWidget(self.op_recalc_warn)


        self.verticalLayout_7.addLayout(self.op_settings)

        self.tabWidget_4 = QTabWidget(self.optimise_t)
        self.tabWidget_4.setObjectName(u"tabWidget_4")
        self.plot_op = QMplTwinxPlot()
        self.plot_op.setObjectName(u"plot_op")
        self.verticalLayout_8 = QVBoxLayout(self.plot_op)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_16 = QLabel(self.plot_op)
        self.label_16.setObjectName(u"label_16")
        sizePolicy2.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy2)

        self.horizontalLayout_11.addWidget(self.label_16)

        self.op_ax_left = QComboBox(self.plot_op)
        self.op_ax_left.setObjectName(u"op_ax_left")
        sizePolicy12 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy12.setHorizontalStretch(0)
        sizePolicy12.setVerticalStretch(0)
        sizePolicy12.setHeightForWidth(self.op_ax_left.sizePolicy().hasHeightForWidth())
        self.op_ax_left.setSizePolicy(sizePolicy12)

        self.horizontalLayout_11.addWidget(self.op_ax_left)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)

        self.label_17 = QLabel(self.plot_op)
        self.label_17.setObjectName(u"label_17")
        sizePolicy2.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy2)

        self.horizontalLayout_11.addWidget(self.label_17)

        self.op_ax_right = QComboBox(self.plot_op)
        self.op_ax_right.setObjectName(u"op_ax_right")
        sizePolicy12.setHeightForWidth(self.op_ax_right.sizePolicy().hasHeightForWidth())
        self.op_ax_right.setSizePolicy(sizePolicy12)

        self.horizontalLayout_11.addWidget(self.op_ax_right)


        self.verticalLayout_8.addLayout(self.horizontalLayout_11)

        self.tabWidget_4.addTab(self.plot_op, "")
        self.table_op_t = QWidget()
        self.table_op_t.setObjectName(u"table_op_t")
        self.verticalLayout_9 = QVBoxLayout(self.table_op_t)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 2, 0, 0)
        self.table_op = QTableView(self.table_op_t)
        self.table_op.setObjectName(u"table_op")
        self.table_op.setContextMenuPolicy(Qt.PreventContextMenu)
        self.table_op.setFrameShape(QFrame.NoFrame)
        self.table_op.setFrameShadow(QFrame.Plain)
        self.table_op.setLineWidth(0)
        self.table_op.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.table_op.setAlternatingRowColors(True)
        self.table_op.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.table_op.setSortingEnabled(False)
        self.table_op.setWordWrap(True)
        self.table_op.horizontalHeader().setCascadingSectionResizes(False)
        self.table_op.horizontalHeader().setStretchLastSection(False)
        self.table_op.verticalHeader().setVisible(False)
        self.table_op.verticalHeader().setMinimumSectionSize(10)
        self.table_op.verticalHeader().setHighlightSections(False)

        self.verticalLayout_9.addWidget(self.table_op)

        self.tabWidget_4.addTab(self.table_op_t, "")

        self.verticalLayout_7.addWidget(self.tabWidget_4)

        self.tabs.addTab(self.optimise_t, "")
        self.help_t = QWidget()
        self.help_t.setObjectName(u"help_t")
        self.horizontalLayout_3 = QHBoxLayout(self.help_t)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.help = QTextEdit(self.help_t)
        self.help.setObjectName(u"help")
        self.help.setFrameShape(QFrame.NoFrame)
        self.help.setFrameShadow(QFrame.Plain)
        self.help.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.help)

        self.tabs.addTab(self.help_t, "")

        self.data.addWidget(self.tabs)


        self.gridLayout.addLayout(self.data, 0, 1, 1, 1)

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

        self.calc_time = QLabel(self.centralwidget)
        self.calc_time.setObjectName(u"calc_time")

        self.horizontalLayout_4.addWidget(self.calc_time)

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


        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.load_file = QPushButton(self.centralwidget)
        self.load_file.setObjectName(u"load_file")

        self.horizontalLayout.addWidget(self.load_file)

        self.unload_file = QPushButton(self.centralwidget)
        self.unload_file.setObjectName(u"unload_file")

        self.horizontalLayout.addWidget(self.unload_file)

        self.file_path = QLineEdit(self.centralwidget)
        self.file_path.setObjectName(u"file_path")
        self.file_path.setEnabled(True)
        self.file_path.setReadOnly(True)

        self.horizontalLayout.addWidget(self.file_path)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1508, 22))
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
        QWidget.setTabOrder(self.results, self.tabs)
        QWidget.setTabOrder(self.tabs, self.table_eb_t)
        QWidget.setTabOrder(self.table_eb_t, self.table_t)
        QWidget.setTabOrder(self.table_t, self.show_values_t)
        QWidget.setTabOrder(self.show_values_t, self.file_path)
        QWidget.setTabOrder(self.file_path, self.help)

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
        self.algorithm.currentIndexChanged.connect(self.algorithm_options.setCurrentIndex)
        self.use_data_bl.toggled.connect(self.recalc_warn.show)
        self.load_file.clicked.connect(self.recalc_warn.show)
        self.op_setting.currentIndexChanged.connect(self.op_recalc_warn.show)
        self.op_calculate.pressed.connect(self.op_recalc_warn.hide)
        self.predict_final_energy.currentIndexChanged.connect(self.recalc_warn.show)
        self.ttc_end_at.valueChanged.connect(self.recalc_warn.show)
        self.ttc_time_factor.valueChanged.connect(self.recalc_warn.show)
        self.ttc_on_min.valueChanged.connect(self.recalc_warn.show)
        self.sell_price.valueChanged.connect(self.recalc_warn.show)
        self.time_limit.valueChanged.connect(self.recalc_warn.show)
        self.mot_mode.currentIndexChanged.connect(self.recalc_warn.show)

        self.algorithm_options.setCurrentIndex(0)
        self.simulate.setDefault(False)
        self.results.setDefault(False)
        self.tabs.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.op_calculate.setDefault(False)
        self.tabWidget_4.setCurrentIndex(0)


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
        self.algorithm.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.algorithm.setItemText(1, QCoreApplication.translate("MainWindow", u"Hysteresis", None))
        self.algorithm.setItemText(2, QCoreApplication.translate("MainWindow", u"Min On Time", None))
        self.algorithm.setItemText(3, QCoreApplication.translate("MainWindow", u"Time To Consume", None))

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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Time Limit", None))
        self.time_limit.setSuffix(QCoreApplication.translate("MainWindow", u" s", None))
        self.time_limit.setPrefix("")
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.mot_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"2n on if 1st on", None))
        self.mot_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"by order", None))
        self.mot_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"fastest", None))

        self.wh_eq.setText(QCoreApplication.translate("MainWindow", u"= Wh", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Predict Final Energy", None))
        self.predict_final_energy.setItemText(0, QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.predict_final_energy.setItemText(1, QCoreApplication.translate("MainWindow", u"Average Power", None))
        self.predict_final_energy.setItemText(2, QCoreApplication.translate("MainWindow", u"Project Current Power", None))

#if QT_CONFIG(tooltip)
        self.label_18.setToolTip(QCoreApplication.translate("MainWindow", u"External / Not controled", None))
#endif // QT_CONFIG(tooltip)
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"End at", None))
        self.ttc_end_at.setSuffix(QCoreApplication.translate("MainWindow", u" Wh", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Time Factor", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"On min", None))
        self.ttc_on_min.setSuffix(QCoreApplication.translate("MainWindow", u" Wh", None))
        self.ttc_time_factor.setPrefix("")
        self.ttc_time_factor.setSuffix("")
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
        self.algorithm_l_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Generation Factor</p></body></html>", None))
        self.generation_factor.setPrefix("")
        self.generation_factor.setSuffix("")
        self.simulate.setText(QCoreApplication.translate("MainWindow", u"Simulate", None))
        self.results.setText(QCoreApplication.translate("MainWindow", u"Data In Results", None))
        self.recalc_warn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; color:#f4b300;\">\u26a0</span><span style=\" color:#f4b300;\"> Recalculate \u26a0</span></p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Line Style", None))
        self.data_line_style.setInputMask("")
        self.data_line_style.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plot_dr), QCoreApplication.translate("MainWindow", u"\ud83d\udcc8 Graph", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.table_dr_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Table [W, Wh]", None))
        self.tabs.setTabText(self.tabs.indexOf(self.daterange_t), QCoreApplication.translate("MainWindow", u"\ud83d\udd57 Data Range (In)", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Sell Price", None))
        self.sell_price.setPrefix("")
        self.sell_price.setSuffix(QCoreApplication.translate("MainWindow", u" \u20ac/kWh", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">(1:00 hour zone = 1:00 to 1:59)</span></p></body></html>", None))
        self.tabs.setTabText(self.tabs.indexOf(self.price_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcb0 Energy Price (In)", None))
        self.show_values_t.setText(QCoreApplication.translate("MainWindow", u"Show values (rounded)", None))
        self.show_ecm_t.setText(QCoreApplication.translate("MainWindow", u"System Max Consuption", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Subdivide", None))
        self.subdivide_t.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.subdivide_t.setItemText(1, QCoreApplication.translate("MainWindow", u"Level 1", None))
        self.subdivide_t.setItemText(2, QCoreApplication.translate("MainWindow", u"Level 2", None))

        self.tabs.setTabText(self.tabs.indexOf(self.global_results), QCoreApplication.translate("MainWindow", u"\ud83d\udcca\ud83d\udcc5 Results", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Line Style", None))
        self.sim_line_style.setInputMask("")
        self.sim_line_style.setText("")
        self.show_loads_area.setText(QCoreApplication.translate("MainWindow", u"Power Consumed by Load", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Max. Consuption", None))
        self.show_max_cons.setItemText(0, QCoreApplication.translate("MainWindow", u"Hide", None))
        self.show_max_cons.setItemText(1, QCoreApplication.translate("MainWindow", u"Line", None))
        self.show_max_cons.setItemText(2, QCoreApplication.translate("MainWindow", u"Area", None))
        self.show_max_cons.setItemText(3, QCoreApplication.translate("MainWindow", u"Line & Area", None))

        self.energyP_s.setText(QCoreApplication.translate("MainWindow", u"Energy Produced", None))
        self.show_th.setText(QCoreApplication.translate("MainWindow", u"Thresholds", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.plot_s), QCoreApplication.translate("MainWindow", u"\ud83d\udcc8 Grapth", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.table_s_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Table [W, Wh]", None))
        self.tabs.setTabText(self.tabs.indexOf(self.simulation_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcc9 Simulation", None))
        self.show_values_eb.setText(QCoreApplication.translate("MainWindow", u"Values (rounded)", None))
        self.show_ecm_eb.setText(QCoreApplication.translate("MainWindow", u"System Max Consuption", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Subdivide", None))
        self.subdivide_eb.setItemText(0, QCoreApplication.translate("MainWindow", u"None", None))
        self.subdivide_eb.setItemText(1, QCoreApplication.translate("MainWindow", u"Level 1", None))
        self.subdivide_eb.setItemText(2, QCoreApplication.translate("MainWindow", u"Level 2", None))

        self.label_23.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">(1:00 hour zone = 1:00 to 1:59)</span></p></body></html>", None))
        self.show_values_effC.setText(QCoreApplication.translate("MainWindow", u"Values", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">(1:00 hour zone = 1:00 to 1:59)</span></p></body></html>", None))
        self.show_values_effGR.setText(QCoreApplication.translate("MainWindow", u"Values", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">(1:00 hour zone = 1:00 to 1:59)</span></p></body></html>", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.eff_t), QCoreApplication.translate("MainWindow", u"% Efficiencnies", None))
        self.show_values_balance.setText(QCoreApplication.translate("MainWindow", u"Values", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">(1:00 hour zone = 1:00 to 1:59)</span></p></body></html>", None))
        self.show_values_commut.setText(QCoreApplication.translate("MainWindow", u"Values", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-style:italic;\">(1:00 hour zone = 1:00 to 1:59)</span></p></body></html>", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.bal_com_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcc3 Balance && Commut", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.table_t_2), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Table [Wh, %, c\u00e8nt.]", None))
        self.tabs.setTabText(self.tabs.indexOf(self.resultsH_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcca Hourly Results", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Setting:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"End", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.op_calculate.setText(QCoreApplication.translate("MainWindow", u"Calculate", None))
        self.op_recalc_warn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700; color:#f4b300;\">\u26a0</span><span style=\" color:#f4b300;\"> Recalculate \u26a0</span></p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Left Axis", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Right Axis", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.plot_op), QCoreApplication.translate("MainWindow", u"\ud83d\udcc8 Grapth", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.table_op_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcc5 Table [W, Wh]", None))
        self.tabs.setTabText(self.tabs.indexOf(self.optimise_t), QCoreApplication.translate("MainWindow", u"\ud83d\udcc8 Optimize", None))
        self.help.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:xx-large; font-weight:700;\"><br /></p></body></html>", None))
        self.tabs.setTabText(self.tabs.indexOf(self.help_t), QCoreApplication.translate("MainWindow", u"\u2139 Help", None))
        self.sampling_rate.setText(QCoreApplication.translate("MainWindow", u"Sampling Rate", None))
        self.date_range.setText(QCoreApplication.translate("MainWindow", u"Date Range", None))
        self.calc_time.setText(QCoreApplication.translate("MainWindow", u"Calculation Time", None))
        self.plotting_time.setText(QCoreApplication.translate("MainWindow", u"Plotting Time", None))
        self.n_samples.setText(QCoreApplication.translate("MainWindow", u"N Samples", None))
        self.load_file.setText(QCoreApplication.translate("MainWindow", u"Load File", None))
        self.unload_file.setText(QCoreApplication.translate("MainWindow", u"Unload File", None))
    # retranslateUi

