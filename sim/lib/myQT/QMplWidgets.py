import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, Signal
import matplotlib as mp
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolbar
from matplotlib.backend_bases import PickEvent
import numpy as np
import datetime as dt
from enum import Enum

from sqlalchemy import false

# Ensure using PyQt5 backend
mp.use('QT5Agg')

def align_yaxis(ax1, ax2):
    """Align zeros of the two axes, zooming them out by same ratio"""
    axes = np.array([ax1, ax2])
    extrema = np.array([ax.get_ylim() for ax in axes])
    tops = extrema[:,1] / (extrema[:,1] - extrema[:,0])
    # Ensure that plots (intervals) are ordered bottom to top:
    if tops[0] > tops[1]:
        axes, extrema, tops = [a[::-1] for a in (axes, extrema, tops)]

    # How much would the plot overflow if we kept current zoom levels?
    tot_span = tops[1] + 1 - tops[0]

    extrema[0,1] = extrema[0,0] + tot_span * (extrema[0,1] - extrema[0,0])
    extrema[1,0] = extrema[1,1] + tot_span * (extrema[1,0] - extrema[1,1])
    for i in range(2):
        axes[i].set_ylim(*extrema[i]) 

class CossHairAction(QAction):
    def __init__(self, icon:QIcon, text:str, parent):
        super().__init__(icon, text)
        self.setCheckable(True)
        self.toggled.connect(self.toggle_snap_cursor)
        self.parent = parent
        self.snap_cursor = None
        self.snap_cursor_ps = None

    def toggle_snap_cursor(self, value):
        if value:
            lines = []
            for ax in self.parent.axes:
                lines += ax.get_lines()
            if lines != []:
                self.snap_cursor = SnappingCursor(self.parent.fig, self.parent.ax, lines[0])
                self.snap_cursor_ps = PickStack(lines, self._snap_cursor_on_pick)
            else:
                self.setChecked(False)
        else:
            if self.snap_cursor != None:
                self.snap_cursor.remove()
                self.snap_cursor_ps = None
                self.snap_cursor = None

    def _snap_cursor_on_pick(self, event):
        line = event.artist
        self.snap_cursor.remove()
        for ax in self.parent.axes:
            if line in ax.get_lines():
                self.snap_cursor = SnappingCursor(self.parent.fig, ax, line)
                return

    def coords(self):
        return self.snap_cursor.snap_data

class SnappingCursor:
    """
    A cross hair cursor that snaps to the data point of a line, which is
    closest to the *x* position of the cursor.

    For simplicity, this assumes that *x* values of the data are sorted.
    """
    def __init__(self, fig, ax, line):
        self.fig = fig
        self.ax = ax
        self.x, self.y = line.get_data()
        if isinstance(self.x[0], (dt.datetime, np.datetime64)):
            f = lambda x: mp.dates.date2num(x)
            self.x = f(self.x)
        self.hline = ax.axhline(y=self.y[0], color='k', lw=0.8, ls='--')
        self.vline = ax.axvline(x=self.x[0], color='k', lw=0.8, ls='--')
        self.snap_data = (0, 0)
        self._last_index = None
        self.cid = self.fig.canvas.mpl_connect('motion_notify_event', self._on_mouse_move)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.hline.get_visible() != visible
        self.hline.set_visible(visible)
        self.vline.set_visible(visible)
        return need_redraw

    def _on_mouse_move(self, event):
        if not event.inaxes:
            self._last_index = None
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.draw_idle()
        else:
            self.set_cross_hair_visible(True)
            x, y = event.xdata, event.ydata
            index = min(np.searchsorted(self.x, x), len(self.x) - 1)
            if (index > 0) and (x-self.x[index-1]) <= ((self.x[index]-self.x[index-1])/2):
                index -= 1
            if index == self._last_index:
                return  # still on the same data point. Nothing to do.
            self._last_index = index
            x = self.x[index]
            y = self.y[index]
            self.snap_data = (x, y)
            # update the line positions
            self.hline.set_ydata(y)
            self.vline.set_xdata(x)
            self.ax.figure.canvas.draw_idle()

    def remove(self):
        try:
            lines = self.ax.get_lines()
            i = lines.index(self.vline)
            self.ax.lines.pop(i)
            i = lines.index(self.hline)
            self.ax.lines.pop(i)
            self.fig.canvas.mpl_disconnect(self.cid)
        except Exception as e:
            print(e)
        self.fig.canvas.draw_idle()

class PickStack:
    def __init__(self, stack, on_pick):
        self.stack = stack
        self.ax = [artist.axes for artist in self.stack][0]
        self.on_pick = on_pick
        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self._fire_pick_event)

    def _fire_pick_event(self, event):
        if not event.inaxes:
            return
        cont = [a for a in self.stack if a.contains(event)[0]]
        if not cont:
            return
        pick_event = PickEvent("pick_Event", self.ax.figure.canvas, 
                               event, cont[0],
                               guiEvent=event.guiEvent,
                               **cont[0].contains(event)[1])
        self.on_pick(pick_event)

class Zoom:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.cur_ylim2 = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        self.xzoom = True
        self.yzoom = True
        self.cidBP = None
        self.cidBR = None
        self.cidBM = None
        self.cidKeyP = None
        self.cidKeyR = None
        self.cidScroll = None

    def zoom_factory(self, ax, ax2=None, base_scale=2.0, align=False):
        def zoom(event):
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
            if xdata is None: return
            if ydata is None: return
            if not event.inaxes: return
            
            if event.button == 'up': # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'down': # deal with zoom out
                scale_factor = base_scale
            else: # deal with something that should never happen
                scale_factor = 1
                print(event.button)

            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()

            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])

            if(self.xzoom): ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            if(self.yzoom): ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])

            if ax2 != None: # If twins axes
                eventC = ax.transData.transform((event.xdata,event.ydata))
                _, ydata = ax2.transData.inverted().transform(eventC)

                cur_ylim = ax2.get_ylim()
                new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
                rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
                if(self.yzoom): ax2.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
                if align:
                    align_yaxis(ax, ax2)
                
            ax.figure.canvas.draw_idle()
            ax.figure.canvas.flush_events()

        def onKeyPress(event):
            self.xzoom = event.key == 'x'
            self.yzoom = event.key == 'y'

        def onKeyRelease(event):
            self.xzoom = self.yzoom= True

        fig = ax.get_figure() # get the figure of interest

        self.cidScroll = fig.canvas.mpl_connect('scroll_event', zoom)
        self.cidKeyP = fig.canvas.mpl_connect('key_press_event',onKeyPress)
        self.cidKeyR = fig.canvas.mpl_connect('key_release_event',onKeyRelease)

        return zoom

# Matplotlib plot widget
class QMplPlot(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.fig, self.ax = plt.subplots()
        self.axes = [self.ax]
        self.canvas = Canvas(self.fig)
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()
        self.toolbar = NavToolbar(self.canvas, self)
        self.legend_PS = None
        
        # Make layout
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.fig.tight_layout()

        # Resize thight
        self.fig.canvas.mpl_connect('resize_event', self.draw_idle)

        # Navbar add custom actions
        self.snap_cross_hair = CossHairAction(QIcon('./lib/myQT/cross.png'), 'Enable snaping cross hair cursor \nClick any line to snap to it', self)
        self.toolbar.insertAction(self.toolbar.actions()[4], self.snap_cross_hair)
        
        # Mouse Zoom
        self.zp = Zoom()
        self.zp.zoom_factory(self.ax, base_scale = 1.1)
        
        # Custom Home (fit plot)
        self.ax_xlimit = None
        self.ax_ylimit = None
        self.toolbar.home = self.home_view

        # Custom coords format
        if not isinstance(self, QMplTwinxPlot):
            self.ax.format_coord = self._make_format()

    #regions -> Generic
    def draw_idle(self, *_):
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
    
    
    def home_view(self):
        for ax in self.axes:
            ax.relim()      # make sure all the data fits
            ax.autoscale()  # auto-scale
        if self.ax_xlimit != None:
            self.ax.set_xlim(*self.ax_xlimit)
        if self.ax_ylimit != None:
            self.ax.set_ylim(*self.ax_ylimit)
        if isinstance(self, QMplTwinxPlot) and self.align:
            if self.ax2_xlimit != None:
                self.ax2.set_xlim(*self.ax2_xlimit)
            if self.ax2_ylimit != None:
                self.ax2.set_ylim(*self.ax2_ylimit)
            self.align_yaxis()
        self.draw_idle()
        
    def clear(self):
        self.snap_cross_hair.setChecked(False)
        for ax in self.axes:
            ax.clear()
    
    def set_visible(self, artist, val): # Line or Area
        artist.set_visible(val)
        label = artist.get_label()
        label = '_'+label if not val else label[1:] if label[0] == "_" else label
        artist.set_label(label)

    def redraw_legend(self, ax_num = 1):
        ax = self.axes[ax_num-1]
        legend = ax.get_legend()
        old_lines = legend.get_lines()
        ax.legend()._set_loc(legend._loc)

        # Restore hidden lines and alpha level
        new_lines = ax.get_legend().get_lines()
        new_lines_labels = [line.get_label() for line in new_lines]
        for line in old_lines:
            label = line.get_label()
            if label in new_lines_labels:
                i = new_lines_labels.index(label)
                new_lines[i].set(visible=line.get_visible(), alpha=line.get_alpha())
        
        if self.legend_PS is not None:
            self.toggable_legend_lines()
        self.draw_idle()
    #endregion

    #region -> Show/Hide lines if selected in legend
    def toggable_legend_lines(self):
        lines = []
        for ax in self.axes:
            if ax.get_legend() == None:
                ax.legend()
            lines += ax.get_legend().get_lines()
        self.legend_PS = PickStack(lines, self._legend_on_pick)
        
    def _legend_on_pick(self, event):
        self._hide_legline(event.artist)

    def _hide_legline(self, legline):
        label = legline.get_label()
        # Get right axes
        for ax in self.axes:
            leglines = ax.get_legend().get_lines()
            if legline in leglines:
                # Find line
                for line in ax.get_lines():
                    if label == line.get_label():
                        visible = not line.get_visible()
                        line.set_visible(visible)
                        legline.set_alpha(1.0 if visible else 0.2)
                        break
                break
        self.fig.canvas.draw_idle()
    #endregion

    #region -> Display XY coords
    def _make_format(self):
        def format_coord(x, y):
            if self.snap_cross_hair.isChecked():
                x, y = self.snap_cross_hair.coords()
            x = self._format_coord_x(x)
            return self._format_coords_str(x, y)
        return format_coord

    def _format_coord_x(self, x):
        for ax in self.axes:
            line = ax.get_lines()
            if line != []:
                xdata, _ = line[0].get_data()
                if isinstance(xdata[0], (dt.datetime, np.datetime64)):
                    return mp.dates.num2date(x).strftime("%m/%d/%Y %H:%M:%S")
        return x

    def _format_coords_str(self, x, y):
        if isinstance(x, str):
            return f'({x}, {y:.3f})'
        return f'({x:.3f}, {y:.3f})'
    #endregion

# Two axes matplotlib plot widget
class QMplTwinxPlot(QMplPlot):
    def __init__(self, parent=None):
        QMplPlot.__init__(self, parent)
        self.ax1 = self.ax
        self.ax2 = self.ax.twinx()
        self.axes = [self.ax1, self.ax2]
        self.align = False

        # Custom Home (fit plot)
        self.ax2_xlimit = None
        self.ax2_ylimit = None

        # Mouse Zoom
        self.zp = Zoom()
        self.zp.zoom_factory(self.ax, self.ax2, 1.1, self.align)

        self.ax2.format_coord = self._make_format(self.ax2, self.ax1)

    def align_yaxis(self):
        self.align = True
        align_yaxis(self.ax1, self.ax2)

    def _make_format(self, current, other):
        # current and other are axes
        def format_coord(x, y):
            if self.snap_cross_hair.isChecked():
                x, y = self.snap_cross_hair.coords()
                x = self._format_coord_x(x)
                return self._format_coords_str(x, y)
            else:
                display_coord = current.transData.transform((x,y))
                inv = other.transData.inverted()
                # convert back to data coords with respect to ax
                X, Y = inv.transform(display_coord)
                x = self._format_coord_x(x)
                X = self._format_coord_x(X)
                coords = [(X, Y), (x, y)]
                return ('Left: {:<}  |  Right: {:<}'.format(*[self._format_coords_str(x, y) for x, y in coords]))
        return format_coord

# Editable matplotli plot by moving poits in y axis
class QMplPlotterWidget(QMplPlot):
    dataChanged = Signal([object, object])

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = False

    def set_line(self, x, y, linestyle='-o', *arg, **kwargs):
        self.clear()
        self.draw_idle()
        self.line = self.ax.plot(x, y, linestyle, *arg, **kwargs)[0]
        self.data_lines_PS = PickStack([self.line], self._on_click)

    def set_value(self, i, val):
        y = self.line.get_ydata()
        y[i] = val
        self.line.set_ydata(y)
        self.draw_idle()

    def get_value(self, i):
        return self.line.get_ydata()[i]

    def _on_click(self, event):
        if not self.selected:
            self.selected = True
            self.i = event.ind[0]
            self.y0 = self.get_value(self.i)
            self.vline = self.ax.axvline(self.line.get_xdata()[self.i], color='#a5a5a5',linestyle=':')
            self.on_move_cid = self.fig.canvas.mpl_connect('motion_notify_event', self._on_move)
            self.on_keypress_cid = self.fig.canvas.mpl_connect('key_press_event', self._on_keypress)
            self.on_button_press_cid = self.fig.canvas.mpl_connect('button_press_event', self._on_button_press)
        else:
            self._exit_selection()
    
    def _on_move(self, event):
        if event.inaxes:
            self.set_value(self.i, event.ydata)

    def _on_keypress(self, event):
        if event.key == "escape":
            self.set_value(self.i, self.y0,)
            self._exit_selection()   

    def _on_button_press(self, event):
        if not self.line.contains(event)[0]:
            self._exit_selection()

    def _exit_selection(self, *_):
        self.dataChanged.emit(self.get_value(self.i), self.i)
        self.selected = False
        if self.vline in self.ax.lines:
            i = self.ax.lines.index(self.vline)
            self.ax.lines.pop(i)
        self.draw_idle()
        self.fig.canvas.mpl_disconnect(self.on_move_cid)
        self.fig.canvas.mpl_disconnect(self.on_keypress_cid)
        self.fig.canvas.mpl_disconnect(self.on_button_press_cid)

# Selectable and movable hline or vline
class QMplHVLineType(Enum):
    hline = 'vline'
    vline = 'hline'

class QMplMovableHVLine(QWidget):
    dataChanged = Signal([object, object])

    def __init__(self, line:Line2D, type:QMplHVLineType, fig, parent=None):
        QWidget.__init__(self, parent)
        self.line = line
        self.type = type
        self.fig = fig
        self.selected = False
        self.ps = PickStack([line], self._on_pick)

    def _on_pick(self, _):
        x, y = self.line.get_data()
        self.x0 = x[0] if isinstance(x, list) else x
        self.y0 = y[0] if isinstance(y, list) else y
        self.x0, self.y0 = self._process_val(x, y)
        
        if not self.selected:
            self.selected = True
            self.on_move_cid = self.fig.canvas.mpl_connect('motion_notify_event', self._on_move)
            self.on_keypress_cid = self.fig.canvas.mpl_connect('key_press_event', self._on_keypress)
        else:
            self._exit()

    def _on_move(self, event):
        if event.inaxes:
            self.set_xydata( event.xdata, event.ydata )
            self.fig.canvas.draw_idle()
    
    def _on_keypress(self, event):
        if event.key == "escape":
            self._reset()
    
    def _exit(self):
        x, y = self.line.get_data()
        x = x[0] if isinstance(x, list) else x
        y = y[0] if isinstance(y, list) else y
        if self.type == QMplHVLineType.hline:
            self.dataChanged.emit(y, self.type)
        elif self.type == QMplHVLineType.vline:
            self.dataChanged.emit(x, self.type)

        self.selected = False
        self.fig.canvas.mpl_disconnect(self.on_move_cid)
        self.fig.canvas.mpl_disconnect(self.on_keypress_cid)

    def _reset(self):
        self.set_xydata(self.x0, self.y0)
        self.fig.canvas.draw_idle()
        self._exit()

    def _process_val(self, x, y):
        x = mp.dates.date2num(x) if isinstance(x, (dt.datetime, np.datetime64)) else x
        y = mp.dates.date2num(y) if isinstance(y, (dt.datetime, np.datetime64)) else y
        return (x, y)

    def set_xydata(self, x, y):
        x, y = self._process_val(x, y)
        if self.type == QMplHVLineType.hline:
            self.line.set_ydata(y)
        elif self.type == QMplHVLineType.vline:
            self.line.set_xdata(x)
        

def vhline_print(val, type):
    print(val, type)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    random_dates_1 = []
    for i in range(10):
        random_dates_1.append( np.datetime64(dt.datetime.now() + dt.timedelta(days=i)) )

    p = QMplPlotterWidget()
    p.set_line(range(0,24), np.zeros(24))
    tmp = QMplMovableHVLine( p.ax.axvline(1), QMplHVLineType.vline, p.fig)
    tmp2 = QMplMovableHVLine( p.ax.axhline(1), QMplHVLineType.hline, p.fig)
    tmp.dataChanged.connect(vhline_print)
    tmp2.dataChanged.connect(vhline_print)

    a = QMplPlot()
    a.ax.plot(random_dates_1, range(0,10), '-o', label='A')
    tmp3 = QMplMovableHVLine( a.ax.axvline(1), QMplHVLineType.vline, a.fig)
    tmp3.dataChanged.connect(vhline_print)
    a.toggable_legend_lines()

    b = QMplTwinxPlot()
    b.ax1.plot(range(10,20), range(0,10), '-o', label='B1', color='orange')
    b.ax2.plot(range(0,10), range(0,-10,-1), '-o', color='red')
    b.ax2.plot(range(0,10), range(0,10), '-o', label='B2', color='green')
    b.toggable_legend_lines()
    b.align_yaxis()

    c = QMplTwinxPlot()
    c.ax1.plot(random_dates_1, range(0,10), '-o', label='C1', color='orange')
    c.ax2.plot(random_dates_1, range(0,-10,-1), '-o', label='C2')
    c.toggable_legend_lines()

    window = QTabWidget()
    window.addTab(p, 'p')
    window.addTab(a, 'a')
    window.addTab(b, 'b')
    window.addTab(c, 'c')
    window.show()
    sys.exit(app.exec())