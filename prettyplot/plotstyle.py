'''
Example color palettes:
http://repec.sowi.unibe.ch/stata/palettes/colors.html#cbrew
https://chartio.com/learn/charts/how-to-choose-colors-data-visualization/
'''

LINEWIDTH = 2 #default linewidth
CURSORWIDTH = 2
CURSORDOTSIZE = 4
YAXIS_WIDTH = 35 #allows alignment of y axis in vertically-stacked graphs
label_style = {'color': 'k', 'font-size': '10pt'} #'#191919'
title_style = {'color': 'k', 'size': '12pt'} #note: use size, not font-size
legend_label_style = {'color': 'k', 'size': '8pt'} #, 'bold': True, 'italic': False


#Color palettes for lines 
palette_1 = ['#1F77B4','#2CA02C','#D62728','#9467BD','#FAA43A'] #standard
# palette_2 = ['#1F77B4','#2CA02C','#D62728','#9467BD','#f7ce47'] 
palette_2 = ['#1F77B4','#2CA02C','#D62728','#9467BD','#f7d55b'] 
palette_3 = ['#00BFC4','#39B600','#ff5a51','#E76BF3','#ffa600'] #bright

#Inbuilt graph styles
style_white = {'background': '#FFFFFF', 'grid': '#c0c0c0', 'text': 'k', 'cursor': '#00ffff', 'linecolors': palette_1} 
style_grey = {'background': '#c0c0c0', 'grid': '#f2f2f2', 'text': 'k', 'cursor': '#ffff33', 'linecolors': palette_2}
style_dark = {'background': '#565656', 'grid': 'k', 'text': 'k', 'cursor': '#ffff33', 'linecolors': palette_3}
