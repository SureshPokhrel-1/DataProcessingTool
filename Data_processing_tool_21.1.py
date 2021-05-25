# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:19:50 2021

@author: supokhrel
"""

Height = 450
Width = 650

Data_res_1_opt = [ "1", "2","3","4","5", "7", "10", "15", "20", "30", "45", "60"]
Data_res_2_opt = [ "Minute", "Hour","Day","Month","Year"]

Hour_opt = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

Min_opt = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
           "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
           "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
           "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
           "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
           "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]

Slice_YES_NO = ["NO", "YES"]
Stats_Yes_NO = ["NO", "YES"]

Stats_type_opt = ["Mean", "Mode", "SD" ,"Percentile", "Sum", "Min-Max"]

Stats_period_1_opt = [ "1", "2","3","4", "5","7", "10", "15", "20", "30", "45", "60"]
Stats_period_2_opt = [ "Minute", "Hour","Day","Month","Year"]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


import tkinter as tkt
from tkinter import filedialog 
from tkcalendar import DateEntry
from tkinter import ttk
import os
from datetime import datetime
   

File_Path = '' 

window = tkt.Tk()
window.title("Data Processing Tool v21.1 (Beta)")
window.focus_set()

canvas = tkt.Canvas(window, height = Height , width = Width )
canvas.pack()
#canvas.focus()

frame = tkt.Frame(window, bg = 'skyblue', bd = 0)
frame.place(relx = 0.05, rely = 0.05, relheight = 0.85, relwidth = 0.9)
#frame.focus()

var = tkt.StringVar()
var.set('Press Run after the required entries are filled')
lbl_finish = tkt.Label(frame, textvariable=var, fg = 'darkgreen')
lbl_finish.place(relx = 0.25, rely = 0.92, relheight = 0.05, relwidth = 0.65)

init_dir = os.getcwd()

def browseFiles(): 
    global File_Path
    global init_dir
    filename = filedialog.askopenfilename(initialdir = init_dir, 
                                          title = "Select a File", 
                                          filetypes = (("CSV files", 
                                                        "*.csv*"), 
                                                       )) 
    if (filename != ''):
        label_file_explorer.configure(text = filename, fg = 'black') 
        File_Path = filename
        var.set('')
        window.update()
    #    sleep(5)
        var.set('Press Run after the required entries are filled')
        init_dir = os.path.dirname(os.path.abspath(filename))
    else:
        label_file_explorer.configure(text="!!!File Not Selected", fg = 'crimson')
        File_Path = ''
        var.set('')
        window.update()
    #    sleep(5)
        var.set('Press Run after the required entries are filled')
label_msz = ''


def Data_process(): 
    import time
    start_time = time.time()
    import pandas as pd
    import glob
    import numpy as np
    
    
    File = glob.glob(File_Path)

    if not File:

        var.set('')
        window.update()
    
        var.set('Error: No input file selected.')
        return 0
        

    var.set('')
    window.update()
    var.set('Processing: Reading User inputs')
    window.update()   
    
    Data_res_1 = Data_res_1_.get()
    Data_res_2 = Data_res_2_.get()
    
    Slice_status = Slice_status_.get()
    Start_date_str = cal_start.get() + " " + Start_hour_Menu.get() + ":" + Start_min_Menu.get()
    End_date_str = cal_end.get() + " " + End_hour_Menu.get() + ":" + End_min_Menu.get()
    
    Stats_status = Stats_status_.get()
    Stats_type = Stats_type_.get()
    Stats_period_1 = Stats_period_1_.get()
    Stats_period_2 = Stats_period_2_.get()
#    Q_val = 1
    Q_val = Q_entry.get()
    
    if(Stats_status == 'YES' and Stats_type == 'Percentile'):
        
        
        if(Q_val != '' and is_number(Q_val)):
            
            Q_val = float(Q_val)
            Q_val = Q_val/100
            if(Q_val < 0.0 or Q_val > 1.0):
                var.set('')
                window.update()
            
                var.set('Error!! Please enter valid percentile value (0-100)')
                window.update()  
                return 0
        else:
            var.set('')
            window.update()
        
            var.set('Error!! Please enter valid percentile value (0-100)')
            window.update()  
            return 0
            
    if(Data_res_2 == 'Minute'):
        Data_res = Data_res_1 + 'T'
    elif(Data_res_2 == 'Hour'):
        Data_res = Data_res_1 + 'H'
    elif(Data_res_2 == 'Day'):
        Data_res = Data_res_1 + 'D'
    elif(Data_res_2 == 'Month'):
        Data_res = Data_res_1 + 'M'
    elif(Data_res_2 == 'Year'):
        Data_res = Data_res_1 + 'Y'
        
    if(Slice_status == 'YES'):
        Start_date = pd.to_datetime(Start_date_str)
        End_date = pd.to_datetime(End_date_str)
        if(End_date < Start_date):
            var.set('')
            window.update()
            var.set('Error!! End Date is earlier than Start Date')
            window.update()
            return 0
    
    df = pd.DataFrame()
    var.set('')
    window.update()
    var.set('Processing: Reading input file')
    window.update()
    try:
        df = pd.concat([pd.read_csv(fp, low_memory=False) for fp in File], ignore_index=True)
    except:
        var.set('')
        window.update()
        var.set('Error!! Invalid content in the input file')
        window.update()
        return 0
    
    var.set('')
    window.update()
    var.set('Processing: Reading Timestamps')
    window.update()
    try:
        df.insert(0, 'Date_temp', pd.to_datetime(df[df.columns[0]]))
    except:
        var.set('')
        window.update()
        var.set('Error!! Invalid or unsupported TimeStamp in the input file')
        window.update()
        return 0
    df.drop(columns=[df.columns[1]], inplace = True)
    df.rename(columns = {'Date_temp':'Date'}, inplace = True)
    df.drop_duplicates(subset='Date', keep = 'last', inplace = True)
    df = df.sort_values(by='Date')
    df = df.set_index(['Date']).asfreq(Data_res)
    
    if(Slice_status == 'YES'):
        var.set('')
        window.update()
        var.set('Processing: Data Slicing')
        window.update()
        df = df.truncate(before=Start_date, after=End_date)
    
    Inital_cols = len(df.columns)
    for i in range(0, Inital_cols):
        df[df.columns[i]] = pd.to_numeric(df[df.columns[i]], errors='coerce')
        if(Stats_status == 'YES'):
            Data_Percent = '%_'
            DAP = Data_Percent+df.columns[i]
            df[DAP] = (~np.isnan(df[df.columns[i]])).astype(int)
            
            
    if(Stats_status == 'YES'):
        var.set('')
        window.update()
        var.set('Processing: Performing Statistics and Calculations')
        window.update()
        if(Stats_period_2 == 'Minute'):
            Stats_period = Stats_period_1 + 'T'
        elif(Stats_period_2 == 'Hour'):
            Stats_period = Stats_period_1 + 'H'
        elif(Stats_period_2 == 'Day'):
            Stats_period = Stats_period_1 + 'D'
        elif(Stats_period_2 == 'Month'):
            Stats_period = Stats_period_1 + 'M'
        elif(Stats_period_2 == 'Year'):
            Stats_period = Stats_period_1 + 'Y'
       
        df_1 = pd.DataFrame()
        try:
            df_1 = df.resample(Stats_period).mean()
        except:
            var.set('')
            window.update()
            var.set('Error!! Could not perform Statistics-Mean')
            window.update()
            return 0
        Final_cols = len(df.columns)
        for i in range(Inital_cols, Final_cols):
            df_1[df_1.columns[i]] = df_1[df_1.columns[i]]*100
            df_1[df_1.columns[i]] = df_1[df_1.columns[i]].round(decimals = 1)
        
        if(Stats_type == 'Mean'):
            df = df_1
        else:
            df_1.drop(list(df_1)[0:Inital_cols], inplace = True, axis = 1)                
            df.drop(list(df)[Inital_cols:], inplace = True, axis = 1) 
            
            if(Stats_type == 'Sum'):
                try:
                    df = df.resample(Stats_period).sum()
                except:
                    var.set('')
                    window.update()
                    var.set('Error!! Could not perform Statistics-Sum')
                    window.update() 
                    return 0
            elif(Stats_type == 'Mode'):
                import scipy.stats as st
                try:
                    df = df.resample(Stats_period).apply(lambda x: st.mode(x)[0])
                except:
                    var.set('')
                    window.update()
                    var.set('Error!! Could not perform Statistics-Mode')
                    window.update() 
                    return 0
            elif(Stats_type == 'SD'):
                try:
                    df = df.resample(Stats_period).std()
                except:
                    var.set('')
                    window.update()
                    var.set('Error!! Could not perform Statistics-SD')
                    window.update()
                    return 0
            elif(Stats_type == 'Percentile'):
                try:
                    df = df.resample(Stats_period).apply(lambda x: x.quantile(Q_val))
                except:
                    var.set('')
                    window.update()
                    var.set('Error!! Could not perform Statistics-Percentile')
                    window.update()
                    return 0
            elif(Stats_type == 'Min-Max'):
                try:
                    df = df.resample(Stats_period).agg(['min', 'max'])
                except:
                    var.set('')
                    window.update()
                    var.set('Error!! Could not perform Statistics- Min-Max')
                    window.update()
                    return 0
            
            df = pd.concat([df, df_1], axis=1, join='outer').reindex(df.index)
            
        if(Stats_period_2 == 'Month'):
            df = df.reset_index()
#            print(df)
            df[df.columns[0]] = df[df.columns[0]].apply(lambda x: x.strftime('%Y-%m'))
            df.set_index(df.columns[0], inplace=True)
            
    var.set('')
    window.update()
    var.set('Processing: Writing results in a new file')
    window.update()
    InputFolder_path = os.path.dirname(os.path.abspath(File_Path)) 
    InputFileName = os.path.basename(File_Path)
    now = datetime.now()
    dt_string = now.strftime("%b-%d-%Y_%H-%M-%S")
    Output_FilePath = InputFolder_path + '/'+ dt_string+ '_' + InputFileName 
    df.to_csv(Output_FilePath, index= True)
    
    Total_time = round (time.time()-start_time, 2)
#    print(Total_time)
    var.set('')
    window.update()
#    sleep(5)
    var.set('Successfully Completed: '+ ' Time Taken = ' + str(Total_time) + ' Sec')
    window.update()
    print('\a')
    os.startfile(InputFolder_path)

########################################### GUI #########################################################
 
label = tkt.Label(frame, text = 'Input File :', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.02, relheight = 0.05, relwidth = 0.12)

label_file_explorer = tkt.Label(frame,text = "", fg = "Green") 
label_file_explorer.place(relx = 0.15, rely = 0.02, relheight = 0.05, relwidth = 0.70) 

button_explore = tkt.Button(frame,  text = "Browse", command = browseFiles, fg = 'red') 
button_explore.place(relx = 0.88, rely = 0.02, relheight = 0.05, relwidth = 0.1)

label = tkt.Label(frame, text = 'Input Data Resolution', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.11, relheight = 0.05, relwidth = 0.22)

Data_res_1_ = tkt.StringVar(frame)
Data_res_1_.set(Data_res_1_opt[0])
Data_res_1_Menu = tkt.OptionMenu(frame, Data_res_1_, *Data_res_1_opt)
Data_res_1_Menu.place(relx = 0.25, rely = 0.11, relheight = 0.06, relwidth = 0.1)

Data_res_2_ = tkt.StringVar(frame)
Data_res_2_.set(Data_res_2_opt[0])
Data_res_2_Menu = tkt.OptionMenu(frame, Data_res_2_, *Data_res_2_opt)
Data_res_2_Menu.place(relx = 0.37, rely = 0.11, relheight = 0.06, relwidth = 0.15)

label = tkt.Label(frame, text = 'Data Slicing Required ?', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.32, relheight = 0.05, relwidth = 0.22)

################################################################################
label_1 = tkt.Label(frame, text = 'Start Date', fg = 'black', bg = 'skyblue')


label_2 = tkt.Label(frame, text = '(mm/dd/yyyy)', fg = 'black', bg = 'skyblue')

label_3 = tkt.Label(frame, text = '(hh)', fg = 'black', bg = 'skyblue')

label_4 = tkt.Label(frame, text = '(mm)', fg = 'black', bg = 'skyblue')

Date = datetime.now()
Year = int(Date.strftime("%Y"))
Month = int(Date.strftime("%m"))
Day = int(Date.strftime("%d"))

cal_start = DateEntry(frame,bg="darkblue",fg="white",year=Year, month = Month, day = Day, date_pattern = 'm/d/y', state = "readonly" )

Start_hour_= tkt.StringVar(frame)
Start_hour_.set(Hour_opt[0])
Start_hour_Menu = ttk.Combobox(frame, textvariable = Start_hour_, values =  Hour_opt, state = "readonly")

label_5 = tkt.Label(frame, text = ':', fg = 'black', bg = 'skyblue')

Start_min_= tkt.StringVar(frame)
Start_min_.set(Min_opt[0])
Start_min_Menu = ttk.Combobox(frame, textvariable = Start_min_, values =  Min_opt, state = "readonly")

label_6 = tkt.Label(frame, text = 'End Date', fg = 'black', bg = 'skyblue')

cal_end = DateEntry(frame,bg="darkblue",fg="white",year=Year, month = Month, day = Day, date_pattern = 'm/d/y', state = "readonly")

End_hour_= tkt.StringVar(frame)
End_hour_.set(Hour_opt[23])
End_hour_Menu = ttk.Combobox(frame, textvariable = End_hour_, values =  Hour_opt, state = "readonly")

label_7 = tkt.Label(frame, text = ':', fg = 'black', bg = 'skyblue')

End_min_= tkt.StringVar(frame)
End_min_.set(Min_opt[59])
End_min_Menu = ttk.Combobox(frame, textvariable = End_min_, values =  Min_opt, state = "readonly")

def slice_status():
    if(Slice_status_.get() == 'YES'):
        label_1.place(relx =0.38, rely = 0.25, relheight = 0.05, relwidth = 0.20)
        label_2.place(relx =0.52, rely = 0.19, relheight = 0.05, relwidth = 0.20)
        label_3.place(relx =0.74, rely = 0.19, relheight = 0.05, relwidth = 0.05)
        label_4.place(relx =0.82, rely = 0.19, relheight = 0.05, relwidth = 0.07)
        cal_start.place(relx =0.55, rely = 0.255, relheight = 0.05, relwidth = 0.15)
        Start_hour_Menu.place(relx = 0.73, rely = 0.25, relheight = 0.06, relwidth = 0.07)
        label_5.place(relx =0.80, rely = 0.25, relheight = 0.06, relwidth = 0.02)
        Start_min_Menu.place(relx = 0.82, rely = 0.25, relheight = 0.06, relwidth = 0.07)
        label_6.place(relx =0.38, rely = 0.4, relheight = 0.05, relwidth = 0.20)
        cal_end.place(relx =0.55, rely = 0.4, relheight = 0.05, relwidth = 0.15)
        End_hour_Menu.place(relx = 0.73, rely = 0.395, relheight = 0.06, relwidth = 0.07)
        label_7.place(relx =0.80, rely = 0.395, relheight = 0.06, relwidth = 0.02)
        End_min_Menu.place(relx = 0.82, rely = 0.395, relheight = 0.06, relwidth = 0.07)
    else:
        label_1.place_forget()
        label_2.place_forget()
        label_3.place_forget()
        label_4.place_forget()
        label_5.place_forget()
        label_6.place_forget()
        label_7.place_forget()
        cal_start.place_forget()
        Start_hour_Menu.place_forget()
        Start_min_Menu.place_forget()
        cal_end.place_forget()
        End_hour_Menu.place_forget()
        End_min_Menu.place_forget()

Slice_status_= tkt.StringVar(frame)
Slice_status_.set(Slice_YES_NO[0])
Slice_status_Menu = tkt.OptionMenu(frame, Slice_status_, *Slice_YES_NO, command= lambda event: slice_status())
Slice_status_Menu.place(relx = 0.24, rely = 0.32, relheight = 0.06, relwidth = 0.10)

#################################################Start###########################################

label = tkt.Label(frame, text = 'Statistics Required ?', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.62, relheight = 0.05, relwidth = 0.22)

label_stats = tkt.Label(frame, text = 'Statistics types', fg = 'black', bg = 'skyblue')

Q_label = tkt.Label(frame, text = 'Percentile (0-100)%', fg = 'black', bg = 'skyblue')

Q_entry = tkt.Entry(frame)


def Stats_type():
#    print("Option ")
    if (Stats_type_.get() == 'Percentile' ):
        Q_label.place(relx =0.28, rely = 0.72, relheight = 0.06, relwidth = 0.20)
        Q_entry.place(relx = 0.485, rely = 0.72, relheight = 0.05, relwidth = 0.07)
        
    else:
        Q_label.place_forget()
        Q_entry.place_forget()


Stats_type_ = tkt.StringVar(frame)
Stats_type_.set(Stats_type_opt[0])
Stats_type_Menu = tkt.OptionMenu(frame, Stats_type_, *Stats_type_opt,command= lambda event: Stats_type())

Stats_period_1_ = tkt.StringVar(frame)
Stats_period_1_.set(Stats_period_1_opt[0])
Stats_period_1_Menu = tkt.OptionMenu(frame, Stats_period_1_, *Stats_period_1_opt)

Stats_period_2_ = tkt.StringVar(frame)
Stats_period_2_.set(Stats_period_2_opt[2])
Stats_period_2_Menu = tkt.OptionMenu(frame, Stats_period_2_, *Stats_period_2_opt)

def Stats_status():
    if (Stats_status_.get() == 'YES'):
#        print()
        label_stats.place(relx =0.35, rely = 0.56, relheight = 0.06, relwidth = 0.20)
        Stats_type_Menu.place(relx = 0.38, rely = 0.62, relheight = 0.06, relwidth = 0.18)
        Stats_period_1_Menu.place(relx = 0.6, rely = 0.62, relheight = 0.06, relwidth = 0.1)
        Stats_period_2_Menu.place(relx = 0.72, rely = 0.62, relheight = 0.06, relwidth = 0.15)
        if (Stats_type_.get() == 'Percentile' ):
            Q_label.place(relx =0.28, rely = 0.72, relheight = 0.06, relwidth = 0.20)
            Q_entry.place(relx = 0.485, rely = 0.72, relheight = 0.05, relwidth = 0.07)
    else:
        print()
        label_stats.place_forget()
        Stats_type_Menu.place_forget()
        Stats_period_1_Menu.place_forget()
        Stats_period_2_Menu.place_forget()
        Q_label.place_forget()
        Q_entry.place_forget()
    

Stats_status_= tkt.StringVar(frame)
Stats_status_.set(Stats_Yes_NO[0])
Stats_status_Menu = tkt.OptionMenu(frame, Stats_status_, *Stats_Yes_NO ,command= lambda event: Stats_status())
Stats_status_Menu.place(relx = 0.24, rely = 0.62, relheight = 0.06, relwidth = 0.10)

#########################################################################################################

bt = tkt.Button(frame, text = 'RUN', bg = 'coral', fg = 'blue', command = Data_process )
bt.place(relx = 0.05, rely = 0.90, relheight = 0.08, relwidth = 0.08)

label = tkt.Label(frame, text = 'Message:', fg = 'saddlebrown', bg = 'skyblue', font = ("Helvetica",9,'bold'))
label.place(relx = 0.45, rely = 0.86, relheight = 0.05, relwidth = 0.22)

label = tkt.Label(window, text = 'Developed by Suresh, ICIMOD', fg = 'grey')
label.place(relx = 0.64, rely = 0.95, relheight = 0.05, relwidth = 0.45)

window.bind_all("<1>", lambda event:event.widget.focus_set())

window.mainloop()
