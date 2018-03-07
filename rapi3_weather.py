

import urllib.request
# import pigpio
# import DHT22
import random
from tkinter import *
from time import time
from PIL import Image, ImageTk
from datetime import datetime

root = Tk()

x = 0.25
x2 = 0.75
font = "Century Gothic"

sensorVar = StringVar()
sensorVar.set('Updating Data')
sensorDataLabel = Label(root, textvariable = sensorVar, font=("Calibri", 10), foreground="White", background='black')
sensorDataLabel.place(relx=x2, rely=0.5, anchor=CENTER)

#Web Data: Text label
webVarTxt = StringVar()
webVarTxt.set('')
webVarTxtLabel = Label(root, textvariable = webVarTxt, font=(font, 34), foreground="White", background='black')
webVarTxtLabel.place(relx=x, rely=0.1, anchor=CENTER)

#Web Data: Text forecast label
webVarTxtFore = StringVar()
webVarTxtFore.set('')
webVarTxtForeLabel = Label(root, textvariable = webVarTxtFore, font=(font, 10), foreground="White", background='black')
webVarTxtForeLabel.place(relx=x, rely=0.18, anchor=CENTER)

#Web Data: Big Temperature label
webVarTemp = StringVar()
webVarTemp.set('')
webVarTempLabel = Label(root, textvariable = webVarTemp, font=(font, 100), foreground="White", background='black')
webVarTempLabel.place(relx=x, rely=0.75, anchor=CENTER)

#Web Data: Secondary Humidity and Celcius label
webVarTempHC = StringVar()
webVarTempHC.set('')
webVarTempHCLabel = Label(root, textvariable = webVarTempHC, font=(font, 18), foreground="White", background='black')
webVarTempHCLabel.place(relx=x+0.05, rely=0.9, anchor=CENTER)



# Setup default Web image size and place image
originalImage = Image.open('updating.png')
resized = originalImage.resize((180, 180), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
imageLabelWeb = Label(root, image=image, background='black')
imageLabelWeb.place(relx=x, rely=0.45, anchor=CENTER)

# Setup default Sensor image size and place image
originalImage = Image.open('updating.png')
resized = originalImage.resize((180, 180), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
imageLabelSensor = Label(root, image=image, background='black')
imageLabelSensor.place(relx=x2, rely=0.45, anchor=CENTER)

# Update Web image
def changeImageWeb(newWebImageString):
    newImage = Image.open(newWebImageString)
    newResizedImage = newImage.resize((180, 180), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(newResizedImage)
    imageLabelWeb.configure(image=image)
    imageLabelWeb.image = image

# Update Sensor image
def changeImageSensor(newSensorImageString):
    newImage = Image.open(newSensorImageString)
    newResizedImage = newImage.resize((180, 180), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(newResizedImage)
    imageLabelSensor.configure(image=image)
    imageLabelSensor.image = image


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
    humidityWeb = float(extractedTextBlock[start:end].replace(',', '0'))

    # Extract mini-title from main block
    start = extractedTextBlock.find('"summary":') + 11
    end = extractedTextBlock.find(',"icon":') - 1
    snippetWebMini = 'Outside: ' + extractedTextBlock[start:end]

    # Extract text snippet for DAY
    start = webTextCode.find('span class="next swap"')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]

    start = extractedTextBlock.find('"next swap">') + 36
    end = extractedTextBlock.find('</span>') - 10
    snippetWebDay = 'Forecast: ' + extractedTextBlock[start:end].replace('&nbsp;', ' ').replace('&lt;', ' less than ').replace(',', ',\n')
    # Partly cloudy starting tonight, continuing until tomorrow morning. 

    # Extract text snippet for NEXT HOUR
    start = webTextCode.find('<strong class="swiap">')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]

    start = extractedTextBlock.find('class="swiap">') + 14
    end = extractedTextBlock.find('</span>')
    snippetWebHour = extractedTextBlock[start:end].replace('</strong>: <span class="swap">', ': ')

    webVarTemp.set(str('{:.1f}'.format(temperatureWeb)) + '˚')

    webVarTempHC.set(str('{:.1f}'.format(humidityWeb)) + '%  ' + str('{:.1f}'.format((temperatureWeb - 32)*(5/9)) + 'C'))

    webVarTxt.set(str(snippetWebMini))

    webVarTxtFore.set(str(snippetWebDay))

    return(float(temperatureWeb))

def getSensorData():
    # run sudo pigpiod
    # pi = pigpio.pi()
    # dht22 = DHT22.sensor(pi, 22)
    # dht22.trigger()
    # temperatureSensor = (dht22.temperature() * 1.8) + 32
    # humiditySensor = dht22.humidity()

    # sensorVar.set('Inside Temperature: ' + str('{:.1f}'.format(temperatureSensor)) + '˚' + '\n' + 'Inside Humidity: ' + str('{:.0f}'.format(humiditySensor)) + '%')

    temperatureSensor = '{:.1f}'.format(random.uniform(10, 99))
    sensorVar.set('Inside Temperature: ' + str(temperatureSensor) + '˚' + '\n' + 'Inside Humidity: ' + str(99) + '%')

    return(float(temperatureSensor))

def selectWebImage():

    temperatureWeb = getWebData()

    if (temperatureWeb<80):
        changeImageWeb('normal.png')
    else:
        changeImageWeb('rustle.png')

    root.after(60000, selectWebImage)

def selectSensorImage():

    temperatureSensor = getSensorData()

    if (temperatureSensor<80):
        changeImageSensor('normal.png')
    else:
        changeImageSensor('rustle.png')

    root.after(60000, selectSensorImage)

# Call procedures to update values
root.after(100, getWebData)
root.after(100, getSensorData)
root.after(2000, selectWebImage)
root.after(3000, selectSensorImage)

# Set window "always on top"
root.call('wm', 'attributes', '.', '-topmost', True)

# Disable window controls
# root.overrideredirect(1)

# Set window parameters
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(800, 480))
root.configure(background='black')

root.mainloop()