import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavToolbar
from matplotlib.backend_bases import PickEvent
import matplotlib
import numpy as np
import datetime as dt

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

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
            f = lambda x: mdate.date2num(x)
            self.x = f(self.x)
        self.hline = ax.axhline(y=self.y[0], color='k', lw=0.8, ls='--')
        self.vline = ax.axvline(x=self.x[0], color='k', lw=0.8, ls='--')
        self.snap_data = (0, 0)
        self._last_index = None
        self.cid = self.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.hline.get_visible() != visible
        self.hline.set_visible(visible)
        self.vline.set_visible(visible)
        return need_redraw

    def on_mouse_move(self, event):
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
        self.cid = self.ax.figure.canvas.mpl_connect('button_press_event', self.fire_pick_event)

    def fire_pick_event(self, event):
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

    def zoom_factory(self, ax, ax2=None, base_scale=2.0):
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

# Matplotlib widget
class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.fig, self.ax = plt.subplots()
        self.axes = [self.ax]
        self.canvas = Canvas(self.fig)
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()
        self.toolbar = NavToolbar(self.canvas, self)

        # Navbar add custom actions
        self.snap_cursor = None
        self.snap_cursor_ps = None
        self.snap_cursor_a = QAction(QIcon('./lib/myQT/cross.png'), 'Enable cross hair cursor /nClick any line to snap to it')
        self.snap_cursor_a.setCheckable(True)
        self.snap_cursor_a.toggled.connect(self.toggle_snap_cursor)
        self.toolbar.insertAction(self.toolbar.actions()[4], self.snap_cursor_a)

        # Make layout
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.toolbar)
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
        self.fig.tight_layout()

        # Resize thight
        self.fig.canvas.mpl_connect('resize_event', self.on_resize)
        # Mouse Zoom
        self.zp = Zoom()
        self.zp.zoom_factory(self.ax, base_scale = 1.1)

        self.toolbar.home = self.draw_idle

        # Custom coords format
        if not isinstance(self, MplTwinxWidget):
            self.ax.format_coord = self.make_format()

    def draw_idle(self):
        for ax in self.axes:
            ax.relim()      # make sure all the data fits
            ax.autoscale()  # auto-scale
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
    
    def on_resize(self, _):
        self.fig.tight_layout()
        self.fig.canvas.draw_idle()
    
    def clear(self):
        for ax in self.axes:
            ax.clear()

    # Show/Hide lines if selected in legend
    def toggable_legend_lines(self):
        lines = []
        for ax in self.axes:
            if ax.get_legend() == None:
                ax.legend()
            lines += ax.get_legend().get_lines()
        self.legend_PS = PickStack(lines, self.legend_on_pick)
        
    def legend_on_pick(self, event):
        legline = event.artist
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
                        break
                break
        legline.set_alpha(1.0 if visible else 0.2)
        self.fig.canvas.draw_idle()
    
    # Display XY coords
    def make_format(self):
        def format_coord(x, y):
            if self.snap_cursor_a.isChecked():
                x, y = self.snap_cursor.snap_data
            x = self.format_coord_x(x)
            return self.format_coords_str(x, y)
        return format_coord

    def format_coord_x(self, x):
        for ax in self.axes:
            line = ax.get_lines()
            if line != []:
                xdata, _ = line[0].get_data()
                if isinstance(xdata[0], (dt.datetime, np.datetime64)):
                    return mdate.num2date(x).strftime("%m/%d/%Y %H:%M:%S")
        return x

    def format_coords_str(self, x, y):
        if isinstance(x, str):
            return f'({x}, {y:.3f})'
        return f'({x:.3f}, {y:.3f})'

    # Mouse Cross hair cursor
    def toggle_snap_cursor(self, value):
        if value:
            lines = []
            for ax in self.axes:
                lines += ax.get_lines()
            if lines != []:
                self.snap_cursor = SnappingCursor(self.fig, self.ax, lines[0])
                self.snap_cursor_ps = PickStack(lines, self.snap_cursor_on_pick)
            else:
                self.snap_cursor_a.setChecked(False)
        else:
            if self.snap_cursor != None:
                self.snap_cursor.remove()
                self.snap_cursor_ps = None
                self.snap_cursor = None

    def snap_cursor_on_pick(self, event):
        line = event.artist
        self.snap_cursor.remove()
        for ax in self.axes:
            if line in ax.get_lines():
                self.snap_cursor = SnappingCursor(self.fig, ax, line)
                return

# Two axes matplotlib widget
class MplTwinxWidget(MplWidget):
    def __init__(self, parent=None):
        MplWidget.__init__(self, parent)
        self.ax1 = self.ax
        self.ax2 = self.ax.twinx()
        self.axes = [self.ax1, self.ax2]

        # Mouse Zoom
        self.zp = Zoom()
        self.zp.zoom_factory(self.ax, self.ax2, base_scale = 1.1)

        self.ax2.format_coord = self.make_format(self.ax2, self.ax1)

    def align_yaxis(self):
        """Align zeros of the two axes, zooming them out by same ratio"""
        axes = np.array([self.ax1, self.ax2])
        extrema = np.array([ax.get_ylim() for ax in axes])
        tops = extrema[:,1] / (extrema[:,1] - extrema[:,0])
        # Ensure that plots (intervals) are ordered bottom to top:
        if tops[0] > tops[1]:
            axes, extrema, tops = [a[::-1] for a in (axes, extrema, tops)]

        # How much would the plot overflow if we kept current zoom levels?
        tot_span = tops[1] + 1 - tops[0]

        extrema[0,1] = extrema[0,0] + tot_span * (extrema[0,1] - extrema[0,0])
        extrema[1,0] = extrema[1,1] + tot_span * (extrema[1,0] - extrema[1,1])
        [axes[i].set_ylim(*extrema[i]) for i in range(2)]

    def make_format(self, current, other):
        # current and other are axes
        def format_coord(x, y):
            if self.snap_cursor_a.isChecked():
                x, y = self.snap_cursor.snap_data
                x = self.format_coord_x(x)
                return self.format_coords_str(x, y)
            else:
                display_coord = current.transData.transform((x,y))
                inv = other.transData.inverted()
                # convert back to data coords with respect to ax
                X, Y = inv.transform(display_coord)
                x = self.format_coord_x(x)
                X = self.format_coord_x(X)
                coords = [(X, Y), (x, y)]
                return ('Left: {:<}  |  Right: {:<}'.format(*[self.format_coords_str(x, y) for x, y in coords]))
        return format_coord


if __name__ == '__main__':
    app = QApplication(sys.argv)

    random_dates_1 = []
    for i in range(10):
        random_dates_1.append( np.datetime64(dt.datetime.now() + dt.timedelta(days=i)) )

    a = MplWidget()
    a.ax.plot(random_dates_1, range(0,10), '-o', label='A')
    a.toggable_legend_lines()

    b = MplTwinxWidget()
    b.ax1.plot(range(10,20), range(0,10), '-o', label='B1', color='orange')
    b.ax2.plot(range(0,10), range(0,-10,-1), '-o', color='red')
    b.ax2.plot(range(0,10), range(0,10), '-o', label='B2', color='green')
    b.toggable_legend_lines()

    c = MplTwinxWidget()
    c.ax1.plot(random_dates_1, range(0,10), '-o', label='C1', color='orange')
    c.ax2.plot(random_dates_1, range(0,-10,-1), '-o', label='C2')
    c.toggable_legend_lines()

    window = QTabWidget()
    window.addTab(a, 'a')
    window.addTab(b, 'b')
    window.addTab(c, 'c')
    window.show()
    sys.exit(app.exec())