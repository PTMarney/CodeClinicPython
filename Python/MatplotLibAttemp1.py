from ast import Import
import csv
from datetime import datetime, timedelta
from unicodedata import combining
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates
from matplotlib.widgets import TextBox
import numpy as np
   

def main():
    print("Start Program")
    
    print("Testing Importing CVS File 2012")
    data = AM1importCSVFile("Python\\Code Clinic Python 2018\\Ex_Files_Code_Clinic_Python\\Ch01\\resources\\Environmental_Data_Deep_Moor_2012.txt")
    print("Testing Importing CVS File 2013")
   # data1 = importCSVFile("Python\\Code Clinic Python 2018\\Ex_Files_Code_Clinic_Python\\Ch01\\resources\\Environmental_Data_Deep_Moor_2013.txt")
    print("Testing Importing CVS File 2014")
   # data2 = importCSVFile("Python\\Code Clinic Python 2018\\Ex_Files_Code_Clinic_Python\\Ch01\\resources\\Environmental_Data_Deep_Moor_2014.txt")
    print("Testing Importing CVS File 2015")
    #data3 = importCSVFile("Python\\Code Clinic Python 2018\\Ex_Files_Code_Clinic_Python\\Ch01\\resources\\Environmental_Data_Deep_Moor_2015.txt")
    print("Testing Importing CVS File Complete")

    print("Combining all dataset together")
    #combiningDataFiles(data,data1)
    #combiningDataFiles(data,data2)
    #combiningDataFiles(data,data3)
    print("Combining all dataset together Completed")


    print("Mapping with MatplotLib test data")
    AM1MatplotSetup(data)


def AM1importCSVFile(fileName):
    data = []
    with open(fileName) as f:
        reader = csv.DictReader(f, delimiter='\t')
        data = [d for d in reader]
    return data

def AM1combiningDataFiles(data,tempdata):
    for obj in tempdata:
        data.append(obj)
    return

def AM1MatplotSetup(data):
    fig, ax = plt.subplots()

    print("Converting String To Datetime and Barometric_Press to float value")
    format = '%Y_%m_%d %H:%M:%S'
    dates = [datetime.strptime(obj['date       time    '], format) for obj in data]
    barometricrpess = [float(obj['Barometric_Press'])for obj in data]

    ax.plot_date(dates, barometricrpess)

    date_format = mpl_dates.DateFormatter('%Y_%m_%d')
    plt.gca().xaxis.set_major_formatter(date_format)

    ax.tick_params(axis='x', which='major', labelsize = 6)
    plt.yticks(np.arange(22, 32, step=2))

    plt.subplots_adjust(bottom=0.2)
    
    def visualizeGraphStart(text):
        print("start")
        pass

    def visualizeGraphEnd(text):
        print("end")       
        pass

    axbox = fig.add_axes([0.1, 0.05, 0.3, 0.075])
    text_box = TextBox(axbox, "Start Point")
    text_box.on_submit(visualizeGraphStart)

    axbox2 = plt.axes([0.5, 0.05, 0.3, 0.075])
    text_box2 = TextBox(axbox2, "End Point")
    text_box2.on_submit(visualizeGraphEnd)

    #ax = plt.subplot(100)
    #tb = TextBox(ax, "Name:", initial="Jane Doe")
    #tb.label.set_color('red')      # label color
    #tb.text_disp.set_color('blue') # text inside the edit box
    #txtBox.on_submit(visualizeGraph)
    ## Add Textbox to search between the two points
    ## https://www.geeksforgeeks.org/matplotlib-textbox-widgets/
    plt.show()

if __name__ == '__main__':
    main()
