'''
Example color palettes:
http://repec.sowi.unibe.ch/stata/palettes/colors.html#cbrew
https://chartio.com/learn/charts/how-to-choose-colors-data-visualization/
'''

LINEWIDTH = 2 #default linewidth
CURSORWIDTH = 2
CURSORDOTSIZE = 4
YAXIS_WIDTH = 35 #allows alignment of y axis in vertically-stacked graphs
TITLE_HEIGHT = 30
LEGEND_OFFSET = 15 #both x and y

#Useful for creating palettes by name
colors = {
    'blue': '#1F77B4',
    'green': '#2CA02C',
    'red': '#D62728',
    'black': '#1b1b1b',
    'yellow': '#fad000',
    'white': '#ffffff',
    'purple': 'e76bf3'
}

#These are CSS parameters
axis_label_style = {'color': 'k', 'font-size': '10pt', 'font-weight': '500'} 
title_style = {'color': 'k', 'size': '12pt', 'font-weight': '500'} #note: use size, not font-size
legend_label_style = {'color': 'k', 'size': '8pt'} #, 'bold': True, 'italic': False

fonts = {'axis': 'Roboto', 'axis-tick': 'Roboto', 'title': 'Roboto', 'legend': 'Roboto'}

#Color palettes for lines 
palette_1 = ['#1F77B4','#2CA02C','#D62728','#9467BD','#FAA43A'] #standard
# palette_2 = ['#1F77B4','#2CA02C','#D62728','#9467BD','#f7ce47'] 
palette_2 = ['#1F77B4','#2CA02C','#D62728','#9467BD','#f7d55b'] 
palette_3 = ['#00BFC4','#39B600','#ed3012','#E76BF3','#ff7f0e', colors['yellow']] #bright palette used for dark theme
# Reds: 
# Old: ff5a51
# Tried: fc2605, f72504 good but too bright

#Candlestickpalettes
cp1 = cp2 = ['#2CA02C','#D62728']
cp3 = ['#39B600','#ed3012']

#Zoombox colors
zoom_yellow = [255, 255, 0, 80] #RGBA
zoom_blue = [0,177,242, 64]
zoom_green = [0,219,73,64]
# ligh_blue = 105,154,188,64


#Inbuilt graph styles
style_white = {'background': '#FFFFFF', 'grid': '#c0c0c0', 'text': 'k', 'cursor': '#00ffff', 'linecolors': palette_1, 'candlecolors': cp1, 'zoombox': zoom_blue} 
style_grey = {'background': '#c0c0c0', 'grid': '#f2f2f2', 'text': 'k', 'cursor': '#ffff33', 'linecolors': palette_2, 'candlecolors': cp2, 'zoombox': zoom_blue}
style_dark = {'background': '#565656', 'grid': 'k', 'text': 'k', 'cursor': '#ffff33', 'linecolors': palette_3, 'candlecolors': cp3, 'zoombox': zoom_blue}
