import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.stats import sigma_clip, mad_std
import time as t

# Moving median and saving the values but not making a line of best fit as of yet
def median_fit(dataframe,version=0,x_data='X(FITS)_T1',y_data='rel_flux_SNR_T1',show_crossed=False,name='test_graph'):
    # the original version that can only work with a single set of data
    x=dataframe[x_data]
    if version==0:y=dataframe[y_data]
    # version=1 is a way of inputting a very specific data that the user can change and control  
    if version==1:y=y_data
    # sigma_clip creates an array of True and False where True is to be cut at False is safe
    filtered_data=sigma_clip(y, sigma=3, maxiters=1, stdfunc=mad_std)
    # plot the original and rejected data if wanted
    if show_crossed==True:
        plt.plot(x, y,'+',color='#1f77b4',label="original data")
        plt.plot(x[filtered_data.mask],y[filtered_data.mask],'x',color='#d62728',label="rejected data")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend(loc=2, numpoints=1)
        plt.savefig(f'marked_cut_data_T1.png')
        plt.close()
    # delete the .mask out of the original set to only have the 'good' data
    delete=[]
    for i in range(len(y)):
        if filtered_data.mask[i]==True: delete.append(i)
    y=y.drop(delete)
    x=x.drop(delete)
    plt.plot(x, y, '+', color='#1f77b4', label="cut data")
    plt.xlabel('time')
    plt.ylabel('Flux SNR')
    plt.legend(loc=2, numpoints=1)
    plt.savefig(f'{name}.png')
    plt.close()
    return x,y

def do_everything_T1(file_position,custom_name=r'movin_median_plot_single',filetype='.png'):
    csv_full = pd.read_csv(file_position)
    time_line,moving_median=median_fit(csv_full)
    curve=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line,curve[0]*time_line**2+curve[1]*time_line+curve[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f'{custom_name}{filetype}')
    plt.close()
    print(f'saved as {custom_name}')
    return 'done'

def do_everything_mult(file_position,comp_stars=0,style='sum',custom_name=r'ratio_movin_median_plot',filetype=r'.png'):
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
    print(f'saved as {custom_name}')
    return 'done'


# next step is to try and figure out how to stack them together
# so far it works through but doesn't actually make the correct picture
# as of now the 07/21/2022 and 
def do_everything_stack(file_position,comp_stars=0,style='sum',custom_name=r'ratio_movin_median_plot_stacked',filetype=r'.png'):
    csv_full=pd.read_csv(file_position)
    time_line_single,moving_median_single=median_fit(csv_full)
    minimum=min(moving_median_single)
    rang=max(moving_median_single)-minimum
    star_normalize=np.zeros(len(moving_median_single))
    for pos,data_point in enumerate(moving_median_single):star_normalize[pos]+=(data_point-minimum)/rang
    curve_single=np.polyfit(time_line_single,star_normalize,deg=2)
    main_star=csv_full['rel_flux_SNR_T1']
    avg_star=np.zeros(len(main_star))
    for time in range(len(main_star)):
        for star in range(2,comp_stars+2): avg_star[time]+=csv_full[f'rel_flux_SNR_C{star}'][time]
        if style=='mean': avg_star[time]/=comp_stars
        continue
    ratio_main_avg=main_star/avg_star
    time_line,moving_median=median_fit(csv_full,version=1,y_data=ratio_main_avg)
    curve_mult=np.polyfit(time_line,moving_median,deg=2)
    plt.plot(time_line_single,curve_single[0]*time_line_single**2+curve_single[1]*time_line_single+curve_single[2],'r-')
    plt.plot(time_line_single,star_normalize,'g*')
    plt.plot(time_line,curve_mult[0]*time_line**2+curve_mult[1]*time_line+curve_mult[2],'b-')
    plt.plot(time_line,moving_median,'k*')
    plt.savefig(f'{custom_name}_{style}{filetype}')
    plt.close()
    print(f'\n\nsaved as {custom_name}_{style}{filetype}\n')
    return 'done'

print(do_everything_stack(r'C:\Users\guswo\Documents\Astronomy Pictures\06_09_2022 - WASP-3\csv\Measurements.csv',style='mean',comp_stars=5,custom_name=r'final_version_possible_stack'))