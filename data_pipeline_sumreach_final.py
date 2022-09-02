import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.stats import sigma_clip, mad_std


def median_fit(
    dataframe,
    version=0,
    x_data="X(FITS)_T1",
    y_data="rel_flux_SNR_T1",
    sig=3,
    save_graph=False,
    name="test_graph",
    style=".png",
    delete_carry=False,
    delete=False
):
    if isinstance(dataframe, str):
        print(
            """         
Function median_fit:
    Variables:
        --dataframe; array, dataframe:
            +datafraame object from pandas which is also imported in the function.
        --version=0; integer:
            +For version=0 y_data is a location i.e column name.
            +For version=1 y_data is the data in the form of an array, dataframe, or similar object.
        --x_data='X(FITS)_T1); string:
            +Location of the column to be used for the x data. Must be the same size as y_data.
        --y_data='rel_flux_SNR_T1; string,array,dataframe:
            +Either the location of data in the dataframe object put as variable dataframe or the array/dataframe wanted.
        --sig=3; integer:
            +How many standard deviations points will need to be to not be included in output.
        --save_graph; True, False:
            +Whether or not the graph that can be created by this function is created and saved or not.
        --name='test_graph'; string:
            +If the graph is saved, this is the file name it will be saved under.
        --type='.png'; string beggining with '.':
            +The file type that the graph will be saved as using function matplotlib.pyplot.savefig().
    return:
        x: array of x values reduced to fit a median fit graph of y.
        y: array of y values reduced to not intclude points outside sig standard deviasions.
Use:
    Uses moving median method to erase the data that is so far from the median at every point. The hope is that this will get rid of many if not all outliars to help improve accuracy. This is used throughout the rest of the library to complete computations. The aim of making the function was to have more control and maybe even speed up the library as a whole. Not only did it make it easier to write but it condencesed the code by a lot. The very first finished draft was around 300 lines with minimal comments. Before writing the help commands the code was under 100 lines and much faster with all new functions that didnt' exists in the original version.
"""
        )
        return
    # the original version that can only work with a single set of data
    x = dataframe[x_data]
    if version == 0:
        y = dataframe[y_data]
    # version=1 is a way of inputting a very specific data that the user can change and control
    elif version == 1:
        y = y_data
    if delete == False:
        # sigma_clip creates an array of True and False where True is to be cut at False is kept
        filtered_data = sigma_clip(y, sigma=sig, maxiters=1, stdfunc=mad_std)
        # delete the .mask out of the original set to only have the 'good' data
        delete = []
        for i in range(len(y)):
            if filtered_data.mask[i] == True:
                delete.append(i)
            continue
    y = y.drop(delete)
    x = x.drop(delete)
    y = y.to_numpy()
    x = x.to_numpy()
    if save_graph == True:
        plt.plot(x, y, "+", color="#1f77b4", label="cut data")
        plt.xlabel("time")
        plt.ylabel("Flux SNR")
        plt.legend(loc=2, numpoints=1)
        plt.savefig(f"{name}{style}")
        plt.close()
    if delete_carry == False:
        return x, y
    else:
        return x, y, delete


def Pocess_sngl(
    file_position,
    custom_name=r"movin_median_plot_single",
    filetype=r".png",
    scale="linear",
):
    if file_position == "help":
        print(
            """            
Function Process_sngl:
    Variables:
        --file_position; raw string:
            +Path to csv file, should be rstring to make sure it functions correctly.
        --custom_name=r'movin_median_plot_single'; string:
            +The name the file should be saved under, will replace if a file of the same name already exists.  
        --filetype='.png'; string beggining with '.'
            +The file type that the graph will be saved as using function 
                matplotlib.pyplot.savefig().
        --scale=linear; string:
            +The scale of the y coordinate.
    return: 
        ++Does not return anything and instead does computation and saves everything as a file.
Use:
    The point of this function is to create and save a graph of the change in light-levels over time of a single star. This is not always directly the most useful but may sometimes be interesting or reveal something some of the more processed graphs cannot. This was the first function written and was a learning curve for me. In the process of writing it went rhougfh many different iterations. Once I had the single star version working, all others were sinple modifications to the same algorythm.
"""
        )
        return
    csv_full = pd.read_csv(file_position)
    time_line, moving_median = median_fit(csv_full)
    curve = np.polyfit(time_line, moving_median, deg=2)
    plt.plot(
        time_line, curve[0] * time_line ** 2 +
        curve[1] * time_line + curve[2], "b-"
    )
    plt.plot(time_line, moving_median, "k*")
    plt.yscale(scale)
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f"{custom_name}_{scale}{filetype}")
    plt.close()
    print(f"\n\nsaved as {custom_name}_{scale}{filetype}\n")
    return


def Process_mlt(
    file_position,
    comp_stars=0,
    style="sum",
    custom_name=r"ratio_movin_median_plot",
    filetype=r".png",
    scale="linear",
):
    if file_position == "help":
        print(
            """          
Function Process_mult:
    Variables:
        --file_position; raw string:
            +Path to csv file, should be rstring to make sure it functions correctly.
        --comp_stars=0; integer:
            +The number of comparative stars in the csv file or the number of comp stars wanted to use.
        --style='sum'; string, sum,mean:
            +Chooses how to combine all the comperative stars, either as a sum or as the mean for every frame in the set.
        --custom_name=r'ratio_moving_median_plot': raw string:
            +The name the file should be saved under, will replace if a file of the same name already exists.
        --filetype=r'.png'; string beggining with '.':
            +The file type that the graph will be saved as using function matplotlib.pyplot.savefig().
        --scale=linear; string:
            +The scale of the y coordinate.
    Return:
        ++Does not return anything and instead does computation and saves everything
            as a file.
Use:
    Process and complete the computation of the given file in an effort to find the change in brightness throughout a night to identify exoplanets orbiting those suns. _mult compares multiple stars in an effort to get rid of any variables that could be effecting individual frames. For instance if only a single star is taken into account there is a posibility that the enviroment got darker than lighter do to externalreasons but this will cause the grapoh to appear to have captured the exoplanet where one does not exist. By analyzing and multiple stars and looking at the ratio and how it changes, a more accurate model can be found with many external variables now being accounted for.
"""
        )
        return
    csv_full = pd.read_csv(file_position)
    main_star = csv_full["rel_flux_SNR_T1"]
    avg_star = np.zeros(len(main_star))
    for time in range(len(main_star)):
        for star in range(2, comp_stars + 2):
            avg_star[time] += csv_full[f"rel_flux_SNR_C{star}"][time]
        continue
    if style == "mean":
        avg_star /= comp_stars
    ratio_main_avg = main_star / avg_star
    time_line, moving_median = median_fit(
        csv_full, version=1, y_data=ratio_main_avg)
    curve = np.polyfit(time_line, moving_median, deg=2)
    plt.plot(
        time_line, curve[0] * time_line ** 2 +
        curve[1] * time_line + curve[2], "b-"
    )
    plt.plot(time_line, moving_median, "k*")
    plt.yscale(scale)
    # instead of showing and stopping the program try and save it instead
    plt.savefig(f"{custom_name}_{style}_{scale}{filetype}")
    plt.close()
    print(f"\n\nsaved as {custom_name}_{style}_{scale}{filetype}\n")
    return


def Process_stck(
    file_position,
    comp_stars=0,
    style="sum",
    custom_name=r"ratio_movin_median_plot_stacked",
    filetype=r".png",
    scale="linear",
):
    if file_position == "help":
        print(
            """          
Function Process_stack:
    Variables:
        --file_position; raw string:
            +Path to csv file, should be rstring to make sure it functions correctly.
        --comp_stars=0; integer:
            +The number of comparative stars in the csv file or the number of comp stars wanted to use.
        --style='sum'; string, sum,mean:
            +Chooses how to combine all the comperative stars, either as a sum or as the mean for every frame in the set.
        --custom_name=r'ratio_moving_median_plot': raw string:
            +The name the file should be saved under, will replace if a file of the same name already exists.
        --filetype=r'.png'; string beggining with '.':
            +The file type that the graph will be saved as using function matplotlib.pyplot.savefig().
        --scale=linear; string:
            +The scale of the y coordinate.
    Return:
        ++Does not return anything and instead does computation and saves everything as a file.   
Use:
    This function is a way to stack the two oher graphs possible to make to directly visually compare. The scientific use of this is minimal but it may sometimes be interesting and a useful way to show the importants of the ratio method for comparing stars.
"""
        )
        return
    csv_full = pd.read_csv(file_position)
    time_line_single, moving_median_single = median_fit(csv_full)
    minimum = min(moving_median_single)
    rang = max(moving_median_single) - minimum
    star_normalize = np.zeros(len(moving_median_single))
    for pos, data_point in enumerate(moving_median_single):
        star_normalize[pos] += (data_point - minimum) / rang
    moving_median_single = pd.DataFrame(data=star_normalize, columns=["set"])
    curve_single = np.polyfit(
        time_line_single, moving_median_single["set"], deg=2)
    main_star = csv_full["rel_flux_SNR_T1"]
    avg_star = np.zeros(len(main_star))
    for time in range(len(main_star)):
        for star in range(2, comp_stars + 2):
            avg_star[time] += csv_full[f"rel_flux_SNR_C{star}"][time]
        continue
    if style == "mean":
        avg_star[time] /= comp_stars
    ratio_main_avg = main_star / avg_star
    ratio_main_avg *= 10000
    minimum = min(ratio_main_avg)
    rang = max(ratio_main_avg) - minimum
    star_normalize = np.zeros(len(ratio_main_avg))
    for pos, data_point in enumerate(ratio_main_avg):
        star_normalize[pos] += (data_point - minimum) / rang
    ratio_main_avg = pd.DataFrame(data=star_normalize, columns=["set"])
    time_line, moving_median = median_fit(
        csv_full, version=1, y_data=ratio_main_avg)
    curve_mult = np.polyfit(time_line, moving_median, deg=2)
    plt.plot(time_line_single,
             moving_median_single["set"], "g*", label="single star")
    plt.plot(
        time_line_single,
        curve_single[0] * time_line_single ** 2
        + curve_single[1] * time_line_single
        + curve_single[2],
        "r-",
        label="best fit of single",
    )
    plt.plot(time_line, moving_median["set"], "k*", label="ratio of stars")
    plt.plot(
        time_line,
        curve_mult[0] * time_line ** 2 +
        curve_mult[1] * time_line + curve_mult[2],
        "b-",
        label="best fit of ratio",
    )
    plt.yscale(scale)
    plt.legend()
    plt.savefig(f"{custom_name}_{style}_{scale}{filetype}")
    plt.close()
    print(f"\n\nsaved as {custom_name}_{style}_{scale}{filetype}\n")
    return


def AxisPlots(
    file_position,
    comp_stars=1,
    figure_size=False,
    custom_name=r"Axis_plot",
    file_type=r".png"
):
    if file_position == "help":
        print("""
Function axis_plot:
    Variables:
        --  file_position; raw string:
            + Path to the csv file that will be processed by the function. Must be raw string or will not correctly process.
        --  comp_stars=1; integer:
            + the number of comperative stars that there are or that are waanted to use.
        -- figure_size=False; tuple:
            + a specified size for the figure to be made. If left False, will do an automatic size out of controll.
        --custom_name=r'ratio_moving_median_plot': raw string:
            +The name the file should be saved under, will replace if a file of the same name already exists.
        --filetype=r'.png'; string beggining with '.':
            +The file type that the graph will be saved as using function matplotlib.pyplot.savefig().
    Return:
        ++ Doesn't return anything but does save the figure made to the file type specified and with the name specified using the matplotlib.pyplot funtion .savefig()
        
Use:
    The use of this function is too create three graphs for multiple stars in the csv file. The first graph is just the graph of the light volume from each star. The second is a graph of the values of the calculated line of best fit. The third is then the correlation coefficient matrix of the main star to each star named in the graph.
    
              """)
        return
    csv_full = pd.read_csv(file_position)
    if figure_size != False:
        figure, axis = plt.subplots(comp_stars+1, 3, figsize=figure_size)
    else:
        figure, axis = plt.subplots(comp_stars+1, 3)
    timeline_T1, moving_median_T1, save_delete = median_fit(
        csv_full, y_data="rel_flux_SNR_T1", delete_carry=True)
    curve_T1 = np.polyfit(timeline_T1, moving_median_T1, deg=2)
    flux_T1 = np.zeros(len(moving_median_T1))
    for point in range(len(flux_T1)):
        flux_T1[point] += moving_median_T1[point] - \
            (curve_T1[0]*timeline_T1[point]**2 +
             curve_T1[1]*timeline_T1[point]+curve_T1[2])
    axis[0, 0].plot(timeline_T1, moving_median_T1, 'b.')
    axis[0, 1].plot(timeline_T1, flux_T1, 'b.')
    axis[0, 1].plot(timeline_T1, np.zeros(len(timeline_T1)), 'k')
    dataframe = pd.DataFrame(data=timeline_T1, columns=["XSET"])
    dataframe.insert(1, 'flux_T1', flux_T1)
    for star in range(2, comp_stars + 2):
        timeline_c, moving_median_c = median_fit(
            csv_full, y_data=f"rel_flux_SNR_C{star}", delete=save_delete)
        curve_c = np.polyfit(timeline_c, moving_median_c, deg=2)
        flux_c = np.zeros(len(flux_T1))
        for point in range(len(flux_T1)):
            flux_c[point] = moving_median_c[point] - \
                (curve_c[0] * timeline_c[point] ** 2 +
                 curve_c[1] * timeline_c[point] + curve_c[2])
        dataframe[f"flux_C{star}"] = flux_c
        axis[star-1, 0].plot(timeline_c, moving_median_c, 'b.')
        axis[star-1, 1].plot(timeline_c, flux_c, 'b.')
        axis[star-1, 1].plot(timeline_c, np.zeros(len(timeline_c)), 'k')
        flux_T1_c = np.vstack((flux_T1, flux_c))
        matrix = np.corrcoef(flux_T1_c, rowvar=False)
        plot = axis[star-2, 2].imshow(matrix, cmap='PiYG')
        axis[star-2, 2].set_title(f"Flux_T1 correlation to Flux_C{star}")
        position = axis[star-2, 2]
        figure.colorbar(plot, ax=position)
    plt.savefig(f"{custom_name}{file_type}")
    plt.close()
    print(f"\n\nsaved as {custom_name}{file_type}\n")
    return


AxisPlots(r"C:\Users\guswo\Documents\Astronomy Pictures\06_09_2022 - WASP-3\csv\Measurements.csv",
          comp_stars=5, custom_name=r"Trial_graph", figure_size=(16, 20))