#!/usr/bin/python3

import urllib.request
import random
import sys
import platform
from tkinter import *
from time import time
from PIL import Image, ImageTk
from datetime import datetime

# Ajust path to files based on system
if (platform.system() == 'Windows'):
    path = ''
    pathImg = 'images/'
else:
    path = '/home/pi/pi3_weather/'
    pathImg = '/home/pi/pi3_weather/images/'
    import pigpio
    import DHT22
    pi = pigpio.pi()
    dht22 = DHT22.sensor(pi, 22)
    dht22.trigger()

root = Tk()

x1 = 0.165 #+ 0.025 # Column 1
x2 = 0.495          # Column 2
x3 = 0.825 #- 0.025 # Column 3

if (platform.system() == 'Windows'):
    y1 = 0.225
else:
    y1 = 0.275

font = "Josefin Sans Light"
font2 = "Forum"
font3 = "Abel"

# # Draw a line
# canvas = Canvas(root, background = 'black', highlightthickness=0)
# canvas.create_line(190, 20, 190, 235, fill = '#7a7a7a') # 190 offset for Pi
# canvas.pack()

# Values are not rounded! Only truncated. Need to round.

# Big Temperature Number: Inside - Sensor
sensorVarTemp = StringVar()
sensorVarTemp.set('')
sensorVarTempLabel = Label(root, textvariable = sensorVarTemp, font=(font, 115), foreground='white', background='black')
sensorVarTempLabel.place(relx=x1+0.025, rely=y1, anchor=CENTER) # y at 0.3 for Pi

# Big Temperature Number: Web - Fremont
webVarTemp = StringVar()
webVarTemp.set('')
webVarTempLabel = Label(root, textvariable = webVarTemp, font=(font, 115), foreground='white', background='black')
webVarTempLabel.place(relx=x2+0.025, rely=y1, anchor=CENTER) # y at 0.3 for Pi

# Big Temperature Number: Web - City
webVarTempII = StringVar()
webVarTempII.set('')
webVarTempIILabel = Label(root, textvariable = webVarTempII, font=(font, 115), foreground='white', background='black')
webVarTempIILabel.place(relx=x3+0.025, rely=y1, anchor=CENTER) # y at 0.3 for Pi

# Top row labels (Outside/Inside) (Got to be after Big Temp labels, so it would appear in foreground.)
Label(root, text = "- Inside -", font=(font3, 34), foreground='white', background='black').place(relx=x1, rely=0.075, anchor=CENTER)
Label(root, text = "- Fremont -", font=(font3, 34), foreground='white', background='black').place(relx=x2, rely=0.075, anchor=CENTER)
Label(root, text = "- San Fran -", font=(font3, 34), foreground='white', background='black').place(relx=x3, rely=0.075, anchor=CENTER)

# Humidity - Sensor
sensorVarHumi = StringVar()
sensorVarHumi.set('Loading...')
sensorVarHumiLabel = Label(root, textvariable = sensorVarHumi, font=(font3, 20), foreground='white', background='black')
sensorVarHumiLabel.place(relx=x1, rely=0.425, anchor=CENTER)

# Humidity - Fremont
webVarHumi = StringVar()
webVarHumi.set('Loading...')
webVarHumiLabel = Label(root, textvariable = webVarHumi, font=(font3, 20), foreground='white', background='black')
webVarHumiLabel.place(relx=x2, rely=0.425, anchor=CENTER)

# Humidity - City
webVarHumiII = StringVar()
webVarHumiII.set('Loading...')
webVarHumiLabelII = Label(root, textvariable = webVarHumiII, font=(font3, 20), foreground='white', background='black')
webVarHumiLabelII.place(relx=x3, rely=0.425, anchor=CENTER)






# Setup image size and place image
originalImage = Image.open(pathImg + 'derp.jpg')
resized = originalImage.resize((240, 180), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
imageLabelWeb = Label(root, image=image, background='black')
imageLabelWeb.place(relx=0.165, rely=0.77, anchor=CENTER)

# Setup Description Box label
descTextVar = StringVar()
descTextVar.set('Loading...')
descTextVarLabel = Label(root, textvariable = descTextVar, font=(font3, 25), foreground='white', background='black', wraplength=425, justify=LEFT)
descTextVarLabel.place(relx=0.425, rely=0.78, anchor=W)


# Update image
def changeImage(newWebImageString):
    newImage = Image.open(newWebImageString)
    newResizedImage = newImage.resize((240, 180), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(newResizedImage)
    imageLabelWeb.configure(image=image)
    imageLabelWeb.image = image


# Get Web Data - Fremont
def getWebData():

    webURL = urllib.request.urlopen("https://darksky.net/forecast/37.5483,-121.9886/us12/en")
    webTextCode = str(webURL.read())
    
    # Extract main block
    start = webTextCode.find('currently = {"time"')
    end = start + 400
    extractedTextBlock = webTextCode[start:end]

    # Extract temperature from main block
    start = extractedTextBlock.find('"temperature"') + 14
    end = start + 4
    temperatureWeb = float(extractedTextBlock[start:end].replace(',', '').replace('"', ''))

    # Extract humidity from main block
    start = extractedTextBlock.find('"humidity"') + 13
    end = start + 2
    humidityWeb = float(extractedTextBlock[start:end].replace(',', '0').replace('"p', '100')) # "p is for rare case of 100%

    # Extract Mini-Description text from main block
    start = extractedTextBlock.find('"summary":') + 11
    end = extractedTextBlock.find(',"icon":') - 1
    snippetWebMini = extractedTextBlock[start:end]

    # Extract Next Hour text snippet
    start = webTextCode.find('<strong class="swiap">')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]
    snippetWebHour = ''
    start = extractedTextBlock.find('class="swiap">') + 14
    end = extractedTextBlock.find('</span>')
    snippetWebHour = extractedTextBlock[start:end].replace('</strong>: <span class="swap">', ': ').replace('&lt;', '>').replace('Next Hour: ', '').replace('min.', 'min')

    # Extract Forecast text snippet 
    start = webTextCode.find('span class="next swap"')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]
    start = extractedTextBlock.find('span class="next swap"') + 47
    end = extractedTextBlock.find('</span>') - 10
    snippetWebCast = extractedTextBlock[start:end].replace('&nbsp;', ' ')
    snippetWebCast = snippetWebCast[0:85] + '...'   # Only 80 characted fit into text box.

    # Extract Government Alerts
    start = webTextCode.find('bang')
    end = start + 100
    extractedGovAlert = webTextCode[start:end]
    snippetGovAlert = ''
    start = 16
    end = extractedGovAlert.find('</a>') - 10
    snippetGovAlert = extractedGovAlert[start:end].replace('  ', '') 

    # Set variables, and directly change labels
    webVarTemp.set(str('{:.0f}'.format(round(temperatureWeb))) + '˚')
    webVarHumi.set('Humidity ' + str('{:.0f}'.format(round(humidityWeb))) + '%')

 

    # Set global variables
    global extWebTemp
    extWebTemp = float('{:.0f}'.format(temperatureWeb))

    global extWebText
    if (str(snippetWebHour) != ''):
        extWebText = str(snippetWebMini) + "\n" + str(snippetWebHour)
    if (str(snippetGovAlert) != ''):
        extWebText = str(snippetWebMini) + "\n" + str(snippetGovAlert) 
    else:
        extWebText = str(snippetWebMini) + "\n" + str(snippetWebCast)

# Get Web Data - San Fran
def getWebDataII():

    webURL = urllib.request.urlopen("https://darksky.net/forecast/37.7934,-122.3959/us12/en")
    webTextCode = str(webURL.read())
    
    # Extract main block
    start = webTextCode.find('currently = {"time"')
    end = start + 400
    extractedTextBlock = webTextCode[start:end]

    # Extract temperature from main block
    start = extractedTextBlock.find('"temperature"') + 14
    end = start + 4
    temperatureWeb = float(extractedTextBlock[start:end].replace(',', '').replace('"', ''))

    # Extract humidity from main block
    start = extractedTextBlock.find('"humidity"') + 13
    end = start + 2
    humidityWeb = float(extractedTextBlock[start:end].replace(',', '0').replace('"p', '100')) # "p is for rare case of 100%

    # Extract Mini-Description text from main block
    start = extractedTextBlock.find('"summary":') + 11
    end = extractedTextBlock.find(',"icon":') - 1
    snippetWebMini = extractedTextBlock[start:end]

    # Extract Next Hour text snippet
    start = webTextCode.find('<strong class="swiap">')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]

    snippetWebHour = ''
    start = extractedTextBlock.find('class="swiap">') + 14
    end = extractedTextBlock.find('</span>')
    snippetWebHour = extractedTextBlock[start:end].replace('</strong>: <span class="swap">', ': ').replace('&lt;', '>').replace('Next Hour: ', '').replace('min.', 'min')

    # Extract Forecast text snippet 
    start = webTextCode.find('span class="next swap"')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]

    start = extractedTextBlock.find('span class="next swap"') + 47
    end = extractedTextBlock.find('</span>') - 10
    snippetWebCast = extractedTextBlock[start:end].replace('&nbsp;', ' ')
    snippetWebCast = snippetWebCast[0:85] + '...'   # Only 80 characted fit into text box.

    # Extract Government Alerts
    start = webTextCode.find('bang')
    end = start + 100
    extractedGovAlert = webTextCode[start:end]
    
    snippetGovAlert = ''
    start = 16
    end = extractedGovAlert.find('</a>') - 10
    snippetGovAlert = extractedGovAlert[start:end].replace('  ', '') 

    # Set variables, and directly change labels
    webVarTempII.set(str('{:.0f}'.format(round(temperatureWeb))) + '˚')
    webVarHumiII.set('Humidity ' + str('{:.0f}'.format(round(humidityWeb))) + '%')

# Get Sensor Data
def getSensorData():

    # Ajust vars based on system
    if (platform.system() == 'Windows'):
        temperatureSensor = float('{:.0f}'.format(random.uniform(69, 76)))
        humiditySensor = float('{:.0f}'.format(random.uniform(1, 99)))
    else:
        dht22.trigger()
        temperatureSensor = float(dht22.temperature()) * 9/5 + 32
        humiditySensor = float(dht22.humidity())

    # Set variables, and directly change labels
    sensorVarTemp.set(str('{:.0f}'.format(round(temperatureSensor))) + '˚')
    sensorVarHumi.set('Humidity ' + str('{:.0f}'.format(round(humiditySensor))) + '%')

    # Set global variables
    global extSnsTemp
    extSnsTemp = float('{:.0f}'.format(temperatureSensor))

def LoopUpdateWebData():
    getWebData()
    randomTime = 120000 + (int(random.uniform(0, 60)) * 1000)
    root.after(randomTime, LoopUpdateWebData)

def LoopUpdateWebDataII():
    getWebDataII()
    randomTime = 180000 + (int(random.uniform(0, 60)) * 1000)
    root.after(randomTime, LoopUpdateWebDataII)

def LoopUpdateSnsData():
    getSensorData()
    root.after(5000, LoopUpdateSnsData)

def getStatus():

    # Meme conditions
    if (extWebTemp == 69.0 or extSnsTemp == 69.0):
        outside = 'DatGeof'

    if (extWebTemp == 42.0 or extSnsTemp == 42.0):
        outside = 'Shrek'

    # Outside
    if (extWebTemp >= 100.0):
        outside = 'Lava'  

    elif (extWebTemp >= 85.0 and extWebTemp <= 99.9):
        outside = 'Hot'  

    elif (extWebTemp >= 45.0 and extWebTemp <= 84.9):
        outside = 'Normal'  

    elif (extWebTemp >= 15.0 and extWebTemp <= 44.9):
        outside = 'Cold'
    
    elif (extWebTemp <= 15.1):
        outside = 'Arctic'  

    # Inside
    if (extSnsTemp >= 85.0):
        inside = 'Lava'  

    elif (extSnsTemp >= 80.0 and extSnsTemp <= 84.9):
        inside = 'Hot'  

    elif (extSnsTemp >= 71.0 and extSnsTemp <= 79.9):
        inside = 'Normal'  

    elif (extSnsTemp >= 65.0 and extSnsTemp <= 70.9):
        inside = 'Cold'
    
    elif (extSnsTemp <= 64.9):
        inside = 'Arctic'  

    return(inside, outside)

def LoopImage():

    inside, outside = getStatus()

    if (inside == 'DatGeof' or outside == 'DatGeof'):
        changeImage(pathImg + 'rustle.jpg')

    elif (inside == 'Shrek' or outside == 'Shrek'):
        changeImage(pathImg + 'rustle.jpg')   

    if (inside == 'Lava' or outside == 'Lava'):
        changeImage(pathImg + 'mextroll.jpg')

    elif (inside == 'Arctic' or outside == 'Arctic'):
        changeImage(pathImg + 'rustle.jpg')   
    
    elif (inside == 'Cold'):
        changeImage(pathImg + 'rustle.jpg')     

    elif (inside == 'Hot'):
        changeImage(pathImg + 'rustle.jpg')     

    else:
        changeImage(pathImg + 'normal.jpg')

    root.after(1000, LoopImage)


def LoopDescription():

    inside, outside = getStatus()

    if (inside == 'DatGeof' or outside == 'DatGeof'):
        descTextVar.set('Now: ' + str(extWebText) + '\n' + 'It\'s 69 degrees HEHEHE')

    elif (inside == 'Shrek' or outside == 'Shrek'):
         descTextVar.set('Now: ' + str(extWebText) + '\n' + 'The temperature is DANK degrees.')

    elif (inside == 'Lava' or outside == 'Lava'):
        descTextVar.set('Now: ' + str(extWebText) + '\n' + 'Very hot inside.')

    elif (inside == 'Arctic' or outside == 'Arctic'):
         descTextVar.set('Now: ' + str(extWebText) + '\n' + 'Very cold inside.')
    
    elif (inside == 'Cold'):
        descTextVar.set('Now: ' + str(extWebText) + '\n' + 'Kelsey\'s favorite temperature.')

    elif (inside == 'Hot'):
        descTextVar.set('Now: ' + str(extWebText) + '\n' + 'Pretty hot inside.')

    else:
        descTextVar.set('Now: ' + str(extWebText))

    root.after(1000, LoopDescription)

# Any key release = event var.
def closeApp(event):
    root.destroy()

# Call procedures to update values
root.after(500, getWebData) #temp
root.after(500, getWebDataII) #temp
root.after(500, getSensorData) #temp
root.after(1000, LoopImage)
root.after(1000, LoopDescription)
root.after(2000, LoopUpdateWebData)
root.after(2000, LoopUpdateWebDataII)
root.after(3000, LoopUpdateSnsData)

# Ajust path to files based on system
if (platform.system() == 'Windows'):
    path = ''
else:
    # Disable window controls
    root.overrideredirect(1)
    # root.after(10000, closeApp)

# Set window "always on top"
root.call('wm', 'attributes', '.', '-topmost', True)

# Set window parameters
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(1024, 600))
root.configure(background='black')

# Call closeApp on any key release
root.bind_all('<KeyRelease>', closeApp)

# Start main tk loop
root.mainloop()




