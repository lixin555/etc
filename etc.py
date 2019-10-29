#!/usr/bin/env python
#ect.py
#Anaconda is recommended for users.
#The script is used to convert engineering stress-strain curve to true stress-strain curve.
#GNU General Public License v3.0
#Author: Li Xin, a graduate student studying Materials Science & Engineering in USTB
#Email: lixin@xs.ustb.edu.cn
#Reference: Liu Bing-yu,one diagrammatic solution on true stress-strain curve --analysis for necking process
import os
import pandas as pd
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
def select_inputfile():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title=u'Input File',filetypes=[('csv file', '.csv')])
    print('input path:',filepath)
    return filepath
def select_savefile():
    root = tk.Tk()
    root.withdraw()
    save_path = filedialog.asksaveasfilename(title=u'Save File',filetypes=[('csv file', '.csv')])+".csv"
    print('save path:',save_path)
    return save_path
print("**********ect.py**********")
print("a script to convert engineering stress-strain curve to ture stress-strain curve")
print("**********ect.py**********")
#input
print("Please input original gauge length(mm):")
gauge_length = float(input())
print("Please input original size of cross-section(mm^2)")
size_cross_section = float(input())
print("Please input final size of cross-section(mm^2)")
final_cross_section = float(input())
print("Please input the data file of engineering stress(.csv)")
print("Format: | strain / % | stress / MPa | displacement / mm | ***No header is needed*** ")
path = select_inputfile()
data_file = pd.read_csv(path, header = None, names = ["strain", "stress", "displacement"])
stress = data_file["stress"]
strain = data_file["strain"]
displacement = data_file["displacement"]
#find the max stress
maxn = 0
num = 0
for i in range(0,len(stress)):
    if stress[i] >= maxn:
        maxn = stress[i]
        num = i
print("Max Stress:" ,str(maxn),"Num", str(num))
print("Stran:",str(strain[num]),"Displacement:",str(displacement[num]))
#calculate Max stress size
max_size_cross_section = size_cross_section*gauge_length/(gauge_length+float(displacement[num]))
a = (final_cross_section - max_size_cross_section) / (float(displacement.iloc[-1]) - float(displacement[num]))
b = (max_size_cross_section * float(displacement.iloc[-1]) - float(displacement[num]) * final_cross_section) / (float(displacement.iloc[-1]) - float(displacement[num]))
print("Fitting curve:","Size =", a,"× Displacement +",b)
#calculate true strain
ture_strain = []
for i in range(0,len(stress)):
    ture_strain.append(np.log(float(strain[i]) * 0.01 + 1) *100)
data_file["ture_strain"] = ture_strain
#calculate ture stress of uniform deformation
ture_stress = []
for i in range(0,num):
    ture_stress.append(float(stress[i])*(float(strain[i])*0.01+1))
for i in range(num,len(stress)):
    ture_stress.append(float(stress[i])*size_cross_section/(a*float(displacement[i])+b))
data_file["ture_stress"] = ture_stress
#output
print("Please select the directory where you want to output data:")
out_path = select_savefile()
data_file.to_csv(out_path,index = False, header = True)
#plot the diagram
plt.title("Ture stress-strain curve") 
plt.xlabel("Strain / %") 
plt.ylabel("Stress / MPa")
plt.plot(ture_strain, ture_stress)
plt.show()
print("Work done")
print("**********ect.py**********")
os.system('pause')
