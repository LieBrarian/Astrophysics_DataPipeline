import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time as t

def delete_useless(csv_full):
    csv_columns = csv_full.columns
    csv_columns=csv_columns.delete(0)
    delete_list=[]
    for i in range(len(csv_columns)):
        std,mean,ignore = acc(csv_full[csv_columns[i]])
        if std==0 or mean==0: delete_list.append(i)
        continue
    csv_columns_small = csv_columns.delete(delete_list)
    # make a new csv file with only first standard deviasion left from the already reduced column list
    csv_new = csv_full[csv_columns_small]
    return csv_new, csv_columns_small

def acc(part_chart):
    std = np.std(part_chart)
    mean = np.mean(part_chart)
    if mean==0 or std==0: std_mean=0
    else: std_mean = std/mean
    return std, mean, std_mean

def acc_stdmean(part_chart):
    std=np.std(part_chart)
    mean=np.mean(part_chart)
    return std, mean

def reduce_out_standard(values,cols,check):
    dataframe = pd.DataFrame(values,columns=cols)
    data=dataframe[check]
    delete=[]
    for points in range(4,len(data)-4):
        median=np.median(data.values[range(points-4, points+5)])
        std=np.std(data.values[range(points-4, points+5)])
        for i in range(points-4, points+5):
            if data.values[i]>median+3*std: delete.append(i)
            if data.values[i]<median-3*std: delete.append(i)
    dataframe=dataframe.drop(delete)        
    return dataframe

def find_difference_bme(set,scan_area):
    length=len(set)
    middle=round(length/2)
    scan_area_half=round(scan_area/2)-1
    val_big=np.median(set.values[range(scan_area)])
    val_mid=np.median(set.values[range(middle-scan_area_half,middle+scan_area_half)])
    val_end=np.median(set.values[range(length-scan_area,length)])
    return val_big,val_mid,val_end

def usefull_2(x,y):
    # difference
    if x-y < 0: 
        dif=y-x
        dif_per=((y-x)/y)*100
        dif_sum=(y-x)/(y+x)
    else: 
        dif=x-y
        dif_per=((x-y)/x)*100
        dif_sum=(x-y)/(x+y)
    return dif,dif_per,dif_sum

def median_plot(dataset,cuts=10):
    # the point of the function is to plot how the median over the course of time changes
    sets = round(len(dataset)/cuts)-1
    if sets*cuts>len(dataset): print('to long you fool dumb dumb')
    data = np.zeros(cuts)
    for spot in range(cuts):
        start=sets*spot
        array_mean=np.zeros(cuts)
        for i in range(sets):
            array_mean[i:]+=dataset.values[i+start]
        data[spot]+=np.mean(array_mean)
    return data

def do_everything(file_position):
    start_count=t.time()
    csv_full = pd.read_csv(file_position)
    # make a list of the column names
    csv_columns = csv_full.columns
    csv_columns=csv_columns.delete(0)
    # delete the columns that don't have interesting data ie 'saturation, exposure time and more'
    csv_new, csv_columns_small = delete_useless(csv_full)
    csv_reduced=reduce_out_standard(csv_new,csv_columns_small,'rel_flux_SNR_T1')
    #    this is where the new csv file would be made as an easy way to save what has been done outside of memory to hopefully keep the program running faster
    #    or making it viable to process multiple csv's without having to restart the function every time
    flux_t1 = csv_reduced['rel_flux_SNR_T1']
    mom_big,mom_mid,mom_end=find_difference_bme(flux_t1,25)
    dif_mb,dif_percentage_mb,dif_sumation_mb=usefull_2(mom_big,mom_mid)
    dif_me,dif_percentage_me,dif_sumation_me=usefull_2(mom_mid,mom_end)
    median_over_time=median_plot(flux_t1,20)
    x=range(len(median_over_time))
    slope, y_inter=np.polyfit(x,median_over_time,1)
    plt.plot(x,slope*x+y_inter,'b-')
    plt.plot(x,median_over_time,'k*-')
    plt.show ###################################################
    plt.close()
    end_count=t.time()
    print(f'''---> differences in the middle to beggining
-dif={dif_mb}\t-dif%={dif_percentage_mb}%\t-dif using sum={dif_sumation_mb}
---> differences in the middle to end
-dif={dif_me}\t-dif%={dif_percentage_me}%\t-dif using sum={dif_sumation_me}
\n\n----->time it took={end_count-start_count}''')
    return

do_everything(r"C:\Users\guswo\Documents\Astronomy Pictures\06_09_2022 - WASP-3\csv\Measurements.csv")