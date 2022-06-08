import sys, json, traceback
from time import time
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QDateTime, QCoreApplication, Qt, QModelIndex
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView, QItemDelegate, QCheckBox, QTableView, QDateTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit
import pandas as pd
import matplotlib as mp
from lib.sim.Load import Load
from lib.sim.Results import Results
from lib.sim.Optimize import Optimize
import lib.sim.Simulator as sim
import lib.sim.AlgorithmsConfig as ac
import lib.sim.DataFrames as df
import lib.myQT.QMplWidgets as mw
import lib.myQT.QPandasWidgets as pw
from constants import *

class AlignDelegate(QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = Qt.AlignCenter
        QItemDelegate.paint(self, painter, option, index)

class QPandasModelTranslate(pw.QPandasModel):

    def __init__(self, dataframe: pd.DataFrame, i=0, use_unit=False, precision=3, parent=None):
        super().__init__(dataframe, precision, parent)
        self.i = i
        self.use_unit = use_unit

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                title = str(self._dataframe.columns[section])
            if orientation == Qt.Vertical:
                title = str(self._dataframe.index[section])
            if title in OCT.keys():
                name = OCT[title]['translate'][self.i]
                if self.use_unit == True or (isinstance(self.use_unit, list) and title in self.use_unit):
                    if (unit:=OCT[title]["unit"]) != '':
                        return f'{name} [{unit}]'
                return name
        
        return super().headerData(section, orientation, role)

def df_plot_col(df:pd.DataFrame, xcol:str, ycol:str, ax):
    return ax.plot(df[xcol], df[ycol], color=OCT[ycol]['color'], label=OCT[ycol]['translate'][0])

def QTable_fit_items_heigh(table):
    height = -54
    for i in range(table.model().rowCount()):
        height += table.verticalHeader().sectionSize(i) 
    if not table.horizontalScrollBar().isHidden():
        height += table.horizontalScrollBar().height()
    if not table.horizontalHeader().isHidden():
        height += table.horizontalHeader().height()
    table.verticalHeader().setMaximumHeight(height)

class App(QMainWindow):
    #region -> Init
    def __init__(self):
        self.first_table_show = True
        self.sim_prev_ls = self.data_prev_ls = ''
        self.th_lines = self.sim_areas = self.sim_lines = self.data_lines = self.date_range_lines = []
        self.results = self.optimize = None

        t0 = time()
        super().__init__()
        self.load_ui()
        self.load_ui_manual_part()
        t1 = time()
        self.load_prev_settings()
        t2 = time()
        self.sig_init()
        self.ui.calc_time.setText(f'Program loaded in {time()-t0-(t2-t1):.3f} s.')

    def load_ui(self):
        # Check if file exists
        ui_file = QFile(UI_FILE)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {UI_FILE}: {ui_file.errorString()}")
            sys.exit(-1)
        # Load .ui & external widgets
        loader = QUiLoader()
        loader.registerCustomWidget(mw.QMplPlot)
        loader.registerCustomWidget(mw.QMplTwinxPlot)
        loader.registerCustomWidget(mw.QMplPlotterWidget)
        self.ui = loader.load(ui_file)
        self.ui.show()
        ui_file.close()
    
    def load_ui_manual_part(self): 
        # Other ui stuff
        self.ui.plot_op.align = False
        # Tables view style
        for table in self.ui.findChildren(QTableView):
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.setItemDelegate(AlignDelegate())
        for name in ['table_eb_t', 'table_t', 'table_price_energy']:
            table = self.ui.findChild(QTableView, name)
            table.verticalHeader().setDefaultAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # Warning Optimize not resize on hiden
        pol = self.ui.op_recalc_warn.sizePolicy()
        pol.setRetainSizeWhenHidden(True)
        self.ui.op_recalc_warn.setSizePolicy(pol) 
        # List Optimze Axes values
        for key, value in OpAxDict.items():
            self.ui.op_ax_left.addItem(key)
            self.ui.op_ax_right.addItem(key)
            
    def sig_init(self):
        # Date Time
        self.ui.start_date.dateTimeChanged.connect(self.start_date_changed)
        self.ui.end_date.dateTimeChanged.connect(self.end_date_changed)
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
        # Buttons
        self.ui.load_file.clicked.connect(self.load_file)
        self.ui.unload_file.clicked.connect(self.unload_file)
        self.ui.simulate.clicked.connect(self.simulate_press)
        self.ui.results.clicked.connect(self.results_press)
        # Line Style
        self.ui.data_line_style.textChanged.connect(self.data_line_style)
        self.ui.sim_line_style.textChanged.connect(self.sim_line_style)
        # Price 
        self.ui.sell_price.valueChanged.connect(self.sell_price_changed)
        self.price_model.dataChanged.connect(self.table_price_edited)
        self.ui.plot_price.dataChanged.connect(self.plot_price_edited)
        # Simulation plot
        self.ui.show_loads_area.stateChanged.connect( self.toggle_loads_area)
        self.ui.energyP_s.stateChanged.connect( self.toggle_energyP)
        self.ui.show_th.stateChanged.connect( self.toggle_th)
        # Energy balance plot
        self.ui.show_values_eb.stateChanged.connect( self.plot_eb)
        self.ui.show_ecm_eb.stateChanged.connect( self.plot_eb)
        self.ui.subdivide_eb.stateChanged.connect( self.plot_eb)
        # Summary balance plot
        self.ui.show_values_t.stateChanged.connect( self.plot_t)
        self.ui.show_ecm_t.stateChanged.connect( self.plot_t)
        self.ui.subdivide_t.stateChanged.connect( self.plot_t)
        # Optimize
        self.ui.op_calculate.clicked.connect(self.optimize_press)
        self.ui.op_ax_left.currentIndexChanged.connect(self.plot_op)
        self.ui.op_ax_right.currentIndexChanged.connect(self.plot_op)
        # Trigger settings save on window close
        app.aboutToQuit.connect(self.close_save)      
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

        for name in SettingsQCheckBoxes:
            if name in keys:
                self.ui.findChild(QCheckBox, name).setChecked(settings[name])

        for name in SettingsQLineEdits:
            if name in keys:
                self.ui.findChild(QLineEdit, name).setText(settings[name])

        if 'file_path' in keys and settings['file_path'] != '':
            self.load_csv(settings['file_path'])

        list = settings['table_price_energy'] if 'table_price_energy' in keys else [0.0]*24
        self.df_price = pd.DataFrame( {'Price [€/kWh]':list} )
        self.talbe_price(self.df_price.T)
        self.plot_price(self.df_price)
       
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

        settings['table_price_energy'] = self.df_price.iloc[:,0].values.astype(float).tolist()

        with open('prev_settings.json', 'w') as f:
            json.dump(settings, f, indent=4)
    #endregion

    #region -> Load data
    def load_file(self):
        path = QFileDialog.getOpenFileName(self, "Select Generated Power", './db', '*.csv')[0]
        if path != '':
            self.load_csv(path)

    def load_csv(self, path):
        t0 = time()
        try:
            dataframe = pd.read_csv(path, parse_dates=['timestamp'])
            self.df_in = df.DataFrameIn(dataframe)
            try:    self.df_in = df.DataFrameOut(dataframe)
            except: self.ui.results.setEnabled(False)
            else:   self.ui.results.setEnabled(True)

        except Exception as ex:
            self.unload_file()
            self.df_in = None
            print(f"[{type(ex).__name__}] {ex} \n\n {traceback.format_exc()}")
            QMessageBox.warning(self, "Error", f"{ex}", QMessageBox.Ok)

        else:
            self.df_in.rearange_cols()
            # Enable options
            self.ui.simulate.setEnabled(True)
            self.ui.op_calculate.setEnabled(True)
            # Update UI
            self.ui.file_path.setText(path)
            self.limit_datarange_selectors()
            self.ui.sampling_rate.setText(f'Sampling rate: {self.df_in.Ts} s')
            # Update table
            self.ui.table_in.setModel(QPandasModelTranslate(self.df_in.df))
            t1 = time()
            self.plot_in_data()
            self.ui.plotting_time.setText(f'Data loaded in {t1-t0:.3f} s. Plotted in {time()-t1:.3f} s')
    
    def limit_datarange_selectors(self):
        min_date = self.df_in.df['timestamp'].min()
        max_date = self.df_in.df['timestamp'].max()
        format = '%Y-%m-%d %H:%M:%S'
        self.ui.date_range.setText(f'Date Range: {min_date.strftime(format)} - {max_date.strftime(format)} ({self.df_in.nsamples} Samples)')
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

    #region -> Price
    def plot_price(self, df:pd.DataFrame):
        plot = self.ui.plot_price
        ax = plot.ax

        plot.set_line(df.index, df['Price [€/kWh]'], label='Buy Price')

        self.sell_price_line = mw.QMplMovableHVLine(
            ax.axhline(self.ui.sell_price.value(), color=COLOR_G1, linestyle='-', label='Sell Price'), 
            mw.QMplHVLineType.hline,
            plot.fig
        )
        self.sell_price_line.dataChanged.connect(self.sell_price_line_changed)

        ax.grid(True, linestyle=':')
        ax.legend(loc="upper left")
        ax.set_xlabel('Hour [h]')
        ax.set_ylabel('Price [€/kWh]')
    
    def talbe_price(self, df:pd.DataFrame):
        self.price_model = pw.QPandasModelEdit(df, 5)
        self.ui.table_price_energy.setModel(self.price_model)
        QTable_fit_items_heigh(self.ui.table_price_energy)

    def table_price_edited(self, index:QModelIndex, _):
        val = self.price_model.data(index, Qt.DisplayRole)
        self.ui.plot_price.set_value(index.column(), float(val))
        self.ui.plot_price.home_view()

    def plot_price_edited(self, val, i):
        index = self.price_model.index(0, i)
        self.price_model.setData(index, val, Qt.EditRole)
    
    def sell_price_line_changed(self, val):
        self.ui.sell_price.setValue(val)

    def sell_price_changed(self, val):
        self.sell_price_line.set_xydata(0, val)
        self.ui.plot_price.draw_idle()
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
        t0 = time()
        df = self.df_in.select_daterange(
            self.ui.start_date.dateTime().toString(), 
            self.ui.end_date.dateTime().toString()
        )
        df.fill_missing_power()
        df.rearange_cols()
        self.results = Results(df, self.df_price.iloc[:, 0], self.ui.sell_price.value())
        self.ui.calc_time.setText(f'Results calculated in {time()-t0:.3f} s')
        self.show_results(df.df)

    def simulate_press(self):
        t0 = time()
        err = self.simulate()
        t1 = time()
        if not err:
            self.results = Results(self.df_out, self.df_price.iloc[:, 0], self.ui.sell_price.value())
            self.ui.calc_time.setText(f'Simulated in {time()-t0:.3f} s. Results calculated in {time()-t1:.3f} s')
            self.print_sim_duration()
            self.show_results(self.df_out.df)          

    def optimize_press(self):
        t0 = time()
        self.optimize = Optimize(self.ui.op_setting.currentText(), OpAxDict)
        values = range(self.ui.op_start.value(), self.ui.op_end.value()+self.ui.op_step.value(), self.ui.op_step.value()) 
        for value in values:
            err = self.simulate(value)
            if err: 
                break
            self.optimize.add_results(value, Results(self.df_out, self.df_price.iloc[:, 0], self.ui.sell_price.value()))
        if not err:
            self.ui.calc_time.setText(f'Optimize calculations in {time()-t0:.3f} s')
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
            self.df_out = sim.simulate(
                self.df_in.select_daterange(
                    self.ui.start_date.dateTime().toString(),
                    self.ui.end_date.dateTime().toString()
                ),
                get_algorithm_config(),
                Load(load1),
                Load(load2),
                None if isinstance(self.df_in, df.DataFrameOut) and self.ui.use_data_bl.isChecked() else self.ui.base_load.value()
            )
        except Exception as ex:
            print(f"[{type(ex).__name__}] {ex} \n\n {traceback.format_exc()}")
            QMessageBox.warning(self, "Error", f"Date & Time interval must be at least 5 min", QMessageBox.Ok)
            return 1
        return 0
    
    def print_sim_duration(self):
        self.ui.n_samples.setText(f'Simulating {self.df_out.nsec/3600:.3f} h ({self.df_out.nsamples} Samples)')
    #endregion

    #region -> Show results
    def show_results(self, df:pd.DataFrame): 
        columns = list(OCT.keys())
        header = ['energyT', 'energyDT']
        columns = [col for col in columns if 'energy' in col and col not in header]
        self.ui.table_eb_t.setModel( QPandasModelTranslate(self.results.df_total[columns].T, i=1, use_unit=header) )
        self.ui.table_t.setModel( QPandasModelTranslate(self.results.df_results, use_unit=True) )
        self.ui.table_s.setModel( QPandasModelTranslate(df) )
        self.ui.table_eb.setModel( QPandasModelTranslate(self.results.df_hour, i=1) )

        # Remove wierd under space
        if self.first_table_show:
            self.first_table_show = False
            QTable_fit_items_heigh(self.ui.table_eb_t)
            QTable_fit_items_heigh(self.ui.table_t)

        # Ensure datetime is shown fully
        for name in ['table_eb', 'table_s', 'table_in']:
            table = self.ui.findChild(QTableView, name)
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            
        t0 = time()
        self.plot_general(df)
        self.plot_eb()
        self.plot_t()
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')

        # Checkboxes enable
        for c in self.ui.findChildren(QCheckBox): 
            c.setEnabled(True)
        
        self.ui.sim_line_style.setEnabled(True)
    
    def show_optimitzation_results(self):
        self.ui.table_op.setModel( QPandasModelTranslate(self.optimize.df, i=1, use_unit=True) )
        t0 = time()
        self.plot_op()
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')
    #endregion

    #region -> Plots
    def plot_in_data(self):
        plot = self.ui.plot_dr
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()
        df = self.df_in.df

        # Plot Data
        self.data_lines = df_plot_col(df, 'timestamp', 'powerG', ax1)
        if 'powerLB' in self.df_in.df.columns:
            self.data_lines += df_plot_col(df, 'timestamp', 'powerLB', ax2)

        # Plot start & end
        self.date_range_lines = [
            mw.QMplMovableHVLine(
                ax1.axvline(self.ui.start_date.dateTime().toPython(), color=COLOR_SD, linestyle=':', label='Start Date'), 
                mw.QMplHVLineType.vline,
                plot.fig
            ),
            mw.QMplMovableHVLine(
                ax1.axvline(self.ui.end_date.dateTime().toPython(), color=COLOR_ED, linestyle=':', label='End Date') , 
                mw.QMplHVLineType.vline,
                plot.fig
            )
        ]
        self.date_range_lines[0].dataChanged.connect(self.start_date_line_changed)
        self.date_range_lines[1].dataChanged.connect(self.end_date_line_changed)

        # Visuals
        ax1.grid(True, linestyle=':')
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")
        ax1.set_xlabel('Date & Time')
        ax1.set_ylabel('Power [W]')
        ax2.set_ylabel('Power [W]')
        ax1.set_title('Data Range/In')
        plot.fig.autofmt_xdate()
        plot.home_view()
        plot.toggable_legend_lines()
        self.data_line_style(self.ui.data_line_style.text())

    def plot_general(self, df:pd.DataFrame):
        if df is None:
            return

        t0 = time()
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
                self.th_lines.append( ax2.axhline(self.tl_eq, color=COLOR_GR) )
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
        plot.toggable_legend_lines()
        plot.home_view()
        self.sim_line_style(self.ui.sim_line_style.text())
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')

    def plot_eb(self):
        if self.results is not None:
            showV = self.ui.show_values_eb.isChecked()
            showD = self.ui.subdivide_eb.isChecked()
            showCM = self.ui.show_ecm_eb.isChecked()
            self.plot_bars(self.results.df_hour, self.ui.plot_eb, showV, showD, showCM)

    def plot_t(self):
        if self.results is not None:
            data = self.results.df_total
            data['timestamp'] = self.results.df_hour.iloc[-1]['timestamp']
            showV = self.ui.show_values_t.isChecked()
            showD = self.ui.subdivide_t.isChecked()
            showCM = self.ui.show_ecm_t.isChecked()
            self.plot_bars(data, self.ui.plot_eb_t, showV, showD, showCM, None, 'horizontal', False)

    def plot_bars(self, data, plot, showV, showD, showCM, gaxis='both', lrot='vertical', xtimestamp = True):
        if data is None:
            return

        t0 = time()
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
        # Energy consume max
        barsCM = ['energyCM']
        labelsCM = [OCT[col]['translate'][1] for col in barsCM]
        colorsCM = [OCT[col]['color'] for col in barsCM]
        # All
        bars_ = barsL + barsSY + barsGSL

        # Plot types
        data.plot.bar(y=bars, ax=ax, color=colors, label=labels, width=0.60)
        pre_xlim = ax.get_xlim()
        width = ax.patches[0].get_width()

        # Plot Divisions
        if showD:
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

        if showCM:
            data.plot.bar(y=barsCM, ax=ax, color="none", edgecolor=colorsCM, label=labelsCM, stacked=True, position=1.5, width=width)

        # Add value labels
        if showV:
            containers = ax.containers
            for i, name in enumerate(bars):
                label = [f'{p:.0f}' for p in data[name]]
                ax.bar_label(containers[i], labels=label, rotation=lrot, color=colors[i], fontsize=8, padding=4)
            off = i+1
            if showD:
                for i, names in enumerate(bars_):
                    label = [f'{p:.0f}' if p>0 else '' for p in data[names]]
                    ax.bar_label(containers[i+off], labels=label, rotation=lrot, fontsize=8, color='#1e1e1e', label_type='center')
                off +=i+1
            if showCM:
                label = [f'{p:.0f}' for p in data[barsCM[0]]]
                ax.bar_label(containers[off], labels=label, rotation=lrot, color=colorsCM[0], fontsize=8, padding=4)
        
        # Visuals
        ax.margins(y=0.1)
        ax.legend(loc="upper right")
        ax.set_ylabel('Energy [Wh]')
        ax.set_title('Energy Balance')
        if gaxis != None:
            ax.set_axisbelow(True)
            ax.grid(True, linestyle=':', axis=gaxis)
        if xtimestamp:
            ax.set_xlabel('Date & Time')
            ax.set_xticklabels([x.strftime("%m-%d %H") for x in data['timestamp']], rotation=45)
            plot.fig.autofmt_xdate()
        else:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            plot.ax_xlimit= (-0.38, 1.75)
        plot.home_view()
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')
    
    def plot_op(self):
        if self.optimize is None:
            return

        t0 = time()
        plot = self.ui.plot_op
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()

        # Init
        df = self.optimize.df
        x = self.ui.op_setting.currentText()
        if (y1 := self.ui.op_ax_left.currentText()) != 'None':
            name = y1.split('[')[0]
            ax1.plot(df[x], df[y1], color='#2176db', label=name, marker='o')
            ax1.set_ylabel(y1)
            ax1.legend(loc="upper left")
        if (y2 := self.ui.op_ax_right.currentText()) != 'None':
            name = y2.split('[')[0]
            ax2.plot(df[x], df[y2], color='#f8a62a', label=name, marker='o')
            ax2.set_ylabel(y2)
            ax2.legend(loc="upper right")
        ax1.set_xlabel(x)
        ax1.grid(True, linestyle=':')
        plot.home_view()
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')
    #endregion
  
    #region -> Simulation Plot Options
    def toggle_loads_area(self, val):
        if self.sim_areas: # List Not emptyj
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
        if self.df_out is not None:
            self.plot_general(self.df_out.df)

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
    def start_date_changed(self, _):
        if self.date_range_lines:
            self.date_range_lines[0].set_xydata(self.ui.start_date.dateTime().toPython(), 0)
            self.ui.plot_dr.draw_idle()

    def end_date_changed(self, _):
            self.date_range_lines[1].set_xydata(self.ui.end_date.dateTime().toPython(), 0)
            self.ui.plot_dr.draw_idle()

    def start_date_line_changed(self, date, _):
        self.ui.start_date.setDateTime(mp.dates.num2date(date))

    def end_date_line_changed(self, date, _):
        self.ui.end_date.setDateTime(mp.dates.num2date(date))
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
    sys_argv = sys.argv
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())
