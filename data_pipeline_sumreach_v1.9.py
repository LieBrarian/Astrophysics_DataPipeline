import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial import polynomial as P
import scipy.stats as stats
from astropy.stats import sigma_clip, mad_std
import time as t

def delete_useless(csv_full): 
    # Find any useless data by saving the position of the columns with no useful information
    # and use the built in function for pandas.delete(['list'])
    csv_columns = csv_full.columns
    csv_columns=csv_columns.delete(0)
    delete_list=[]
    for i in range(len(csv_columns)):
        std,ignore0,median,ignore1 = acc(csv_full[csv_columns[i]])
        if std==0 or median==0: delete_list.append(i)
        continue
    csv_columns_small = csv_columns.delete(delete_list)
    # make a new csv file with only first standard deviasion left from the already reduced column list
    csv_new = csv_full[csv_columns_small]
    return csv_new, csv_columns_small

def acc(part_chart):
    # Was built for an earlier version and may soon be replaced or deleted
    std = np.std(part_chart)
    mean = np.mean(part_chart)
    median = np.median(part_chart)
    if mean==0 or std==0: std_mean=0
    else: std_mean = std/mean
    return std, mean, median, std_mean

def acc_stdmean(part_chart):
    # same as function acc it may be replaced or deleted in future
    std=np.std(part_chart)
    mean=np.mean(part_chart)
    return std, mean

def reduce_out_standard(values,cols,check,steps=3):
    # gets rid of any data outside some value of standard deviations with a default of 3
    dataframe = pd.DataFrame(values,columns=cols)
    data=dataframe[check]
    delete=[]
    for points in range(4,len(data)-4):
        median=np.median(data.values[range(points-4, points+5)])
        std=np.std(data.values[range(points-4, points+5)])
        for i in range(points-4, points+5):
            if data.values[i]>median+steps*std: delete.append(i)
            if data.values[i]<median-steps*std: delete.append(i)
    dataframe=dataframe.drop(delete)        
    return dataframe

def find_difference_bme(set,scan_area):
    # Finds the diference values of the beggining middle and end
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

# Moving median and saving the values but not making a line of best fit as of yet
def median_fit(dataframe,x_pos='X(FITS)_T1',y_pos='rel_flux_SNR_T1',show_crossed=False):
    # will try and use astropy function to do the same as median_plot and see which is better
    x=dataframe[x_pos]
    y=dataframe[y_pos]
    
    filtered_data = sigma_clip(y, sigma=3, maxiters=1, stdfunc=mad_std)
    # plot the original and rejected data
    if show_crossed==True:
        plt.figure(figsize=(8,5))
        plt.plot(x, y, '+', color='#1f77b4', label="original data")
        plt.plot(x[filtered_data.mask], y[filtered_data.mask], 'x',
                color='#d62728', label="rejected data")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc=2, numpoints=1)
        plt.savefig(f'marked_cut_data.png')
        plt.close()
        
    plt.figure(figsize=(8,5))
    delete=[]
    for i in range(len(y)):
        if filtered_data.mask[i]==True: 
            delete.append(i)
    y=y.drop(delete)
    x=x.drop(delete)    
    plt.plot(x, y, '+', color='#1f77b4', label="cut data")
    plt.xlabel('time')
    plt.ylabel('Flux SNR')
    plt.legend(loc=2, numpoints=1)
    plt.savefig(f'001_t1_new_try.png')
    plt.close()
    
    # Try and find a way to take out the filtered out points
    
    return x,y

def do_everything_T1(file_position):
    start_count=t.time() # timing is only used in debugging and will be deleted in final version
    csv_full = pd.read_csv(file_position)
    time_line,moving_median=median_fit(csv_full)
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f't1_movingmedian_plot.png')
    plt.close()
    end_count=t.time()
    print(f'\n\n-----> time it took => {end_count-start_count}\n\n')
    return 'done'

def do_everything_all(file_position, comp_stars=1,style='sum'):
    start_count=t.time() # timing is only used in debugging and will be deleted in final version
    csv_full = pd.read_csv(file_position)
    main_star=csv_full['rel_flux_SNR_T1']
    avg_star=np.zeros(len(main_star))
    for time in range(len(main_star)):
        for star in range(2,comp_stars+2):
            avg_star[time]+=csv_full[f'rel_flux_SNR_C{star}'][time]
            continue
        if style=='mean': avg_star[time]/=comp_stars
        continue
    ratio_main_avg=main_star/avg_star
    x_axis=csv_full['X(FITS)_T1']
    plt.plot(x_axis,ratio_main_avg, 'k*')
    plt.savefig(f'ratio_mainavg_standard_{style}.png')
    plt.close()
    plt.plot(x_axis,ratio_main_avg, 'k*')
    plt.yscale('log')
    plt.savefig(f'ratio_mainavg_log_{style}.png')
    plt.close()
    end_count=t.time()
    print(f'\n\n-----> time it took => {end_count-start_count}\n\n')
    return 'done'
    
do_everything_all(r"C:\Users\guswo\Documents\Astronomy Pictures\06_09_2022 - WASP-3\csv\Measurements.csv",comp_stars=5,style='sum')