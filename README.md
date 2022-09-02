# Astrophysics_DataPipeline
A summer research project that I want to attempt to take further than I was able to in that time. 

The code was originally designed to be used in conjunction with AIJ.
The process of making it more universal has begun with the _editable.py.
This version is currently not working, as I made the mistake of adding most the features before testing them.
The _final.py is the version finished before editability was a question, it works great with AIJ and runs relatively quickly.

Some General Problems;
1) The full csv is used constantly, this can cause some slow downs sense the whole thing is getting read multiple times.
2) [Currently] only works with CSV files made during AIJ's process. A future part could be a new function that does some to all of that without help of AIJ.
3) No user interface, most astronomers don't know python so many may be scarred of or confused.
4) Bad naming. One thing I want to do after getting the editable version finished is make one with better naming conventions for variables.

The two csv files are ones made by AIJ from pictures I took over summer 2022. The main part of the project was to attempt to improve accuracy of finding exoplanets in
urban inviroments. The two uploaded are good data (WASP-3 is slightly better) and though other data was gathered, the majority of it is hard or impossible to find anything
of interest in. I am posting this here to hopefully have more people working on the code. For me, it's been a great learning experience with numpy pandas and statistical
analysis in python. Before this the most major code I had written was a text adventure game for a school project.

Please keep in mind that this is unfinished code and is prone to errors. I have had multiple times where I had to restart the kernel to get things running again.
