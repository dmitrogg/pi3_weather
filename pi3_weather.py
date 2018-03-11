# Main file

import urllib.request
import pigpio
import DHT22
import random
from tkinter import *
from time import time
from PIL import Image, ImageTk
from datetime import datetime

root = Tk()
pi = pigpio.pi()
dht22 = DHT22.sensor(pi, 22)
dht22.trigger()

x = 0.25
x2 = 0.98 - x
font = "Josefin Sans Light"
font2 = "Forum"
font3 = "Abel"

# Draw a line
canvas = Canvas(root, background = 'black', highlightthickness=0)
canvas.create_line(190, 20, 190, 235, fill = '#7a7a7a') # 190 offset for Pi
canvas.pack()

# Web: Big Temperature label
webVarTemp = StringVar()
webVarTemp.set('')
webVarTempLabel = Label(root, textvariable = webVarTemp, font=(font, 115), foreground='white', background='black')
webVarTempLabel.place(relx=x+0.025, rely=0.3, anchor=CENTER) # y at 0.3 for Pi

# Sensor: Big Temperature label
sensorVarTemp = StringVar()
sensorVarTemp.set('')
sensorVarTempLabel = Label(root, textvariable = sensorVarTemp, font=(font, 115), foreground='white', background='black')
sensorVarTempLabel.place(relx=x2+0.025, rely=0.3, anchor=CENTER) # y at 0.3 for Pi

# Top row label (Outside/Inside)
Label(root, text = "- Outside -", font=(font3, 34), foreground='white', background='black').place(relx=x, rely=0.075, anchor=CENTER)
Label(root, text = "- Inside -", font=(font3, 34), foreground='white', background='black').place(relx=x2, rely=0.075, anchor=CENTER)

# Web: Humidity label
webVarHumi = StringVar()
webVarHumi.set('Loading...')
webVarHumiLabel = Label(root, textvariable = webVarHumi, font=(font3, 25), foreground='white', background='black')
webVarHumiLabel.place(relx=x, rely=0.47, anchor=CENTER)

# Sensor: Humidity label
sensorVarHumi = StringVar()
sensorVarHumi.set('Loading...')
sensorVarHumiLabel = Label(root, textvariable = sensorVarHumi, font=(font3, 25), foreground='white', background='black')
sensorVarHumiLabel.place(relx=x2, rely=0.47, anchor=CENTER)

# Setup image size and place image
originalImage = Image.open('/pi3_weather/derp.jpg')
resized = originalImage.resize((240, 180), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
imageLabelWeb = Label(root, image=image, background='black')
imageLabelWeb.place(relx=x+0.125, rely=0.75, anchor=CENTER)

# Setup Description Box label
descTextVar = StringVar()
descTextVar.set('Loading...')
descTextVarLabel = Label(root, textvariable = descTextVar, font=(font3, 25), foreground='white', background='black', wraplength=360, justify=LEFT)
descTextVarLabel.place(relx=0.525, rely=0.75, anchor=W)


# Update image
def changeImage(newWebImageString):
    newImage = Image.open(newWebImageString)
    newResizedImage = newImage.resize((240, 180), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(newResizedImage)
    imageLabelWeb.configure(image=image)
    imageLabelWeb.image = image

def getWebData():

    webURL = urllib.request.urlopen("https://darksky.net/forecast/30.3583,-90.0656/us12/en")
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

    start = extractedTextBlock.find('class="swiap">') + 14
    end = extractedTextBlock.find('</span>')
    snippetWebHour = extractedTextBlock[start:end].replace('</strong>: <span class="swap">', ': ')

    # Extract Forecast text snippet 
    start = webTextCode.find('span class="next swap"')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]

    start = extractedTextBlock.find('span class="next swap"') + 47
    end = extractedTextBlock.find('</span>') - 10
    snippetWebCast = extractedTextBlock[start:end].replace('&nbsp;', ' ')
    snippetWebCast = snippetWebCast[0:80]   # Only 80 characted fit into text box.

    # Set variables, and directly change labels
    webVarTemp.set(str('{:.1f}'.format(temperatureWeb)) + '˚')
    
    webVarHumi.set('Humidity ' + str('{:.0f}'.format(humidityWeb)) + '%')

    # Set global variables
    global extWebTemp
    extWebTemp = float('{:.1f}'.format(temperatureWeb))

    global extWebText
    if (str(snippetWebHour) == ''):
        extWebText = str(snippetWebMini) + "\n" + str(snippetWebCast)
    else:
        extWebText = str(snippetWebMini) + "\n" + str(snippetWebHour)



def getSensorData():
    dht22.trigger()
    temperatureSensor = float(dht22.temperature()) * 9/5 + 32
    humiditySensor = float(dht22.humidity())

    # Testing solution
    # temperatureSensor = float('{:.1f}'.format(random.uniform(68, 77)))
    # humiditySensor = float('{:.1f}'.format(random.uniform(1, 99)))

    # Set variables, and directly change labels
    sensorVarTemp.set(str('{:.1f}'.format(temperatureSensor)) + '˚')
   
    sensorVarHumi.set('Humidity ' + str('{:.0f}'.format(humiditySensor)) + '%')

    # Set global variables
    global extSnsTemp
    extSnsTemp = float('{:.1f}'.format(temperatureSensor))

def LoopUpdateWebData():
    getWebData()
    randomTime = 60000 + (int(random.uniform(0, 60)) * 1000)
    root.after(randomTime, LoopUpdateWebData)

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

    elif (extSnsTemp >= 75.0 and extSnsTemp <= 84.9):
        inside = 'Hot'  

    elif (extSnsTemp >= 71.0 and extSnsTemp <= 74.9):
        inside = 'Normal'  

    elif (extSnsTemp >= 65.0 and extSnsTemp <= 70.9):
        inside = 'Cold'
    
    elif (extSnsTemp <= 64.9):
        inside = 'Arctic'  

    return(inside, outside)

def LoopImage():

    inside, outside = getStatus()

    if (inside == 'DatGeof' or outside == 'DatGeof'):
        changeImage('/pi3_weather/rustle.jpg')

    elif (inside == 'Shrek' or outside == 'Shrek'):
        changeImage('/pi3_weather/rustle.jpg')   

    if (inside == 'Lava' or outside == 'Lava'):
        changeImage('/pi3_weather/mextroll.jpg')

    elif (inside == 'Arctic' or outside == 'Arctic'):
        changeImage('/pi3_weather/rustle.jpg')   
    
    elif (inside == 'Cold'):
        changeImage('/pi3_weather/rustle.jpg')     

    elif (inside == 'Hot'):
        changeImage('/pi3_weather/rustle.jpg')     

    else:
        changeImage('/pi3_weather/normal.jpg')

    root.after(1000, LoopImage)


def LoopDescription():

    inside, outside = getStatus()

    if (inside == 'DatGeof' or outside == 'DatGeof'):
        descTextVar.set('It\'s 69 degrees HEHEHE')

    elif (inside == 'Shrek' or outside == 'Shrek'):
         descTextVar.set('The temperature is DANK degrees.')

    if (inside == 'Lava' or outside == 'Lava'):
        descTextVar.set('Very hot inside.')

    elif (inside == 'Arctic' or outside == 'Arctic'):
         descTextVar.set('Very cold inside.')
    
    elif (inside == 'Cold'):
        descTextVar.set('Kelsey\'s favorite temperature.')

    elif (inside == 'Hot'):
        descTextVar.set('Pretty hot inside.')

    else:
        descTextVar.set('Now: Sky is ' + str(extWebText))

    root.after(1000, LoopDescription)


def closeApp():
    root.destroy()

# Call procedures to update values
root.after(500, getWebData) #temp
root.after(500, getSensorData) #temp
root.after(1000, LoopImage)
root.after(1000, LoopDescription)
root.after(2000, LoopUpdateWebData)
root.after(3000, LoopUpdateSnsData)
root.after(30000, closeApp)

# Set window "always on top"
root.call('wm', 'attributes', '.', '-topmost', True)

# Disable window controls
root.overrideredirect(1)

# Set window parameters
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(800, 480))
root.configure(background='black')

root.mainloop()


  