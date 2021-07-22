'''
Example color palettes:
http://repec.sowi.unibe.ch/stata/palettes/colors.html#cbrew
https://chartio.com/learn/charts/how-to-choose-colors-data-visualization/
'''

LINEWIDTH = 2 #default linewidth
CURSORWIDTH = 2
YAXIS_WIDTH = 35 #allows alignment of y axis in vertically-stacked graphs
label_style = {'color': 'k', 'font-size': '10pt'} #'#191919'
title_style = {'color': 'k', 'size': '12pt'} #note: use size, not font-size
legend_label_style = {'color': 'k', 'size': '8pt'} #, 'bold': True, 'italic': False


#Color palettes for lines
palette_1 = ['#1F77B4', '#2CA02C', '#9467BD', '#D62728'] #standard
palette_1_light = ['#AEC7E8', '#C5B0D5', '#98DF8A', '#FF9896']
palette_2 = ['#F8766D', '#D89000', '#39B600', '#00BFC4', '#E76BF3'] #bright

#Inbuilt graph styles
style_white = {'background': '#FFFFFF', 'grid': '#c0c0c0', 'text': 'k', 'cursor': '#00ffff', 'linecolors': palette_1} 
style_grey = {'background': '#c0c0c0', 'grid': '#f2f2f2', 'text': 'k', 'cursor': '#ffff33', 'linecolors': palette_1}
style_dark = {'background': '#565656', 'grid': 'k', 'text': 'k', 'cursor': 'White', 'linecolors': palette_2}
