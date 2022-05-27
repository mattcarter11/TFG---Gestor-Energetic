import sys, json, PySide6
from time import time
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView, QItemDelegate, QCheckBox, QTableView
from PySide6.QtCore import QFile, QIODevice, QDateTime, QCoreApplication, Qt
from lib.sim.Simulator import Simulator
from lib.sim.Load import Load
from lib.sim.Results import Results
import lib.sim.AlgorithmsConfig as ac
import lib.sim.DataFrames as df
import lib.myQT.QMplWidgets as mw
import lib.myQT.QPandasWidgets as pw
import pandas as pd
import numpy as np
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
        super().__init__()
        self.sim_prev_ls = self.data_prev_ls = ''
        self.load_ui()
        self.load_prev_settings()
        self.sig_init()
        # Tables view style
        for name in ['table_in', 'table_s', 'table_eb', 'table_loads_aprox', 'table_eb_t', 'table_t']:
            table = self.ui.findChild(QTableView, name)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setItemDelegate(AlignDelegate())
        for name in ['table_loads_aprox', 'table_eb_t', 'table_t']:
            table = self.ui.findChild(QTableView, name)
            table.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            
    def sig_init(self):
        # Options
        self.ui.algorithm.currentIndexChanged.connect(self.algorithm_changed)
        self.ui.load_file.clicked.connect(self.load_file)
        self.ui.simulate.clicked.connect(self.simulate_press)
        self.ui.results.clicked.connect(self.results_press)
        self.ui.time_limit.valueChanged.connect(self.time_limit_changed)
        self.ui.load1.valueChanged.connect(self.time_limit_changed)
        self.time_limit_changed()
        self.ui.load1.valueChanged.connect(self.th_disable)
        self.ui.load2.valueChanged.connect(self.th_disable)
        self.th_disable()
        self.ui.start_date.dateTimeChanged.connect(self.datetime_changed)
        self.ui.end_date.dateTimeChanged.connect(self.datetime_changed)
        # Data Range
        self.ui.data_line_style.textChanged.connect(self.data_line_style)
        # Simulation Plot
        self.ui.sim_line_style.textChanged.connect(self.sim_line_style)
        # Checkboxes
        connections = {
            self.plot_general: ['energyP_s'],
            self.toggle_th: ['show_th'],
            self.toggle_loads_area: ['show_loads_area'],
            self.plot_eb: ['show_values_eb', 'subdivide_eb'],
            self.plot_t: ['show_values_t', 'subdivide_t']
        }
        for fun, names in connections.items():
            for name in names:
                self.ui.findChild(QCheckBox, name).stateChanged.connect(fun)
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
        if 'start_date' in keys:
            self.ui.start_date.setDateTime(QDateTime.fromString(settings['start_date'], DT_FORMAT))
        if 'end_date' in keys:
            self.ui.end_date.setDateTime(QDateTime.fromString(settings['end_date'], DT_FORMAT))
        if 'algorithm' in keys:
            self.ui.algorithm.setCurrentText(settings['algorithm'])
            
        if 'th_top1' in keys:
            self.ui.th_top1.setValue(settings['th_top1'])
        if 'th_top2' in keys:
            self.ui.th_top2.setValue(settings['th_top2'])
        if 'th_bottom1' in keys:
            self.ui.th_bottom1.setValue(settings['th_bottom1'])
        if 'th_bottom2' in keys:
            self.ui.th_bottom2.setValue(settings['th_bottom2'])
        if 'time_limit' in keys:
            self.ui.time_limit.setValue(settings['time_limit'])
        if 'predict_final_energy' in keys:
            self.ui.predict_final_energy.setCurrentText(settings['predict_final_energy'])

        if 'use_data_bl' in keys:
            self.ui.use_data_bl.setChecked(settings['use_data_bl'])
        if 'base_load' in keys:
            self.ui.base_load.setValue(settings['base_load'])
        if 'load1' in keys:
            self.ui.load1.setValue(settings['load1'])
        if 'load2' in keys:
            self.ui.load2.setValue(settings['load2'])

        if 'data_line_style' in keys:
            self.ui.data_line_style.setText(settings['data_line_style'])

        if 'sim_line_style' in keys:
            self.ui.sim_line_style.setText(settings['sim_line_style'])
        if 'show_loads_area' in keys:
            self.ui.show_loads_area.setChecked(settings['show_loads_area'])
        if 'show_th' in keys:
            self.ui.show_th.setChecked(settings['show_th'])
        if 'energyP_s' in keys:
            self.ui.energyP_s.setChecked(settings['energyP_s'])

        if 'subdivide_eb' in keys:
            self.ui.subdivide_eb.setChecked(settings['subdivide_eb'])
        if 'subdivide_eb' in keys:
            self.ui.subdivide_eb.setChecked(settings['subdivide_eb'])

        if 'show_values_t' in keys:
            self.ui.show_values_t.setChecked(settings['show_values_t'])
        if 'subdivide_eb' in keys:
            self.ui.subdivide_eb.setChecked(settings['subdivide_eb'])

        if 'file_path' in keys and settings['file_path'] != '':
            self.load_csv(settings['file_path'])
       
    def close_save(self):
        settings = {}
        settings["file_path"] = self.ui.file_path.text()
        settings["start_date"] = self.ui.start_date.dateTime().toString(DT_FORMAT)
        settings["end_date"] = self.ui.end_date.dateTime().toString(DT_FORMAT)

        settings["algorithm"] = self.ui.algorithm.currentText()
        settings["time_limit"] = self.ui.time_limit.value()
        settings["predict_final_energy"] = self.ui.predict_final_energy.currentText()
        settings["th_top1"] = self.ui.th_top1.value()
        settings["th_top2"] = self.ui.th_top2.value()
        settings["th_bottom1"] = self.ui.th_bottom1.value()
        settings["th_bottom2"] = self.ui.th_bottom2.value()

        settings["use_data_bl"] = self.ui.use_data_bl.isChecked()
        settings["base_load"] = self.ui.base_load.value()
        settings["load1"] = self.ui.load1.value()
        settings["load2"] = self.ui.load2.value()

        settings["data_line_style"] = self.ui.data_line_style.text()

        settings["sim_line_style"] = self.ui.sim_line_style.text()
        settings["show_loads_area"] = self.ui.show_loads_area.isChecked()
        settings["energyP_s"] = self.ui.energyP_s.isChecked()
        settings["show_th"] = self.ui.show_th.isChecked()

        settings["show_values_eb"] = self.ui.show_values_eb.isChecked()
        settings["subdivide_eb"] = self.ui.subdivide_eb.isChecked()

        settings["show_values_t"] = self.ui.show_values_t.isChecked()
        settings["subdivide_eb"] = self.ui.subdivide_eb.isChecked()

        with open('prev_settings.json', 'w') as f:
            json.dump(settings, f, indent=4)
    #endregion

    #region -> Load data
    def load_file(self):
        path = QFileDialog.getOpenFileName(self, "Select Generated Power", './db', '*.csv')[0]
        if path != '':
            self.load_csv(path)

    def load_csv(self, path):
        l = [self.ui.simulate, self.ui.data_line_style]
        try:
            self.dfI = df.DataFrameIn(pd.read_csv(path, parse_dates=['timestamp']))
            try:
                self.dfI = df.DataFrameOut(self.dfI.df)
            except:
                pass
            else:
                self.ui.results.setEnabled(True)

        except Exception as err:
            if self.ui.file_path.text() == "":
                self.ui.results.setEnabled(False)
                for e in l:
                    e.setEnabled(False)
            QMessageBox.warning(self, "Error", str(err), QMessageBox.Ok)

        else:
            self.sim = Simulator(self.dfI)
            # Enable options
            for e in l:
                e.setEnabled(True)
            # Update UI
            self.ui.file_path.setText(path)
            self.limit_datarange_selectors()
            self.ui.sampling_rate.setText(f'Sampling Rate: {self.sim.Ts} s')
            # Update table
            model = QPandasModelPlus(self.dfI.df, i=0)
            self.ui.table_in.setModel(model)
            self.plot_in_data()
    
    def limit_datarange_selectors(self):
        self.min_date = self.dfI.df['timestamp'].min()
        self.max_date = self.dfI.df['timestamp'].max()
        self.ui.date_range.setText(f'Min Date: {self.min_date}  -  Max Date: {self.max_date}')
        self.ui.start_date.setMinimumDateTime(self.min_date)
        self.ui.end_date.setMinimumDateTime(self.min_date)
        self.ui.start_date.setMaximumDateTime(self.max_date)
        self.ui.end_date.setMaximumDateTime(self.max_date)
    #endregion

    #region -> Simulation Settings
    def time_limit_changed(self):
        self.tl_eq = self.ui.time_limit.value() * self.ui.load1.value() / 3600
        self.ui.wh_eq.setText(f'Top threshold {self.tl_eq:.2f} Wh')

    def algorithm_changed(self, i):
        self.ui.load2.setEnabled(i == 0)

    def th_disable(self):
        status_l1 = (self.ui.load1.value() > 0)
        self.ui.th_top1.setEnabled(status_l1)
        self.ui.th_bottom1.setEnabled(status_l1)
        status_l2 = (self.ui.load2.value() > 0)
        self.ui.th_top2.setEnabled(status_l2)
        self.ui.th_bottom2.setEnabled(status_l2)
    #endregion

    #region ->  Line style
    def data_line_style(self, text):
        self.set_line_style(self.ui.plot_dr, self.data_lines, text, self.data_prev_ls, self.ui.data_line_style)
        
    def sim_line_style(self, text):
        self.set_line_style(self.ui.plot_s, self.sim_lines, text, self.sim_prev_ls, self.ui.sim_line_style)
    
    def set_line_style(self, plot, lines, text, prev, ui_input):
        if text == "":
            return
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
                plot.draw()
    #endregion

    #region ->  Data range selection
    def datetime_changed(self, _):
        self.date_range_lines[0].set_xdata(self.ui.start_date.dateTime().toPython())
        self.date_range_lines[1].set_xdata(self.ui.end_date.dateTime().toPython())
        self.ui.plot_dr.draw()
    #endregion

    #region ->  Toggle Options
    def toggle_th(self, val):
        if val:
            for line in self.th_lines:
                line.set_linestyle(':')
        else:
            for line in self.th_lines:
                line.set_linestyle('None')
        self.ui.plot_s.draw()

    def toggle_loads_area(self, val):
        self.toggle_areas(val, self.sim_areas)

    def toggle_areas(self, val, areas):
        for area in areas:
            area.set_visible(val)
            label = area.get_label()
            label = '_'+label if not val else label[1:] if label[0] == "_" else label
            area.set_label(label)

        plot = self.ui.plot_s
        handles, labels = plot.ax.get_legend_handles_labels()
        legend = plot.ax.get_legend()
        plot.ax.legend(handles, labels)._set_loc(legend._loc)
        plot.draw()
    #endregion

    #region ->  Date Range Selection lines
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
            self.ui.plot_dr.draw()
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
            self.ui.plot_dr.draw()
    #endregion

    #region -> Simulation/Results
    def results_press(self):
        self.is_sim = False
        start = time()
        startDT = self.ui.start_date.dateTime().toString()
        endDT = self.ui.end_date.dateTime().toString()
        self.results = Results(self.dfI.select_daterange(startDT, endDT, 300))
        self.ui.simulation_time.setText(f'Results Time: {time()-start:.3f} s')
        self.show_results()

    def simulate_press(self):
        self.is_sim = True
        start = time()
        try:
            self.sim.simulate(
                self.ui.start_date.dateTime().toString(),
                self.ui.end_date.dateTime().toString(),
                self.get_algorithm_config(),
                Load(self.ui.load1.value()), 
                Load(self.ui.load2.value()),
                None if isinstance(self.dfI, df.DataFrameOut) and self.ui.use_data_bl.isChecked() else self.ui.base_load.value()
            )
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Error", f"Date & Time interval must be at least 5 min", QMessageBox.Ok)
        else:
            self.ui.n_samples.setText(f'Simulation duration {self.sim.simulated_nsec/3600:.3f} h ({self.sim.simulated_nsec} Samples)')
            self.ui.simulation_time.setText(f'Simulation Time: {time()-start:.3f} s')
            self.results = Results(df.DataFrameOut(self.sim.df_out))
            self.show_results()

    def get_algorithm_config(self):
        match self.ui.algorithm.currentIndex():
            case 0: 
                return ac.HysteresisConfig(
                    self.ui.th_top1.value(), self.ui.th_bottom1.value(),
                    self.ui.th_top2.value(), self.ui.th_bottom2.value(),
                )
            case 1:
                return ac.MinOnTimeConfig( self.ui.time_limit.value() )
            case 2:
                match self.ui.predict_final_energy.currentIndex():
                    case 0: predict = ac.PredictFinalEnergy.disabled
                    case 1: predict = ac.PredictFinalEnergy.avarage_power
                    case 2: predict = ac.PredictFinalEnergy.project_current_power
                return ac.TimeToConsume( predict )
    #endregion

    #region ->  Plots
    def plot_in_data(self):
        start = time()
        plot = self.ui.plot_dr
        ax1, ax2 = plot.ax1, plot.ax2
        ax1.clear()
        ax2.clear()
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
        plot.draw()
        self.data_line_style(self.ui.data_line_style.text())
        self.ui.plotting_time.setText(f'Plotting Time: {time()-start:.3f} s')

    def plot_general(self):
        start = time()
        plot = self.ui.plot_s
        ax1, ax2 = plot.ax1, plot.ax2
        ax1.clear()
        ax2.clear()
        df = self.sim.df_out if self.is_sim else self.results.dfI.df

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
        plot.draw()
        self.sim_line_style(self.ui.sim_line_style.text())
        self.ui.plotting_time.setText(f'Plotting Time: {time()-start:.3f} s')

    def plot_eb(self):
        showV = self.ui.show_values_eb.isChecked()
        showD = self.ui.subdivide_eb.isChecked()
        self.plot_bars(self.results.df_hour, self.ui.plot_eb, showV, showD)

    def plot_t(self):
        data = self.results.df_total
        data['timestamp'] = self.results.df_hour.iloc[-1]['timestamp']
        showV = self.ui.show_values_t.isChecked()
        showD = self.ui.subdivide_t.isChecked()
        self.plot_bars(data, self.ui.plot_eb_t, showV, showD, None, 'horizontal', False)

    def plot_bars(self, data, plot, showV, showD, gaxis='both', lrot='vertical', xtimestamp = True):
        start = time()
        ax = plot.ax
        ax.clear()

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

        # Draw
        plot.draw()
        self.ui.plotting_time.setText(f'Plotting Time: {time()-start:.3f} s')
    #endregion

    #region ->  Show data
    def show_results(self): 
        df = self.sim.df_out if self.is_sim else self.results.dfI.df
        self.ui.table_s.setModel( QPandasModelPlus(df, i=0) )
        self.ui.table_eb.setModel( QPandasModelPlus(self.results.df_hour, i=0) )
        self.ui.table_loads_aprox.setModel( QPandasModelPlus(self.results.df_load_aprox) )
        self.ui.table_eb_t.setModel( QPandasModelPlus(self.results.df_total.T) )
        self.ui.table_t.setModel( QPandasModelPlus(self.results.df_results.T))

        start = time()
        self.plot_general()
        self.plot_eb()
        self.plot_t()
        self.ui.plotting_time.setText(f'Plotting Time: {time()-start:.3f} s')

        # Checkboxes enable
        for c in self.ui.findChildren(QCheckBox): 
            c.setEnabled(True)
        
        self.ui.sim_line_style.setEnabled(True)
    #endregion


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())
