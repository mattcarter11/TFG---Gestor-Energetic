import sys, json, traceback
from time import time
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QDateTime, QCoreApplication, Qt, QModelIndex
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView, QCheckBox, QTableView, QDateTimeEdit, QSpinBox, QDoubleSpinBox, QComboBox, QLineEdit
import pandas as pd
import matplotlib as mp
import numpy as np
import datetime as dt
from lib.sim.Load import Load
from lib.sim.Results import Results
from lib.sim.Optimize import Optimize   
import lib.sim.PlotController as pc 
import lib.sim.Simulator as sim
import lib.sim.AlgorithmsConfig as ac
import lib.sim.DataFrames as df
import lib.myQT.QMplWidgets as mw
import lib.myQT.QPandasWidgets as pw
from lib.sim.constants import *

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
            if title in COL_ORDER:
                use_unit = self.use_unit == True or (isinstance(self.use_unit, list) and title in self.use_unit)
                return oct_translate(title, self.i, use_unit)
        
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
        self.th_lines = self.sim_load_areas = self.sim_lines = self.data_lines = self.date_range_lines = []
        self.results = self.optimize = self.df_out = self.max_load_line = None
        self.eb_plotC = pc.EBPlotController()
        self.ebt_plotC = pc.EBPlotController()
        self.eff_plotC = pc.BarPlotController()
        self.bl_plotC = pc.BarPlotController()

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
        # Tables view style
        for table in self.ui.findChildren(QTableView):
            table.setHorizontalHeader(pw.WrapHeader(Qt.Horizontal))
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            table.horizontalHeader().setVisible(True)
        # Warning Optimize not resize on hiden
        pol = self.ui.op_recalc_warn.sizePolicy()
        pol.setRetainSizeWhenHidden(True)
        self.ui.op_recalc_warn.setSizePolicy(pol) 
        # List Optimze Axes values
        for key, _ in OpAxDict.items():
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
        self.ui.show_max_cons.currentIndexChanged.connect( self.toggle_max_cons)
        self.ui.energyP_s.stateChanged.connect( self.toggle_energyP)
        self.ui.show_th.stateChanged.connect( self.toggle_th)
        # Energy balance plot
        self.ui.show_values_eb.stateChanged.connect( self.eb_plotC.set_show_values)
        self.ui.show_ecm_eb.stateChanged.connect( self.eb_plotC.set_show_cm)
        self.ui.subdivide_eb.currentIndexChanged.connect( self.eb_plotC.set_subdivide)
        # Other plot
        self.ui.show_values_eff.stateChanged.connect( self.eff_plotC.set_show_values)
        self.ui.show_values_balance.stateChanged.connect( self.bl_plotC.set_show_values)
        # Summary balance plot
        self.ui.show_values_t.stateChanged.connect( self.ebt_plotC.set_show_values)
        self.ui.show_ecm_t.stateChanged.connect( self.ebt_plotC.set_show_cm)
        self.ui.subdivide_t.currentIndexChanged.connect( self.ebt_plotC.set_subdivide)
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
        path = QFileDialog.getOpenFileName(self, "Select Data", './db', '*.csv')[0]
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
        self.min_date = self.df_in.df['timestamp'].min()
        self.max_date = self.df_in.df['timestamp'].max()
        format = '%Y-%m-%d %H:%M:%S'
        self.ui.date_range.setText(f'Date Range: {self.min_date.strftime(format)} - {self.max_date.strftime(format)} ({self.df_in.nsamples} Samples)')
        self.ui.start_date.setMinimumDateTime(self.min_date)
        self.ui.end_date.setMinimumDateTime(self.min_date)
        self.ui.start_date.setMaximumDateTime(self.max_date)
        self.ui.end_date.setMaximumDateTime(self.max_date)
    
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
            ax.axhline(self.ui.sell_price.value(), color=GREEN1, linestyle='-', label='Sell Price'), 
            mw.QMplHVLineType.hline,
            plot.fig
        )
        self.sell_price_line.dataChanged.connect(self.sell_price_line_changed)

        ax.grid(True, linestyle=':')
        ax.legend(loc="upper left")
        ax.set_xlabel('Hour Zone [h]')
        ax.set_ylabel('Price [€/kWh]')
    
    def talbe_price(self, df:pd.DataFrame):
        self.price_model = pw.QPandasModelEdit(df, 3)
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
        self.ui.load1.setEnabled(i != 0)
        self.ui.load2.setEnabled(i != 0)
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
        df = self.df_in.select_daterange( self.ui.start_date.dateTime().toString(), self.ui.end_date.dateTime().toString(), 3600 )
        df.calc_powerAG()
        df.calc_powerCM()
        df.fill_missing_energy()
        df.rearange_cols()
        self.results = Results(df, self.df_price.iloc[:, 0], self.ui.sell_price.value())
        self.ui.calc_time.setText(f'Results calculated in {time()-t0:.3f} s')
        self.show_results(df)

    def simulate_press(self):
        t0 = time()
        err = self.simulate()
        t1 = time()
        if not err:
            self.results = Results(self.df_out, self.df_price.iloc[:, 0], self.ui.sell_price.value())
            self.ui.calc_time.setText(f'Simulated in {time()-t0:.3f} s. Results calculated in {time()-t1:.3f} s')
            self.print_sim_duration()
            self.show_results(self.df_out)          

    def optimize_press(self):
        t0 = time()
        self.optimize = Optimize(self.ui.op_setting.currentText(), OpAxDict)
        values = np.arange(self.ui.op_start.value(), self.ui.op_end.value()+self.ui.op_step.value(), self.ui.op_step.value()) 
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
            match alI:
                case 0:
                    return ac.AlgorithmConfig()
                case 1: 
                    th_top1     = value if value is not None and element == 'th_top1' else self.ui.th_top1.value()
                    th_bottom1  = value if value is not None and element == 'th_bottom1' else self.ui.th_bottom1.value()
                    th_top2     = value if value is not None and element == 'th_top2' else self.ui.th_top2.value()
                    th_bottom2  = value if value is not None and element == 'th_bottom2' else self.ui.th_bottom2.value()
                    th_bottom2  = value if value is not None and element == 'th_bottom2' else self.ui.th_bottom2.value()
                    return ac.HysteresisConfig(th_top1, th_bottom1, th_top2, th_bottom2)
                case 2: 
                    time_limit  = value if value is not None and element == 'time_limit' else self.ui.time_limit.value()
                    return ac.MinOnTimeConfig(time_limit)
                case 3:
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
        dfRG = self.df_in.select_daterange( self.ui.start_date.dateTime().toString(), self.ui.end_date.dateTime().toString(), 3600 )
        dfRG.df['powerP'] = dfRG.df['powerP'].values * self.ui.generation_factor.value()
        try:
            self.df_out = sim.simulate(
                dfRG,
                get_algorithm_config(),
                Load(load1),
                Load(load2),
                None if isinstance(self.df_in, df.DataFrameOut) and self.ui.use_data_bl.isChecked() else self.ui.base_load.value()
            )
        except Exception as ex:
            QMessageBox.warning(self, "Error", f"[{type(ex).__name__}] {ex} \n\n {traceback.format_exc()}", QMessageBox.Ok)
            return 1
        return 0
    
    def print_sim_duration(self):
        self.ui.n_samples.setText(f'Simulating {self.df_out.nsec/3600:.3f} h ({self.df_out.nsamples} Samples)')
    #endregion

    #region -> Show results
    def show_results(self, df:df.DataFrameOut): 
        header = ['energyT', 'energyDT']
        columns = [col for col in COL_ORDER if 'energy' in col and col not in header+['energyB']]
        self.ui.table_eb_t.setModel( QPandasModelTranslate(self.results.df_total[columns].T, i=1, use_unit=header) )
        self.ui.table_t.setModel( QPandasModelTranslate(self.results.df_results, use_unit=True) )
        self.ui.table_s.setModel( QPandasModelTranslate(df.df) )
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
        self.plot_sim(df)
        self.plot_eb()
        self.plot_other()
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
        plot: mw.QMplTwinxPlot = self.ui.plot_dr
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()
        df = self.df_in.df

        # Plot Data
        self.data_lines = df_plot_col(df, 'timestamp', 'powerP', ax1)
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
        plot.fig.autofmt_xdate()
        plot.home_view()
        plot.toggable_legend_lines()
        self.data_line_style(self.ui.data_line_style.text())

    def plot_sim(self, df:df.DataFrameOut):
        t0 = time()
        plot: mw.QMplTwinxPlot = self.ui.plot_s
        ax1, ax2 = plot.ax1, plot.ax2
        plot.clear()

        max_load = df.aproximate_max_load()
        df = df.df

        # Plot Power Lines
        self.sim_lines = []
        for col in ['powerC', 'powerP', 'powerA', 'powerG', 'powerCM']:
            self.sim_lines += df_plot_col(df, 'timestamp', col, ax1)

        # Power CM
        self.max_load_line = ax1.axhline(max_load, color=oct_color('powerCM'))
        self.sim_cm_area = df.plot.area('timestamp', ['powerCM'], ax=ax1, linewidth=0, color=[GRAY0], label=[oct_translate('powerCM')]).collections[0]

        # Power Load Areas
        cols = ['powerLB', 'powerL1', 'powerL2']
        labels = [oct_translate(col) for col in cols]
        colors = [oct_color(col) for col in cols]
        self.sim_load_areas = df.plot.area('timestamp', cols, ax=ax1, linewidth=0, color=colors, label=labels).collections[1:] # Ignore CM area

        # Add energy thresholds
        self.th_lines = []
        match self.ui.algorithm.currentIndex():
            case 1:
                if self.ui.load1.value() > 0:
                    self.th_lines.append( ax2.axhline(self.ui.th_top1.value(), color=GRAY1) )
                    self.th_lines.append( ax2.axhline(self.ui.th_bottom1.value(), color=GRAY1) )
                if self.ui.load2.value() > 0:
                    self.th_lines.append( ax2.axhline(self.ui.th_top2.value(), color=GRAY1) )
                    self.th_lines.append( ax2.axhline(self.ui.th_bottom2.value(), color=GRAY1) )
            case 2:
                self.th_lines.append( ax2.axhline(self.tl_eq, color=GRAY1) )
                self.th_lines.append( ax2.axhline(self.tl_eq*2, color=GRAY1) )
            case 3:
                self.th_lines.append( ax2.axhline(self.ui.ttc_end_at.value(), color=GRAY1) )
                self.th_lines.append( ax2.axhline(self.ui.ttc_on_min.value(), color=GRAY1) )
        self.toggle_th(self.ui.show_th.isChecked())

        # Energy
        if self.ui.energyP_s.isChecked():
            self.sim_lines += df_plot_col(df, 'timestamp', 'energyP', ax2)
        self.sim_lines += df_plot_col(df, 'timestamp', 'energyAB', ax2)
        self.sim_lines += df_plot_col(df, 'timestamp', 'energyGD', ax2)

        # Visuals
        ax1.grid(True, linestyle=':')
        ax2.legend(loc="upper right")
        ax1.legend(loc="upper left")
        for legline in ax1.get_legend().get_lines()[2:4]:
            plot._hide_legline(legline)
        
        ax1.set_xlabel('Date & Time')
        ax1.set_ylabel('Power [W]')
        ax2.set_ylabel('Energy Balance [Wh]')
        plot.fig.autofmt_xdate()
        plot.toggable_legend_lines()
        plot.align = True
        plot.ax_ylimit = (0, df['powerP'].max()*1.05)
        plot.home_view()
        self.toggle_loads_area(self.ui.show_loads_area.isChecked())
        self.toggle_max_cons(self.ui.show_max_cons.currentIndex())
        self.sim_line_style(self.ui.sim_line_style.text())
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')

    def plot_eb(self):
        if self.results is not None:
            showV = self.ui.show_values_eb.isChecked()
            showD = self.ui.subdivide_eb.currentIndex()
            showCM = self.ui.show_ecm_eb.isChecked()
            self.eb_plotC.new_plot(self.results.df_hour, self.ui.plot_eb, showV, showD, showCM)

    def plot_other(self):
        if self.results is not None:
            showV = self.ui.show_values_eff.isChecked()
            self.eff_plotC.new_plot(self.results.df_hour[['timestamp','efficCM']], self.ui.plot_eff, showV, lrot=None)
            showV = self.ui.show_values_balance.isChecked()
            self.bl_plotC.new_plot(self.results.df_hour[['timestamp','balance']], self.ui.plot_balance, showV, lrot=None)

    def plot_t(self):
        if self.results is not None:
            data = self.results.df_total
            data['timestamp'] = self.results.df_hour.iloc[-1]['timestamp']
            showV = self.ui.show_values_t.isChecked()
            showD = self.ui.subdivide_t.currentIndex()
            showCM = self.ui.show_ecm_t.isChecked()
            self.ebt_plotC.new_plot(data, self.ui.plot_eb_t, showV, showD, showCM, None, 'horizontal', False)

    def plot_op(self):
        if self.optimize is None:
            return

        t0 = time()
        plot: mw.QMplTwinxPlot = self.ui.plot_op
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
        ax1.ticklabel_format(useOffset=False)
        ax2.ticklabel_format(useOffset=False)
        plot.home_view()
        self.ui.plotting_time.setText(f'Plotted in {time()-t0:.3f} s')
    #endregion
  
    #region -> Simulation Plot Options
    def toggle_loads_area(self, val):
        if self.sim_load_areas: # List Not emptyj
            plot:mw.QMplPlot = self.ui.plot_s
            for area in self.sim_load_areas:
                plot.set_visible(area, val)
            plot.redraw_legend()
    
    def toggle_max_cons(self, i):
        if self.max_load_line is not None:
            plot:mw.QMplPlot = self.ui.plot_s
            self.max_load_line.set_linestyle(':' if i != 0 else 'None')
            plot.set_visible(self.sim_lines[4], i in (1, 3))
            plot.set_visible(self.sim_cm_area, i in (2, 3))
            plot.redraw_legend()

    def toggle_energyP(self):
        if self.df_out is not None:
            self.plot_sim(self.df_out)

    def toggle_th(self, val):
        if self.th_lines: # List Not empty
            style = ':' if val else 'None'
            for line in self.th_lines:
                line.set_linestyle(style)
            self.ui.plot_s.draw_idle()
    #endregion

    #region -> Date Range Plot Selection lines
    def start_date_changed(self, date):
        if self.date_range_lines:
            date = date.toPython()
            date_diff = date + dt.timedelta(hours=1)
            end_date = self.ui.end_date.dateTime().toPython()
            if date_diff > end_date:
                self.ui.end_date.setDateTime(date_diff)

            self.date_range_lines[0].set_xydata(date, 0)
            self.ui.plot_dr.draw_idle()

    def end_date_changed(self, date):
        if self.date_range_lines:
            date = date.toPython()
            date_diff = date - dt.timedelta(hours=1)
            start_date = self.ui.start_date.dateTime().toPython()
            if date_diff < start_date:
                self.ui.start_date.setDateTime(date_diff)

            self.date_range_lines[1].set_xydata(date, 0)
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
