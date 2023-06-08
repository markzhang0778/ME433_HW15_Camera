# get a line of raw bitmap and plot the components
import serial
import numpy as np
ser = serial.Serial('COM4',115200) # the name of your Pico port
print('Opening port: ')
print(ser.name)

def rgb_to_grey(r,g,b):
    # gray=0.299red+0.587green+0.114blue
    return (0.299*r + 0.587*g + 0.114*b)

def wb(b):
    if(b > 70):
        return 1
    else:
        return 0

for i in range(100):
    ser.write(b'hi\r\n') # send a newline to request data
    data_read = ser.read_until(b'\n',50) # read the echo

    sampnum = 0
    index = 0
    raw = []
    reds = []
    greens = []
    blues = []
    bright = []

    # Pico sends back index and raw pixel value
    while sampnum < 60: # width of bitmap
        data_read = ser.read_until(b'\n',50) # read until newline
        data_text = str(data_read,'utf-8') # convert bytes to string
        data = list(map(int,data_text.split())) # convert string to values

        if(len(data)==2):
            index = data[0]
            raw.append(data[1])
            reds.append(((data[1]>>5)&0x3F)/0x3F*100) # red value is middle 6 bits
            greens.append((data[1]&0x1F)/0x1F*100) # green value is rightmost 5 bits
            blues.append(((data[1]>>11)&0x1F)/0x1F*100) # blue vale is leftmost 5 bits
            bright.append((data[1]&0x1F)+((data[1]>>5)&0x3F)+((data[1]>>11)&0x1F)) # sum of colors
            sampnum = sampnum + 1

    # print the raw color as a 16bit binary to double check bitshifting
    # for i in range(len(reds)):
    #     print(f"{raw[i]:#018b}")

    # plot the colors 
    # import matplotlib.pyplot as plt 
    # x = range(len(reds)) # time array
    # plt.plot(x,reds,'r*-',x,greens,'g*-',x,blues,'b*-')
    # plt.ylabel('color')
    # plt.xlabel('position')
    # plt.show()

    # ci = 0
    # c = rgb_to_grey(np.sum(reds), np.sum(greens), np.sum(blues))
    # for ii in range(sampnum):
    #     ci = ci + rgb_to_grey(reds[ii], greens[ii], blues[ii]) * ii
    # COM = ci/c
    # print(COM)

    # ci = 0
    # c = np.sum(bright)
    # for ii in range(sampnum):
    #     ci = ci + (bright[ii] * ii)
    # COM = ci/c
    # print(COM)

    ci = 0
    c = 1
    for ii in range(sampnum):
        w_or_b = wb(bright[ii])
        c = c+ w_or_b
        ci = ci + (w_or_b * ii)
    COM = ci/c
    print(COM)

ser.close()


