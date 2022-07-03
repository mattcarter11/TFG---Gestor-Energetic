import warnings
from pandas import DataFrame
from ..myQT.QMplWidgets import QMplPlot
from .constants import oct_color, oct_translate

warnings.filterwarnings("ignore", category=UserWarning)

if True:
    # System view
    barsS0  = [['energyC'], ['energySY'], ['energyPL']]
    barsS0_ = [col for grup in barsS0 for col in grup]
    labelsS0 = [oct_translate(col, 1) for col in barsS0_]
    colorsS0 = [oct_color(col) for col in barsS0_]
    # Subdivide 1
    barsS1   = [['energyLB', 'energyL1', 'energyL2'], ['energyG', 'energyP'], ['energyGR', 'energyAB']]
    labelsS1 = [[oct_translate(col, 1) for col in grup] for grup in barsS1 ]
    colorsS1 = [[oct_color(col) for col in grup] for grup in barsS1]
    # Subdivide 2
    barsS2   = [[], ['energyGP', 'energyGnP', 'energyPC','energyPL'], ['energyGR', 'energyL', 'energyS']]
    labelsS2 = [[oct_translate(col, 1) for col in grup] for grup in barsS2]
    colorsS2 = [[oct_color(col) for col in grup] for grup in barsS2]
    # Energy consume max
    barsCM   = ['energyCM']
    labelsCM = [oct_translate(col, 1) for col in barsCM]
    colorsCM = [oct_color(col) for col in barsCM]

def flatten(x):
    result = []
    for el in x:
        if isinstance(el, list):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

class BarPlotController:

    def __init__(self):
        self.plotted = False
        self.showV = False
        self.showD = False
        self.showCM = False
        self.glabels = None # Base, Divide 1, Divide 2, CM
        self.gbars = None
        self.ghandlab = None

    def new_plot(self, data:DataFrame, plot:QMplPlot, showV:bool=True, showD:int=0, showCM:bool=True, gaxis:str='both', lrot:str='vertical', xtime:bool=True, decimas:int=0):
        self.data = data
        self.plot = plot
        self.showV = showV
        self.showD = showD
        self.showCM = showCM
        self.plot = plot
        self.gaxis = gaxis
        self.lrot = lrot
        self.xtime = xtime
        self.decimas = decimas
        self._plot_bars()
        self._set_show_values(showV)
        self._set_subdivide(showD)
        self._set_show_cm(showCM)
        self._set_legend()
        self.plot.draw_idle()

    def _plot_bars(self):
        columns = self.data.columns[1:].values
        colors = [oct_color(col) for col in columns]
        labels = [oct_translate(col) for col in columns]
        ax = self.plot.ax
        self.plot.clear()
        
        # Plot types
        self.data.plot.bar(y=columns, ax=ax, color=colors, label=labels, width=0.60)

        # Add Labels + Separate containers
        containers = ax.containers
        self.glabels= [[[]], [[]], [[]], []]
        for i, col in enumerate(columns):
            labels = [f'{p:.{self.decimas}f}' for p in self.data[col]]
            self.glabels[0][0].extend( ax.bar_label(containers[i], labels=labels, rotation=self.lrot, fontsize=8, padding=4, label_type='center') )

        # Visuals
        ax.margins(y=0.1)
        ax.legend(loc="upper right")
        if len(columns) == 1:
            ylabel = oct_translate(columns[0], 0, True)
        else:
            ylabel = 'Efficiency [%]'
        ax.set_ylabel(ylabel)
        self._xformat()
        self._plot_grid()
        self.plot.home_view()
        self.plotted = True

    def set_show_values(self, val:bool):
        if self.plotted and val != self.showV:
            self.showV = val
            self._set_show_values(val)
            self.plot.draw_idle()

    def set_subdivide(self, val:bool):
        if self.plotted and val != self.showD:
            self.showD = val
            self._set_subdivide(self.showD)
            self._set_show_values(self.showV)
            self._set_legend()
            self.plot.draw_idle()

    def set_show_cm(self, val:bool):
        if self.plotted and val != self.showCM:
            self.showCM = val
            self._set_show_cm(self.showCM)
            self._set_show_values(self.showV)
            self._set_legend()
            self.plot.draw_idle()

    def _set_show_values(self, val:bool):
        if self.glabels is not None:
            for label in list(flatten(self.glabels)):
                label.set_visible(False)
            if val:
                for glabels in self.glabels[self.showD]:
                    for label in glabels:
                        label.set_visible(True)
                for label in self.glabels[3]:
                    label.set_visible(self.showCM)
            self.showV = val

    def _set_subdivide(self, val:bool):
        if self.gbars is not None:
            # Hide all
            for sublevel in self.gbars[:-1]:
                for gbars in sublevel:
                    for bar in gbars:
                        self.plot.set_visible(bar, False)
            # Show specific
            for gbars in self.gbars[val]:
                    for bar in gbars:
                        self.plot.set_visible(bar, True)

    def _set_show_cm(self, val:bool):
        if self.gbars is not None:
            for bar in self.gbars[3]:
                self.plot.set_visible(bar, val)

    def _set_legend(self):
        if self.ghandlab is not None:
            handles, labels = self.plot.ax.get_legend_handles_labels()
            # Hide all labels
            for i, label in enumerate(labels):
                labels[i] = f'_{label}'
            # Show only active
            for ghandlab in self.ghandlab[self.showD]:
                for handler, label in ghandlab:
                    i = handles.index(handler)
                    labels[i] = label
            if self.showCM:
                for ghandlab in self.ghandlab[3]:
                    for handler, label in ghandlab:
                        i = handles.index(handler)
                        labels[i] = label

            self.plot.ax.legend(handles, labels, loc="upper right")

    def _plot_grid(self):
        if self.gaxis != None:
            self.plot.ax.set_axisbelow(True)
            self.plot.ax.grid(True, linestyle=':', axis=self.gaxis)

    def _xformat(self):
        ax = self.plot.ax
        if self.xtime:
            ax.set_xlabel('Hour Zone [h]')
            ax.set_xticklabels([x.strftime("%m-%d %H") for x in self.data['timestamp']], rotation=45)
            self.plot.fig.autofmt_xdate()
        else:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            self.plot.ax_xlimit= (-0.38, 1.75)

class EBPlotController(BarPlotController):

    def _plot_bars(self):
        if not self.xtime:
            self.data.index = [
                oct_translate(self.data.index.values[0], 0, True), 
                oct_translate(self.data.index.values[1], 0, True)
            ]

        ax = self.plot.ax
        self.plot.clear()
        
        # Plot System view
        width = 0.2
        self.data.plot.bar(y=barsS0_, ax=ax, color=colorsS0, label=labelsS0, width=width*3)
        pre_xlim = ax.get_xlim()
    
        # Plot Load Subtypes
        for i in range(len(barsS0_)):
            if barsS1[i] != []:
                self.data.plot.bar(y=barsS1[i], ax=ax, color=colorsS1[i], label=labelsS1[i], stacked=True, position=1.5-1*i, width=width)
        for i in range(len(barsS0_)):
            if barsS2[i] != []:
                self.data.plot.bar(y=barsS2[i], ax=ax, color=colorsS2[i], label=labelsS2[i], stacked=True, position=1.5-1*i, width=width)
        ax.set_xlim(pre_xlim)

        # Plot energy Consum
        self.data.plot.bar(y=barsCM, ax=ax, color="none", edgecolor=colorsCM, label=labelsCM, stacked=True, position=1.5, width=width)

        # Add Labels + Separate containers
        containers = ax.containers
        self.glabels = [[], [], [], []]
        self.gbars = [[], [], [], []]
        off = 0
        # Labels System, Subdivide 1 & 2
        for j, barsX in enumerate([ barsS0, barsS1, barsS2 ]):
            for p, bars in enumerate(barsX):
                if bars == []: # No divisions, use previous labels
                    self.glabels[j].append(self.glabels[j-1][p])
                    self.gbars[j].append(self.gbars[j-1][p])
                    off += len(bars)
                else:
                    self.glabels[j].append([])
                    self.gbars[j].append([])
                    for i, name in enumerate(bars):
                        labels = [f'{p:.0f}' for p in self.data[name]]
                        self.glabels[j][p].extend(ax.bar_label(containers[i+off], labels=labels, rotation=self.lrot, fontsize=8, label_type='center') )
                        self.gbars[j][p].extend(containers[i+off])
                    off += i+1
        # Labels Energy ConsumeMax
        labels = [f'{p:.0f}' for p in self.data[barsCM[0]]]
        self.glabels[j+1].extend( ax.bar_label(containers[off], labels=labels, rotation=self.lrot, fontsize=8, padding=4) )
        self.gbars[j+1].extend(containers[off])

        # Visuals
        ax.margins(y=0.1)
        ax.legend()
        ax.set_ylabel('Energy [Wh]')
        self._xformat()
        self._plot_grid()
        self.plot.home_view()
        self.plotted = True

        # Legend handles
        h, l = self.plot.ax.get_legend_handles_labels()
        self.ghandlab = [[], [], [], []]
        off = 0
        for j, barsX in enumerate([ barsS0, barsS1, barsS2 ]):
            for p, bars in enumerate(barsX):
                if bars == []: # No divisions, use previous handles
                    self.ghandlab[j].append(self.ghandlab[j-1][p])
                else:
                    self.ghandlab[j].append([])
                    for i in range(len(bars)):
                        self.ghandlab[j][p].append((h[i+off], l[i+off]))
                    off += i+1
        self.ghandlab[j+1].append([(h[off], l[off])])