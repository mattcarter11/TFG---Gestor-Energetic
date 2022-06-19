from abc import abstractclassmethod
import warnings
from pandas import DataFrame
from ..myQT.QMplWidgets import QMplPlot
from .constants import oct_color, oct_translate

warnings.filterwarnings("ignore", category=UserWarning)

if True:
    # Sum of each stacked type
    barsT = ['energyC', 'energySY', 'energyGR', 'energyAB']
    labelsT = [oct_translate(col, 1) for col in barsT]
    colorsT = [oct_color(col) for col in barsT]
    # Energy loads subtypes
    barsL = ['energyLB', 'energyL1', 'energyL2']
    labelsL = [oct_translate(col, 1) for col in barsL]
    colorsL = [oct_color(col) for col in barsL]
    # Energy system subtypes
    barsSY = ['energyG', 'energyP']
    labelsSY = [oct_translate(col, 1) for col in barsSY]
    colorsSY = [oct_color(col) for col in barsSY]
    # Energy left subtypes
    barsGSL = ['energyGR', 'energyL', 'energyS']
    labelsGSL = [oct_translate(col, 1) for col in barsGSL]
    colorsGSL = [oct_color(col) for col in barsGSL]
    # All
    barsD = barsL + barsSY + barsGSL
    labelsD = labelsL + labelsSY + labelsGSL
    # Energy consume max
    barsCM = ['energyCM']
    labelsCM = [oct_translate(col, 1) for col in barsCM]
    colorsCM = [oct_color(col) for col in barsCM]

class BarPlotController:

    def __init__(self):
        self.plotted = False
        self.showV = False
        self.showD = False
        self.showCM = False
        self.glabels = [[], [], []]
        self.gbars = [[], [], []]
        self.ghandlab = [[], [], []]

    def new_plot(self, data:DataFrame, plot:QMplPlot, showV:bool=True, showD:bool=True, showCM:bool=True, gaxis:str='both', lrot:str='vertical', xtime:bool=True):
        self.data = data
        self.plot = plot
        self.showV = showV
        self.showD = showD
        self.showCM = showCM
        self.plot = plot
        self.gaxis = gaxis
        self.lrot = lrot
        self.xtime = xtime
        self._plot_bars()
        self._set_show_values(showV)
        self._set_subdivide(showD)
        self._set_show_cm(showCM)
        self._set_legend()
        self.plot.draw_idle()

    @abstractclassmethod
    def _plot_bars(self):
        pass

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
        for label in self.glabels[0]:
            label.set_visible(val and not self.showD)
        for label in self.glabels[1]:
            label.set_visible(val and self.showD)
        for label in self.glabels[2]:
            label.set_visible(val and self.showCM)
        self.showV = val

    def _set_subdivide(self, val:bool):
        for bar in self.gbars[1]:
            bar.set_visible(val)
        for bar in self.gbars[0]:
            bar.set_visible(not val)

    def _set_show_cm(self, val:bool):
        for bar in self.gbars[2]:
            bar.set_visible(val)

    def _set_legend(self):
        val = [not self.showD, self.showD, self.showCM]
        handles, labels = self.plot.ax.get_legend_handles_labels()
        for j, ghandlab in enumerate(self.ghandlab):
            for handler, label in ghandlab:
                i = handles.index(handler)
                labels[i] = label if val[j] else f'_{label}'
        self.plot.ax.legend(handles, labels, loc="upper right")

class EBPlotController(BarPlotController):

    def _plot_bars(self):
        if not self.xtime:
            self.data.index = [
                oct_translate(self.data.index.values[0], 0, True), 
                oct_translate(self.data.index.values[1], 0, True)
            ]

        ax = self.plot.ax
        self.plot.clear()
        
        # Plot types
        width = 0.2
        self.data.plot.bar(y=barsT[:2], ax=ax, color=colorsT[:2], label=labelsT[:2], position=0.75, width=width*2)
        self.data.plot.bar(y=barsT[2:], ax=ax, color=colorsT[2:], label=labelsT[2:], stacked=True, position=-0.5, width=width)
        pre_xlim = ax.get_xlim()
    
        # Plot Load Subtypes
        pos = 1.5
        self.data.plot.bar(y=barsL, ax=ax, color=colorsL, label=labelsL, stacked=True, position=pos, width=width)
        # Plot System Subtypes
        pos = 0.5
        self.data.plot.bar(y=barsSY, ax=ax, color=colorsSY, label=labelsSY, stacked=True, position=pos, width=width)
        # Plot Load Subtypes
        pos = -0.5
        self.data.plot.bar(y=barsGSL, ax=ax, color=colorsGSL, label=labelsGSL, stacked=True, position=pos, width=width)
        # Reset ax limits
        ax.set_xlim(pre_xlim)
        # Plot energy Consum
        self.data.plot.bar(y=barsCM, ax=ax, color="none", edgecolor=colorsCM, label=labelsCM, stacked=True, position=1.5, width=width)

        # Add Labels + Separate containers
        containers = ax.containers
        self.glabels = [[], [], []]
        self.gbars = [[], [], []]
        # Types
        for i, name in enumerate(barsT):
            labels = [f'{p:.0f}' for p in self.data[name]]
            self.glabels[0].extend( ax.bar_label(containers[i], labels=labels, rotation=self.lrot, color=colorsT[i], fontsize=8, padding=4) )
        off = i+1
        # Subtypes
        for i, name in enumerate(barsD):
            labels = [f'{p:.0f}' for p in self.data[name]]
            self.glabels[1].extend(ax.bar_label(containers[i+off], labels=labels, rotation=self.lrot, fontsize=8, color='#1e1e1e', label_type='center') )
            self.gbars[1].extend(containers[i+off])
        off +=i+1
        # Energy ConsumeMax
        labels = [f'{p:.0f}' for p in self.data[barsCM[0]]]
        self.glabels[2].extend( ax.bar_label(containers[off], labels=labels, rotation=self.lrot, color=colorsCM[0], fontsize=8, padding=4) )
        self.gbars[2].extend(containers[off])

        # Visuals
        ax.margins(y=0.1)
        ax.legend()
        ax.set_ylabel('Energy [Wh]')
        if self.gaxis != None:
            ax.set_axisbelow(True)
            ax.grid(True, linestyle=':', axis=self.gaxis)
        if self.xtime:
            ax.set_xlabel('Hour Zone [h]')
            ax.set_xticklabels([x.strftime("%m-%d %H") for x in self.data['timestamp']], rotation=45)
            self.plot.fig.autofmt_xdate()
        else:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            self.plot.ax_xlimit= (-0.38, 1.75)
        self.plot.home_view()
        self.ghandlab = [[], [],[]]
        h, l = self.plot.ax.get_legend_handles_labels()
        for i in range(len(barsT)):
            self.ghandlab[0].append((h[i], l[i]))
        off = i+1
        for i in range(len(barsD)):
            self.ghandlab[1].append((h[i+off], l[i+off]))
        off += i+1
        self.ghandlab[2].append((h[off], l[off]))


        self.plotted = True

class SinglePlotController(BarPlotController):

    def _plot_bars(self):
        column = self.data.columns[1]
        ax = self.plot.ax
        self.plot.clear()
        
        # Plot types
        self.data.plot.bar(y=column, ax=ax, color=oct_color(column), label=oct_translate(column), width=0.60)

        # Add Labels + Separate containers
        containers = ax.containers[0]
        self.glabels= [[], [], []]
        labels = [f'{p:.3f}' for p in self.data[column]]
        self.glabels[0].extend( ax.bar_label(containers, labels=labels, rotation=self.lrot, color=oct_color(column), fontsize=8, padding=4) )

        # Visuals
        ax.margins(y=0.1)
        ax.legend(loc="upper right")
        ax.set_ylabel(oct_translate(column, 0, True))
        if self.gaxis != None:
            ax.set_axisbelow(True)
            ax.grid(True, linestyle=':', axis=self.gaxis)
        if self.xtime:
            ax.set_xlabel('Hour Zone [h]')
            ax.set_xticklabels([x.strftime("%m-%d %H") for x in self.data['timestamp']], rotation=45)
            self.plot.fig.autofmt_xdate()
        else:
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            self.plot.ax_xlimit= (-0.38, 1.75)
        self.plot.home_view()
        self.plotted = True
