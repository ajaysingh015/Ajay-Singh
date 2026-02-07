from os import listdir
from os.path import isfile, join
import serial 

import numpy as np
import pandas as pd 
import time 
from scipy.integrate import trapz

#step1: be sure to the address of the files that the ftir data is exported is matching to line 11 (mypath)
mypath = r"C:\\Users\\Admin\\Desktop\\Ibrutinib automation\\Exp 2024-08-02 18-32"
# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


#step2: make sure that pump and the potentiostat is correctly addressed in the line 16 and 17
pump_1=serial.Serial("COM5",9600) #HPLC Pump
printer = serial.Serial("COM46", 115200, timeout=1)
arduino_port = 'COM50'
baud_rate = 9600

# Establish a serial connection
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the connection to initialize

#step 3: grab the lines from 22 to 90 and presss f9 
def area_under(data,start,end):
    x = np.flip(data.iloc[start:end,0].to_numpy())
    y = np.flip(data.iloc[start:end,1].to_numpy())
    area = trapz(y,x)
    return np.abs(area)

def file_namer(num):
    str1 = str(num)
    length = int(len((str1)))
    empt = ''
    for i in range(5-length):
        empt = empt+'0'
        
    return empt+str1

        
def ftir_extract(filename,init,end):

    filename = filename

    temp_df = pd.read_csv(filename)
    # nump_df = temp_df.to_numpy()
    area = area_under(temp_df, init, end)
    # max_peak = np.max(nump_df[90:120,1])
    print(area)

    return area


#--------------------------------------------------------------------------------

def function(flowrate_1,flowrate_2,temp,pressure_1):
    
    #set the pumps with the flowrate as the desired flowrate for the function
     
    time.sleep(0.1)
    fr_1=flowrate_1*1000 #converting ml/min to ul/min as pump takes this as input val
    pump_1.write(('flow:'+ str(fr_1) + '\r').encode())
    
   
        
    set_max_pressure(pressure_1)
    #pumps run
    pump_1.write(b'on\r')
    time.sleep(0.1)
      
    time.sleep(200)

 
def function2():
    time.sleep(200)
    
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    val = 0
    
    #change wavelengths as per product here.
    f_row=17 #first row of range for wavelength as per IR CSV
    l_row=24 #last row of range for wavelength as per IR CSV
    
    val += ftir_extract(files[-1],f_row,l_row)
    val += ftir_extract(files[-2],f_row,l_row)
    val += ftir_extract(files[-3],f_row,l_row)

    avg_val = val/3
    
    return avg_val
def set_max_pressure(value):
    command = f"setMaxPressure {value}\n"
    ser.write(command.encode())
    time.sleep(1)  # Wait for Arduino to process the command
    response = ser.readline().decode('utf-8').strip()
    print(response)

def set_min_pressure(value):
    command = f"setMinPressure {value}\n"
    ser.write(command.encode())
    time.sleep(1)  # Wait for Arduino to process the command
    response = ser.readline().decode('utf-8').strip()
    print(response)


#step 4:grab the line 93 and f9
from skopt.optimizer import Optimizer


#step5:in line 96 we have to define the range that (flowrate_1,pressure) (from,to) and after (anytime) appllying changes you need to grab the line 96 and f9
#flowrates are in ml/min, temperature is in celsius
bounds = [(1.0,2.0),(10.0,40.0)]
#step 6: grab the line 100 and f9
opter =Optimizer(bounds,base_estimator='gp',n_initial_points=3,acq_func="EI",random_state=np.random.randint(3326))


#step7: to selecte number of the cycles that you have to do the experiment and then grab the line 104 to 121 and f9: the closed loop experimentation is initiated
number_of_cycles = 22
results = []
flowrates_1 = []
Pressure_1 = []

product_wavelength=True #set to true if product wavelengths being monitored

if product_wavelength == True:
    val=1
else:
    val=-1
    
# Step 8: Test Tubes on Printer
USE_PRINTER = True
REST_HEIGHT = 200
X_HOME = -5
Y_HOME = 20
Z_HOME = 175
DEFAULT_PUMP_TIME="1"
# Distance between test tubes
X_SPACING=20
Y_SPACING=20
# Number of test tubes
X_ROWS = 11
Y_COLUMNS = 4

def send_cmd(cmd):
    print(cmd)
    printer.write(f"{cmd}\n".encode("ASCII"))

def move(x=None, y=None, z=None):
    s = "G0"
    if x is not None:
        s += f"X{x}"
    if y is not None:
        s += f"Y{y}"
    if z is not None:
        s += f"Z{z}"
    
    s+= "F5000"
    send_cmd(s)

def printer_positions():
    for j in range(Y_COLUMNS):
        for i in range(X_ROWS):
            if j%2==1:
                yield (X_HOME + (X_ROWS - 1 - i) * X_SPACING, Y_HOME + j * Y_SPACING, Z_HOME)
            else:
                yield (X_HOME + i * X_SPACING, Y_HOME + j * Y_SPACING, Z_HOME)

# Run this.
tube_location = list(printer_positions())

try:

    for i in range(number_of_cycles):
        move(*tube_location[2*i])
        asked = opter.ask()
        print(asked[0])
        print(asked[1])
        function(asked[0],asked[1])
        
        move(*tube_location[2*i+1])
        # told= function2()
        told = float(input("give the results from offline analysis\n"))
        
        print(f"area under the curve in the round {i:.2f} = {told:.2f}")
        opter.tell(asked,-told*val)

        results.append(told)
        flowrates_1.append(asked[0])
        Pressure_1.append(asked[1])

        dict1 = {"flowrate_1":flowrates_1,"Pressure_1":Pressure_1,"area-results":results}
        df2 = pd.DataFrame(dict1)
        df2.to_csv("output round "+str(i)+".csv")
finally:

      
    pump_1.write(b'off\r')
    pump_1.close()

       

