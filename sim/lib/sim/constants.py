UI_FILE = "mainwindow.ui"
HELP_FILE = "Simulator Manual.html"
DT_FORMAT = 'yyyy-MM-dd HH:mm'

# Generci colors
GRAY0    = '#cacaca'
GRAY1    = '#a5a5a5'
GRAY2    = '#7e7e7e'
GREEN1   = '#6dbf31'

# Date time selector colors
COLOR_SD = '#60b0ff'
COLOR_ED = '#9865c6'

# === Translation ===
# Used to get the color, unit, and text of each pandas colum (OCT = color, unit, translate)
OCT = {
    'timestamp' :{"color":None,         "unit":'',     "translate": ('Timestamp', 'Timestamp')},

    'powerP'    :{"color":'#33ab1d',    "unit":'W',     "translate": ('Power Produced', 'Produced')}, 
    'powerC'    :{"color":'#f8a62a',    "unit":'W',     "translate": ('Power Consumed', 'Consumed')},
    'powerG'    :{"color":'#dc604d',    "unit":'W',     "translate": ('Power Grid', 'Grid')},
    'powerGP'   :{"color":'#d03429',    "unit":'W',     "translate": ('Power Grid while Prod.', 'Grid while Prod.')},
    'powerA'    :{"color":'#4b90f3',    "unit":'W',     "translate": ('Power Available', 'Available')},
    'powerLB'   :{"color":'#e7d6a9',    "unit":'W',     "translate": ('Power Base Load', 'Base Load')},
    'powerL1'   :{"color":'#fdc26c',    "unit":'W',     "translate": ('Power Load 1', 'Load 1')},
    'powerL2'   :{"color":'#ffd463',    "unit":'W',     "translate": ('Power Load 2', 'Load 2')},
    'powerCM'   :{"color":GRAY2,        "unit":'W',     "translate": ('Power Max. Consuption', 'Max. Cons.')},


    'on_offL1'  :{"color":'#fdc26c',    "unit":'',      "translate": ('On/Off Load 1', 'On/Off L1')}, 
    'on_offL2'  :{"color":'#ffd463',    "unit":'',      "translate": ('On/Off Load 2', 'On/Off L2')}, 

    'energySY'  :{"color":'#195aa7',    "unit":'Wh',    "translate": ('Energy System', 'System')}, 
    'energyP'   :{"color":'#2176db',    "unit":'Wh',    "translate": ('Energy Produced', 'Produced')}, 
    'energyPC'  :{"color":'#2176db',    "unit":'Wh',    "translate": ('Energy Produced Consumed', 'Prod Cons')},
    'energyPL'  :{"color":'#60b0ff',    "unit":'Wh',    "translate": ('Energy Produced Left', 'Prod. Left')}, 
    'energyG'   :{"color":'#dc604d',    "unit":'Wh',    "translate": ('Energy Grid', 'Grid')}, 
    'energyGP'  :{"color":'#d03429',    "unit":'Wh',    "translate": ('Energy Grid while Prod.', 'Grid w Prod.')},
    'energyGnP' :{"color":GRAY1,        "unit":'Wh',    "translate": ('Energy Grid while not Prod.', 'Grid w not Prod.')},
    'energyC'   :{"color":'#f8a62a',    "unit":'Wh',    "translate": ('Energy Consumed', 'Consumed')}, 
    'energyLB'  :{"color":'#e7d6a9',    "unit":'Wh',    "translate": ('Energy Base Load', 'Base Load')}, 
    'energyL1'  :{"color":'#fdc26c',    "unit":'Wh',    "translate": ('Energy Load 1', 'Load 1')}, 
    'energyL2'  :{"color":'#ffd463',    "unit":'Wh',    "translate": ('Energy Load 2', 'Load 2')},
    'energyCM'  :{"color":GRAY2,        "unit":'Wh',    "translate": ('Energy Max. Consuption', 'Max. Cons.')}, 
    'energyB'   :{"color":GRAY2,        "unit":'Wh',    "translate": ('Energy Balance', 'Balance')}, 
    'energyGD'  :{"color":'#ef8271',    "unit":'Wh',    "translate": ('Energy Grid Debt', 'Grid Debt')},
    'energyAB'  :{"color":'#60b0ff',    "unit":'Wh',    "translate": ('Energy Available Balance', 'Available Bal.')}, 
    'energyS'   :{"color":'#7ad92b',    "unit":'Wh',    "translate": ('Energy Surplus', 'Surplus')},
    'energyL'   :{"color":'#f98e7e',    "unit":'Wh',    "translate": ('Energy Lost', 'Lost')},
    'energyGR'  :{"color":'#9865c6',    "unit":'Wh',    "translate": ('Energy Returned to Grid', 'Returned to Grid')},


    'energyT'   :{"color":None,         "unit":'Wh',    "translate": ('Total Energy', 'Total')},
    'energyDT'  :{"color":None,         "unit":'Wh/day',"translate": ('Daily Total', 'Daily Total')},

    'loadApprox':{"color":None,         "unit":'W',     "translate": ('Approx. Load', 'Aprox. Load')},
    'efficC'    :{"color":GREEN1,       "unit":'%',     "translate": ('Cons. Efficiency', 'Cons. Effic.')},
    'efficGR'   :{"color":'#ef8271',    "unit":'%',     "translate": ('Grid Ret. Efficiency', 'Grid Ret. Effic.')},
    'balance'   :{"color":'#60b0ff',    "unit":'c??nt.', "translate": ('Balance', 'Balance')},
    'commut'    :{"color":None,         "unit":'',      "translate": ('Commutations', 'Commut.')},
    'commutD'   :{"color":None,         "unit":'',      "translate": ('Daily Commutations', 'Daily Commut.')},
    'samplesOn' :{"color":None,         "unit":'',      "translate": ('Samples On', 'Samples On')},
    'hoursOn'   :{"color":None,         "unit":'h',     "translate": ('Hours On', 'Hours On')},
    'hoursOnD'  :{"color":None,         "unit":'h/day', "translate": ('Daily Hours On', 'Daily Hours On')},

    'loadB'     :{"color":None,         "unit":'',      "translate": ('Base Load', 'Base Load')},
    'load1'     :{"color":None,         "unit":'',      "translate": ('Load 1', 'Load 1')},
    'load2'     :{"color":None,         "unit":'',      "translate": ('Load 2', 'Load 2')},
    'total'     :{"color":None,         "unit":'',      "translate": ('Total', 'Total')},
    'none'      :{"color":None,         "unit":'',      "translate": ('None', 'None')},
}

COL_ORDER = list(OCT.keys())

def oct_color(key):
    return OCT[key]['color']

def oct_translate(key:str, i:int=0, use_unit:bool=False):
    trans = OCT[key]['translate'][i]
    unit = OCT[key]["unit"]
    if use_unit and unit != '':
        return f'{trans} [{unit}]'
    return trans

# === Load & Save ===
# Used for loading and saving the GUI settings
SettingsQDateTimeEdits = ('start_date', 'end_date')
SettingsQComboBoxes = ('algorithm', 'predict_final_energy', 'subdivide_eb', 'subdivide_t', 'op_setting', 'op_ax_right', 'op_ax_left', 'show_max_cons', 'mot_mode')
SettingsQSpinBoxes = ('th_top1', 'th_top2', 'th_bottom1', 'th_bottom2', 'time_limit', 'base_load', 'load1', 'load2', 'ttc_end_at', 'ttc_on_min')
SettingsQDoubleSpinBox = [ 'op_start', 'op_end', 'op_step', 'ttc_time_factor', 'sell_price', 'generation_factor']
SettingsQCheckBoxes = ('use_data_bl', 'show_loads_area', 'show_th', 'energyP_s', 'show_values_eb', 'show_ecm_eb', 'show_values_effC', 'show_values_effGR', 'show_values_balance', 'show_values_commut', 'show_values_t', 'show_ecm_t')
SettingsQLineEdits = ('data_line_style', 'sim_line_style')

# === Options Options ===
# Possible axes of the optimitation plot
OpAxDict = {
    'None'                      :{'row':'none',     'column':'none',        'table':None}, 
    'Cons. Max. Efficiency [%]' :{'row':'total',    'column':'efficC',      'table':'results'}, 
    'Grid Ret. Efficiency [%]'  :{'row':'total',    'column':'efficGR',     'table':'results'}, 
    'Balance [c??nt.]'           :{'row':'total',    'column':'balance',     'table':'results'}, 
    'Daily Commutations'        :{'row':'total',    'column':'commutD',     'table':'results'}, 
    'Daily Commut. Load 1'      :{'row':'load1',    'column':'commutD',     'table':'results'}, 
    'Daily Commut. Load 2'      :{'row':'load2',    'column':'commutD',     'table':'results'}, 
    'Daily Hours On Load 1'     :{'row':'load1',    'column':'hoursOnD',    'table':'results'}, 
    'Daily Hours On Load 2'     :{'row':'load2',    'column':'hoursOnD',    'table':'results'}, 
    'Energy Grid [Wh]'          :{'row':'energyDT', 'column':'energyG',     'table':'total'},
    'Energy Grid Debt [Wh]'     :{'row':'energyDT', 'column':'energyGD',    'table':'total'},
    'Energy Avail. Bal. [Wh]'   :{'row':'energyDT', 'column':'energyAB',    'table':'total'},
    'Energy Lost [Wh]'          :{'row':'energyDT', 'column':'energyL',     'table':'total'},
}

# Possible  options to optimize
OpAlgorithm = {
    'None': {},
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