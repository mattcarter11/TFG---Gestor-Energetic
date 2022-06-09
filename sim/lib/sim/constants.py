UI_FILE = "mainwindow.ui"
DT_FORMAT = 'yyyy-MM-dd HH:mm'
COLOR_GR = '#a5a5a5'
COLOR_SD = '#0cb7e8'
COLOR_ED = '#8e09d5'
COLOR_G1 = '#6dbf31'

COLOR_LB = '#e7d6a9'
COLOR_L1 = '#fdc26c'
COLOR_L2 = '#ffd463'

# ordered key: (color, unit, translate)
OCT = {
    'timestamp' :{"color":None,         "unit":'',     "translate": ('Timestamp', 'Timestamp')},

    'powerG'    :{"color":'#33ab1d',    "unit":'W',     "translate": ('Power Generated', 'Generated')}, 
    'powerC'    :{"color":'#f8a62a',    "unit":'W',     "translate": ('Power Consumed', 'Consumed')}, 
    'powerLB'   :{"color":COLOR_LB,     "unit":'W',     "translate": ('Power Base Load', 'Base Load')},
    'powerL1'   :{"color":COLOR_L1,     "unit":'W',     "translate": ('Power Load 1', 'Load 1')},
    'powerL2'   :{"color":COLOR_L2,     "unit":'W',     "translate": ('Power Load 2', 'Load 2')},

    'on_offL1'  :{"color":COLOR_L1,     "unit":'',      "translate": ('On/Off Load 1', 'On/Off L1')}, 
    'on_offL2'  :{"color":COLOR_L2,     "unit":'',      "translate": ('On/Off Load 2', 'On/Off L2')}, 

    'energySY'  :{"color":'#195aa7',    "unit":'Wh',    "translate": ('Energy System', 'System')}, 
    'energyP'   :{"color":'#2176db',    "unit":'Wh',    "translate": ('Energy Produced', 'Produced')}, 
    'energyG'   :{"color":'#ef8271',    "unit":'Wh',    "translate": ('Energy Grid', 'Grid')}, 
    'energyA'   :{"color":'#60b0ff',    "unit":'Wh',    "translate": ('Energy Available', 'Available')}, 
    'energyC'   :{"color":'#f8a62a',    "unit":'Wh',    "translate": ('Energy Consumed', 'Consumed')}, 
    'energyLB'  :{"color":'#e7d6a9',    "unit":'Wh',    "translate": ('Energy Base Load', 'Base Load')}, 
    'energyL1'  :{"color":COLOR_L1,     "unit":'Wh',    "translate": ('Energy Load 1', 'Load 1')}, 
    'energyL2'  :{"color":COLOR_L2,     "unit":'Wh',    "translate": ('Energy Load 2', 'Load 2')},
    'energyCM'  :{"color":'#7e7e7e',    "unit":'Wh',    "translate": ('Energy Consumed Max', 'Cons. Max')}, 
    'energyS'   :{"color":'#6dbf31',    "unit":'Wh',    "translate": ('Energy Surplus', 'Surplus')},
    'energyL'   :{"color":'#e15f4b',    "unit":'Wh',    "translate": ('Energy Lost', 'Lost')}, 

    'energyT'   :{"color":None,         "unit":'Wh',    "translate": ('Total Energy', 'Total')},
    'energyDT'  :{"color":None,         "unit":'Wh/day',"translate": ('Daily Total', 'Daily Total')},

    'loadApprox':{"color":None,         "unit":'W',     "translate": ('Aprox. Load', 'Aprox. Load')},
    'efficiency':{"color":'#6dbf31',    "unit":'%',     "translate": ('Efficiency', 'Efficiency')},
    'balance'   :{"color":'#60b0ff',    "unit":'cént.', "translate": ('Balance', 'Balance')},
    'commut'    :{"color":None,         "unit":'',      "translate": ('Commutations', 'Commut.')},
    'commutD'   :{"color":None,         "unit":'',      "translate": ('Daily Commutations', 'Daily Commut.')},
    'samplesOn' :{"color":None,         "unit":'',      "translate": ('Samples On', 'Samples On')},
    'hoursOn'   :{"color":None,         "unit":'h',     "translate": ('Hours On', 'Hours On')},
    'hoursOnD'  :{"color":None,         "unit":'h/day', "translate": ('Daily Hours On', 'Daily Hours On')},

    'loadB'     :{"color":COLOR_LB,     "unit":'',      "translate": ('Base Load', 'Base Load')},
    'load1'     :{"color":COLOR_L1,     "unit":'',      "translate": ('Load 1', 'Load 1')},
    'load2'     :{"color":COLOR_L2,     "unit":'',      "translate": ('Load 2', 'Load 2')},
    'total'     :{"color":None,         "unit":'',      "translate": ('Total', 'Total')},
    'none'      :{"color":None,         "unit":'',      "translate": ('None', 'None')},
}

def oct_color(key):
    return OCT[key]['color']

def oct_translate(key:str, i:int=0, use_unit:bool=False):
    trans = OCT[key]['translate'][i]
    unit = OCT[key]["unit"]
    if use_unit and unit != '':
        return f'{trans} [{unit}]'
    return trans



SettingsQDateTimeEdits = ('start_date', 'end_date')
SettingsQComboBoxes = ('algorithm', 'predict_final_energy', 'op_setting', 'op_ax_right', 'op_ax_left')
SettingsQSpinBoxes = ('th_top1', 'th_top2', 'th_bottom1', 'th_bottom2', 'time_limit', 'base_load', 'load1', 'load2', 'op_start', 'op_end', 'op_step', 'ttc_end_at', 'ttc_on_min')
SettingsQDoubleSpinBox = ['ttc_time_factor', 'sell_price']
SettingsQCheckBoxes = ('use_data_bl', 'show_loads_area', 'show_th', 'energyP_s', 'show_values_eb', 'show_ecm_eb', 'subdivide_eb', 'show_values_eff', 'show_values_balance', 'show_values_t', 'show_ecm_t', 'subdivide_t')
SettingsQLineEdits = ('data_line_style', 'sim_line_style')

OpAxDict = {
    'None'                      :{'row':'none',     'column':'none',      'table':None}, 
    'Efficiency [%]'            :{'row':'total',    'column':'efficiency',  'table':'results'}, 
    'Balance [cént.]'           :{'row':'total',    'column':'balance',     'table':'results'}, 
    'Daily Commutations'        :{'row':'total',    'column':'commutD',     'table':'results'}, 
    'Daily Commutations Load 1' :{'row':'load1',    'column':'commutD',     'table':'results'}, 
    'Daily Commutations Load 2' :{'row':'load2',    'column':'commutD',     'table':'results'}, 
    'Daily Hours On Load 1'     :{'row':'load1',    'column':'hoursOnD',    'table':'results'}, 
    'Daily Hours On Load 2'     :{'row':'load2',    'column':'hoursOnD',    'table':'results'}, 
    'Energy Grid [Wh]'          :{'row':'energyDT', 'column':'energyG',    'table':'total'}
}

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