# GUI adaptable for multiple controls, originally used for controlling a 
# FieldFox oscilliscope via SCPI commands
# Author: Tedi Qafko
# Date: November 1, 2023

import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
                                               NavigationToolbar2Tk)

def plot(): 
    # TODO: Add embedded data in gui
    l = Label(win, text = "Power Attenuation plot")
    l.grid(row = 6, column = 1, columnspan = 2, sticky = W + E)
    fig = Figure(figsize = (7, 4), dpi = 60) 
    plt = fig.add_subplot() 
    plt.set_title("Keysight FieldFox Spectrum Trace Data via Python " +
                  "- PyVisa - SCPI", fontsize = 10)
    plt.set_xlabel("Frequency", fontsize = 10)
    plt.set_ylabel("Amplitude (dBm)", fontsize = 10)
    # Example for plotting data:
    # plt.plot(scope.get_data()[0], scope.get_data()[1])
    canvas = FigureCanvasTkAgg(fig, master = win)
    canvas.draw() 
    canvas.get_tk_widget().grid(row = 7, column = 1, columnspan = 2, 
                                rowspan = 10, sticky = N + W)

def maximum_power():
   # Prints data into the text box via a function scope that 
   # returns maximum power levels of a signal
   display_data([round(scope.get_maximum_power(), 2)]) # Round 2 decimal

def display_data(arr):
    # The input is printed to a text box for user to identify 
    # the current process based off the button commands programmed
    l = Label(win, text = "Data/Text for User")
    l.grid(row = 6, column = 3)
    e = Text(win, height = 1, width = widthR1 - 6, fg = 'blue') 
    e.grid(row = 7, column = 3, rowspan = 10, sticky = N + S)
    c = ttk.Button(text = "Copy to Clipboard", 
                  command = lambda: copy_toClipboard(arr), 
                  width = widthR1)
    c.grid(row = 17, column = 3, columnspan = 1, rowspan = 1)
    e.delete(tk.END)
    e.insert(tk.END, str(arr))
    plot()
    # copy_toClipboard(arr)

def copy_toClipboard(arr):
    # An array entered as a parameter can be saved into your clipboard
    # in a format to paste into an excel spreadsheet column
    pd.DataFrame(arr).to_clipboard(excel = True, index = False, 
                                   header = False)
    print("Copied to clipboard!")

# Initial setup of Tkinter window
win = Tk()
w = 1300 # Width 
h = 600 # Height
widthR1 = 30 # First row of button width
widthR2 = 30 # Second row of button width
widthR3 = 30 # Third ....
widthR4 = 30 # Forth ....
delay = 0.7
screen_width = win.winfo_screenwidth()  # Width of the screen
screen_height = win.winfo_screenheight() # Height of the screen
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (w/2)
y = (screen_height/2) - (h/2)
win.geometry('%dx%d+%d+%d' % (w, h, x, y))
win.title('Graphical User Interface: Enter Title Here')
display_data("")

#----------------------------------------------------------------
# Bottom save as button with text box for name
label = Label(win, text = "Save As:")
label.config(state='normal')
label.grid(row = 18, column = 0, sticky = W, padx = 5)
entry = Entry(win, width = 30, bg = "white")
entry.grid(row = 18, column = 1)
save = ttk.Button(win, text = "Save s2p file", 
                command = lambda: scope.save_s2p_file(entry.get()), 
                width = widthR1) # Scope function can be anything
save.grid(row = 18, column = 2, pady = 20)
#----------------------------------------------------------------
# First column with 4 buttons in a vertical setup
label = Label(win, text = "General", width = widthR1)
label.grid(row = 1, column = 1, sticky = W + E, pady = 10)

power = ttk.Button(win, text = "Power Measurement setup", 
                   command = lambda: scope.setup(), 
                   width = widthR1)
power.grid(row = 2, column = 1)

vna = ttk.Button(win, text = "S-Parameters setup", 
               command = lambda: scope.VNAsetup(), 
               width = widthR1)
vna.grid(row = 3, column = 1, padx = 10)

getMaxPower = ttk.Button(win, text = "Get max power", 
                       command = lambda: maximum_power(), 
                       width = widthR1)
getMaxPower.grid(row = 4, column = 1, padx = 10)

get_power_data = ttk.Button(win, text = "Plot power attenuation", 
                          command = lambda: plot(), 
                          width = widthR1)
get_power_data.grid(row = 5, column = 1, padx = 10)

#----------------------------------------------------------------
# Second column with 4 buttons in a vertical setup
label = Label(win, text = "Control Setup 1", width = widthR2)
label.grid(row = 1, column = 2, sticky = W + E, pady = 2)

cs1_ts1 = ttk.Button(win, text = "Test 1", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR2)
cs1_ts1.grid(row = 2, column = 2, padx = 10)

cs1_ts2 = ttk.Button(win, text = "Test 2", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR2)
cs1_ts2.grid(row = 3, column = 2)

cs1_ts3 = ttk.Button(win, text = "Test 3", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR2)
cs1_ts3.grid(row = 4, column = 2)

cs1_ts4 = ttk.Button(win, text = "Test 4", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR2)
cs1_ts4.grid(row = 5, column = 2)

#----------------------------------------------------------------
# Third column with 4 buttons in a vertical setup
label = Label(win, text = "Control Setup 2", width = widthR3)
label.grid(row = 1, column = 3, sticky = W + E, pady = 2)

cs2_ts1 = ttk.Button(win, text = "Test 1", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR3)
cs2_ts1.grid(row = 2, column = 3, padx = 10)

cs2_ts2 = ttk.Button(win, text = "Test 2", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR3)
cs2_ts2.grid(row = 3, column = 3)

cs2_ts3 = ttk.Button(win, text = "Test 3", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR3)
cs2_ts3.grid(row = 4, column = 3)

cs2_ts4 = ttk.Button(win, text = "Test 4", 
                   command = lambda: print("Enter function instead"), 
                   width = widthR3)
cs2_ts4.grid(row = 5, column = 3)

#----------------------------------------------------------------
# Fourth column with 16 buttons in a vertical setup
label = Label(win, text = "Control Setup 3", width = widthR4)
label.grid(row = 1, column = 4, sticky = W + E, pady = 2)

cs3_ts1 = ttk.Button(win, text = "Test 1", 
                   command = lambda: f_ts1(), 
                   width = widthR4)
cs3_ts1.grid(row = 2, column = 4, padx = 10)

cs3_ts2 = ttk.Button(win, text = "Test 2", 
                   command = lambda: f_ts2(), 
                   width = widthR4)
cs3_ts2.grid(row = 3, column = 4)

cs3_ts3 = ttk.Button(win, text = "Test 3", 
                   command = lambda: f_ts3(), 
                   width = widthR4)
cs3_ts3.grid(row = 4, column = 4)

cs3_ts4 = ttk.Button(win, text = "Test 4", 
                   command = lambda: f_ts4(), 
                   width = widthR4)
cs3_ts4.grid(row = 5, column = 4)

cs3_ts5 = ttk.Button(win, text = "Test 5", 
                   command = lambda: f_ts5(), 
                   width = widthR4)
cs3_ts5.grid(row = 6, column = 4)

cs3_ts6 = ttk.Button(win, text = "Test 6", 
                   command = lambda: f_ts6(), 
                   width = widthR4)
cs3_ts6.grid(row = 7, column = 4)

cs3_ts7 = ttk.Button(win, text = "Test 7", 
                   command = lambda: f_ts7(), 
                   width = widthR4)
cs3_ts7.grid(row = 8, column = 4)

cs3_ts8 = ttk.Button(win, text = "Test 8", 
                   command = lambda: f_ts8(), 
                   width = widthR4)
cs3_ts8.grid(row = 9, column = 4)

cs3_ts9 = ttk.Button(win, text = "Test 9", 
                   command = lambda: f_ts9(), 
                   width = widthR4)
cs3_ts9.grid(row = 10, column = 4)

cs3_ts10 = ttk.Button(win, text = "Test 10", 
                    command = lambda: f_ts10(), 
                    width = widthR4)
cs3_ts10.grid(row = 11, column = 4)

cs3_ts11 = ttk.Button(win, text = "Test 11", 
                    command = lambda: f_ts11(), 
                    width = widthR4)
cs3_ts11.grid(row = 12, column = 4)

cs3_ts12 = ttk.Button(win, text = "Test 12", 
                    command = lambda: f_ts12(), 
                    width = widthR4)
cs3_ts12.grid(row = 13, column = 4)

cs3_ts13 = ttk.Button(win, text = "Test 13", 
                    command = lambda: f_ts13(), 
                    width = widthR4)
cs3_ts13.grid(row = 14, column = 4)

cs3_ts14 = ttk.Button(win, text = "Test 14", 
                    command = lambda: f_ts14(),
                    width = widthR4)
cs3_ts14.grid(row = 15, column = 4)

cs3_ts15 = ttk.Button(win, text = "Test 15", 
                    command = lambda: f_ts15(), 
                    width = widthR4)
cs3_ts15.grid(row = 16, column = 4)

cs3_ts16 = ttk.Button(win, text = "Test 16", 
                    command = lambda: f_ts16(), 
                    width = widthR4)
cs3_ts16.grid(row = 17, column = 4)

# These functions add additional function to the previous buttons.
def f_ts1():
    print("Start Test 1")
    display_data("Test")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 2, column = 5)
    
def f_ts2():
    print("Start Test 2")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 3, column = 5)

def f_ts3():
    print("Start Test 3")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 4, column = 5)

def f_ts4():
    print("Start Test 4")
    cont = ttk.Button(text = "Bonus", 
                  command = print("Enter function instead"))
    cont.grid(row = 5, column = 5)

def f_ts5():
    print("Start Test 5")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 6, column = 5)

def f_ts6():
    print("Start Test 6")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 7, column = 5)

def f_ts7():
    print("Start Test 7")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 8, column = 5)

def f_ts8():
    print("Start Test 8")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 9, column = 5)

def f_ts9():
    print("Start Test 9")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 10, column = 5)

def f_ts10():
    print("Start Test 10")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 11, column = 5)

def f_ts11():
    print("Start Test 11")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 12, column = 5)

def f_ts12():
    print("Start Test 12")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 13, column = 5)

def f_ts13():
    print("Start Test 13")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 14, column = 5)

def f_ts14():
    print("Start Test 14")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 15, column = 5)

def f_ts15():
    print("Start Test 15")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 16, column = 5)

def f_ts16():
    print("Start Test 16")
    cont = ttk.Button(text = "Bonus", 
                  command = lambda: print("Enter function instead"))
    cont.grid(row = 17, column = 5)

win.mainloop()