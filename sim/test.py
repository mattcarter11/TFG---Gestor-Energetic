# Implementation of matplotlib function
from matplotlib.axis import Axis
import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider, Button, RadioButtons 
       
fig, ax1 = plt.subplots() 
plt.subplots_adjust(bottom = 0.25) 
t = np.arange(0.0, 1.0, 0.001) 
  
a0 = 5
f0 = 3
delta_f = 5.0
s = a0 * np.sin(2 * np.pi * f0 * t) 
       
ax1.plot(t, s, lw = 2, color = 'green') 
  
ax1.axes[0].zoom(-2)
   
ax1.grid() 
   
fig.suptitle("""matplotlib.axis.Axis.zoom()
function Example\n""", fontweight ="bold")  
     
plt.show()