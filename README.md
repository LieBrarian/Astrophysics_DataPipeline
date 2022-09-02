# Astrophysics_DataPipeline
A summer research project that I want to attempt to take further than I was able to in that time. 

The code was originally designed to be used in conjunction with AIJ.
The process of making it more universal has begun with the _editable.py
This version is currently not working, as I made the mistake of adding most the features before testing them.
The _final.py is the version finished before editability was a question, it works great with AIJ and runs relatively quickly.

Some General Problems;
1) The full csv is used constantly, this can cause some slow downs sense the whole thing is getting read multiple times.
2) [Currently] only works with CSV files made by AIJ. A future part could be a new function that does some to all of that without help of AIJ.
3) No user interface, most astronomers don't know python so many may be scarred of or confused.
4) Bad naming. One thing I want to do after getting the editable version finished is make one with better naming conventions for variables.

The two csv files are ones made by AIJ from pictures I took over summer 2022. The main part of the project was to attempt to improve accuracy of finding exoplanets in urban inviroments. The two uploaded are good data (WASP-3 is slightly better) and though other data was gathered, the majority of it is hard or impossible to find anything of interest in. I am posting this here to hopefully have more people working on the code. For me, it's been a great learning experience with numpy pandas and statistical analysis in python. Before this the most major code I had written was a text adventure game for a school project.

Please keep in mind that this is unfinished code and is prone to errors. I have had multiple times where I had to restart the kernel to get things running again.

All functions have a "help" command, simply type in the function and "help" {example Process_mlt("help")} and the function will print out a brief explination of all variables and how they work. Bellow, those help commands will be printed.

_____________________________________________
The versions of the help commands shown are based on those of the editable version, only the final and editable have the help command working. The only difference for the help command in editable and final is the use of MainStarName and CompStarName which are not present in the final version.
_____________________________________________


Function median_fit:
1) Variables:
    a) dataframe; dataframe:
        i) datafraame object from pandas which is also imported in the function.
    b) version=0; int:
        -For version=0 y_data is a location i.e column name.
        -For version=1 y_data is the data in the form of an array, dataframe, or similar object.
    c) x_data="J.D.-2400000"; string:
        -Location of the column to be used for the x data. Must be the same size as y_data.
    d) y_data='rel_flux_SNR_T1; string,array,dataframe:
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
