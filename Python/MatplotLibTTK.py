from ast import Import, Try
from asyncio.windows_events import NULL
from cgitb import text
import csv
from datetime import datetime, timedelta

import re
from csv import DictReader
from datetime import datetime
from this import d
from tkinter import *
from tkinter import ttk, messagebox
from tkinter import font
from turtle import color
from matplotlib.axes import Axes
from matplotlib.pyplot import axes

import numpy as np
import matplotlib
from matplotlib.dates import date2num, num2date
from matplotlib.figure import Figure
from matplotlib import dates as mpl_dates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter as tk

matplotlib.use('TkAgg')

class App(tk.Tk):
    _xlim = any
    _ylim = any
    _plot_x_values = any
    _plot_y_values = any
    _plot_draw = NULL
    _plot_label_draw = NULL
    _axes = any 

    def __init__(self):
        super().__init__()

        self.title('Tkinter Matplotlib with Code Clinic')
        self.resizable(True, True)
        self.state('zoomed')

        data = []
        
        for year in range(2012,2013):
            dataLoad = self.importCSVFile("Python\\Code Clinic Python 2018\\Ex_Files_Code_Clinic_Python\\Ch01\\resources\\Environmental_Data_Deep_Moor_{}.txt".format(year))
            self.combiningDataFiles(data,dataLoad)
        
        print("Converting String To Datetime and Barometric_Press to float value")
        format = '%Y_%m_%d %H:%M:%S'
        dates = [datetime.strptime(obj['date       time    '], format) for obj in data]
        barometricrpess = [float(obj['Barometric_Press'])for obj in data]

        # create a figure
        self._figure = Figure(figsize=(6, 4), dpi=100)
        self._figure.tight_layout(rect=[0, 0, 0.5, 1.0])
        
        # create FigureCanvasTkAgg object
        self._figure_canvas = FigureCanvasTkAgg(self._figure, self)

        # create the toolbar
        NavigationToolbar2Tk(self._figure_canvas, self)

        # create axes
        self._axes = self._figure.add_subplot(111)

        # create the barchart
        self._axes.plot_date(dates, barometricrpess)

        date_format = mpl_dates.DateFormatter('%Y-%m-%d')
        self._axes.xaxis.set_major_formatter(date_format)
        self._axes.tick_params(axis='x', which='major', labelsize=6)

        self._axes.set_title('Dates')
        self._axes.set_ylabel('Barometric Press',fontsize=10)
        
        bottom_btn_frame = Frame(height=20, bg='grey')
        
        def submitFunction() :
            #'2012_01_01'
            #'2012_12_31'
            try:
                if (self._plot_label_draw != NULL):
                    self._plot_label_draw.set_visible(False)
            except:
                print("Failed to clear text")

            try:
                if (self._plot_draw != NULL):
                    self._axes.set_xlim(self._xlim)
                    self._axes.set_ylim(self._ylim)
                    self._plot_draw[0].remove()
                    self._figure_canvas.draw()
                    self._plot_draw = NULL
            except:
                print("Plots Cleared failed")

            try:
                
                format = '%Y-%m-%d'
                strStartDate = datetime.strptime(strTxt.get('1.0', 'end').replace("\n",""), format)
                strEndDate = datetime.strptime(endTxt.get('1.0', 'end').replace("\n",""), format)
                start_date_avgBar = self.avgBarmetricPress(strStartDate,data)
                end_date_avgBar = self.avgBarmetricPress(strEndDate,data)

                point1 = [strStartDate,start_date_avgBar]
                point2 = [strEndDate,end_date_avgBar]
                self._plot_x_values = [point1[0], point2[0]]
                self._plot_y_values = [point1[1], point2[1]]
                self._plot_draw = self._axes.plot(self._plot_x_values, self._plot_y_values, 'bo', linestyle="--",label="text")
                self._axes.set_xlim(strStartDate- timedelta (days=1), strEndDate + timedelta (days=1))
                self._axes.set_ylim(start_date_avgBar*.8, end_date_avgBar*1.1)

                strStartDate = date2num(strStartDate)
                strEndDate = date2num(strEndDate)
                dy = strEndDate - strStartDate
                dt = end_date_avgBar - start_date_avgBar
                slope = dt/dy

                # add colored slope value to figure
                color = 'green' if (slope >= 0) else 'red'
                text_x = strStartDate + (strEndDate - strStartDate)/2
                text_y = start_date_avgBar + (end_date_avgBar - start_date_avgBar)/2
                self._plot_label_draw = self._axes.text(num2date(text_x), text_y, '{0:.6f} inHg/day'.format(slope),
                    fontsize=16, horizontalalignment='center',
                    bbox=dict(facecolor=color))
                self._plot_label_draw.set_visible(True)
            except Exception as e:
                print(e) 
                print("Exception thrown. x does not exist.")
                
            self._figure_canvas.draw()
        
        def clearFunction() :

            try:
                self._plot_label_draw.set_visible(False)
            except:
                print("Failed To Clear Text")

            try:
                self._axes.set_xlim(self._xlim)
                self._axes.set_ylim(self._ylim)
                if (self._plot_draw != NULL):
                    self._plot_draw[0].remove()
                    self._figure_canvas.draw()
                    self._plot_draw = NULL
            except:
                print("Failed To Cleared Plot ")

        clearBtn=Button (bottom_btn_frame,command=clearFunction,text='clear')
        clearBtn.pack(side='left')

        submitBtn=Button (bottom_btn_frame,command=submitFunction,text='Submit')
        submitBtn.pack(side='bottom')
        
        bottom_btn_frame.pack(side=tk.BOTTOM)

        bottom_lbl_frame = Frame(height=20, bg='grey')
        strBtmLbl =Label (master=bottom_lbl_frame,height=1,width=20,text="YYYY-MM-DD")
        strBtmLbl.pack(side=tk.LEFT)
        endBtmLbl =Label (master=bottom_lbl_frame,height=1,width=20,text="YYYY-MM-DD")
        endBtmLbl.pack(side=tk.LEFT)
        bottom_lbl_frame.pack(side=tk.BOTTOM)

            #'2012_01_01'
            #'2012_12_31'
        bottom_txt_frame = Frame(height=20, bg='grey')
        strTxt =Text (master=bottom_txt_frame,height=1,width=20)
        strTxt.insert(END, "2012-01-03")
        strTxt.pack(side=tk.LEFT)
        endTxt =Text (master=bottom_txt_frame,height=1,width=20)
        endTxt.insert(END, "2012-01-11")
        endTxt.pack(side=tk.LEFT)
        bottom_txt_frame.pack(side=tk.BOTTOM)

        top_lbl_frame = Frame(height=20, bg='grey')
        strTopLbl =Label (master=top_lbl_frame,height=1,width=20,text="Starting Date")
        strTopLbl.pack(side=tk.LEFT)
        endTopLbl =Label (master=top_lbl_frame,height=1,width=20,text="Ending Date")
        endTopLbl.pack(side=tk.LEFT)
        top_lbl_frame.pack(side=tk.BOTTOM)

        self._xlim = self._axes.get_xlim()
        self._ylim = self._axes.get_ylim()
        self._figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def avgBarmetricPress(self,date,data):
        sorted_bars = []
        for obj in data:    
            formatDatatime = '%Y_%m_%d %H:%M:%S'
            data_x = datetime.strptime(obj['date       time    '], formatDatatime)
            if(date.date().__eq__(data_x.date())):
                sorted_bars.append(float(obj['Barometric_Press']))

        return self.cal_average(sorted_bars)

    def cal_average(self,num):
        sum_num = 0
        for t in num:
            sum_num = sum_num + t           

        avg = sum_num / len(num)
        return avg

    def graph_plots(self,axes,dates,barometricrpess):      
        return axes.plot_date(dates, barometricrpess,color='red')
        

    def importCSVFile(self, fileName):
        data = []
        with open(fileName) as f:
            reader = csv.DictReader(f, delimiter='\t')
            data = [d for d in reader]
        return data

    def combiningDataFiles(self, data,tempdata):
        for obj in tempdata:
            data.append(obj)
        return

if __name__ == '__main__':
    app = App()
    app.mainloop()
