''' 
🌞 卐 Sρәτsgruρρα 卐 🌝
Department of Computer Science & Electronics
Trekking Hardware Analysis (Dept. of CSE) Project ∑oliταri Rәαρәr ( Main )
CO. L.Swarnajith (Project Lead)
'''

# Load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.kernel_regression import KernelReg
from PIL import Image, ImageDraw
from datetime import datetime

# Read file
def read_data(file_name):
    csv_data = pd.read_csv(file_name)
    return csv_data['entry'], csv_data['utc'], csv_data['temperature'], csv_data['pressure'], csv_data['balt'], csv_data['galt'], csv_data['lat'], csv_data['lon']

# Single Variable Plotter
def singlePlot(fig, x, y, title, x_label, y_label, c):
    kr = KernelReg(y, x, 'c')
    y_pred, y_std = kr.fit(x)
    fileName = remove(title) + '.jpeg'

    plt.figure(fig)
    plt.grid(True)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y, '+')
    plt.plot(x, y_pred, color=c)
    print('\n', y_label)
    print('Maximum ', y_label, ' = ', max(y_pred))
    print('Minimum ', y_label, ' = ', min(y_pred))
    print('Average ', y_label, ' = ', np.average(y_pred))
    print(y_label, ' delta = ', max(y_pred) - min(y_pred))
    plt.savefig(fileName, format='jpeg', dpi=1200)
    plt.show()

# Double Variable Plotter
def doublePlot(fig, x, y1, y2, title, x_label, y_label, y1_label, y2_label, c1, c2):
    kr1 = KernelReg(y1, x, 'c')
    y1_pred, y1_std = kr1.fit(x)
    kr2 = KernelReg(y2, x, 'c')
    y2_pred, y2_std = kr2.fit(x)
    fileName = remove(title) + '.jpeg'

    plt.figure(fig)
    plt.grid(True)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x, y1_pred, color=c1)
    plt.plot(x, y2_pred, color=c2)
    plt.plot(x, y1, '+', color=c1)
    plt.plot(x, y2, '+', color=c2)
    plt.legend( [y1_label, y2_label], loc = 'lower right')
    print('\n', y1_label)
    print('Maximum ', y1_label, ' = ', max(y1_pred))
    print('Minimum ', y1_label, ' = ', min(y1_pred))
    print('Average ', y1_label, ' = ', np.average(y1_pred))
    print(y1_label, ' delta = ', max(y1_pred) - min(y1_pred))
    print('\n', y2_label)
    print('Maximum ', y2_label, ' = ', max(y2_pred))
    print('Minimum ', y2_label, ' = ', min(y2_pred))
    print('Average ', y2_label, ' = ', np.average(y2_pred))
    print(y2_label, ' delta = ', max(y2_pred) - min(y2_pred))
    plt.savefig(fileName, format='jpeg', dpi=1200)
    plt.show()

# Space Remove
def remove(string_input): 
    return string_input.replace(" ", "")

# UTC Convert
def strTime(str_time):
    return datetime.strptime(str_time, ' %Y-%m-%dT%H:%M')

def scale_to_img(lat_lon, h_w):
    old = (points[2], points[0])
    new = (0, h_w[1])
    y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
    old = (points[1], points[3])
    new = (0, h_w[0])
    x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) / (old[1] - old[0])) + new[0]
    return int(x), h_w[1] - int(y)

'''    
Main Program Begins Here
Main Program Begins Here
Main Program Begins Here
'''

points = (6.8196, 80.4915, 6.7947, 80.5305)
csvfile = 'Sandagalathenna'
mapfile = csvfile + '.raw.jpeg'
resultMap = csvfile + '.route.jpeg'

entry,utc,temperature,pressure,balt,galt,lat,lon = read_data(csvfile + '.csv')
x = np.array(entry)
xlen = np.size(x)
timeDiff = np.empty(xlen-1)
gVerVeloc = np.empty(xlen)
bVerVeloc = np.empty(xlen)
gVerVeloc[0] = 0
bVerVeloc[0] = 0

# GPS Route
gps_data = tuple(zip(lat,lon))
image = Image.open(mapfile, 'r')
img_points = []
for d in gps_data:
    x1, y1 = scale_to_img(d, (image.size[0], image.size[1]))  # Convert GPS coordinates to image coordinates.
    img_points.append((x1, y1))
draw = ImageDraw.Draw(image)
draw.line(img_points, fill=(255, 0, 0), width=2)  # Draw converted records to the map image.

image.save(resultMap)

# Temperature
y = np.array(temperature-2)
singlePlot(1, x, y, 'Temperature Variation', 'Entry', 'Temperature (*C)', 'green')

# Barometric Pressure
y = np.array(pressure)
singlePlot(2, x, y, 'Barometric Pressure Variation', 'Entry', 'Barometric Pressure (hPa)', 'green')

# Altitude
doublePlot(3, x, galt, balt, 'Altitude Variation', 'Entry', 'Altitude (m)', 'GPS Altitude', 'Barometric Altitude', 'green', 'blue')

# Vertical Velocity
for i in range(xlen-1):
    timeDiff[i] = (strTime(utc[i+1]) - strTime(utc[i])).total_seconds()
    gVerVeloc[i+1] = (galt[i+1] - galt[i])/timeDiff[i]
    bVerVeloc[i+1] = (balt[i+1] - balt[i])/timeDiff[i]
doublePlot(4, x, gVerVeloc, bVerVeloc, 'Vertical Velocity Variation', 'Entry', 'Vertical Velocity (m/s)', 'Vertical Velocity (GPS)', 'Vertical Velocity (Barometric)', 'green', 'blue')

