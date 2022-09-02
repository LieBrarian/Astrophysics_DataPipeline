import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.stats import sigma_clip, mad_std
import time as t

# Moving median and saving the values but not making a line of best fit as of yet
def median_fit(dataframe,version=0,x_data='X(FITS)_T1',y_data='rel_flux_SNR_T1',show_crossed=False):
    # will try and use astropy function to do the same as median_plot and see which is better
    if version==0:
        x=dataframe[x_data]
        y=dataframe[y_data]
        filtered_data = sigma_clip(y, sigma=3, maxiters=1, stdfunc=mad_std)
        # plot the original and rejected data
        if show_crossed==True:
            plt.plot(x, y,'+',color='#1f77b4',label="original data")
            plt.plot(x[filtered_data.mask],y[filtered_data.mask],'x',color='#d62728',label="rejected data")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend(loc=2, numpoints=1)
            plt.savefig(f'marked_cut_data_T1.png')
            plt.close()
        delete=[]
        for i in range(len(y)):
            if filtered_data.mask[i]==True: delete.append(i)
        y=y.drop(delete)
        x=x.drop(delete)    
        plt.plot(x, y, '+', color='#1f77b4', label="cut data")
        plt.xlabel('time')
        plt.ylabel('Flux SNR')
        plt.legend(loc=2, numpoints=1)
        plt.savefig(f'T1_cut_data.png')
        plt.close()
        
    elif version==1:
        x=dataframe[x_data]
        y=y_data
        filtered_data = sigma_clip(y, sigma=3, maxiters=1, stdfunc=mad_std)
        if show_crossed==True:
            plt.plot(x, y, '+', color='#1f77b4', label="original data")
            plt.plot(x[filtered_data.mask],y[filtered_data.mask],'x',color='#d62728', label="rejected data")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend(loc=2, numpoints=1)
            plt.savefig(f'marked_cut_data.png')
            plt.close()
        delete=[]
        for i in range(len(y)): 
            if filtered_data.mask[i]==True: delete.append(i)
        y=y.drop(delete)
        x=x.drop(delete)    
        plt.plot(x, y, '+', color='#1f77b4', label="cut data")
        plt.xlabel('time')
        plt.ylabel('Flux SNR')
        plt.legend(loc=2, numpoints=1)
        plt.savefig(f'001_t1_new_try.png')
        plt.close()
    return x,y

def do_everything_T1(file_position,custom_name=r'movin_median_plot_single',filetype='.png'):
    start_count=t.time() # timing is only used in debugging and will be deleted in final version
    csv_full = pd.read_csv(file_position)
    time_line,moving_median=median_fit(csv_full)
    minimum=min(moving_median)
    rang=max(moving_median)-minimum
    star_normalize=np.zeros(len(moving_median))
    for data_point,pos in enumerate(moving_median):
        star_normalize[pos]+=(data_point-minimum)/rang
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f'{custom_name}{filetype}')
    plt.close()
    end_count=t.time()
    print(f'\n\n-----> time it took => {end_count-start_count}\n\n')
    return 'done'

def do_everything_mult(file_position,comp_stars=0,style='sum',custom_name=r'ratio_movin_median_plot',filetype=r'.png'):
    start_count=t.time() # timing is only used in debugging and will be deleted in final version
    csv_full=pd.read_csv(file_position)
    main_star=csv_full['rel_flux_SNR_T1']
    avg_star=np.zeros(len(main_star))
    for time in range(len(main_star)):
        for star in range(2,comp_stars+2): avg_star[time]+=csv_full[f'rel_flux_SNR_C{star}'][time]
        if style=='mean': avg_star[time]/=comp_stars
        continue
    ratio_main_avg=main_star/avg_star
    time_line,moving_median=median_fit(csv_full,version=1,y_data=ratio_main_avg)
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f'{custom_name}_{style}{filetype}')
    end_count=t.time()
    print(f'\n\n-----> time it took => {end_count-start_count}\n\n')
    return 'done'

def do_everything_stack(file_position,comp_stars=0,style='sum',custom_name=r'ratio_movin_median_plot_stacked',filetype=r'.png'):
    start_count=t.time() # timing is only used in debugging and will be deleted in final version
    csv_full=pd.read_csv(file_position)
    time_line,moving_median=median_fit(csv_full)
    minimum=min(moving_median)
    rang=max(moving_median)-min(moving_median)
    for i in moving_median:
        i=(i-minimum)/rang
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'r-')
    plt.plot(time_line,moving_median,'g*')
    main_star=csv_full['rel_flux_SNR_T1']
    avg_star=np.zeros(len(main_star))
    for time in range(len(main_star)):
        for star in range(2,comp_stars+2): avg_star[time]+=csv_full[f'rel_flux_SNR_C{star}'][time]
        if style=='mean': avg_star[time]/=comp_stars
        continue
    ratio_main_avg=main_star/avg_star
    time_line,moving_median=median_fit(csv_full,version=1,y_data=ratio_main_avg)
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f'{custom_name}_{style}{filetype}')
    end_count=t.time()
    print(f'\n\n-----> time it took => {end_count-start_count}\n\n')
    return 'done'

do_everything_T1(r"C:\Users\guswo\Documents\Astronomy Pictures\06_09_2022 - WASP-3\csv\Measurements.csv")