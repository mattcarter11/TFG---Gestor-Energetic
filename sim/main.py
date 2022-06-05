import sys, json, traceback
from time import time
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView, QItemDelegate, QCheckBox, QTableView, QDateTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit, QWidget
from PySide6.QtCore import QFile, QIODevice, QDateTime, QCoreApplication, Qt
from lib.sim.Simulator import Simulator
from lib.sim.Load import Load
from lib.sim.Results import Results
from lib.sim.Optimize import Optimize
import lib.sim.AlgorithmsConfig as ac
import lib.sim.DataFrames as df
import lib.myQT.QMplWidgets as mw
import lib.myQT.QPandasWidgets as pw
import pandas as pd
import matplotlib as mp

# To hide constants
if True:
    UI_FILE = "mainwindow.ui"
    DT_FORMAT = 'yyyy-MM-dd HH:mm'
    COLOR_GR = '#a5a5a5'
    COLOR_SD = '#0cb7e8'
    COLOR_ED = '#8e09d5'

    # ordered key: (color, translate)
    OCT = {
        'timestamp' :{"color":None,      "translate": ('Timestamp', 'Timestamp')},
        'powerG'    :{"color":'#33ab1d', "translate": ('Power Generated', 'Generated')}, 
        'powerC'    :{"color":'#f8a62a', "translate": ('Power Consumed', 'Consumed')}, 
        'powerLB'   :{"color":'#e7d6a9', "translate": ('Power Base Load', 'Base Load')},
        'powerL1'   :{"color":'#fdc26c', "translate": ('Power Load 1', 'Load 1')},
        'powerL2'   :{"color":'#ffd463', "translate": ('Power Load 2', 'Load 2')},
        'on_offL1'  :{"color":None,      "translate": ('On/Off Load 1', 'On/Off Load 1')}, 
        'on_offL2'  :{"color":None,      "translate": ('On/Off Load 2', 'On/Off Load 2')}, 
        'energySY'  :{"color":'#195aa7', "translate": ('Energy System', 'System')}, 
        'energyP'   :{"color":'#2176db', "translate": ('Energy Produced', 'Produced')}, 
        'energyG'   :{"color":'#ef8271', "translate": ('Energy Grid', 'Grid')}, 
        'energyA'   :{"color":'#60b0ff', "translate": ('Energy Available', 'Available')}, 
        'energyC'   :{"color":'#f8a62a', "translate": ('Energy Consumed', 'Consumed')}, 
        'energyLB'  :{"color":'#e7d6a9', "translate": ('Energy Base Load', 'Base Load')}, 
        'energyL1'  :{"color":'#fdc26c', "translate": ('Energy Load 1', 'Load 1')}, 
        'energyL2'  :{"color":'#ffd463', "translate": ('Energy Load 2', 'Load 2')},
        'energyCM'  :{"color":None,      "translate": ('Energy Consumed Max', 'Consumed Max')}, 
        'energyS'   :{"color":'#6dbf31', "translate": ('Energy Surplus', 'Surplus')},
        'energyL'   :{"color":'#e15f4b', "translate": ('Energy Lost',' Lost')}, 
    }

    SettingsQDateTimeEdits = ('start_date', 'end_date')
    SettingsQComboBoxes = ('algorithm', 'predict_final_energy', 'op_setting', 'op_ax_right', 'op_ax_left')
    SettingsQSpinBoxes = ('th_top1', 'th_top2', 'th_bottom1', 'th_bottom2', 'time_limit', 'base_load', 'load1', 'load2', 'op_start', 'op_end', 'op_step', 'ttc_end_at', 'ttc_on_min')
    SettingsQDoubleSpinBox = ['ttc_time_factor']
    SettingsQCheckBoxes = ('use_data_bl', 'show_loads_area', 'show_th', 'energyP_s', 'show_values_eb', 'subdivide_eb', 'show_values_t', 'subdivide_t')
    SettingsQLineEdits = ('data_line_style', 'sim_line_style')

    OpAxList = ['None', 'Efficiency', 'Daily Commutations', 'Daily Commutations Load 1', 'Daily Commutations Load 2', 'Daily Hours On Load 1', 'Daily Hours On Load 2', 'Energy Grid']

    OpAlgorithm = {
        'Hysteresis':{
            'Threshold Top L1':'th_top1',
            'Threshold Bottom L1':'th_bottom1',
            'Threshold Top L2':'th_top2',
            'Threshold Bottom L2':'th_bottom2',
        },
        'Min Time On': {
            'Time Limit':'time_limit'
        },
        'Time To Consume': {
            'End at [Wh]':'ttc_end_at', 
            'Time factor':'ttc_time_factor', 
            'On Min [Wh]':'ttc_on_min', 
        },
        'Shared':{
            'Base Load [Wh]':'base_load',
            'Load 1 [Wh]':'load1',
            'Load 2 [Wh]':'load2',
        }
    }

class AlignDelegate(QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        QItemDelegate.paint(self, painter, option, index)

class QPandasModelPlus(pw.QPandasModel):

    def __init__(self, dataframe: pd.DataFrame, parent=None, i=1):
        super().__init__(dataframe, parent)
        self.i = i

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                title = str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                title = str(self._dataframe.index[section])
            if title in OCT.keys():
                return OCT[title]['translate'][self.i]
        
        return super().headerData(section, orientation, role)

def df_plot_col(df, xcol, ycol, ax):
    return ax.plot(df[xcol], df[ycol], color=OCT[ycol]['color'], label=OCT[ycol]['translate'][0])

class App(QMainWindow):
    #region -> Init
    def __init__(self):
        start = time()
        super().__init__()
        self.load_ui()
        self.sim_prev_ls = self.data_prev_ls = ''
        self.th_lines = self.sim_areas = self.sim_lines = self.data_lines = self.date_range_lines = []
        self.sim = self.results = self.optimize = None
        # Tables view style
        for table in self.ui.findChildren(QTableView):
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setItemDelegate(AlignDelegate())
        for name in ['table_eb_t', 'table_t']:
            table = self.ui.findChild(QTableView, name)
            table.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # Warning Optimize not resize on hiden
        pol = self.ui.op_recalc_warn.sizePolicy()
        pol.setRetainSizeWhenHidden(True)
        self.ui.op_recalc_warn.setSizePolicy(pol) 
        # List Optimze Axes values
        for item in OpAxList:
            self.ui.op_ax_left.addItem(item)
            self.ui.op_ax_right.addItem(item)
        self.load_prev_settings()
        self.sig_init()
        self.ui.calc_time.setText(f'Program loaded in {time()-start:.3f} s')
        
    def sig_init(self):
        # Date Time
        self.ui.start_date.dateTimeChanged.connect(self.datetime_changed)
        self.ui.end_date.dateTimeChanged.connect(self.datetime_changed)
        # Algorithm
        self.ui.algorithm.currentIndexChanged.connect(self.algorithm_changed)
        self.load_op_settings(self.ui.algorithm.currentIndex())
        self.ui.time_limit.valueChanged.connect(self.time_limit_changed)
        self.ui.load1.valueChanged.connect(self.time_limit_changed)
        self.time_limit_changed()
        # Loads
        self.ui.load1.valueChanged.connect(self.th1_disable)
        self.ui.load2.valueChanged.connect(self.th2_disable)
        self.th1_disable()
        self.th2_disable()
        # Line Style
        self.ui.data_line_style.textChanged.connect(self.data_line_style)
        self.ui.sim_line_style.textChanged.connect(self.sim_line_style)
        # Simulation plot
        self.ui.show_loads_area.stateChanged.connect( self.toggle_loads_area)
        self.ui.energyP_s.stateChanged.connect( self.toggle_energyP)
        self.ui.show_th.stateChanged.connect( self.toggle_th)
        # Energy balance plot
        self.ui.show_values_eb.stateChanged.connect( self.plot_eb)
        self.ui.subdivide_eb.stateChanged.connect( self.plot_eb)
        # Summary balance plot
        self.ui.show_values_t.stateChanged.connect( self.plot_t)
        self.ui.subdivide_t.stateChanged.connect( self.plot_t)
        # Buttons
        self.ui.load_file.clicked.connect(self.load_file)
        self.ui.unload_file.clicked.connect(self.unload_file)
        self.ui.simulate.clicked.connect(self.simulate_press)
        self.ui.results.clicked.connect(self.results_press)
        # Optimize
        self.ui.op_calculate.clicked.connect(self.optimize_press)
        self.ui.op_ax_left.currentIndexChanged.connect(self.plot_op)
        self.ui.op_ax_right.currentIndexChanged.connect(self.plot_op)
        # Trigger settings save on window close
        app.aboutToQuit.connect(self.close_save)
        
    def load_ui(self):
        # Check if file exists
        ui_file = QFile(UI_FILE)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {UI_FILE}: {ui_file.errorString()}")
            sys.exit(-1)
        # Load .ui & external widgets
        loader = QUiLoader()
        loader.registerCustomWidget(mw.MplWidget)
        loader.registerCustomWidget(mw.MplTwinxWidget)
        self.ui = loader.load(ui_file)
        self.ui.show()
        ui_file.close()
    #endregion

    #region -> Settings Load/Save
    def load_prev_settings(self):
        with open('prev_settings.json', 'r') as f:
            settings = json.load(f)
        keys = settings.keys()

        for name in SettingsQDateTimeEdits:
            if name in keys:
                self.ui.findChild(QDateTimeEdit, name).setDateTime(QDateTime.fromString(settings[name], DT_FORMAT))

        for name in SettingsQComboBoxes:
            if name in keys:
                self.ui.findChild(QComboBox, name).setCurrentText(settings[name])

        for name in SettingsQSpinBoxes:
            if name in keys:
                self.ui.findChild(QSpinBox, name).setValue(settings[name])
                
        for name in SettingsQDoubleSpinBox:
            if name in keys:
                self.ui.findChild(QDoubleSpinBox, name).setValue(settings[name])

        for name in SettingsQLineEdits:
            if name in keys:
                self.ui.findChild(QLineEdit, name).setText(settings[name])

        if 'file_path' in keys and settings['file_path'] != '':
            self.load_csv(settings['file_path'])
       
    def close_save(self):
        settings = {}
        settings["file_path"] = self.ui.file_path.text()

        for name in SettingsQDateTimeEdits:
            settings[name]= self.ui.findChild(QDateTimeEdit, name).dateTime().toString(DT_FORMAT)

        for name in SettingsQComboBoxes:
            settings[name] = self.ui.findChild(QComboBox, name).currentText()

        for name in SettingsQSpinBoxes:
            settings[name] = self.ui.findChild(QSpinBox, name).value()

        for name in SettingsQDoubleSpinBox:
            settings[name] = self.ui.findChild(QDoubleSpinBox, name).value()
                
        for name in SettingsQCheckBoxes:
            settings[name] = self.ui.findChild(QCheckBox, name).isChecked()

        for name in SettingsQLineEdits:
            settings[name] = self.ui.findChild(QLineEdit, name).text()

        with open('prev_settings.json', 'w') as f:
            json.dump(settings, f, indent=4)
    #endregion

    #region -> Load data
    def load_file(self):
        path = QFileDialog.getOpenFileName(self, "Select Generated Power", './db', '*.csv')[0]
        if path != '':
            self.load_csv(path)

    def load_csv(self, path):
        start = time()
        try:
            dataframe = pd.read_csv(path, parse_dates=['timestamp'])
            self.dfI = df.DataFrameIn(dataframe)
            try:    self.dfI = df.DataFrameOut(dataframe)
            except: self.ui.results.setEnabled(False)
            else:   self.ui.results.setEnabled(True)

        except Exception as ex:
            self.unload_file()
            print(f"[{type(ex).__name__}] {ex} \n\n {traceback.format_exc()}")
            QMessageBox.warning(self, "Error", f"{ex}", QMessageBox.Ok)

        else:
            self.sim = Simulator(self.dfI)
            # Enable options
            self.ui.simulate.setEnabled(True)
            self.ui.op_calculate.setEnabled(True)
            # Update UI
            self.ui.file_path.setText(path)
            self.limit_datarange_selectors()
            self.ui.sampling_rate.setText(f'Sampling rate: {self.sim.Ts} s')
            # Update table
            self.ui.table_in.setModel(QPandasModelPlus(self.dfI.df, i=0))
            start2 = time()
            self.plot_in_data()
            self.ui.plotting_time.setText(f'Data loaded in {time()-start:.3f} s. Plotted in {time()-start2:.3f} s')
    
    def limit_datarange_selectors(self):
        min_date = self.dfI.df['timestamp'].min()
        max_date = self.dfI.df['timestamp'].max()
        format = '%Y-%m-%d %H:%M:%S'
        self.ui.date_range.setText(f'Date Range: {min_date.strftime(format)} - {max_date.strftime(format)} ({self.dfI.nsamples} Samples)')
        self.ui.start_date.setMinimumDateTime(min_date)
        self.ui.end_date.setMinimumDateTime(min_date)
        self.ui.start_date.setMaximumDateTime(max_date)
        self.ui.end_date.setMaximumDateTime(max_date)
    
    def unload_file(self):
        self.ui.file_path.setText('')
        self.ui.simulate.setEnabled(False)
        self.ui.results.setEnabled(False)
        self.ui.op_calculate.setEnabled(False)
        self.data_lines = self.date_range_lines = []
        self.ui.plot_dr.clear()
        self.ui.plot_dr.draw_idle()
    #endregion

    #region -> Simulation Settings
    def time_limit_changed(self):
        self.tl_eq = self.ui.time_limit.value() * self.ui.load1.value() / 3600
        self.ui.wh_eq.setText(f'Top threshold {self.tl_eq:.2f} Wh')

    def algorithm_changed(self, i):
        self.ui.load2.setEnabled(i == 0)
        self.load_op_settings(i)

    def load_op_settings(self, i):
        self.ui.op_setting.clear()
        key = list(OpAlgorithm)[i]
        self.ui.op_setting.addItems(list(OpAlgorithm[key]))
        self.ui.op_setting.addItems(list(OpAlgorithm['Shared']))

    def th1_disable(self):
        status_l1 = (self.ui.load1.value() > 0)
        self.ui.th_top1.setEnabled(status_l1)
        self.ui.th_bottom1.setEnabled(status_l1)

    def th2_disable(self):
        status_l2 = (self.ui.load2.value() > 0)
        self.ui.th_top2.setEnabled(status_l2)
        self.ui.th_bottom2.setEnabled(status_l2)
    #endregion

    #region -> Simulation/Results/Optimize
    def results_press(self):
        start = time()
        startDT = self.ui.start_date.dateTime().toString()
        endDT = self.ui.end_date.dateTime().toString()
        self.results = Results(self.dfI.select_daterange(startDT, endDT))
        self.ui.calc_time.setText(f'Results calculated in {time()-start:.3f} s')
        self.show_results(self.results.dfI.df)

    def simulate_press(self):
        start = time()
        err = self.simulate()
        start2 = time()
        if not err:
            self.results = Results(df.DataFrameOut(self.sim.df_out))
        self.ui.calc_time.setText(f'Simulated in {time()-start:.3f} s. Results calculated in {time()-start2:.3f} s')
        self.print_sim_duration()
        self.show_results(self.sim.df_out)

    def optimize_press(self):
        start = time()
        self.optimize = Optimize(self.ui.op_setting.currentText(), OpAxList[1:])
        values = range(self.ui.op_start.value(), self.ui.op_end.value()+self.ui.op_step.value(), self.ui.op_step.value()) 
        for value in values:
            err = self.simulate(value)
            if err: 
                break
            self.optimize.add_results(value, Results(df.DataFrameOut(self.sim.df_out)))
        self.ui.calc_time.setText(f'Optimize calculations in {time()-start:.3f} s')
        self.print_sim_duration()
        self.show_optimitzation_results()

    def simulate(self, value=None):
        # when optimizing set the corresponding value
        alI = self.ui.algorithm.currentIndex()
        opI = self.ui.op_setting.currentIndex()
        alKey = list(OpAlgorithm)[alI]
        opKey = list( OpAlgorithm[alKey] )[opI]
        element = OpAlgorithm[alKey][opKey]
            
        def get_algorithm_config():
            match self.ui.algorithm.currentIndex():
                case 0: 
                    th_top1     = value if value is not None and element == 'th_top1' else self.ui.th_top1.value()
                    th_bottom1  = value if value is not None and element == 'th_bottom1' else self.ui.th_bottom1.value()
                    th_top2     = value if value is not None and element == 'th_top2' else self.ui.th_top2.value()
                    th_bottom2  = value if value is not None and element == 'th_bottom2' else self.ui.th_bottom2.value()
                    th_bottom2  = value if value is not None and element == 'th_bottom2' else self.ui.th_bottom2.value()
                    return ac.HysteresisConfig(th_top1, th_bottom1, th_top2, th_bottom2)
                case 1: 
                    time_limit  = value if value is not None and element == 'time_limit' else self.ui.time_limit.value()
                    return ac.MinOnTimeConfig(time_limit)
                case 2:
                    end_at       = value if value is not None and element == 'ttc_end_at' else self.ui.ttc_end_at.value()
                    on_min       = value if value is not None and element == 'ttc_on_min' else self.ui.ttc_on_min.value()
                    time_factor  = value if value is not None and element == 'ttc_time_factor' else self.ui.ttc_time_factor.value()
                    match self.ui.predict_final_energy.currentIndex():
                        case 0: predict = ac.PredictFinalEnergy.disabled
                        case 1: predict = ac.PredictFinalEnergy.avarage_power
                        case 2: predict = ac.PredictFinalEnergy.project_current_power
                    return ac.TimeToConsume(predict, end_at, on_min, time_factor)

        load1 = value if value is not None and element == 'load1' else self.ui.load1.value()
        load2 = value if value is not None and element == 'load2' else self.ui.load2.value()
        try:
            self.sim.simulate(
                self.ui.start_date.dateTime().toString(),
                self.ui.end_date.dateTime().toString(),
                get_algorithm_config(),
                Load(load1),
                Load(load2),
                None if isinstance(self.dfI, df.DataFrameOut) and self.ui.use_data_bl.isChecked() else self.ui.base_load.value()
            )
        except Exception as ex:
            print(f"[{type(ex).__name__}] {ex} \n\n {traceback.format_exc()}")
            QMessageBox.warning(self, "Error", f"Date & Time interval must be at least 5 min", QMessageBox.Ok)
            return 1
        return 0
    
    def print_sim_duration(self):
        self.ui.n_samples.setText(f'Simulating {self.sim.simulated_nsec/3600:.3f} h ({self.sim.simulated_nsec} Samples)')
    #endregion

    #region -> Plots
    def plot_in_data(self):
        plot = self.ui.plot_dr
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()
        df = self.dfI.df

        # Plot Data
        self.data_lines = df_plot_col(df, 'timestamp', 'powerG', ax1)
        if 'powerLB' in self.dfI.df.columns:
            self.data_lines += df_plot_col(df, 'timestamp', 'powerLB', ax2)

        # Plot start & end
        self.date_range_lines = [ 
            ax1.axvline(self.ui.start_date.dateTime().toPython(), color=COLOR_SD, linestyle=':', label='Start Date'),
            ax1.axvline(self.ui.end_date.dateTime().toPython(), color=COLOR_ED, linestyle=':', label='End Date') 
        ]

        # Data move settup
        self.date_line = None
        self.data_lines_PS = mw.PickStack(self.date_range_lines, self.data_lines_on_pick)

        # Visuals
        ax1.grid(True, linestyle=':')
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        ax1.set_xlabel('Date & Time')
        ax1.set_ylabel('Power [W]')
        ax2.set_ylabel('Power [W]')
        ax1.set_title('Data Range/In')
        plot.fig.autofmt_xdate()
        plot.align_yaxis()
        plot.toggable_legend_lines()
        plot.draw_idle()
        self.data_line_style(self.ui.data_line_style.text())

    def plot_general(self, df):
        if df is None:
            return

        start = time()
        plot = self.ui.plot_s
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()

        # Plot Power Lines
        self.sim_lines = df_plot_col(df, 'timestamp', 'powerC', ax1)
        self.sim_lines += df_plot_col(df, 'timestamp', 'powerG', ax1)
        
        # Power Load Areas
        cols = ['powerLB', 'powerL1', 'powerL2']
        labels = [OCT[col]['translate'][0] for col in cols]
        colors = [OCT[col]['color'] for col in cols]
        self.sim_areas = df.plot.area('timestamp', cols, ax=ax1, linewidth=0, color=colors, label=labels).collections
        self.toggle_loads_area(self.ui.show_loads_area.isChecked())

        # Add energy thresholds
        self.th_lines = []
        match self.ui.algorithm.currentIndex():
            case 0:
                if self.ui.load1.value() > 0:
                    self.th_lines.append( ax2.axhline(self.ui.th_top1.value(), color=COLOR_GR) )
                    self.th_lines.append( ax2.axhline(self.ui.th_bottom1.value(), color=COLOR_GR) )
                if self.ui.load2.value() > 0:
                    self.th_lines.append( ax2.axhline(self.ui.th_top2.value(), color=COLOR_GR) )
                    self.th_lines.append( ax2.axhline(self.ui.th_bottom2.value(), color=COLOR_GR) )
            case 1:
                ax2.axhline(self.tl_eq, color=COLOR_GR)
        self.toggle_th(self.ui.show_th.isChecked())

        # Energy
        if self.ui.energyP_s.isChecked():
            self.sim_lines += df_plot_col(df, 'timestamp', 'energyP', ax2)
        self.sim_lines += df_plot_col(df, 'timestamp', 'energyA', ax2)
        self.sim_lines += df_plot_col(df, 'timestamp', 'energyG', ax2)

        # Visuals
        ax1.grid(True, linestyle=':')
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        ax1.set_xlabel('Date & Time')
        ax1.set_ylabel('Power [W]')
        ax2.set_ylabel('Energy [Wh]')
        ax1.set_title('Simulation')
        plot.fig.autofmt_xdate()
        plot.align_yaxis()
        plot.toggable_legend_lines()
        plot.draw_idle()
        self.sim_line_style(self.ui.sim_line_style.text())
        self.ui.plotting_time.setText(f'Plotted in {time()-start:.3f} s')

    def plot_eb(self):
        if self.results is None:
            return

        showV = self.ui.show_values_eb.isChecked()
        showD = self.ui.subdivide_eb.isChecked()
        self.plot_bars(self.results.df_hour, self.ui.plot_eb, showV, showD)

    def plot_t(self):
        if self.results is None:
            return
            
        data = self.results.df_total
        data['timestamp'] = self.results.df_hour.iloc[-1]['timestamp']
        showV = self.ui.show_values_t.isChecked()
        showD = self.ui.subdivide_t.isChecked()
        self.plot_bars(data, self.ui.plot_eb_t, showV, showD, None, 'horizontal', False)

    def plot_bars(self, data, plot, showV, showD, gaxis='both', lrot='vertical', xtimestamp = True):
        if data is None:
            return

        start = time()
        ax = plot.ax
        plot.clear()

        # Sum of each stacked type
        bars = ['energyC', 'energySY', 'energyA']
        labels = [OCT[col]['translate'][1] for col in bars]
        colors = [OCT[col]['color'] for col in bars]
        # Energy loads subtypes
        barsL = ['energyLB', 'energyL1', 'energyL2']
        labelsL = [OCT[col]['translate'][1] for col in barsL]
        colorsL = [OCT[col]['color'] for col in barsL]
        # Energy system subtypes
        barsSY = ['energyG', 'energyP']
        labelsSY = [OCT[col]['translate'][1] for col in barsSY]
        colorsSY = [OCT[col]['color'] for col in barsSY]
        # Energy left subtypes
        barsGSL = ['energyL', 'energyS']
        labelsGSL = [OCT[col]['translate'][1] for col in barsGSL]
        colorsGSL = [OCT[col]['color'] for col in barsGSL]
        # All
        bars_ = barsL + barsSY + barsGSL

        # Plot types
        data.plot.bar(y=bars, ax=ax, color=colors, label=labels, width=0.60)
        pre_xlim = ax.get_xlim()

        # Plot Divisions
        if showD:
            width = ax.patches[0].get_width()
            # Plot Load Subtypes
            pos = 1.5
            data.plot.bar(y=barsL, ax=ax, color=colorsL, label=labelsL, stacked=True, position=pos, width=width)
            # Plot System Subtypes
            pos = 0.5
            data.plot.bar(y=barsSY, ax=ax, color=colorsSY, label=labelsSY, stacked=True, position=pos, width=width)
            # Plot Load Subtypes
            pos = -0.5
            data.plot.bar(y=barsGSL, ax=ax, color=colorsGSL, label=labelsGSL, stacked=True, position=pos, width=width)
            # Reset ax limits
            ax.set_xlim(pre_xlim) 

        # Add value labels
        if showV:
            containers = ax.containers
            for i, name in enumerate(bars):
                label = [f'{p:.0f}' for p in data[name]]
                ax.bar_label(containers[i], labels=label, rotation=lrot, color=colors[i], fontsize=8, padding=4)
            if showD:
                for i, names in enumerate(bars_):
                    label = [f'{p:.0f}' if p>0 else '' for p in data[names]]
                    ax.bar_label(containers[i+3], labels=label, rotation=lrot, fontsize=8, color='#1e1e1e', label_type='center')
        
        # Visuals
        ax.margins(y=0.1)
        if xtimestamp:
            ax.set_xticklabels([x.strftime("%m-%d %H") for x in data['timestamp']], rotation=45)
            plot.fig.autofmt_xdate()
        else:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.legend(loc="best")
        if gaxis != None:
            ax.grid(True, linestyle=':', axis=gaxis)
        ax.set_xlabel('Date & Time')
        ax.set_ylabel('Energy [Wh]')
        ax.set_title('Energy Balance')

        # draw_idle
        plot.draw_idle()
        self.ui.plotting_time.setText(f'Plotted in {time()-start:.3f} s')
    
    def plot_op(self):
        if self.optimize is None:
            return

        start = time()
        plot = self.ui.plot_op
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()

        # Init
        df = self.optimize.df
        x = self.ui.op_setting.currentText()
        if (y1 := self.ui.op_ax_left.currentText()) != 'None': 
            ax1.plot(df[x], df[y1], color='#2176db', label=y1, marker='o')
            ax1.set_ylabel(y1)
            ax1.legend(loc="upper left")
        if (y2 := self.ui.op_ax_right.currentText()) != 'None':
            ax2.plot(df[x], df[y2], color='#f8a62a', label=y2, marker='o')
            ax2.set_ylabel(y2)
            ax2.legend(loc="upper right")
        ax1.set_xlabel(x)
        ax1.grid(True, linestyle=':')
        plot.align_yaxis()

        # draw_idle
        plot.draw_idle()
        self.ui.plotting_time.setText(f'Plotted in {time()-start:.3f} s')
    #endregion

    #region -> Show results
    def show_results(self, df): 
        start = time()
        self.ui.table_s.setModel( QPandasModelPlus(df, i=0) )
        self.ui.table_eb.setModel( QPandasModelPlus(self.results.df_hour) )
        self.ui.table_eb_t.setModel( QPandasModelPlus(self.results.df_total.T) )
        self.ui.table_t.setModel( QPandasModelPlus(self.results.df_results))

        self.plot_general(df)
        self.plot_eb()
        self.plot_t()
        self.ui.plotting_time.setText(f'Plotted in {time()-start:.3f} s')

        # Checkboxes enable
        for c in self.ui.findChildren(QCheckBox): 
            c.setEnabled(True)
        
        self.ui.sim_line_style.setEnabled(True)
    
    def show_optimitzation_results(self):
        self.ui.table_op.setModel( QPandasModelPlus(self.optimize.df) )
        self.plot_op()
    #endregion
  
    #region -> Simulation Plot Options
    def toggle_loads_area(self, val):
        if self.sim_areas: # List Not empty
            for area in self.sim_areas:
                area.set_visible(val)
                label = area.get_label()
                label = '_'+label if not val else label[1:] if label[0] == "_" else label
                area.set_label(label)

            plot = self.ui.plot_s
            handles, labels = plot.ax.get_legend_handles_labels()
            legend = plot.ax.get_legend()
            plot.ax.legend(handles, labels)._set_loc(legend._loc)
            plot.draw_idle()
    
    def toggle_energyP(self):
        if self.sim is not None and self.sim.df_out is not None:
            self.plot_general(self.sim.df_out)

    def toggle_th(self, val):
        if self.th_lines: # List Not empty
            if val:
                for line in self.th_lines:
                    line.set_linestyle(':')
            else:
                for line in self.th_lines:
                    line.set_linestyle('None')
            self.ui.plot_s.draw_idle()
    #endregion

    #region -> Date Range Plot Selection lines
    def datetime_changed(self, _):
        if self.date_range_lines:
            self.date_range_lines[0].set_xdata(self.ui.start_date.dateTime().toPython())
            self.date_range_lines[1].set_xdata(self.ui.end_date.dateTime().toPython())
            self.ui.plot_dr.draw_idle()

    def data_lines_on_pick(self, event):
        line = event.artist
        x, _ = line.get_data()
        x = x[0] if isinstance(x, list) else x
        self.initial_date = mp.dates.date2num(x) if isinstance(x, float) else x

        fig = self.ui.plot_dr.ax.figure
        if self.date_line == None:
            self.date_line = event.artist
            self.on_move_cid = fig.canvas.mpl_connect('motion_notify_event', self.data_lines_on_move)
            self.on_keypress_cid = fig.canvas.mpl_connect('key_press_event', self.data_lines_on_keypress)
        else:
            self.data_lines_exit(mp.dates.num2date(self.date_range))

    def data_lines_on_keypress(self, event):
        if event.key == "escape":
            self.data_lines_exit(self.initial_date, True)
    
    def data_lines_exit(self, date, reset=False):
        if reset:
            self.date_line.set_xdata(mp.dates.date2num(date))
            self.ui.plot_dr.draw_idle()
        else:
            if 'Start' in self.date_line.get_label():
                self.ui.start_date.setDateTime(date)
            else:
                self.ui.end_date.setDateTime(date)
        self.date_line = None
        fig = self.ui.plot_dr.ax.figure
        fig.canvas.mpl_disconnect(self.on_move_cid)
        fig.canvas.mpl_disconnect(self.on_keypress_cid)

    def data_lines_on_move(self, event):
        if event.inaxes:
            self.date_range = event.xdata
            self.date_line.set_xdata(event.xdata)
            self.ui.plot_dr.draw_idle()
    #endregion

    #region -> Plot Line style
    def data_line_style(self, text):
        self.set_line_style(self.ui.plot_dr, self.data_lines, text, self.data_prev_ls, self.ui.data_line_style)
        
    def sim_line_style(self, text):
        self.set_line_style(self.ui.plot_s, self.sim_lines, text, self.sim_prev_ls, self.ui.sim_line_style)
    
    def set_line_style(self, plot, lines, text, prev, ui_input):
        if text != "" and lines:
            try:
                mp.axes._base._process_plot_format(text)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)
                ui_input.setText(prev)
            else:
                if prev != text:
                    linestyle = text
                    for e in mp.lines.lineMarkers.keys():
                        linestyle = linestyle.replace(str(e), '')
                    marker = text
                    for e in mp.lines.lineStyles.keys():
                        marker = marker.replace(e, '')
                    for line in lines:
                        line.set_linestyle(linestyle)
                        line.set_marker(marker)
                    prev = text
                    plot.draw_idle()
    #endregion



if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())
