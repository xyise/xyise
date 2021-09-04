#%%
import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

# %%

root = tk.Tk()
root.wm_title('embedding in Tk')

fig = Figure(figsize=(5,4), dpi=100)
t = np.arange(0, 3, 0.01)
sp = fig.add_subplot(111)
sp.plot(t, 2 * np.sin(2*np.pi * t))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def on_key_press(event):
    print('you pressed {}'.format(event.key))
    if event.key == 'd':
        print('here')
        sp.plot(t, 4 * t)

    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_press)

def _quit():
    root.quit()
    root.destroy()

buttom = tk.Button(master=root, text='quit', command=_quit)
buttom.pack(side=tk.BOTTOM)

tk.mainloop()





# %%
from PyQt5.QtWidgets import QApplication, QLabel

# %%
app = QApplication([])
label = QLabel('Hello World')
label.show()
app.exec_()

# %%
