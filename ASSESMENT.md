Things I like:
    - The simplicity of the functions, most functions aren't very long and simply do what they say
    - Overall readability.
    - Variable naming, in my opnion comments were mostly unnecesary because the variable names describe what's going on
    - The use of mathematical lambda functions to precisely regulate certain variables. 
    - The MultiVarGrid class, it was heavily based on the Mesa Grid class however the base Mesa class wasn't able to accomdate with my needs. Additionally constructing a custom grid class forced me to look into the source code and understand the package more clearly. 
    - The oxygen spread function. Using relatively simple rules the spread looks very natural. see animation/spread.gif
    - The liveview feature. Although it slows down the program a lot.

Things I didn't like:
    - How the simulations are modified, due to time constraints paramters are changed via a python dictionary. 
    - Ineffiency of simulation. Lots of iterating over the grid. By adding a cache maybe speed could be preserved.
    -Visualization. Having two open two vscode tabs and a browser window was extremely janky.
    -Lack of measuring tools. Because of time constraints didn't add in any metrics.

Hardest challenges:
    -Figuring out the parameters. Had many more entities next to oxygen,fish and algae. Howver had to simply because dynamics would get too complicated.
    
    -Visualization, the longest part of the project I used heatmaps and turned them into gifs to preview how the model was working. Or I'd print out tables of text. These were a hastle to setup. In the case of the heatmap gif, it was not possible to view the processes during the model run. Additionally printed numbers are very hard to interpret.

    -Spread had a lot of potential implementations. First, using a multindex dataframe was considered. Afterwards it was conflicting how data should be stored at every step.
