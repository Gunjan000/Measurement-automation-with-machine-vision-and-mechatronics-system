import math
import stl
from stl import mesh
import numpy as np
import ntpath
#import pandas as pd
import serial
import time
from csv import writer
from datetime import datetime


file=r'C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\STLs\p-2004 lower jaw - 10 - model cross.stl'
basename = ntpath.basename(file)
mesh = mesh.Mesh.from_file(file)
threshold= 0.5
#theta spacing
start, stop =-8, 8
theta= np.linspace(start,
               stop,
               num = 5,
               endpoint = True,
               retstep = False,
               dtype = None)

#allinig stl code start
### mass data, volume and inertia data
volume, cog, inertia = mesh.get_mass_properties()
mesh.translate(-cog) #translate to center of mass
l=[]
for thetax in theta:
    from stl import mesh
    def find_mins_maxs(stl):
        minx = stl.x.min()
        maxx = stl.x.max()
        miny = stl.y.min()
        maxy = stl.y.max()
        minz = stl.z.min()
        maxz = stl.z.max()
        X=maxx-minx
        Y=maxy-miny
        Z=maxz-minz
        return X, Y#, Z , minx, maxx, miny, maxy, minz, maxz, 
    mesh = mesh.Mesh.from_file(r'C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\STLs\p-2004 lower jaw - 10 - model cross.stl')
    mesh.translate(-cog)
    mesh.rotate(np.array([0, 0, 1]), np.deg2rad(thetax))
    l.append(find_mins_maxs(mesh))
dim=[]

# append and inset into list
dim.append(list(min(l, key=lambda x: x[1]))) #apend X,Y cordinates to empty list
dim[0].insert(0,basename) #insert file name
#flatlist
dim = [num for sublist in dim for num in sublist]
#creating dataframe
#df=pd.DataFrame(dim)
#allinig stl code end 

###### recorded dimensions
#serial communication for data aquasition
ser = serial.Serial('COM6', 9600)
time.sleep(2)
# Read and record the data

MeasuredData =[]                       # empty list to store the data
for i in range(2):
    b = ser.readline()         # read a byte string
    string_n = b.decode()  # decode byte string into Unicode  
    string = string_n.rstrip() # remove \n and \r
    flt = float(string)        # convert string to float
    MeasuredData.append(flt)           # add to the end of data list
    time.sleep(0.1)            # wait (sleep) 0.1 seconds
ser.close()


# X=60.804382-.4   #float(input("input x dimensions"))
# Y=59.15809-.2   #float(input("input Y dimensions"))
#dim.append(MeasuredData)

dim.append(MeasuredData[0])  #append X dim
dim.append(MeasuredData[1])  #append Y dim

######

dX=round(abs(dim[1]-X),3)
dY=round(abs(dim[2]-Y),3)
dim.append(dX)               #append dX dim
dim.append(dY)               #append dY dim

print("STL X= %s mm, Measured X= %d mm" %(dim[1],dim[3]))
print("STL Y= %s mm, Measured Y= %d mm" %(dim[2],dim[4]))
print("Devivation in X= %s mm Devivation in Y= %s mm" %(dX,dY))
if dX>threshold or dY>threshold:
    dim.append("Rejected")
    print('Status= ',dim[7])
else:
    dim.append("Passed")
    print('Status= ',dim[7])

#time and date
today = datetime.now()
date= today.strftime("%d/%m/%Y")
now = datetime.now()
time= now.strftime("%H:%M:%S")
dim.append(date)
dim.append(time)

######CSV append code start####
csv_path = r'C:\Users\Admin\Desktop\INTERNSHIP\Designs\gauge\test.csv'
# Pre-requisite - Import the writer class from the csv module
# First, open the old CSV file in append mode, hence mentioned as 'a'
# Then, for the CSV file, create a file object
with open(csv_path, 'a', newline='') as f_object:  
    # Pass the CSV  file object to the writer() function
    writer_object = writer(f_object)
    # Result - a writer object
    # Pass the data in the list as an argument into the writerow() function
    writer_object.writerow(dim)  
    # Close the file object
    f_object.close()
######CSV append code end####
print(basename, "data is written successfully")
dim.clear() #erasing all stored data in list