#This code prints the optimized values of x and y 
#and the total loss encountered after minimization 
#of the prameters. Where x is the offset of the 
#average sun wrt the centre and y is the degree
#of inclination of the axis of sun and average sun
#wrt the reference line, Aries, given in radians.

import numpy as np
import pandas as pd
import math
from sklearn.metrics import mean_squared_error
from scipy.stats.mstats import gmean
from scipy.optimize import minimize
import matplotlib.pyplot as plt

df=pd.read_csv("./../data/01_data_mars_opposition.csv")
#print(df)

data_wrt_sun=df[['ZodiacIndex','Degree','Minute','Second']]
#print(data_wrt_sun)
sun_data_list=data_wrt_sun.values.tolist()
#print(sun_data_list)
sun_deg=[]
sun_rad=[]
for i in sun_data_list:
  p=float(i[0]*30+i[1]+i[2]/60+i[3]/3600)
  sun_deg.append(p)
  sun_rad.append(p*math.pi/180)
#print(sun_deg)
#print(sun_rad)

data_wrt_avg_sun=df[['ZodiacIndexAverageSun','DegreeMean','MinuteMean','SecondMean']]
#print(data_wrt_avg_sun)
avg_sun_data_list=data_wrt_avg_sun.values.tolist()
#print(avg_sun_data_list)
avg_sun_deg=[]
avg_sun_rad=[]
for x in avg_sun_data_list:
  q=float(x[0]*30+x[1]+x[2]/60+x[3]/3600)
  avg_sun_deg.append(q)
  avg_sun_rad.append(q*math.pi/180)
#print(avg_sun_deg)
#print(avg_sun_rad)

def rad(val1,val2):
  a=val1
  b=val2
  radlist=[]
  for r in range(len(sun_deg)):
    alpha=avg_sun_rad[r]
    beta=sun_rad[r]
    x=((a*np.tan(alpha) + np.tan(beta))*np.cos(b) - (a+1)*np.sin(b)) / (np.tan(alpha) - np.tan(beta))
    y=a*np.sin(b) + np.tan(alpha)*(x - a* np.cos(b))
    #y= np.tan(beta)*(x + np.cos(b)) - np.sin(b)
    radius=np.sqrt(x*x + y*y)
    radlist.append(radius)
  return radlist

def minimize_mean(xy):
  radius_list=rad(xy[0],xy[1])
  arithmetic_mean = np.mean(radius_list)
  geometric_mean = gmean(radius_list)
  return np.log(arithmetic_mean) - np.log(geometric_mean)

def verif(val1,val2):
  a=val1
  b=val2
  xlist=[]
  ylist=[]
  radlist=[]
  for r in range(len(sun_deg)):
    alpha=avg_sun_rad[r]
    beta=sun_rad[r]
    x=((a*np.tan(alpha) + np.tan(beta))*np.cos(b) - (a+1)*np.sin(b)) / (np.tan(alpha) - np.tan(beta))
    y=a*np.sin(b) + np.tan(alpha)*(x - a* np.cos(b))
    #y= np.tan(beta)*(x + np.cos(b)) - np.sin(b)
    xlist.append(x)
    ylist.append(y)
    radius=np.sqrt(x*x + y*y)
    radlist.append(radius)
  return radlist,xlist,ylist

xy=[2.5,3]
params = minimize(minimize_mean, xy, bounds=[(0, None), (None, None)])
print("total optimized loss : ",params["fun"])
print("optimized x and y values : ", params["x"][0] ,",", params["x"][1])

#optrad,optx,opty=verif(params["x"][0],params["x"][1])
#print("\n\n The points for mars at opposition with their corresponding distance from centre : ")
#for i in range(len(optrad)):
#	print("point (",optx[i],opty[i],") : radius ", optrad[i])
