import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# import scipy.stats as stats
from astropy.stats import sigma_clip, mad_std
import time as t

# Moving median and saving the values but not making a line of best fit as of yet
def median_fit(dataframe,version=0,x_pos='X(FITS)_T1',y_pos='rel_flux_SNR_T1',show_crossed=False):
    # will try and use astropy function to do the same as median_plot and see which is better
    if version==0:
        x=dataframe[x_pos]
        y=dataframe[y_pos]
        
        filtered_data = sigma_clip(y, sigma=3, maxiters=1, stdfunc=mad_std)
        # plot the original and rejected data
        if show_crossed==True:
            plt.plot(x, y, '+', color='#1f77b4', label="original data")
            plt.plot(x[filtered_data.mask], y[filtered_data.mask], 'x',
                    color='#d62728', label="rejected data")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend(loc=2, numpoints=1)
            plt.savefig(f'marked_cut_data_T1.png')
            plt.close()
            
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
        plt.savefig(f'T1_cut_data.png')
        plt.close()
        
    elif version==1:
        x=dataframe[x_pos]
        y=y_pos
        filtered_data = sigma_clip(y, sigma=3, maxiters=1, stdfunc=mad_std)
        if show_crossed==True:
            plt.plot(x, y, '+', color='#1f77b4', label="original data")
            plt.plot(x[filtered_data.mask], y[filtered_data.mask], 'x',
                    color='#d62728', label="rejected data")
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend(loc=2, numpoints=1)
            plt.savefig(f'marked_cut_data.png')
            plt.close()
            
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
    time_line,moving_median=median_fit(csv_full,1,y_pos=ratio_main_avg)
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f'ratio_movin_median_plot.png')
    plt.close()
    end_count=t.time()
    print(f'\n\n-----> time it took => {end_count-start_count}\n\n')
    return 'done'
    
do_everything_all(r"C:\Users\guswo\Documents\Astronomy Pictures\06_09_2022 - WASP-3\csv\Measurements.csv",comp_stars=5,style='sum')