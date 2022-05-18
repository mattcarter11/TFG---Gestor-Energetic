import math
import sys, json
from time import time
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView, QItemDelegate, QCheckBox, QTableView
from PySide6.QtCore import QFile, QIODevice, QDateTime, QCoreApplication, Qt, QModelIndex
import QMplWidgets as mw
import QPandasWidgets as pw
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib as mp
from PySide6.QtGui import QColor

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


class Load():
    def __init__(self):
        self.on = False
        self.commutations = 0

    def turn_on(self):
        if not self.on:
            self.on = True
            self.commutations += 1

    def turn_off(self):
        if self.on:
            self.on = False
            self.commutations += 1

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

def rearange_df(df):
    columns = [col for col in OCT.keys() if col in df.columns]
    return df[columns]

def df_plot_col(df, xcol, ycol, ax):
    return ax.plot(df[xcol], df[ycol], color=OCT[ycol]['color'], label=OCT[ycol]['translate'][0])

class App(QMainWindow):
    # Init
    def __init__(self):
        super().__init__()
        self.sim_prev_ls = self.data_prev_ls = ''
        self.load_ui()
        self.load_prev_settings()
        self.sig_init()
        # Tables view style
        for name in ['table_in', 'table_s', 'table_eb', 'table_eb_t', 'table_t']:
            table = self.ui.findChild(QTableView, name)
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setItemDelegate(AlignDelegate())
        for name in ['table_eb_t', 'table_t']:
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

    # Settings Load/Save
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
            self.ui.predict_final_energy.setChecked(settings['predict_final_energy'])

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
        settings["predict_final_energy"] = self.ui.predict_final_energy.isChecked()
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

    # Load data
    def load_file(self):
        path = QFileDialog.getOpenFileName(self, "Select Generated Power", '.', '*.csv')[0]
        if path != '':
            self.load_csv(path)

    def load_csv(self, path):
        l = [self.ui.simulate, self.ui.data_line_style]
        try:
            self.df = pd.read_csv(path, parse_dates=['timestamp']).fillna(0)
            self.df["powerG"] = self.df["powerG"].clip(lower=0)
            self.validate_df()
            if self.is_full_data():
                self.ui.results.setEnabled(True)
                self.fill_missing_powerLB()
                self.df = rearange_df(self.df)

        except Exception as err:
            if self.ui.file_path.text() == "":
                self.ui.results.setEnabled(False)
                for e in l:
                    e.setEnabled(False)
            QMessageBox.warning(self, "Error", str(err), QMessageBox.Ok)

        else:
            # Enable options
            for e in l:
                e.setEnabled(True)
            # Update UI
            self.ui.file_path.setText(path)
            self.limit_datarange_selectors()
            self.Ts = round((self.df['timestamp'].iloc[2] - self.df['timestamp'].iloc[1]).total_seconds() )
            self.ui.sampling_rate.setText(f'Sampling Rate: {self.Ts} s')
            # Update table
            model = QPandasModelPlus(self.df, i=0)
            self.ui.table_in.setModel(model)
            self.plot_in_data()
    
    def validate_df(self):
        if 'powerG' not in self.df.columns:
            raise Exception('mussint powerG column, must be an int or float')
        if not isinstance(self.df['powerG'].iloc[0], (float, int)):
            raise Exception('powerG must be an int or float')

    def is_full_data(self):
        l = ['on_offL1', 'on_offL2', 'powerC', 'powerG', 'powerL1', 'powerL2']
        return all([x in self.df.columns for x in l])

    def fill_missing_powerLB(self):
        # Calc missing base load power
        if 'powerC' in self.df.columns and 'powerLB' not in self.df.columns:
            self.df['powerLB'] = self.df['powerC']
            if 'powerL1' in self.df.columns:
                self.df['powerLB'] -= self.df['powerL1']
            if 'powerL2' in self.df.columns:
                self.df['powerLB'] -= self.df['powerL2']

    def limit_datarange_selectors(self):
        self.min_date = self.df['timestamp'].min()
        self.max_date = self.df['timestamp'].max()
        self.ui.date_range.setText(f'Min Date: {self.min_date}  -  Max Date: {self.max_date}')
        self.ui.start_date.setMinimumDateTime(self.min_date)
        self.ui.end_date.setMinimumDateTime(self.min_date)
        self.ui.start_date.setMaximumDateTime(self.max_date)
        self.ui.end_date.setMaximumDateTime(self.max_date)

    # Simulation Settings
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

    # Line style
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
                self.data_prev_ls = text
                plot.draw()

    # Data range selection
    def datetime_changed(self, _):
        self.date_range_lines[0].set_xdata(self.ui.start_date.dateTime().toPython())
        self.date_range_lines[1].set_xdata(self.ui.end_date.dateTime().toPython())
        self.ui.plot_dr.draw()

    # Toggle Options
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

    # Date Range Selection lines
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

    # Results
    def results_press(self):
        start = time()
        err = self.fill_missing_data()
        self.ui.simulation_time.setText(f'Simulation Time: {time()-start:.3f} s')
        if not err:
            self.show_results()

    def fill_missing_data(self):
        if self.select_data():
            return

        energyA = []
        energyP = []
        current_hour = None
        for _, row in self.data.iterrows():
            timestamp   = row['timestamp']
            power_g     = row['powerG']
            power_c     = row['powerLB'] + row['powerL1'] + row['powerL2']

            if current_hour != timestamp.hour:
                energy_a = energy_p =  0
                current_hour = timestamp.hour

            energy_a = (power_g - power_c) * self.Ts / 3600 + energy_a
            energy_p = (power_g * self.Ts) / 3600 + energy_p
            energyA.append( energy_a )
            energyP.append( energy_p )

        if 'powerA' not in self.df.columns:
            self.data['energyA'] = energyA
        if 'energyP' not in self.df.columns: 
            self.data['energyP'] = energyP

        # Calc the resot of the data
        self.split_energyA()
        self.simulation_hour_data()
        dic = {'Base Load': 0}
        dic['Load 1'] = self.data['on_offL1'].astype(bool).sum(axis=0)
        dic['Load 2'] = self.data['on_offL2'].astype(bool).sum(axis=0)
        commutations = pd.Series(dic)
        self.simulation_total_data(commutations)

    # Simulate
    def simulate_press(self):
        start = time()
        self.simulation()
        self.ui.simulation_time.setText(f'Simulation Time: {time()-start:.3f} s')
        self.show_results()

    def select_data(self):
        # Get Data limited by Date & Time interval
        start_date = self.ui.start_date.dateTime().toString()
        end_date = self.ui.end_date.dateTime().toString()
        self.data = self.df[self.df['timestamp'].between(start_date, end_date)].copy()

        # And check if there are enought samples (5 min of samples)
        samples = len(self.data.index)
        if samples <= (300/self.Ts):
            QMessageBox.warning(self, "Error", f"Date & Time interval must be at least 5 min", QMessageBox.Ok)
            return True
        self.ui.n_samples.setText(f'Simulation duration {samples*self.Ts/3600:.3f} h ({samples} Samples)')
        return False

    def simulation(self):
        if self.select_data():
            return True
        
        self.data = self.data.drop(['on_offL1', 'on_offL2'],axis=1)
        # [Simulation] Init data results
        sim_data = {'powerC':[], 'powerLB':[], 'powerL1':[], 'powerL2':[], 'energyP':[], 'energyA':[]}

        # [Program] Init data results
        loads = [None, Load(), Load()]
        current_hour = None
        off_timestamp_limit = dt.datetime.now()

        # [Simulation] -> [Program] while True:
        for _, row in self.data.iterrows():
            # [Simulation] Calc Powers at that instant of time
            power_lb = self.ui.base_load.value()                # Base Load (not controled)
            if 'powerLB' in self.data.columns and self.ui.use_data_bl.isChecked():
                power_lb = row['powerLB']
            power_l1 = loads[1].on*self.ui.load1.value()        # Load 1    (controled)
            power_l2 = loads[2].on*self.ui.load2.value()        # Load 2    (controled)
            power_c = power_lb + power_l1 + power_l2            # Total Consumed
            # [Program] Get timestamp power generated and consumed 
            timestamp = row['timestamp']                        # [Program]
            power_g = row['powerG']                             # [Program] power_g = driver.get_generated()
            power_c = power_c                                   # [Program] power_c = driver.get_consumed()

            # [Program] See if hour has passed
            if current_hour != timestamp.hour:
                energy_a =  0
                current_hour = timestamp.hour
                next_hour = timestamp.replace(second=0, microsecond=0, minute=0) + dt.timedelta(hours=1)
                # [Simulation]
                energy_p = 0

            # [Program] Calc Available Energy [Wh]
            energy_a = (power_g - power_c) * self.Ts / 3600 + energy_a

            # [Program] Algorithm
            match self.ui.algorithm.currentIndex():
                case 0:
                    if self.ui.load1.value() > 0:
                        if energy_a >= self.ui.th_top1.value(): 
                            loads[1].turn_on()
                        elif energy_a <= self.ui.th_bottom1.value():
                            loads[1].turn_off()
                    if self.ui.load2.value() > 0:
                        if energy_a >= self.ui.th_top2.value(): 
                            loads[2].turn_on()
                        elif energy_a <= self.ui.th_bottom2.value():
                            loads[2].turn_off()
                
                case 1:
                    time_to_use = energy_a/self.ui.load1.value() * 3600 # [s] <- Wh/W = h
                    time_limit = self.ui.time_limit.value()
                    if time_to_use >= time_limit:
                        off_timestamp_limit = timestamp + dt.timedelta(seconds=time_limit)
                        loads[1].turn_on()
                    elif timestamp >= off_timestamp_limit:
                        loads[1].turn_off()

                case 2:
                    time_remaining = (next_hour - timestamp).total_seconds()
                    if self.ui.predict_final_energy.isChecked():
                        energy = energy_a + time_remaining*power_g/3600
                    else:
                        energy = energy_a
                    time_to_use = energy / self.ui.load1.value() * 3600 # [s] <- Wh/W = h
                    if time_to_use >= time_remaining:
                        loads[1].turn_on()
                    elif energy <= 0:
                        loads[1].turn_off()

            # [Simulation] Calc/Save other energys for data avaluation [Wh]
            energy_p = (power_g * self.Ts) / 3600 + energy_p            # Energy Produced
            sim_data['powerC'].append(power_c)
            sim_data['powerLB'].append(power_lb)
            sim_data['powerL1'].append(power_l1)
            sim_data['powerL2'].append(power_l2)
            sim_data['energyP'].append(energy_p)
            sim_data['energyA'].append(energy_a)
        
        # [Simulation] Store data to pandas dataframe
        for key, value in sim_data.items():
            self.data[key] = value

        # Calc the resot of the data
        self.split_energyA()
        self.simulation_hour_data()
        commutations = pd.Series({'Base Load': 0, 'Load 1': loads[1].commutations, 'Load 2': loads[2].commutations})
        self.simulation_total_data(commutations)
        return False
    
    def split_energyA(self):
        # Split available into grid and available
        energy_g = self.data['energyA'].copy()
        energy_g[energy_g > 0] = 0
        self.data['energyG'] = - energy_g
        self.data['energyA'] = self.data['energyA'].mask(self.data['energyA'] < 0, 0)
        
    def simulation_hour_data(self):
        # Grup data by hour, select only energies, copy data in new place, add hour grups to get total
        data_h = self.data.groupby(pd.Grouper(key='timestamp', freq='H'), as_index=False)
        select = ['timestamp', 'energyP', 'energyG', 'energyA']
        self.data_h = data_h[select].last().copy()
        data_h_sum = data_h.sum()
        # Energy in system
        self.data_h.insert(1, 'energySY', (self.data_h['energyP'] + self.data_h['energyG']).values)
        # Max Energy Consunption
        n_elements = self.data_h.shape[0] # Number of rows
        energy_cm = self.ui.base_load.value() + self.ui.load1.value() + self.ui.load2.value()
        self.data_h['energyCM'] = np.repeat(energy_cm, n_elements)
        # Energy Consumptions
        self.data_h['energyC'] = (data_h_sum['powerC']*self.Ts/3600).values
        self.data_h['energyLB'] = (data_h_sum['powerLB']*self.Ts/3600).values
        self.data_h['energyL1'] = (data_h_sum['powerL1']*self.Ts/3600).values
        self.data_h['energyL2'] = (data_h_sum['powerL2']*self.Ts/3600).values
        # Energy Surplus
        energy_s = (self.data_h['energyP'] - energy_cm).values
        energy_s[energy_s < 0] = 0
        self.data_h['energyS'] = energy_s
        # Energy Lost
        energy_l = (self.data_h['energyA'] - self.data_h['energyS']).values
        energy_l[energy_l < 0] = 0
        self.data_h['energyL'] = energy_l

    def simulation_total_data(self, commutations):
        samples = len(self.data.index)
        sim_hours = samples*self.Ts/3600
        sim_days = 24/sim_hours

        # Energy Balance - Add hourly columns to get one row series of the total        
        self.data_eb_t = self.data_h.sum(numeric_only=True).rename('Total [Wh]')
        self.data_eb_t = self.data_eb_t.to_frame()
        self.data_eb_t['Daily Total [Wh/day]'] = self.data_eb_t['Total [Wh]'].mul(sim_days)
        self.data_eb_t = self.data_eb_t.T

        # Average commutations (day)
        dayly_com = commutations*sim_days
        # Time On/Powered
        select = ['powerLB', 'powerL1', 'powerL2']
        name = ['Base Load', 'Load 1', 'Load 2']
        samples_on = self.data[select][self.data[select] > 0].count()
        samples_on.rename(dict(zip(select, name)), inplace = True)
        hours_on = samples_on*self.Ts/3600
        hours_on_daily = hours_on*sim_days
        # Convert to dataframe
        dic = {'Commutations':commutations, 'Daily Commutations':dayly_com, 'Time On [samples]':samples_on, 'Time On [h]':hours_on, 'Daily Time On [h/day]': hours_on_daily}
        self.data_t = pd.DataFrame.from_dict(dic).T

    # Plots
    def plot_in_data(self):
        start = time()
        plot = self.ui.plot_dr
        ax1, ax2 = plot.ax1, plot.ax2
        ax1.clear()
        ax2.clear()

        # Plot Data
        self.data_lines = df_plot_col(self.df, 'timestamp', 'powerG', ax1)
        if 'powerLB' in self.df.columns:
            self.data_lines += df_plot_col(self.df, 'timestamp', 'powerLB', ax2)

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

        # Plot Power Lines
        self.sim_lines = df_plot_col(self.data, 'timestamp', 'powerC', ax1)
        self.sim_lines += df_plot_col(self.data, 'timestamp', 'powerG', ax1)
        
        # Power Load Areas
        cols = ['powerLB', 'powerL1', 'powerL2']
        labels = [OCT[col]['translate'][0] for col in cols]
        colors = [OCT[col]['color'] for col in cols]
        self.sim_areas = self.data.plot.area('timestamp', cols, ax=ax1, linewidth=0, color=colors, label=labels).collections
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
            self.sim_lines += df_plot_col(self.data, 'timestamp', 'energyP', ax2)
        self.sim_lines += df_plot_col(self.data, 'timestamp', 'energyA', ax2)
        self.sim_lines += df_plot_col(self.data, 'timestamp', 'energyG', ax2)

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
        self.plot_bars(self.data_h, self.ui.plot_eb, showV, showD)

    def plot_t(self):
        data = self.data_eb_t
        data['timestamp'] = self.data_h.iloc[-1]['timestamp']
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

    # Show data
    def show_results(self): 
        model = QPandasModelPlus(self.data, i=0)
        self.ui.table_s.setModel(model)
        model = QPandasModelPlus(self.data_h, i=0)
        self.ui.table_eb.setModel(model)
        model = QPandasModelPlus(self.data_eb_t.T)
        self.ui.table_eb_t.setModel(model)
        model = QPandasModelPlus(self.data_t.T)
        self.ui.table_t.setModel(model)

        start = time()
        self.plot_general()
        self.plot_eb()
        self.plot_t()
        self.ui.plotting_time.setText(f'Plotting Time: {time()-start:.3f} s')

        # Checkboxes enable
        for c in self.ui.findChildren(QCheckBox): 
            c.setEnabled(True)
        
        self.ui.sim_line_style.setEnabled(True)

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())
