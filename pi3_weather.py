# Main file

import urllib.request
# import pigpio
# import DHT22
import random
from tkinter import *
from time import time
from PIL import Image, ImageTk
from datetime import datetime

root = Tk()
# pi = pigpio.pi()
# dht22 = DHT22.sensor(pi, 22)
# dht22.trigger()

x = 0.25
x2 = 0.98 - x
font = "Josefin Sans Light"
font2 = "Forum"
font3 = "Abel"

#Web: Big Temperature label
webVarTemp = StringVar()
webVarTemp.set('...')
webVarTempLabel = Label(root, textvariable = webVarTemp, font=(font, 110), foreground='white', background='black')
webVarTempLabel.place(relx=x+0.025, rely=0.28, anchor=CENTER)

#Sensor: Big Temperature label
sensorVarTemp = StringVar()
sensorVarTemp.set('...')
sensorVarTempLabel = Label(root, textvariable = sensorVarTemp, font=(font, 110), foreground='white', background='black')
sensorVarTempLabel.place(relx=x2+0.025, rely=0.28, anchor=CENTER)

#Web: Short description label
webVarTxt = StringVar()
webVarTxt.set('...')
webVarTxtLabel = Label(root, textvariable = webVarTxt, font=(font2, 34), foreground='white', background='black')
webVarTxtLabel.place(relx=x, rely=0.075, anchor=CENTER)

#Sensor: Short description label
sensorVarTxt = StringVar()
sensorVarTxt.set('...')
sensorVarTxtLabel = Label(root, textvariable = sensorVarTxt, font=(font2, 34), foreground='white', background='black')
sensorVarTxtLabel.place(relx=x2, rely=0.075, anchor=CENTER)

#Web: Humidity and Celcius label
webVarTempHC = StringVar()
webVarTempHC.set('...')
webVarTempHCLabel = Label(root, textvariable = webVarTempHC, font=(font3, 20), foreground='white', background='black')
webVarTempHCLabel.place(relx=x, rely=0.475, anchor=CENTER)

#Sensor: Humidity and Celcius label
sensorVarTempHC = StringVar()
sensorVarTempHC.set('...')
sensorVarTempHCLabel = Label(root, textvariable = sensorVarTempHC, font=(font3, 20), foreground='white', background='black')
sensorVarTempHCLabel.place(relx=x2, rely=0.475, anchor=CENTER)

#Web: Setup default image size and place image
originalImage = Image.open('updating.png')
resized = originalImage.resize((180, 180), Image.ANTIALIAS)
image = ImageTk.PhotoImage(resized)
imageLabelWeb = Label(root, image=image, background='black')
imageLabelWeb.place(relx=x, rely=0.775, anchor=CENTER)

#Sensor: Setup default image size and place image
originalImage2 = Image.open('updating.png')
resized2 = originalImage.resize((180, 180), Image.ANTIALIAS)
image2 = ImageTk.PhotoImage(resized2)
imageLabelSensor = Label(root, image=image2, background='black')
imageLabelSensor.place(relx=x2, rely=0.775, anchor=CENTER)

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

def closeApp():
    root.destroy()

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
    snippetWebMini = extractedTextBlock[start:end]

    # Extract text snippet for NEXT HOUR
    start = webTextCode.find('<strong class="swiap">')
    end = start + 150
    extractedTextBlock = webTextCode[start:end]

    start = extractedTextBlock.find('class="swiap">') + 14
    end = extractedTextBlock.find('</span>')
    snippetWebHour = extractedTextBlock[start:end].replace('</strong>: <span class="swap">', ': ')

    # Set all variables
    webVarTxt.set('Outside: ' + str(snippetWebMini))
    
    webVarTemp.set(str('{:.1f}'.format(temperatureWeb)) + '˚')

    # Include NEXT HOUR text if present
    if (snippetWebHour == ''):
        webVarTempHC.set(str('{:.1f}'.format(humidityWeb)) + '%   ' + str('{:.1f}'.format((temperatureWeb - 32)*(5/9)) + 'C'))
    else:
        webVarTempHC.set(str('{:.1f}'.format(humidityWeb)) + '%   ' + str('{:.1f}'.format((temperatureWeb - 32)*(5/9)) + 'C') + '\n' + str(snippetWebHour))

    # Return temparature for picture change
    return(float(temperatureWeb))

def getSensorData():
    # dht22.trigger()
    # temperatureSensor = float(dht22.temperature()) * 9/5 + 32
    # humiditySensor = float(dht22.humidity())

    # Temp solution
    temperatureSensor = float('{:.1f}'.format(random.uniform(30, 105)))
    humiditySensor = float('{:.1f}'.format(random.uniform(1, 99)))
    snippetSensorHour = 'Home will remain refrigirated.'

    # Set all variables, simulated temperature
    sensorVarTxt.set('Inside: Nice')

    sensorVarTemp.set(str('{:.1f}'.format(temperatureSensor)) + '˚')

    # Include NEXT HOUR text if present
    if (snippetSensorHour == ''):
        sensorVarTempHC.set(str('{:.1f}'.format(humiditySensor)) + '%    ' + str('{:.1f}'.format((temperatureSensor - 32)*(5/9)) + 'C'))
    else:
        sensorVarTempHC.set(str('{:.1f}'.format(humiditySensor)) + '%    ' + str('{:.1f}'.format((temperatureSensor - 32)*(5/9)) + 'C') + '\n' + str(snippetSensorHour))

    # Return temparature for picture change
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

    root.after(10000, selectSensorImage)

# Call procedures to update values
root.after(2000, getWebData)
root.after(2000, getSensorData)
root.after(3000, selectWebImage)
root.after(4000, selectSensorImage)
root.after(15000, closeApp)

# Set window "always on top"
root.call('wm', 'attributes', '.', '-topmost', True)

# Disable window controls
#root.overrideredirect(1)

# Set window parameters
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(800, 480))
root.configure(background='black')

root.mainloop()


