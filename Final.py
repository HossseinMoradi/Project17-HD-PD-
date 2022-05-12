import math
import ast
from math import e
from decimal import *
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import ast
getcontext().prec = 28


# first we have defined functions to access signals and vehicles data


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier



def toList(NestedTuple):
    return list(map(toList, NestedTuple)) if isinstance(NestedTuple, (list, tuple)) else NestedTuple

def GetVissimDataVehicles():
    global vehsAttributes
    global vehsAttNames
    vehsAttributesNames = ['No', 'VehType\No', 'Pos', 'VehType\No', 'Lane\Link', 'Speed']
    vehsAttributes = toList(Vissim.Net.Vehicles.GetMultipleAttributes(vehsAttributesNames))
    vehsAttNames = {}
    cnt = 0
    for att in vehsAttributesNames:
        vehsAttNames.update({att: cnt})
        cnt += 1
    global CarCV
    global BusCV
    global Car
    global Bus
    vehTypesAttributes = Vissim.Net.VehicleTypes.GetMultipleAttributes(['No', 'IsCarCV','IsBusCV','IsCar', 'IsBus' ])
    CarCV = [x[0] for x in vehTypesAttributes if x[1] == True and x[3] == True]
    BusCV = [x[0] for x in vehTypesAttributes if x[2] == True and x[4] == True]
    Car = [x[0] for x in vehTypesAttributes if x[3] == True]
    Bus = [x[0] for x in vehTypesAttributes if x[4] == True]



"""
def Signal():
    #we define a user attributre to access SimSec
    Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('SimSec',Vissim.Net.Simulation.SimulationSecond)
    Seconds = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('CycSec')
    SimSec = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('SimSec')
    CLength = 60
    G1=13
    G2=13
    G3=13
    G4=13
    # When we start the simulation, we determine that the signals are operating upon com script
    if SimSec<=1:
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('ContrByCOM', True)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenTimeDuration', G1)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenTimeDuration', G2)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenTimeDuration', G3)
        Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenTimeDuration', G4)



    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenStart', 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('GreenEnd', Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenTimeDuration'))
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenStart',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') + 2)
    Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('GreenEnd',Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') + Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenTimeDuration'))




    if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenStart') - 1:
        if Seconds <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')
        if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') - 1:
            if Seconds < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenStart') - 1:
        if Seconds <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')

        if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') - 1:
            if Seconds < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenStart') - 1:
        if Seconds <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

        if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') - 1:
            if Seconds < Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).AttValue('GreenEnd') + 1:
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
                Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')

    if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenStart') - 1:
        if Seconds <= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'GREEN')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')

        if Seconds >= Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).AttValue('GreenEnd') - 1:
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(1).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(2).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(3).SetAttValue('SigState', 'RED')
            Vissim.Net.SignalControllers.ItemByKey(1).SGs.ItemByKey(4).SetAttValue('SigState', 'RED')



"""


def GeneratingDataLink():
    GetVissimDataVehicles()
    Vissim.Net.SignalControllers.ItemByKey(1).SetAttValue('SimSec',Vissim.Net.Simulation.SimulationSecond)
    
    CellLength=22
    deltaT=1
    SimSec = Vissim.Net.SignalControllers.ItemByKey(1).AttValue('SimSec')
    #we should correlate deltaT with the simulation resolution. In other words, number of simulation per second should be one here. 
    Starting_time=0
    Ending_time=18000


    TimeNo=[]
    i=Starting_time
    k=0
    while i< Ending_time:
        TimeNo.append(k)
        k+=1
        i=i+deltaT



    LinkLength9= Vissim.Net.Links.ItemByKey(9).AttValue('Length2D')
    CellsNo_line9=[]
    i=0
    k=0
    while i< truncate(LinkLength9,-1):
        CellsNo_line9.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k19=[[]]*len(CellsNo_line9)
            z19=[[]]*len(CellsNo_line9)
            m19=[[]]*len(CellsNo_line9)
            n19=[[]]*len(CellsNo_line9)
            T19=[[]]*len(CellsNo_line9)

            for j in CellsNo_line9:
                k29=[]
                z29=[]
                m29=[]
                n29=[]
                T29=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '9':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k29.append(vehAttributes[vehsAttNames['No']])
                                    k19[j]=k29
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z29.append(vehAttributes[vehsAttNames['No']])
                                    z19[j]=z29
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m29.append(vehAttributes[vehsAttNames['No']])
                                    m19[j]=m29

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n29.append(vehAttributes[vehsAttNames['No']])
                                    n19[j]=n29

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T29.append(vehAttributes[vehsAttNames['No']])
                                T19[j]=T29                        


            f2= open("19.txt","a")
            f2.write(str(k19))
            f2.write("\n")
            f2.close()
            f2= open("119.txt","a")
            f2.write(str(z19))
            f2.write("\n")
            f2.close()
            f2= open("1119.txt","a")
            f2.write(str(m19))
            f2.write("\n")
            f2.close()
            f2= open("11119.txt","a")
            f2.write(str(n19))
            f2.write("\n")
            f2.close()

            f2= open("111119.txt","a")
            f2.write(str(T19))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk19=[[]]*len(CellsNo_line9)
                f2= open("09.txt","a")
                f2.write(str(kk19))
                f2.write("\n")
                f2.close()

                zz19=[[]]*len(CellsNo_line9)
                f2= open("009.txt","a")
                f2.write(str(zz19))
                f2.write("\n")
                f2.close()

                mm19=[[]]*len(CellsNo_line9)
                f2= open("0009.txt","a")
                f2.write(str(mm19))
                f2.write("\n")
                f2.close()

                nn19=[[]]*len(CellsNo_line9)
                f2= open("00009.txt","a")
                f2.write(str(nn19))
                f2.write("\n")
                f2.close()     
            
            else:
                kk19=[[]]*len(CellsNo_line9)
                zz19=[[]]*len(CellsNo_line9)
                mm19=[[]]*len(CellsNo_line9)
                nn19=[[]]*len(CellsNo_line9)
                for j in CellsNo_line9:
                    kk29=[]
                    zz29=[]
                    mm29=[]
                    nn29=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '9':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk29.append(vehAttributes[vehsAttNames['No']])
                                        kk19[j]=kk29
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz29.append(vehAttributes[vehsAttNames['No']])
                                        zz19[j]=zz29


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm29.append(vehAttributes[vehsAttNames['No']])
                                        mm19[j]=mm29


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn29.append(vehAttributes[vehsAttNames['No']])
                                        nn19[j]=nn29
                                        

                                        


                f2= open("09.txt","a")
                f2.write(str(kk19))
                f2.write("\n")
                f2.close()


                f2= open("009.txt","a")
                f2.write(str(zz19))
                f2.write("\n")
                f2.close()


                f2= open("0009.txt","a")
                f2.write(str(mm19))
                f2.write("\n")
                f2.close()

                f2= open("00009.txt","a")
                f2.write(str(nn19))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk19=[[]]*len(CellsNo_line9)
            zzz19=[[]]*len(CellsNo_line9)
            mmm19=[[]]*len(CellsNo_line9)
            nnn19=[[]]*len(CellsNo_line9)
            for j in CellsNo_line9:
                kkk29=[]
                zzz29=[]
                mmm29=[]
                nnn29=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '9':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk29.append(vehAttributes[vehsAttNames['No']])
                                    kkk19[j]=kkk29

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '9':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz29.append(vehAttributes[vehsAttNames['No']])
                                        zzz19[j]=zzz29


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm29.append(vehAttributes[vehsAttNames['No']])
                                        mmm19[j]=mmm29


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn29.append(vehAttributes[vehsAttNames['No']])
                                        nnn19[j]=nnn29
                                
            f2= open("29.txt","a")
            f2.write(str(kkk19))
            f2.write("\n")
            f2.close()

            f2= open("229.txt","a")
            f2.write(str(zzz19))
            f2.write("\n")
            f2.close()



            f2= open("2229.txt","a")
            f2.write(str(mmm19))
            f2.write("\n")
            f2.close()


            f2= open("22229.txt","a")
            f2.write(str(nnn19))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('09.txt', 'r')
        g09=[]
        for line in f.readlines():
            A09= ast.literal_eval(line)
            g09.append(A09)
        f.close()


        f = open('009.txt', 'r')
        g009=[]
        for line in f.readlines():
            A009= ast.literal_eval(line)
            g009.append(A009)
        f.close()

        f = open('0009.txt', 'r')
        g0009=[]
        for line in f.readlines():
            A0009= ast.literal_eval(line)
            g0009.append(A0009)
        f.close()

        f = open('00009.txt', 'r')
        g00009=[]
        for line in f.readlines():
            A00009= ast.literal_eval(line)
            g00009.append(A00009)
        f.close()


        f = open('19.txt', 'r')
        g19=[]
        for line in f.readlines():
            A19= ast.literal_eval(line)
            g19.append(A19)
        f.close()

        f = open('119.txt', 'r')
        g119=[]
        for line in f.readlines():
            A119= ast.literal_eval(line)
            g119.append(A119)
        f.close()


        f = open('1119.txt', 'r')
        g1119=[]
        for line in f.readlines():
            A1119= ast.literal_eval(line)
            g1119.append(A1119)
        f.close()


        f = open('11119.txt', 'r')
        g11119=[]
        for line in f.readlines():
            A11119= ast.literal_eval(line)
            g11119.append(A11119)
        f.close()


        f = open('111119.txt', 'r')
        g111119=[]
        for line in f.readlines():
            A111119= ast.literal_eval(line)
            g111119.append(A111119)
        f.close()

        f = open('29.txt', 'r')
        g29=[]
        for line in f.readlines():
            A29= ast.literal_eval(line)
            g29.append(A29)
        f.close()

        f = open('229.txt', 'r')
        g229=[]
        for line in f.readlines():
            A229= ast.literal_eval(line)
            g229.append(A229)
        f.close()

        f = open('2229.txt', 'r')
        g2229=[]
        for line in f.readlines():
            A2229= ast.literal_eval(line)
            g2229.append(A2229)
        f.close()

        f = open('22229.txt', 'r')
        g22229=[]
        for line in f.readlines():
            A22229= ast.literal_eval(line)
            g22229.append(A22229)
        f.close()


        Current_Number_CarCV_line9=[0]*len(CellsNo_line9)
        Current_Number_BusCV_line9=[0]*len(CellsNo_line9)
        Current_Number_Car_line9=[0]*len(CellsNo_line9)
        Current_Number_Bus_line9=[0]*len(CellsNo_line9)
        
        Arrival_CarCV_line9=[0]*len(CellsNo_line9)
        Arrival_BusCV_line9=[0]*len(CellsNo_line9)
        Arrival_Car_line9=[0]*len(CellsNo_line9)
        Arrival_Bus_line9=[0]*len(CellsNo_line9)

        Departure_CarCV_line9=[0]*len(CellsNo_line9)
        Departure_BusCV_line9=[0]*len(CellsNo_line9)
        Departure_Car_line9=[0]*len(CellsNo_line9)
        Departure_Bus_line9=[0]*len(CellsNo_line9)

        Average_speed_CarCV_line9=[0]*len(CellsNo_line9)
        Average_speed_BusCV_line9=[0]*len(CellsNo_line9)
        Average_speed_Car_line9=[0]*len(CellsNo_line9)
        Average_speed_Bus_line9=[0]*len(CellsNo_line9)



        Turn1_line9=[0]*len(CellsNo_line9)
        Turn2_line9=[0]*len(CellsNo_line9)






        for i in g111119: 
            for j in CellsNo_line9:
                if len(i[j])>0:
                    k1=0
                    k2=0
                    for k in i[j]:
                        try:
                            if Vissim.Net.Vehicles.ItemByKey(k).AttValue('NextLink') == '10000':
                                k1=k1+1
                            if Vissim.Net.Vehicles.ItemByKey(k).AttValue('NextLink') == '10002':
                                k2=k2+1     
                            Turn1_line9[j]= k1/(k1+k2)
                            Turn2_line9[j]= k2/(k1+k2)

                        except:
                            Turn1_line9[j]= 0
                            Turn2_line9[j]= 0


                else:
                    Turn1_line9[j]= 0
                    Turn2_line9[j]= 0


        for i in g19: 
            for j in CellsNo_line9:
                Current_Number_CarCV_line9[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line9[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line9[j]= 0




        for i in g119: 
            for j in CellsNo_line9:
                Current_Number_BusCV_line9[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line9[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line9[j]= 0





        for i in g1119: 
            for j in CellsNo_line9:
                Current_Number_Car_line9[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line9[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line9[j]= 0



        for i in g11119: 
            for j in CellsNo_line9:
                Current_Number_Bus_line9[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line9[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line9[j]= 0






        for i in range(len(g19)):          
            for j in CellsNo_line9:
                m=[]
                if len(g19[i][j])>0:
                    for k in g19[i][j]:
                        if k not in g09[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line9[j] = len(m)
                


        for i in range(len(g119)):          
            for j in CellsNo_line9:
                m=[]
                if len(g119[i][j])>0:
                    for k in g119[i][j]:
                        if k not in g009[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line9[j] = len(m)




        for i in range(len(g1119)):          
            for j in CellsNo_line9:
                m=[]
                if len(g1119[i][j])>0:
                    for k in g1119[i][j]:
                        if k not in g0009[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line9[j] = len(m)







        for i in range(len(g11119)):          
            for j in CellsNo_line9:
                m=[]
                if len(g11119[i][j])>0:
                    for k in g11119[i][j]:
                        if k not in g00009[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line9[j] = len(m)






        for i in range(len(g29)):          
            for j in CellsNo_line9:
                m=[]
                if len(g19[i][j])>0:
                    for k in g19[i][j]:
                        if k not in g29[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line9[j] = len(m)
                



        for i in range(len(g229)):          
            for j in CellsNo_line9:
                m=[]
                if len(g119[i][j])>0:
                    for k in g119[i][j]:
                        if k not in g229[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line9[j] = len(m)




        for i in range(len(g2229)):          
            for j in CellsNo_line9:
                m=[]
                if len(g1119[i][j])>0:
                    for k in g1119[i][j]:
                        if k not in g2229[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line9[j] = len(m)



        for i in range(len(g22229)):          
            for j in CellsNo_line9:
                m=[]
                if len(g11119[i][j])>0:
                    for k in g11119[i][j]:
                        if k not in g22229[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line9[j] = len(m)





        f2= open("Current_Number_CarCV_line9.txt","a")
        f2.write(str(Current_Number_CarCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line9.txt","a")
        f2.write(str(Current_Number_BusCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line9.txt","a")
        f2.write(str(Current_Number_Car_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line9.txt","a")
        f2.write(str(Current_Number_Bus_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line9.txt","a")
        f2.write(str(Average_speed_CarCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line9.txt","a")
        f2.write(str(Average_speed_BusCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line9.txt","a")
        f2.write(str(Average_speed_Car_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line9.txt","a")
        f2.write(str(Average_speed_Bus_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line9.txt","a")
        f2.write(str(Arrival_CarCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line9.txt","a")
        f2.write(str(Arrival_BusCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line9.txt","a")
        f2.write(str(Arrival_Car_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line9.txt","a")
        f2.write(str(Arrival_Bus_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line9.txt","a")
        f2.write(str(Departure_CarCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line9.txt","a")
        f2.write(str(Departure_BusCV_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line9.txt","a")
        f2.write(str(Departure_Car_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line9.txt","a")
        f2.write(str(Departure_Bus_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line9.txt","a")
        f2.write(str(Turn1_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line9.txt","a")
        f2.write(str(Turn2_line9))
        f2.write("\n")
        f2.write(",")
        f2.close()






    LinkLength10= Vissim.Net.Links.ItemByKey(10).AttValue('Length2D')
    CellsNo_line10=[]
    i=0
    k=0
    while i< truncate(LinkLength10,-1):
        CellsNo_line10.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k110=[[]]*len(CellsNo_line10)
            z110=[[]]*len(CellsNo_line10)
            m110=[[]]*len(CellsNo_line10)
            n110=[[]]*len(CellsNo_line10)
            T110=[[]]*len(CellsNo_line10)

            for j in CellsNo_line10:
                k210=[]
                z210=[]
                m210=[]
                n210=[]
                T210=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '10':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k210.append(vehAttributes[vehsAttNames['No']])
                                    k110[j]=k210
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z210.append(vehAttributes[vehsAttNames['No']])
                                    z110[j]=z210
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m210.append(vehAttributes[vehsAttNames['No']])
                                    m110[j]=m210

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n210.append(vehAttributes[vehsAttNames['No']])
                                    n110[j]=n210

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T210.append(vehAttributes[vehsAttNames['No']])
                                T110[j]=T210                        


            f2= open("110.txt","a")
            f2.write(str(k110))
            f2.write("\n")
            f2.close()
            f2= open("1110.txt","a")
            f2.write(str(z110))
            f2.write("\n")
            f2.close()
            f2= open("11110.txt","a")
            f2.write(str(m110))
            f2.write("\n")
            f2.close()
            f2= open("111110.txt","a")
            f2.write(str(n110))
            f2.write("\n")
            f2.close()

            f2= open("1111110.txt","a")
            f2.write(str(T110))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk110=[[]]*len(CellsNo_line10)
                f2= open("010.txt","a")
                f2.write(str(kk110))
                f2.write("\n")
                f2.close()

                zz110=[[]]*len(CellsNo_line10)
                f2= open("0010.txt","a")
                f2.write(str(zz110))
                f2.write("\n")
                f2.close()

                mm110=[[]]*len(CellsNo_line10)
                f2= open("00010.txt","a")
                f2.write(str(mm110))
                f2.write("\n")
                f2.close()

                nn110=[[]]*len(CellsNo_line10)
                f2= open("000010.txt","a")
                f2.write(str(nn110))
                f2.write("\n")
                f2.close()     
            
            else:
                kk110=[[]]*len(CellsNo_line10)
                zz110=[[]]*len(CellsNo_line10)
                mm110=[[]]*len(CellsNo_line10)
                nn110=[[]]*len(CellsNo_line10)
                for j in CellsNo_line10:
                    kk210=[]
                    zz210=[]
                    mm210=[]
                    nn210=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '10':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk210.append(vehAttributes[vehsAttNames['No']])
                                        kk110[j]=kk210
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz210.append(vehAttributes[vehsAttNames['No']])
                                        zz110[j]=zz210


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm210.append(vehAttributes[vehsAttNames['No']])
                                        mm110[j]=mm210


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn210.append(vehAttributes[vehsAttNames['No']])
                                        nn110[j]=nn210
                                        

                                        


                f2= open("010.txt","a")
                f2.write(str(kk110))
                f2.write("\n")
                f2.close()


                f2= open("0010.txt","a")
                f2.write(str(zz110))
                f2.write("\n")
                f2.close()


                f2= open("00010.txt","a")
                f2.write(str(mm110))
                f2.write("\n")
                f2.close()

                f2= open("000010.txt","a")
                f2.write(str(nn110))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk110=[[]]*len(CellsNo_line10)
            zzz110=[[]]*len(CellsNo_line10)
            mmm110=[[]]*len(CellsNo_line10)
            nnn110=[[]]*len(CellsNo_line10)
            for j in CellsNo_line10:
                kkk210=[]
                zzz210=[]
                mmm210=[]
                nnn210=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '10':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk210.append(vehAttributes[vehsAttNames['No']])
                                    kkk110[j]=kkk210

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '10':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz210.append(vehAttributes[vehsAttNames['No']])
                                        zzz110[j]=zzz210


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm210.append(vehAttributes[vehsAttNames['No']])
                                        mmm110[j]=mmm210


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn210.append(vehAttributes[vehsAttNames['No']])
                                        nnn110[j]=nnn210
                                
            f2= open("210.txt","a")
            f2.write(str(kkk110))
            f2.write("\n")
            f2.close()

            f2= open("2210.txt","a")
            f2.write(str(zzz110))
            f2.write("\n")
            f2.close()



            f2= open("22210.txt","a")
            f2.write(str(mmm110))
            f2.write("\n")
            f2.close()


            f2= open("222210.txt","a")
            f2.write(str(nnn110))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('010.txt', 'r')
        g010=[]
        for line in f.readlines():
            A010= ast.literal_eval(line)
            g010.append(A010)
        f.close()


        f = open('0010.txt', 'r')
        g0010=[]
        for line in f.readlines():
            A0010= ast.literal_eval(line)
            g0010.append(A0010)
        f.close()

        f = open('00010.txt', 'r')
        g00010=[]
        for line in f.readlines():
            A00010= ast.literal_eval(line)
            g00010.append(A00010)
        f.close()

        f = open('000010.txt', 'r')
        g000010=[]
        for line in f.readlines():
            A000010= ast.literal_eval(line)
            g000010.append(A000010)
        f.close()


        f = open('110.txt', 'r')
        g110=[]
        for line in f.readlines():
            A110= ast.literal_eval(line)
            g110.append(A110)
        f.close()

        f = open('1110.txt', 'r')
        g1110=[]
        for line in f.readlines():
            A1110= ast.literal_eval(line)
            g1110.append(A1110)
        f.close()


        f = open('11110.txt', 'r')
        g11110=[]
        for line in f.readlines():
            A11110= ast.literal_eval(line)
            g11110.append(A11110)
        f.close()


        f = open('111110.txt', 'r')
        g111110=[]
        for line in f.readlines():
            A111110= ast.literal_eval(line)
            g111110.append(A111110)
        f.close()


        f = open('1111110.txt', 'r')
        g1111110=[]
        for line in f.readlines():
            A1111110= ast.literal_eval(line)
            g1111110.append(A1111110)
        f.close()

        f = open('210.txt', 'r')
        g210=[]
        for line in f.readlines():
            A210= ast.literal_eval(line)
            g210.append(A210)
        f.close()

        f = open('2210.txt', 'r')
        g2210=[]
        for line in f.readlines():
            A2210= ast.literal_eval(line)
            g2210.append(A2210)
        f.close()

        f = open('22210.txt', 'r')
        g22210=[]
        for line in f.readlines():
            A22210= ast.literal_eval(line)
            g22210.append(A22210)
        f.close()

        f = open('222210.txt', 'r')
        g222210=[]
        for line in f.readlines():
            A222210= ast.literal_eval(line)
            g222210.append(A222210)
        f.close()


        Current_Number_CarCV_line10=[0]*len(CellsNo_line10)
        Current_Number_BusCV_line10=[0]*len(CellsNo_line10)
        Current_Number_Car_line10=[0]*len(CellsNo_line10)
        Current_Number_Bus_line10=[0]*len(CellsNo_line10)
        
        Arrival_CarCV_line10=[0]*len(CellsNo_line10)
        Arrival_BusCV_line10=[0]*len(CellsNo_line10)
        Arrival_Car_line10=[0]*len(CellsNo_line10)
        Arrival_Bus_line10=[0]*len(CellsNo_line10)

        Departure_CarCV_line10=[0]*len(CellsNo_line10)
        Departure_BusCV_line10=[0]*len(CellsNo_line10)
        Departure_Car_line10=[0]*len(CellsNo_line10)
        Departure_Bus_line10=[0]*len(CellsNo_line10)

        Average_speed_CarCV_line10=[0]*len(CellsNo_line10)
        Average_speed_BusCV_line10=[0]*len(CellsNo_line10)
        Average_speed_Car_line10=[0]*len(CellsNo_line10)
        Average_speed_Bus_line10=[0]*len(CellsNo_line10)



        Turn1_line10=[0]*len(CellsNo_line10)
        Turn2_line10=[0]*len(CellsNo_line10)






        for i in g1111110: 
            for j in CellsNo_line10:
                if len(i[j])>0:
                    Turn1_line10[j]= 1
                    Turn2_line10[j]= 0


                else:
                    Turn1_line10[j]= 0
                    Turn2_line10[j]= 0


        for i in g110: 
            for j in CellsNo_line10:
                Current_Number_CarCV_line10[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line10[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line10[j]= 0




        for i in g1110: 
            for j in CellsNo_line10:
                Current_Number_BusCV_line10[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line10[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line10[j]= 0





        for i in g11110: 
            for j in CellsNo_line10:
                Current_Number_Car_line10[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line10[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line10[j]= 0



        for i in g111110: 
            for j in CellsNo_line10:
                Current_Number_Bus_line10[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line10[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line10[j]= 0






        for i in range(len(g110)):          
            for j in CellsNo_line10:
                m=[]
                if len(g110[i][j])>0:
                    for k in g110[i][j]:
                        if k not in g010[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line10[j] = len(m)
                


        for i in range(len(g1110)):          
            for j in CellsNo_line10:
                m=[]
                if len(g1110[i][j])>0:
                    for k in g1110[i][j]:
                        if k not in g0010[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line10[j] = len(m)




        for i in range(len(g11110)):          
            for j in CellsNo_line10:
                m=[]
                if len(g11110[i][j])>0:
                    for k in g11110[i][j]:
                        if k not in g00010[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line10[j] = len(m)







        for i in range(len(g111110)):          
            for j in CellsNo_line10:
                m=[]
                if len(g111110[i][j])>0:
                    for k in g111110[i][j]:
                        if k not in g000010[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line10[j] = len(m)






        for i in range(len(g210)):          
            for j in CellsNo_line10:
                m=[]
                if len(g110[i][j])>0:
                    for k in g110[i][j]:
                        if k not in g210[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line10[j] = len(m)
                



        for i in range(len(g2210)):          
            for j in CellsNo_line10:
                m=[]
                if len(g1110[i][j])>0:
                    for k in g1110[i][j]:
                        if k not in g2210[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line10[j] = len(m)




        for i in range(len(g22210)):          
            for j in CellsNo_line10:
                m=[]
                if len(g11110[i][j])>0:
                    for k in g11110[i][j]:
                        if k not in g22210[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line10[j] = len(m)



        for i in range(len(g222210)):          
            for j in CellsNo_line10:
                m=[]
                if len(g111110[i][j])>0:
                    for k in g111110[i][j]:
                        if k not in g222210[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line10[j] = len(m)





        f2= open("Current_Number_CarCV_line10.txt","a")
        f2.write(str(Current_Number_CarCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line10.txt","a")
        f2.write(str(Current_Number_BusCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line10.txt","a")
        f2.write(str(Current_Number_Car_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line10.txt","a")
        f2.write(str(Current_Number_Bus_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line10.txt","a")
        f2.write(str(Average_speed_CarCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line10.txt","a")
        f2.write(str(Average_speed_BusCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line10.txt","a")
        f2.write(str(Average_speed_Car_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line10.txt","a")
        f2.write(str(Average_speed_Bus_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line10.txt","a")
        f2.write(str(Arrival_CarCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line10.txt","a")
        f2.write(str(Arrival_BusCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line10.txt","a")
        f2.write(str(Arrival_Car_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line10.txt","a")
        f2.write(str(Arrival_Bus_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line10.txt","a")
        f2.write(str(Departure_CarCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line10.txt","a")
        f2.write(str(Departure_BusCV_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line10.txt","a")
        f2.write(str(Departure_Car_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line10.txt","a")
        f2.write(str(Departure_Bus_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line10.txt","a")
        f2.write(str(Turn1_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line10.txt","a")
        f2.write(str(Turn2_line10))
        f2.write("\n")
        f2.write(",")
        f2.close()




    LinkLength2= Vissim.Net.Links.ItemByKey(2).AttValue('Length2D')
    CellsNo_line2=[]
    i=0
    k=0
    while i< truncate(LinkLength2,-1):
        CellsNo_line2.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k12=[[]]*len(CellsNo_line2)
            z12=[[]]*len(CellsNo_line2)
            m12=[[]]*len(CellsNo_line2)
            n12=[[]]*len(CellsNo_line2)
            T12=[[]]*len(CellsNo_line2)

            for j in CellsNo_line2:
                k22=[]
                z22=[]
                m22=[]
                n22=[]
                T22=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '2':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k22.append(vehAttributes[vehsAttNames['No']])
                                    k12[j]=k22
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z22.append(vehAttributes[vehsAttNames['No']])
                                    z12[j]=z22
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m22.append(vehAttributes[vehsAttNames['No']])
                                    m12[j]=m22

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n22.append(vehAttributes[vehsAttNames['No']])
                                    n12[j]=n22

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T22.append(vehAttributes[vehsAttNames['No']])
                                T12[j]=T22                        


            f2= open("12.txt","a")
            f2.write(str(k12))
            f2.write("\n")
            f2.close()
            f2= open("112.txt","a")
            f2.write(str(z12))
            f2.write("\n")
            f2.close()
            f2= open("1112.txt","a")
            f2.write(str(m12))
            f2.write("\n")
            f2.close()
            f2= open("11112.txt","a")
            f2.write(str(n12))
            f2.write("\n")
            f2.close()

            f2= open("111112.txt","a")
            f2.write(str(T12))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk12=[[]]*len(CellsNo_line2)
                f2= open("02.txt","a")
                f2.write(str(kk12))
                f2.write("\n")
                f2.close()

                zz12=[[]]*len(CellsNo_line2)
                f2= open("002.txt","a")
                f2.write(str(zz12))
                f2.write("\n")
                f2.close()

                mm12=[[]]*len(CellsNo_line2)
                f2= open("0002.txt","a")
                f2.write(str(mm12))
                f2.write("\n")
                f2.close()

                nn12=[[]]*len(CellsNo_line2)
                f2= open("00002.txt","a")
                f2.write(str(nn12))
                f2.write("\n")
                f2.close()     
            
            else:
                kk12=[[]]*len(CellsNo_line2)
                zz12=[[]]*len(CellsNo_line2)
                mm12=[[]]*len(CellsNo_line2)
                nn12=[[]]*len(CellsNo_line2)
                for j in CellsNo_line2:
                    kk22=[]
                    zz22=[]
                    mm22=[]
                    nn22=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '2':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk22.append(vehAttributes[vehsAttNames['No']])
                                        kk12[j]=kk22
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz22.append(vehAttributes[vehsAttNames['No']])
                                        zz12[j]=zz22


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm22.append(vehAttributes[vehsAttNames['No']])
                                        mm12[j]=mm22


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn22.append(vehAttributes[vehsAttNames['No']])
                                        nn12[j]=nn22
                                        

                                        


                f2= open("02.txt","a")
                f2.write(str(kk12))
                f2.write("\n")
                f2.close()


                f2= open("002.txt","a")
                f2.write(str(zz12))
                f2.write("\n")
                f2.close()


                f2= open("0002.txt","a")
                f2.write(str(mm12))
                f2.write("\n")
                f2.close()

                f2= open("00002.txt","a")
                f2.write(str(nn12))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk12=[[]]*len(CellsNo_line2)
            zzz12=[[]]*len(CellsNo_line2)
            mmm12=[[]]*len(CellsNo_line2)
            nnn12=[[]]*len(CellsNo_line2)
            for j in CellsNo_line2:
                kkk22=[]
                zzz22=[]
                mmm22=[]
                nnn22=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '2':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk22.append(vehAttributes[vehsAttNames['No']])
                                    kkk12[j]=kkk22

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '2':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz22.append(vehAttributes[vehsAttNames['No']])
                                        zzz12[j]=zzz22


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm22.append(vehAttributes[vehsAttNames['No']])
                                        mmm12[j]=mmm22


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn22.append(vehAttributes[vehsAttNames['No']])
                                        nnn12[j]=nnn22
                                
            f2= open("22.txt","a")
            f2.write(str(kkk12))
            f2.write("\n")
            f2.close()

            f2= open("222.txt","a")
            f2.write(str(zzz12))
            f2.write("\n")
            f2.close()



            f2= open("2222.txt","a")
            f2.write(str(mmm12))
            f2.write("\n")
            f2.close()


            f2= open("22222.txt","a")
            f2.write(str(nnn12))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('02.txt', 'r')
        g02=[]
        for line in f.readlines():
            A02= ast.literal_eval(line)
            g02.append(A02)
        f.close()


        f = open('002.txt', 'r')
        g002=[]
        for line in f.readlines():
            A002= ast.literal_eval(line)
            g002.append(A002)
        f.close()

        f = open('0002.txt', 'r')
        g0002=[]
        for line in f.readlines():
            A0002= ast.literal_eval(line)
            g0002.append(A0002)
        f.close()

        f = open('00002.txt', 'r')
        g00002=[]
        for line in f.readlines():
            A00002= ast.literal_eval(line)
            g00002.append(A00002)
        f.close()


        f = open('12.txt', 'r')
        g12=[]
        for line in f.readlines():
            A12= ast.literal_eval(line)
            g12.append(A12)
        f.close()

        f = open('112.txt', 'r')
        g112=[]
        for line in f.readlines():
            A112= ast.literal_eval(line)
            g112.append(A112)
        f.close()


        f = open('1112.txt', 'r')
        g1112=[]
        for line in f.readlines():
            A1112= ast.literal_eval(line)
            g1112.append(A1112)
        f.close()


        f = open('11112.txt', 'r')
        g11112=[]
        for line in f.readlines():
            A11112= ast.literal_eval(line)
            g11112.append(A11112)
        f.close()


        f = open('111112.txt', 'r')
        g111112=[]
        for line in f.readlines():
            A111112= ast.literal_eval(line)
            g111112.append(A111112)
        f.close()

        f = open('22.txt', 'r')
        g22=[]
        for line in f.readlines():
            A22= ast.literal_eval(line)
            g22.append(A22)
        f.close()

        f = open('222.txt', 'r')
        g222=[]
        for line in f.readlines():
            A222= ast.literal_eval(line)
            g222.append(A222)
        f.close()

        f = open('2222.txt', 'r')
        g2222=[]
        for line in f.readlines():
            A2222= ast.literal_eval(line)
            g2222.append(A2222)
        f.close()

        f = open('22222.txt', 'r')
        g22222=[]
        for line in f.readlines():
            A22222= ast.literal_eval(line)
            g22222.append(A22222)
        f.close()


        Current_Number_CarCV_line2=[0]*len(CellsNo_line2)
        Current_Number_BusCV_line2=[0]*len(CellsNo_line2)
        Current_Number_Car_line2=[0]*len(CellsNo_line2)
        Current_Number_Bus_line2=[0]*len(CellsNo_line2)
        
        Arrival_CarCV_line2=[0]*len(CellsNo_line2)
        Arrival_BusCV_line2=[0]*len(CellsNo_line2)
        Arrival_Car_line2=[0]*len(CellsNo_line2)
        Arrival_Bus_line2=[0]*len(CellsNo_line2)

        Departure_CarCV_line2=[0]*len(CellsNo_line2)
        Departure_BusCV_line2=[0]*len(CellsNo_line2)
        Departure_Car_line2=[0]*len(CellsNo_line2)
        Departure_Bus_line2=[0]*len(CellsNo_line2)

        Average_speed_CarCV_line2=[0]*len(CellsNo_line2)
        Average_speed_BusCV_line2=[0]*len(CellsNo_line2)
        Average_speed_Car_line2=[0]*len(CellsNo_line2)
        Average_speed_Bus_line2=[0]*len(CellsNo_line2)



        Turn1_line2=[0]*len(CellsNo_line2)
        Turn2_line2=[0]*len(CellsNo_line2)






        for i in g111112: 
            for j in CellsNo_line2:
                if len(i[j])>0:

                    Turn1_line2[j]= 1
                    Turn2_line2[j]= 0

                else:
                    Turn1_line2[j]= 0
                    Turn2_line2[j]= 0


        for i in g12: 
            for j in CellsNo_line2:
                Current_Number_CarCV_line2[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line2[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line2[j]= 0




        for i in g112: 
            for j in CellsNo_line2:
                Current_Number_BusCV_line2[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line2[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line2[j]= 0





        for i in g1112: 
            for j in CellsNo_line2:
                Current_Number_Car_line2[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line2[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line2[j]= 0



        for i in g11112: 
            for j in CellsNo_line2:
                Current_Number_Bus_line2[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line2[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line2[j]= 0






        for i in range(len(g12)):          
            for j in CellsNo_line2:
                m=[]
                if len(g12[i][j])>0:
                    for k in g12[i][j]:
                        if k not in g02[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line2[j] = len(m)
                


        for i in range(len(g112)):          
            for j in CellsNo_line2:
                m=[]
                if len(g112[i][j])>0:
                    for k in g112[i][j]:
                        if k not in g002[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line2[j] = len(m)




        for i in range(len(g1112)):          
            for j in CellsNo_line2:
                m=[]
                if len(g1112[i][j])>0:
                    for k in g1112[i][j]:
                        if k not in g0002[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line2[j] = len(m)







        for i in range(len(g11112)):          
            for j in CellsNo_line2:
                m=[]
                if len(g11112[i][j])>0:
                    for k in g11112[i][j]:
                        if k not in g00002[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line2[j] = len(m)






        for i in range(len(g22)):          
            for j in CellsNo_line2:
                m=[]
                if len(g12[i][j])>0:
                    for k in g12[i][j]:
                        if k not in g22[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line2[j] = len(m)
                



        for i in range(len(g222)):          
            for j in CellsNo_line2:
                m=[]
                if len(g112[i][j])>0:
                    for k in g112[i][j]:
                        if k not in g222[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line2[j] = len(m)




        for i in range(len(g2222)):          
            for j in CellsNo_line2:
                m=[]
                if len(g1112[i][j])>0:
                    for k in g1112[i][j]:
                        if k not in g2222[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line2[j] = len(m)



        for i in range(len(g22222)):          
            for j in CellsNo_line2:
                m=[]
                if len(g11112[i][j])>0:
                    for k in g11112[i][j]:
                        if k not in g22222[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line2[j] = len(m)





        f2= open("Current_Number_CarCV_line2.txt","a")
        f2.write(str(Current_Number_CarCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line2.txt","a")
        f2.write(str(Current_Number_BusCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line2.txt","a")
        f2.write(str(Current_Number_Car_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line2.txt","a")
        f2.write(str(Current_Number_Bus_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line2.txt","a")
        f2.write(str(Average_speed_CarCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line2.txt","a")
        f2.write(str(Average_speed_BusCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line2.txt","a")
        f2.write(str(Average_speed_Car_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line2.txt","a")
        f2.write(str(Average_speed_Bus_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line2.txt","a")
        f2.write(str(Arrival_CarCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line2.txt","a")
        f2.write(str(Arrival_BusCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line2.txt","a")
        f2.write(str(Arrival_Car_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line2.txt","a")
        f2.write(str(Arrival_Bus_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line2.txt","a")
        f2.write(str(Departure_CarCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line2.txt","a")
        f2.write(str(Departure_BusCV_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line2.txt","a")
        f2.write(str(Departure_Car_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line2.txt","a")
        f2.write(str(Departure_Bus_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line2.txt","a")
        f2.write(str(Turn1_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line2.txt","a")
        f2.write(str(Turn2_line2))
        f2.write("\n")
        f2.write(",")
        f2.close()






    LinkLength1= Vissim.Net.Links.ItemByKey(1).AttValue('Length2D')
    CellsNo_line1=[]
    i=0
    k=0
    while i< truncate(LinkLength1,-1):
        CellsNo_line1.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k11=[[]]*len(CellsNo_line1)
            z11=[[]]*len(CellsNo_line1)
            m11=[[]]*len(CellsNo_line1)
            n11=[[]]*len(CellsNo_line1)
            T11=[[]]*len(CellsNo_line1)

            for j in CellsNo_line1:
                k21=[]
                z21=[]
                m21=[]
                n21=[]
                T21=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '1':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k21.append(vehAttributes[vehsAttNames['No']])
                                    k11[j]=k21
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z21.append(vehAttributes[vehsAttNames['No']])
                                    z11[j]=z21
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m21.append(vehAttributes[vehsAttNames['No']])
                                    m11[j]=m21

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n21.append(vehAttributes[vehsAttNames['No']])
                                    n11[j]=n21

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T21.append(vehAttributes[vehsAttNames['No']])
                                T11[j]=T21                        


            f2= open("11.txt","a")
            f2.write(str(k11))
            f2.write("\n")
            f2.close()
            f2= open("111.txt","a")
            f2.write(str(z11))
            f2.write("\n")
            f2.close()
            f2= open("1111.txt","a")
            f2.write(str(m11))
            f2.write("\n")
            f2.close()
            f2= open("11111.txt","a")
            f2.write(str(n11))
            f2.write("\n")
            f2.close()

            f2= open("111111.txt","a")
            f2.write(str(T11))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk11=[[]]*len(CellsNo_line1)
                f2= open("01.txt","a")
                f2.write(str(kk11))
                f2.write("\n")
                f2.close()

                zz11=[[]]*len(CellsNo_line1)
                f2= open("001.txt","a")
                f2.write(str(zz11))
                f2.write("\n")
                f2.close()

                mm11=[[]]*len(CellsNo_line1)
                f2= open("0001.txt","a")
                f2.write(str(mm11))
                f2.write("\n")
                f2.close()

                nn11=[[]]*len(CellsNo_line1)
                f2= open("00001.txt","a")
                f2.write(str(nn11))
                f2.write("\n")
                f2.close()     
            
            else:
                kk11=[[]]*len(CellsNo_line1)
                zz11=[[]]*len(CellsNo_line1)
                mm11=[[]]*len(CellsNo_line1)
                nn11=[[]]*len(CellsNo_line1)
                for j in CellsNo_line1:
                    kk21=[]
                    zz21=[]
                    mm21=[]
                    nn21=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '1':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk21.append(vehAttributes[vehsAttNames['No']])
                                        kk11[j]=kk21
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz21.append(vehAttributes[vehsAttNames['No']])
                                        zz11[j]=zz21


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm21.append(vehAttributes[vehsAttNames['No']])
                                        mm11[j]=mm21


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn21.append(vehAttributes[vehsAttNames['No']])
                                        nn11[j]=nn21
                                        

                                        


                f2= open("01.txt","a")
                f2.write(str(kk11))
                f2.write("\n")
                f2.close()


                f2= open("001.txt","a")
                f2.write(str(zz11))
                f2.write("\n")
                f2.close()


                f2= open("0001.txt","a")
                f2.write(str(mm11))
                f2.write("\n")
                f2.close()

                f2= open("00001.txt","a")
                f2.write(str(nn11))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk11=[[]]*len(CellsNo_line1)
            zzz11=[[]]*len(CellsNo_line1)
            mmm11=[[]]*len(CellsNo_line1)
            nnn11=[[]]*len(CellsNo_line1)
            for j in CellsNo_line1:
                kkk21=[]
                zzz21=[]
                mmm21=[]
                nnn21=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '1':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk21.append(vehAttributes[vehsAttNames['No']])
                                    kkk11[j]=kkk21

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '1':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz21.append(vehAttributes[vehsAttNames['No']])
                                        zzz11[j]=zzz21


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm21.append(vehAttributes[vehsAttNames['No']])
                                        mmm11[j]=mmm21


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn21.append(vehAttributes[vehsAttNames['No']])
                                        nnn11[j]=nnn21
                                
            f2= open("21.txt","a")
            f2.write(str(kkk11))
            f2.write("\n")
            f2.close()

            f2= open("221.txt","a")
            f2.write(str(zzz11))
            f2.write("\n")
            f2.close()



            f2= open("2221.txt","a")
            f2.write(str(mmm11))
            f2.write("\n")
            f2.close()


            f2= open("22221.txt","a")
            f2.write(str(nnn11))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('01.txt', 'r')
        g01=[]
        for line in f.readlines():
            A01= ast.literal_eval(line)
            g01.append(A01)
        f.close()


        f = open('001.txt', 'r')
        g001=[]
        for line in f.readlines():
            A001= ast.literal_eval(line)
            g001.append(A001)
        f.close()

        f = open('0001.txt', 'r')
        g0001=[]
        for line in f.readlines():
            A0001= ast.literal_eval(line)
            g0001.append(A0001)
        f.close()

        f = open('00001.txt', 'r')
        g00001=[]
        for line in f.readlines():
            A00001= ast.literal_eval(line)
            g00001.append(A00001)
        f.close()


        f = open('11.txt', 'r')
        g11=[]
        for line in f.readlines():
            A11= ast.literal_eval(line)
            g11.append(A11)
        f.close()

        f = open('111.txt', 'r')
        g111=[]
        for line in f.readlines():
            A111= ast.literal_eval(line)
            g111.append(A111)
        f.close()


        f = open('1111.txt', 'r')
        g1111=[]
        for line in f.readlines():
            A1111= ast.literal_eval(line)
            g1111.append(A1111)
        f.close()


        f = open('11111.txt', 'r')
        g11111=[]
        for line in f.readlines():
            A11111= ast.literal_eval(line)
            g11111.append(A11111)
        f.close()


        f = open('111111.txt', 'r')
        g111111=[]
        for line in f.readlines():
            A111111= ast.literal_eval(line)
            g111111.append(A111111)
        f.close()

        f = open('21.txt', 'r')
        g21=[]
        for line in f.readlines():
            A21= ast.literal_eval(line)
            g21.append(A21)
        f.close()

        f = open('221.txt', 'r')
        g221=[]
        for line in f.readlines():
            A221= ast.literal_eval(line)
            g221.append(A221)
        f.close()

        f = open('2221.txt', 'r')
        g2221=[]
        for line in f.readlines():
            A2221= ast.literal_eval(line)
            g2221.append(A2221)
        f.close()

        f = open('22221.txt', 'r')
        g22221=[]
        for line in f.readlines():
            A22221= ast.literal_eval(line)
            g22221.append(A22221)
        f.close()


        Current_Number_CarCV_line1=[0]*len(CellsNo_line1)
        Current_Number_BusCV_line1=[0]*len(CellsNo_line1)
        Current_Number_Car_line1=[0]*len(CellsNo_line1)
        Current_Number_Bus_line1=[0]*len(CellsNo_line1)
        
        Arrival_CarCV_line1=[0]*len(CellsNo_line1)
        Arrival_BusCV_line1=[0]*len(CellsNo_line1)
        Arrival_Car_line1=[0]*len(CellsNo_line1)
        Arrival_Bus_line1=[0]*len(CellsNo_line1)

        Departure_CarCV_line1=[0]*len(CellsNo_line1)
        Departure_BusCV_line1=[0]*len(CellsNo_line1)
        Departure_Car_line1=[0]*len(CellsNo_line1)
        Departure_Bus_line1=[0]*len(CellsNo_line1)

        Average_speed_CarCV_line1=[0]*len(CellsNo_line1)
        Average_speed_BusCV_line1=[0]*len(CellsNo_line1)
        Average_speed_Car_line1=[0]*len(CellsNo_line1)
        Average_speed_Bus_line1=[0]*len(CellsNo_line1)



        Turn1_line1=[0]*len(CellsNo_line1)
        Turn2_line1=[0]*len(CellsNo_line1)






        for i in g111111: 
            for j in CellsNo_line1:
                if len(i[j])>0:
 
                    Turn1_line1[j]= 0
                    Turn2_line1[j]= 0

                else:
                    Turn1_line1[j]= 0
                    Turn2_line1[j]= 0


        for i in g11: 
            for j in CellsNo_line1:
                Current_Number_CarCV_line1[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line1[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line1[j]= 0




        for i in g111: 
            for j in CellsNo_line1:
                Current_Number_BusCV_line1[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line1[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line1[j]= 0





        for i in g1111: 
            for j in CellsNo_line1:
                Current_Number_Car_line1[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line1[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line1[j]= 0



        for i in g11111: 
            for j in CellsNo_line1:
                Current_Number_Bus_line1[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line1[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line1[j]= 0






        for i in range(len(g11)):          
            for j in CellsNo_line1:
                m=[]
                if len(g11[i][j])>0:
                    for k in g11[i][j]:
                        if k not in g01[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line1[j] = len(m)
                


        for i in range(len(g111)):          
            for j in CellsNo_line1:
                m=[]
                if len(g111[i][j])>0:
                    for k in g111[i][j]:
                        if k not in g001[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line1[j] = len(m)




        for i in range(len(g1111)):          
            for j in CellsNo_line1:
                m=[]
                if len(g1111[i][j])>0:
                    for k in g1111[i][j]:
                        if k not in g0001[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line1[j] = len(m)







        for i in range(len(g11111)):          
            for j in CellsNo_line1:
                m=[]
                if len(g11111[i][j])>0:
                    for k in g11111[i][j]:
                        if k not in g00001[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line1[j] = len(m)






        for i in range(len(g21)):          
            for j in CellsNo_line1:
                m=[]
                if len(g11[i][j])>0:
                    for k in g11[i][j]:
                        if k not in g21[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line1[j] = len(m)
                



        for i in range(len(g221)):          
            for j in CellsNo_line1:
                m=[]
                if len(g111[i][j])>0:
                    for k in g111[i][j]:
                        if k not in g221[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line1[j] = len(m)




        for i in range(len(g2221)):          
            for j in CellsNo_line1:
                m=[]
                if len(g1111[i][j])>0:
                    for k in g1111[i][j]:
                        if k not in g2221[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line1[j] = len(m)



        for i in range(len(g22221)):          
            for j in CellsNo_line1:
                m=[]
                if len(g11111[i][j])>0:
                    for k in g11111[i][j]:
                        if k not in g22221[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line1[j] = len(m)





        f2= open("Current_Number_CarCV_line1.txt","a")
        f2.write(str(Current_Number_CarCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line1.txt","a")
        f2.write(str(Current_Number_BusCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line1.txt","a")
        f2.write(str(Current_Number_Car_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line1.txt","a")
        f2.write(str(Current_Number_Bus_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line1.txt","a")
        f2.write(str(Average_speed_CarCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line1.txt","a")
        f2.write(str(Average_speed_BusCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line1.txt","a")
        f2.write(str(Average_speed_Car_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line1.txt","a")
        f2.write(str(Average_speed_Bus_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line1.txt","a")
        f2.write(str(Arrival_CarCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line1.txt","a")
        f2.write(str(Arrival_BusCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line1.txt","a")
        f2.write(str(Arrival_Car_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line1.txt","a")
        f2.write(str(Arrival_Bus_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line1.txt","a")
        f2.write(str(Departure_CarCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line1.txt","a")
        f2.write(str(Departure_BusCV_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line1.txt","a")
        f2.write(str(Departure_Car_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line1.txt","a")
        f2.write(str(Departure_Bus_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line1.txt","a")
        f2.write(str(Turn1_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line1.txt","a")
        f2.write(str(Turn2_line1))
        f2.write("\n")
        f2.write(",")
        f2.close()






    LinkLength16= Vissim.Net.Links.ItemByKey(16).AttValue('Length2D')
    CellsNo_line16=[]
    i=0
    k=0
    while i< truncate(LinkLength16,-1):
        CellsNo_line16.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k116=[[]]*len(CellsNo_line16)
            z116=[[]]*len(CellsNo_line16)
            m116=[[]]*len(CellsNo_line16)
            n116=[[]]*len(CellsNo_line16)
            T116=[[]]*len(CellsNo_line16)

            for j in CellsNo_line16:
                k216=[]
                z216=[]
                m216=[]
                n216=[]
                T216=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '16':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k216.append(vehAttributes[vehsAttNames['No']])
                                    k116[j]=k216
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z216.append(vehAttributes[vehsAttNames['No']])
                                    z116[j]=z216
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m216.append(vehAttributes[vehsAttNames['No']])
                                    m116[j]=m216

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n216.append(vehAttributes[vehsAttNames['No']])
                                    n116[j]=n216

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T216.append(vehAttributes[vehsAttNames['No']])
                                T116[j]=T216                        


            f2= open("116.txt","a")
            f2.write(str(k116))
            f2.write("\n")
            f2.close()
            f2= open("1116.txt","a")
            f2.write(str(z116))
            f2.write("\n")
            f2.close()
            f2= open("11116.txt","a")
            f2.write(str(m116))
            f2.write("\n")
            f2.close()
            f2= open("111116.txt","a")
            f2.write(str(n116))
            f2.write("\n")
            f2.close()

            f2= open("1111116.txt","a")
            f2.write(str(T116))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk116=[[]]*len(CellsNo_line16)
                f2= open("016.txt","a")
                f2.write(str(kk116))
                f2.write("\n")
                f2.close()

                zz116=[[]]*len(CellsNo_line16)
                f2= open("0016.txt","a")
                f2.write(str(zz116))
                f2.write("\n")
                f2.close()

                mm116=[[]]*len(CellsNo_line16)
                f2= open("00016.txt","a")
                f2.write(str(mm116))
                f2.write("\n")
                f2.close()

                nn116=[[]]*len(CellsNo_line16)
                f2= open("000016.txt","a")
                f2.write(str(nn116))
                f2.write("\n")
                f2.close()     
            
            else:
                kk116=[[]]*len(CellsNo_line16)
                zz116=[[]]*len(CellsNo_line16)
                mm116=[[]]*len(CellsNo_line16)
                nn116=[[]]*len(CellsNo_line16)
                for j in CellsNo_line16:
                    kk216=[]
                    zz216=[]
                    mm216=[]
                    nn216=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '16':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk216.append(vehAttributes[vehsAttNames['No']])
                                        kk116[j]=kk216
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz216.append(vehAttributes[vehsAttNames['No']])
                                        zz116[j]=zz216


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm216.append(vehAttributes[vehsAttNames['No']])
                                        mm116[j]=mm216


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn216.append(vehAttributes[vehsAttNames['No']])
                                        nn116[j]=nn216
                                        

                                        


                f2= open("016.txt","a")
                f2.write(str(kk116))
                f2.write("\n")
                f2.close()


                f2= open("0016.txt","a")
                f2.write(str(zz116))
                f2.write("\n")
                f2.close()


                f2= open("00016.txt","a")
                f2.write(str(mm116))
                f2.write("\n")
                f2.close()

                f2= open("000016.txt","a")
                f2.write(str(nn116))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk116=[[]]*len(CellsNo_line16)
            zzz116=[[]]*len(CellsNo_line16)
            mmm116=[[]]*len(CellsNo_line16)
            nnn116=[[]]*len(CellsNo_line16)
            for j in CellsNo_line16:
                kkk216=[]
                zzz216=[]
                mmm216=[]
                nnn216=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '16':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk216.append(vehAttributes[vehsAttNames['No']])
                                    kkk116[j]=kkk216

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '16':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz216.append(vehAttributes[vehsAttNames['No']])
                                        zzz116[j]=zzz216


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm216.append(vehAttributes[vehsAttNames['No']])
                                        mmm116[j]=mmm216


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn216.append(vehAttributes[vehsAttNames['No']])
                                        nnn116[j]=nnn216
                                
            f2= open("216.txt","a")
            f2.write(str(kkk116))
            f2.write("\n")
            f2.close()

            f2= open("2216.txt","a")
            f2.write(str(zzz116))
            f2.write("\n")
            f2.close()



            f2= open("22216.txt","a")
            f2.write(str(mmm116))
            f2.write("\n")
            f2.close()


            f2= open("222216.txt","a")
            f2.write(str(nnn116))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('016.txt', 'r')
        g016=[]
        for line in f.readlines():
            A016= ast.literal_eval(line)
            g016.append(A016)
        f.close()


        f = open('0016.txt', 'r')
        g0016=[]
        for line in f.readlines():
            A0016= ast.literal_eval(line)
            g0016.append(A0016)
        f.close()

        f = open('00016.txt', 'r')
        g00016=[]
        for line in f.readlines():
            A00016= ast.literal_eval(line)
            g00016.append(A00016)
        f.close()

        f = open('000016.txt', 'r')
        g000016=[]
        for line in f.readlines():
            A000016= ast.literal_eval(line)
            g000016.append(A000016)
        f.close()


        f = open('116.txt', 'r')
        g116=[]
        for line in f.readlines():
            A116= ast.literal_eval(line)
            g116.append(A116)
        f.close()

        f = open('1116.txt', 'r')
        g1116=[]
        for line in f.readlines():
            A1116= ast.literal_eval(line)
            g1116.append(A1116)
        f.close()


        f = open('11116.txt', 'r')
        g11116=[]
        for line in f.readlines():
            A11116= ast.literal_eval(line)
            g11116.append(A11116)
        f.close()


        f = open('111116.txt', 'r')
        g111116=[]
        for line in f.readlines():
            A111116= ast.literal_eval(line)
            g111116.append(A111116)
        f.close()


        f = open('1111116.txt', 'r')
        g1111116=[]
        for line in f.readlines():
            A1111116= ast.literal_eval(line)
            g1111116.append(A1111116)
        f.close()

        f = open('216.txt', 'r')
        g216=[]
        for line in f.readlines():
            A216= ast.literal_eval(line)
            g216.append(A216)
        f.close()

        f = open('2216.txt', 'r')
        g2216=[]
        for line in f.readlines():
            A2216= ast.literal_eval(line)
            g2216.append(A2216)
        f.close()

        f = open('22216.txt', 'r')
        g22216=[]
        for line in f.readlines():
            A22216= ast.literal_eval(line)
            g22216.append(A22216)
        f.close()

        f = open('222216.txt', 'r')
        g222216=[]
        for line in f.readlines():
            A222216= ast.literal_eval(line)
            g222216.append(A222216)
        f.close()


        Current_Number_CarCV_line16=[0]*len(CellsNo_line16)
        Current_Number_BusCV_line16=[0]*len(CellsNo_line16)
        Current_Number_Car_line16=[0]*len(CellsNo_line16)
        Current_Number_Bus_line16=[0]*len(CellsNo_line16)
        
        Arrival_CarCV_line16=[0]*len(CellsNo_line16)
        Arrival_BusCV_line16=[0]*len(CellsNo_line16)
        Arrival_Car_line16=[0]*len(CellsNo_line16)
        Arrival_Bus_line16=[0]*len(CellsNo_line16)

        Departure_CarCV_line16=[0]*len(CellsNo_line16)
        Departure_BusCV_line16=[0]*len(CellsNo_line16)
        Departure_Car_line16=[0]*len(CellsNo_line16)
        Departure_Bus_line16=[0]*len(CellsNo_line16)

        Average_speed_CarCV_line16=[0]*len(CellsNo_line16)
        Average_speed_BusCV_line16=[0]*len(CellsNo_line16)
        Average_speed_Car_line16=[0]*len(CellsNo_line16)
        Average_speed_Bus_line16=[0]*len(CellsNo_line16)



        Turn1_line16=[0]*len(CellsNo_line16)
        Turn2_line16=[0]*len(CellsNo_line16)






        for i in g1111116: 
            for j in CellsNo_line16:
                if len(i[j])>0:
                    Turn1_line16[j]= 1
                    Turn2_line16[j]= 0
                else:
                    Turn1_line16[j]= 0
                    Turn2_line16[j]= 0


        for i in g116: 
            for j in CellsNo_line16:
                Current_Number_CarCV_line16[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line16[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line16[j]= 0




        for i in g1116: 
            for j in CellsNo_line16:
                Current_Number_BusCV_line16[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line16[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line16[j]= 0





        for i in g11116: 
            for j in CellsNo_line16:
                Current_Number_Car_line16[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line16[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line16[j]= 0



        for i in g111116: 
            for j in CellsNo_line16:
                Current_Number_Bus_line16[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line16[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line16[j]= 0






        for i in range(len(g116)):          
            for j in CellsNo_line16:
                m=[]
                if len(g116[i][j])>0:
                    for k in g116[i][j]:
                        if k not in g016[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line16[j] = len(m)
                


        for i in range(len(g1116)):          
            for j in CellsNo_line16:
                m=[]
                if len(g1116[i][j])>0:
                    for k in g1116[i][j]:
                        if k not in g0016[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line16[j] = len(m)




        for i in range(len(g11116)):          
            for j in CellsNo_line16:
                m=[]
                if len(g11116[i][j])>0:
                    for k in g11116[i][j]:
                        if k not in g00016[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line16[j] = len(m)







        for i in range(len(g111116)):          
            for j in CellsNo_line16:
                m=[]
                if len(g111116[i][j])>0:
                    for k in g111116[i][j]:
                        if k not in g000016[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line16[j] = len(m)






        for i in range(len(g216)):          
            for j in CellsNo_line16:
                m=[]
                if len(g116[i][j])>0:
                    for k in g116[i][j]:
                        if k not in g216[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line16[j] = len(m)
                



        for i in range(len(g2216)):          
            for j in CellsNo_line16:
                m=[]
                if len(g1116[i][j])>0:
                    for k in g1116[i][j]:
                        if k not in g2216[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line16[j] = len(m)




        for i in range(len(g22216)):          
            for j in CellsNo_line16:
                m=[]
                if len(g11116[i][j])>0:
                    for k in g11116[i][j]:
                        if k not in g22216[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line16[j] = len(m)



        for i in range(len(g222216)):          
            for j in CellsNo_line16:
                m=[]
                if len(g111116[i][j])>0:
                    for k in g111116[i][j]:
                        if k not in g222216[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line16[j] = len(m)





        f2= open("Current_Number_CarCV_line16.txt","a")
        f2.write(str(Current_Number_CarCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line16.txt","a")
        f2.write(str(Current_Number_BusCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line16.txt","a")
        f2.write(str(Current_Number_Car_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line16.txt","a")
        f2.write(str(Current_Number_Bus_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line16.txt","a")
        f2.write(str(Average_speed_CarCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line16.txt","a")
        f2.write(str(Average_speed_BusCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line16.txt","a")
        f2.write(str(Average_speed_Car_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line16.txt","a")
        f2.write(str(Average_speed_Bus_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line16.txt","a")
        f2.write(str(Arrival_CarCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line16.txt","a")
        f2.write(str(Arrival_BusCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line16.txt","a")
        f2.write(str(Arrival_Car_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line16.txt","a")
        f2.write(str(Arrival_Bus_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line16.txt","a")
        f2.write(str(Departure_CarCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line16.txt","a")
        f2.write(str(Departure_BusCV_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line16.txt","a")
        f2.write(str(Departure_Car_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line16.txt","a")
        f2.write(str(Departure_Bus_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line16.txt","a")
        f2.write(str(Turn1_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line16.txt","a")
        f2.write(str(Turn2_line16))
        f2.write("\n")
        f2.write(",")
        f2.close()







    LinkLength15= Vissim.Net.Links.ItemByKey(15).AttValue('Length2D')
    CellsNo_line15=[]
    i=0
    k=0
    while i< truncate(LinkLength15,-1):
        CellsNo_line15.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k115=[[]]*len(CellsNo_line15)
            z115=[[]]*len(CellsNo_line15)
            m115=[[]]*len(CellsNo_line15)
            n115=[[]]*len(CellsNo_line15)
            T115=[[]]*len(CellsNo_line15)

            for j in CellsNo_line15:
                k215=[]
                z215=[]
                m215=[]
                n215=[]
                T215=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '15':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k215.append(vehAttributes[vehsAttNames['No']])
                                    k115[j]=k215
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z215.append(vehAttributes[vehsAttNames['No']])
                                    z115[j]=z215
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m215.append(vehAttributes[vehsAttNames['No']])
                                    m115[j]=m215

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n215.append(vehAttributes[vehsAttNames['No']])
                                    n115[j]=n215

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T215.append(vehAttributes[vehsAttNames['No']])
                                T115[j]=T215                        


            f2= open("115.txt","a")
            f2.write(str(k115))
            f2.write("\n")
            f2.close()
            f2= open("1115.txt","a")
            f2.write(str(z115))
            f2.write("\n")
            f2.close()
            f2= open("11115.txt","a")
            f2.write(str(m115))
            f2.write("\n")
            f2.close()
            f2= open("111115.txt","a")
            f2.write(str(n115))
            f2.write("\n")
            f2.close()

            f2= open("1111115.txt","a")
            f2.write(str(T115))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk115=[[]]*len(CellsNo_line15)
                f2= open("015.txt","a")
                f2.write(str(kk115))
                f2.write("\n")
                f2.close()

                zz115=[[]]*len(CellsNo_line15)
                f2= open("0015.txt","a")
                f2.write(str(zz115))
                f2.write("\n")
                f2.close()

                mm115=[[]]*len(CellsNo_line15)
                f2= open("00015.txt","a")
                f2.write(str(mm115))
                f2.write("\n")
                f2.close()

                nn115=[[]]*len(CellsNo_line15)
                f2= open("000015.txt","a")
                f2.write(str(nn115))
                f2.write("\n")
                f2.close()     
            
            else:
                kk115=[[]]*len(CellsNo_line15)
                zz115=[[]]*len(CellsNo_line15)
                mm115=[[]]*len(CellsNo_line15)
                nn115=[[]]*len(CellsNo_line15)
                for j in CellsNo_line15:
                    kk215=[]
                    zz215=[]
                    mm215=[]
                    nn215=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '15':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk215.append(vehAttributes[vehsAttNames['No']])
                                        kk115[j]=kk215
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz215.append(vehAttributes[vehsAttNames['No']])
                                        zz115[j]=zz215


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm215.append(vehAttributes[vehsAttNames['No']])
                                        mm115[j]=mm215


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn215.append(vehAttributes[vehsAttNames['No']])
                                        nn115[j]=nn215
                                        

                                        


                f2= open("015.txt","a")
                f2.write(str(kk115))
                f2.write("\n")
                f2.close()


                f2= open("0015.txt","a")
                f2.write(str(zz115))
                f2.write("\n")
                f2.close()


                f2= open("00015.txt","a")
                f2.write(str(mm115))
                f2.write("\n")
                f2.close()

                f2= open("000015.txt","a")
                f2.write(str(nn115))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk115=[[]]*len(CellsNo_line15)
            zzz115=[[]]*len(CellsNo_line15)
            mmm115=[[]]*len(CellsNo_line15)
            nnn115=[[]]*len(CellsNo_line15)
            for j in CellsNo_line15:
                kkk215=[]
                zzz215=[]
                mmm215=[]
                nnn215=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '15':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk215.append(vehAttributes[vehsAttNames['No']])
                                    kkk115[j]=kkk215

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '15':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz215.append(vehAttributes[vehsAttNames['No']])
                                        zzz115[j]=zzz215


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm215.append(vehAttributes[vehsAttNames['No']])
                                        mmm115[j]=mmm215


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn215.append(vehAttributes[vehsAttNames['No']])
                                        nnn115[j]=nnn215
                                
            f2= open("215.txt","a")
            f2.write(str(kkk115))
            f2.write("\n")
            f2.close()

            f2= open("2215.txt","a")
            f2.write(str(zzz115))
            f2.write("\n")
            f2.close()



            f2= open("22215.txt","a")
            f2.write(str(mmm115))
            f2.write("\n")
            f2.close()


            f2= open("222215.txt","a")
            f2.write(str(nnn115))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('015.txt', 'r')
        g015=[]
        for line in f.readlines():
            A015= ast.literal_eval(line)
            g015.append(A015)
        f.close()


        f = open('0015.txt', 'r')
        g0015=[]
        for line in f.readlines():
            A0015= ast.literal_eval(line)
            g0015.append(A0015)
        f.close()

        f = open('00015.txt', 'r')
        g00015=[]
        for line in f.readlines():
            A00015= ast.literal_eval(line)
            g00015.append(A00015)
        f.close()

        f = open('000015.txt', 'r')
        g000015=[]
        for line in f.readlines():
            A000015= ast.literal_eval(line)
            g000015.append(A000015)
        f.close()


        f = open('115.txt', 'r')
        g115=[]
        for line in f.readlines():
            A115= ast.literal_eval(line)
            g115.append(A115)
        f.close()

        f = open('1115.txt', 'r')
        g1115=[]
        for line in f.readlines():
            A1115= ast.literal_eval(line)
            g1115.append(A1115)
        f.close()


        f = open('11115.txt', 'r')
        g11115=[]
        for line in f.readlines():
            A11115= ast.literal_eval(line)
            g11115.append(A11115)
        f.close()


        f = open('111115.txt', 'r')
        g111115=[]
        for line in f.readlines():
            A111115= ast.literal_eval(line)
            g111115.append(A111115)
        f.close()


        f = open('1111115.txt', 'r')
        g1111115=[]
        for line in f.readlines():
            A1111115= ast.literal_eval(line)
            g1111115.append(A1111115)
        f.close()

        f = open('215.txt', 'r')
        g215=[]
        for line in f.readlines():
            A215= ast.literal_eval(line)
            g215.append(A215)
        f.close()

        f = open('2215.txt', 'r')
        g2215=[]
        for line in f.readlines():
            A2215= ast.literal_eval(line)
            g2215.append(A2215)
        f.close()

        f = open('22215.txt', 'r')
        g22215=[]
        for line in f.readlines():
            A22215= ast.literal_eval(line)
            g22215.append(A22215)
        f.close()

        f = open('222215.txt', 'r')
        g222215=[]
        for line in f.readlines():
            A222215= ast.literal_eval(line)
            g222215.append(A222215)
        f.close()


        Current_Number_CarCV_line15=[0]*len(CellsNo_line15)
        Current_Number_BusCV_line15=[0]*len(CellsNo_line15)
        Current_Number_Car_line15=[0]*len(CellsNo_line15)
        Current_Number_Bus_line15=[0]*len(CellsNo_line15)
        
        Arrival_CarCV_line15=[0]*len(CellsNo_line15)
        Arrival_BusCV_line15=[0]*len(CellsNo_line15)
        Arrival_Car_line15=[0]*len(CellsNo_line15)
        Arrival_Bus_line15=[0]*len(CellsNo_line15)

        Departure_CarCV_line15=[0]*len(CellsNo_line15)
        Departure_BusCV_line15=[0]*len(CellsNo_line15)
        Departure_Car_line15=[0]*len(CellsNo_line15)
        Departure_Bus_line15=[0]*len(CellsNo_line15)

        Average_speed_CarCV_line15=[0]*len(CellsNo_line15)
        Average_speed_BusCV_line15=[0]*len(CellsNo_line15)
        Average_speed_Car_line15=[0]*len(CellsNo_line15)
        Average_speed_Bus_line15=[0]*len(CellsNo_line15)



        Turn1_line15=[0]*len(CellsNo_line15)
        Turn2_line15=[0]*len(CellsNo_line15)






        for i in g1111115: 
            for j in CellsNo_line15:
                if len(i[j])>0:
                    Turn1_line15[j]= 1
                    Turn2_line15[j]= 0

                else:
                    Turn1_line15[j]= 0
                    Turn2_line15[j]= 0


        for i in g115: 
            for j in CellsNo_line15:
                Current_Number_CarCV_line15[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line15[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line15[j]= 0




        for i in g1115: 
            for j in CellsNo_line15:
                Current_Number_BusCV_line15[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line15[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line15[j]= 0





        for i in g11115: 
            for j in CellsNo_line15:
                Current_Number_Car_line15[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line15[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line15[j]= 0



        for i in g111115: 
            for j in CellsNo_line15:
                Current_Number_Bus_line15[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line15[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line15[j]= 0






        for i in range(len(g115)):          
            for j in CellsNo_line15:
                m=[]
                if len(g115[i][j])>0:
                    for k in g115[i][j]:
                        if k not in g015[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line15[j] = len(m)
                


        for i in range(len(g1115)):          
            for j in CellsNo_line15:
                m=[]
                if len(g1115[i][j])>0:
                    for k in g1115[i][j]:
                        if k not in g0015[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line15[j] = len(m)




        for i in range(len(g11115)):          
            for j in CellsNo_line15:
                m=[]
                if len(g11115[i][j])>0:
                    for k in g11115[i][j]:
                        if k not in g00015[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line15[j] = len(m)







        for i in range(len(g111115)):          
            for j in CellsNo_line15:
                m=[]
                if len(g111115[i][j])>0:
                    for k in g111115[i][j]:
                        if k not in g000015[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line15[j] = len(m)






        for i in range(len(g215)):          
            for j in CellsNo_line15:
                m=[]
                if len(g115[i][j])>0:
                    for k in g115[i][j]:
                        if k not in g215[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line15[j] = len(m)
                



        for i in range(len(g2215)):          
            for j in CellsNo_line15:
                m=[]
                if len(g1115[i][j])>0:
                    for k in g1115[i][j]:
                        if k not in g2215[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line15[j] = len(m)




        for i in range(len(g22215)):          
            for j in CellsNo_line15:
                m=[]
                if len(g11115[i][j])>0:
                    for k in g11115[i][j]:
                        if k not in g22215[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line15[j] = len(m)



        for i in range(len(g222215)):          
            for j in CellsNo_line15:
                m=[]
                if len(g111115[i][j])>0:
                    for k in g111115[i][j]:
                        if k not in g222215[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line15[j] = len(m)





        f2= open("Current_Number_CarCV_line15.txt","a")
        f2.write(str(Current_Number_CarCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line15.txt","a")
        f2.write(str(Current_Number_BusCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line15.txt","a")
        f2.write(str(Current_Number_Car_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line15.txt","a")
        f2.write(str(Current_Number_Bus_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line15.txt","a")
        f2.write(str(Average_speed_CarCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line15.txt","a")
        f2.write(str(Average_speed_BusCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line15.txt","a")
        f2.write(str(Average_speed_Car_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line15.txt","a")
        f2.write(str(Average_speed_Bus_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line15.txt","a")
        f2.write(str(Arrival_CarCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line15.txt","a")
        f2.write(str(Arrival_BusCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line15.txt","a")
        f2.write(str(Arrival_Car_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line15.txt","a")
        f2.write(str(Arrival_Bus_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line15.txt","a")
        f2.write(str(Departure_CarCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line15.txt","a")
        f2.write(str(Departure_BusCV_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line15.txt","a")
        f2.write(str(Departure_Car_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line15.txt","a")
        f2.write(str(Departure_Bus_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line15.txt","a")
        f2.write(str(Turn1_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line15.txt","a")
        f2.write(str(Turn2_line15))
        f2.write("\n")
        f2.write(",")
        f2.close()







    LinkLength7= Vissim.Net.Links.ItemByKey(7).AttValue('Length2D')
    CellsNo_line7=[]
    i=0
    k=0
    while i< truncate(LinkLength7,-1):
        CellsNo_line7.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k17=[[]]*len(CellsNo_line7)
            z17=[[]]*len(CellsNo_line7)
            m17=[[]]*len(CellsNo_line7)
            n17=[[]]*len(CellsNo_line7)
            T17=[[]]*len(CellsNo_line7)

            for j in CellsNo_line7:
                k27=[]
                z27=[]
                m27=[]
                n27=[]
                T27=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '7':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k27.append(vehAttributes[vehsAttNames['No']])
                                    k17[j]=k27
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z27.append(vehAttributes[vehsAttNames['No']])
                                    z17[j]=z27
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m27.append(vehAttributes[vehsAttNames['No']])
                                    m17[j]=m27

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n27.append(vehAttributes[vehsAttNames['No']])
                                    n17[j]=n27

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T27.append(vehAttributes[vehsAttNames['No']])
                                T17[j]=T27                        


            f2= open("17.txt","a")
            f2.write(str(k17))
            f2.write("\n")
            f2.close()
            f2= open("117.txt","a")
            f2.write(str(z17))
            f2.write("\n")
            f2.close()
            f2= open("1117.txt","a")
            f2.write(str(m17))
            f2.write("\n")
            f2.close()
            f2= open("11117.txt","a")
            f2.write(str(n17))
            f2.write("\n")
            f2.close()

            f2= open("111117.txt","a")
            f2.write(str(T17))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk17=[[]]*len(CellsNo_line7)
                f2= open("07.txt","a")
                f2.write(str(kk17))
                f2.write("\n")
                f2.close()

                zz17=[[]]*len(CellsNo_line7)
                f2= open("007.txt","a")
                f2.write(str(zz17))
                f2.write("\n")
                f2.close()

                mm17=[[]]*len(CellsNo_line7)
                f2= open("0007.txt","a")
                f2.write(str(mm17))
                f2.write("\n")
                f2.close()

                nn17=[[]]*len(CellsNo_line7)
                f2= open("00007.txt","a")
                f2.write(str(nn17))
                f2.write("\n")
                f2.close()     
            
            else:
                kk17=[[]]*len(CellsNo_line7)
                zz17=[[]]*len(CellsNo_line7)
                mm17=[[]]*len(CellsNo_line7)
                nn17=[[]]*len(CellsNo_line7)
                for j in CellsNo_line7:
                    kk27=[]
                    zz27=[]
                    mm27=[]
                    nn27=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '7':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk27.append(vehAttributes[vehsAttNames['No']])
                                        kk17[j]=kk27
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz27.append(vehAttributes[vehsAttNames['No']])
                                        zz17[j]=zz27


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm27.append(vehAttributes[vehsAttNames['No']])
                                        mm17[j]=mm27


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn27.append(vehAttributes[vehsAttNames['No']])
                                        nn17[j]=nn27
                                        

                                        


                f2= open("07.txt","a")
                f2.write(str(kk17))
                f2.write("\n")
                f2.close()


                f2= open("007.txt","a")
                f2.write(str(zz17))
                f2.write("\n")
                f2.close()


                f2= open("0007.txt","a")
                f2.write(str(mm17))
                f2.write("\n")
                f2.close()

                f2= open("00007.txt","a")
                f2.write(str(nn17))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk17=[[]]*len(CellsNo_line7)
            zzz17=[[]]*len(CellsNo_line7)
            mmm17=[[]]*len(CellsNo_line7)
            nnn17=[[]]*len(CellsNo_line7)
            for j in CellsNo_line7:
                kkk27=[]
                zzz27=[]
                mmm27=[]
                nnn27=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '7':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk27.append(vehAttributes[vehsAttNames['No']])
                                    kkk17[j]=kkk27

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '7':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz27.append(vehAttributes[vehsAttNames['No']])
                                        zzz17[j]=zzz27


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm27.append(vehAttributes[vehsAttNames['No']])
                                        mmm17[j]=mmm27


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn27.append(vehAttributes[vehsAttNames['No']])
                                        nnn17[j]=nnn27
                                
            f2= open("27.txt","a")
            f2.write(str(kkk17))
            f2.write("\n")
            f2.close()

            f2= open("227.txt","a")
            f2.write(str(zzz17))
            f2.write("\n")
            f2.close()



            f2= open("2227.txt","a")
            f2.write(str(mmm17))
            f2.write("\n")
            f2.close()


            f2= open("22227.txt","a")
            f2.write(str(nnn17))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('07.txt', 'r')
        g07=[]
        for line in f.readlines():
            A07= ast.literal_eval(line)
            g07.append(A07)
        f.close()


        f = open('007.txt', 'r')
        g007=[]
        for line in f.readlines():
            A007= ast.literal_eval(line)
            g007.append(A007)
        f.close()

        f = open('0007.txt', 'r')
        g0007=[]
        for line in f.readlines():
            A0007= ast.literal_eval(line)
            g0007.append(A0007)
        f.close()

        f = open('00007.txt', 'r')
        g00007=[]
        for line in f.readlines():
            A00007= ast.literal_eval(line)
            g00007.append(A00007)
        f.close()


        f = open('17.txt', 'r')
        g17=[]
        for line in f.readlines():
            A17= ast.literal_eval(line)
            g17.append(A17)
        f.close()

        f = open('117.txt', 'r')
        g117=[]
        for line in f.readlines():
            A117= ast.literal_eval(line)
            g117.append(A117)
        f.close()


        f = open('1117.txt', 'r')
        g1117=[]
        for line in f.readlines():
            A1117= ast.literal_eval(line)
            g1117.append(A1117)
        f.close()


        f = open('11117.txt', 'r')
        g11117=[]
        for line in f.readlines():
            A11117= ast.literal_eval(line)
            g11117.append(A11117)
        f.close()


        f = open('111117.txt', 'r')
        g111117=[]
        for line in f.readlines():
            A111117= ast.literal_eval(line)
            g111117.append(A111117)
        f.close()

        f = open('27.txt', 'r')
        g27=[]
        for line in f.readlines():
            A27= ast.literal_eval(line)
            g27.append(A27)
        f.close()

        f = open('227.txt', 'r')
        g227=[]
        for line in f.readlines():
            A227= ast.literal_eval(line)
            g227.append(A227)
        f.close()

        f = open('2227.txt', 'r')
        g2227=[]
        for line in f.readlines():
            A2227= ast.literal_eval(line)
            g2227.append(A2227)
        f.close()

        f = open('22227.txt', 'r')
        g22227=[]
        for line in f.readlines():
            A22227= ast.literal_eval(line)
            g22227.append(A22227)
        f.close()


        Current_Number_CarCV_line7=[0]*len(CellsNo_line7)
        Current_Number_BusCV_line7=[0]*len(CellsNo_line7)
        Current_Number_Car_line7=[0]*len(CellsNo_line7)
        Current_Number_Bus_line7=[0]*len(CellsNo_line7)
        
        Arrival_CarCV_line7=[0]*len(CellsNo_line7)
        Arrival_BusCV_line7=[0]*len(CellsNo_line7)
        Arrival_Car_line7=[0]*len(CellsNo_line7)
        Arrival_Bus_line7=[0]*len(CellsNo_line7)

        Departure_CarCV_line7=[0]*len(CellsNo_line7)
        Departure_BusCV_line7=[0]*len(CellsNo_line7)
        Departure_Car_line7=[0]*len(CellsNo_line7)
        Departure_Bus_line7=[0]*len(CellsNo_line7)

        Average_speed_CarCV_line7=[0]*len(CellsNo_line7)
        Average_speed_BusCV_line7=[0]*len(CellsNo_line7)
        Average_speed_Car_line7=[0]*len(CellsNo_line7)
        Average_speed_Bus_line7=[0]*len(CellsNo_line7)



        Turn1_line7=[0]*len(CellsNo_line7)
        Turn2_line7=[0]*len(CellsNo_line7)






        for i in g111117: 
            for j in CellsNo_line7:
                if len(i[j])>0:
                    Turn1_line7[j]= 1
                    Turn2_line7[j]= 0

                else:
                    Turn1_line7[j]= 0
                    Turn2_line7[j]= 0


        for i in g17: 
            for j in CellsNo_line7:
                Current_Number_CarCV_line7[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line7[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line7[j]= 0




        for i in g117: 
            for j in CellsNo_line7:
                Current_Number_BusCV_line7[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line7[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line7[j]= 0





        for i in g1117: 
            for j in CellsNo_line7:
                Current_Number_Car_line7[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line7[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line7[j]= 0



        for i in g11117: 
            for j in CellsNo_line7:
                Current_Number_Bus_line7[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line7[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line7[j]= 0






        for i in range(len(g17)):          
            for j in CellsNo_line7:
                m=[]
                if len(g17[i][j])>0:
                    for k in g17[i][j]:
                        if k not in g07[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line7[j] = len(m)
                


        for i in range(len(g117)):          
            for j in CellsNo_line7:
                m=[]
                if len(g117[i][j])>0:
                    for k in g117[i][j]:
                        if k not in g007[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line7[j] = len(m)




        for i in range(len(g1117)):          
            for j in CellsNo_line7:
                m=[]
                if len(g1117[i][j])>0:
                    for k in g1117[i][j]:
                        if k not in g0007[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line7[j] = len(m)







        for i in range(len(g11117)):          
            for j in CellsNo_line7:
                m=[]
                if len(g11117[i][j])>0:
                    for k in g11117[i][j]:
                        if k not in g00007[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line7[j] = len(m)






        for i in range(len(g27)):          
            for j in CellsNo_line7:
                m=[]
                if len(g17[i][j])>0:
                    for k in g17[i][j]:
                        if k not in g27[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line7[j] = len(m)
                



        for i in range(len(g227)):          
            for j in CellsNo_line7:
                m=[]
                if len(g117[i][j])>0:
                    for k in g117[i][j]:
                        if k not in g227[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line7[j] = len(m)




        for i in range(len(g2227)):          
            for j in CellsNo_line7:
                m=[]
                if len(g1117[i][j])>0:
                    for k in g1117[i][j]:
                        if k not in g2227[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line7[j] = len(m)



        for i in range(len(g22227)):          
            for j in CellsNo_line7:
                m=[]
                if len(g11117[i][j])>0:
                    for k in g11117[i][j]:
                        if k not in g22227[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line7[j] = len(m)





        f2= open("Current_Number_CarCV_line7.txt","a")
        f2.write(str(Current_Number_CarCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line7.txt","a")
        f2.write(str(Current_Number_BusCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line7.txt","a")
        f2.write(str(Current_Number_Car_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line7.txt","a")
        f2.write(str(Current_Number_Bus_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line7.txt","a")
        f2.write(str(Average_speed_CarCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line7.txt","a")
        f2.write(str(Average_speed_BusCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line7.txt","a")
        f2.write(str(Average_speed_Car_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line7.txt","a")
        f2.write(str(Average_speed_Bus_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line7.txt","a")
        f2.write(str(Arrival_CarCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line7.txt","a")
        f2.write(str(Arrival_BusCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line7.txt","a")
        f2.write(str(Arrival_Car_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line7.txt","a")
        f2.write(str(Arrival_Bus_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line7.txt","a")
        f2.write(str(Departure_CarCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line7.txt","a")
        f2.write(str(Departure_BusCV_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line7.txt","a")
        f2.write(str(Departure_Car_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line7.txt","a")
        f2.write(str(Departure_Bus_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line7.txt","a")
        f2.write(str(Turn1_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line7.txt","a")
        f2.write(str(Turn2_line7))
        f2.write("\n")
        f2.write(",")
        f2.close()







    LinkLength14= Vissim.Net.Links.ItemByKey(14).AttValue('Length2D')
    CellsNo_line14=[]
    i=0
    k=0
    while i< truncate(LinkLength14,-1):
        CellsNo_line14.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k114=[[]]*len(CellsNo_line14)
            z114=[[]]*len(CellsNo_line14)
            m114=[[]]*len(CellsNo_line14)
            n114=[[]]*len(CellsNo_line14)
            T114=[[]]*len(CellsNo_line14)

            for j in CellsNo_line14:
                k214=[]
                z214=[]
                m214=[]
                n214=[]
                T214=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '14':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k214.append(vehAttributes[vehsAttNames['No']])
                                    k114[j]=k214
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z214.append(vehAttributes[vehsAttNames['No']])
                                    z114[j]=z214
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m214.append(vehAttributes[vehsAttNames['No']])
                                    m114[j]=m214

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n214.append(vehAttributes[vehsAttNames['No']])
                                    n114[j]=n214

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T214.append(vehAttributes[vehsAttNames['No']])
                                T114[j]=T214                        


            f2= open("114.txt","a")
            f2.write(str(k114))
            f2.write("\n")
            f2.close()
            f2= open("1114.txt","a")
            f2.write(str(z114))
            f2.write("\n")
            f2.close()
            f2= open("11114.txt","a")
            f2.write(str(m114))
            f2.write("\n")
            f2.close()
            f2= open("111114.txt","a")
            f2.write(str(n114))
            f2.write("\n")
            f2.close()

            f2= open("1111114.txt","a")
            f2.write(str(T114))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk114=[[]]*len(CellsNo_line14)
                f2= open("014.txt","a")
                f2.write(str(kk114))
                f2.write("\n")
                f2.close()

                zz114=[[]]*len(CellsNo_line14)
                f2= open("0014.txt","a")
                f2.write(str(zz114))
                f2.write("\n")
                f2.close()

                mm114=[[]]*len(CellsNo_line14)
                f2= open("00014.txt","a")
                f2.write(str(mm114))
                f2.write("\n")
                f2.close()

                nn114=[[]]*len(CellsNo_line14)
                f2= open("000014.txt","a")
                f2.write(str(nn114))
                f2.write("\n")
                f2.close()     
            
            else:
                kk114=[[]]*len(CellsNo_line14)
                zz114=[[]]*len(CellsNo_line14)
                mm114=[[]]*len(CellsNo_line14)
                nn114=[[]]*len(CellsNo_line14)
                for j in CellsNo_line14:
                    kk214=[]
                    zz214=[]
                    mm214=[]
                    nn214=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '14':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk214.append(vehAttributes[vehsAttNames['No']])
                                        kk114[j]=kk214
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz214.append(vehAttributes[vehsAttNames['No']])
                                        zz114[j]=zz214


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm214.append(vehAttributes[vehsAttNames['No']])
                                        mm114[j]=mm214


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn214.append(vehAttributes[vehsAttNames['No']])
                                        nn114[j]=nn214
                                        

                                        


                f2= open("014.txt","a")
                f2.write(str(kk114))
                f2.write("\n")
                f2.close()


                f2= open("0014.txt","a")
                f2.write(str(zz114))
                f2.write("\n")
                f2.close()


                f2= open("00014.txt","a")
                f2.write(str(mm114))
                f2.write("\n")
                f2.close()

                f2= open("000014.txt","a")
                f2.write(str(nn114))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk114=[[]]*len(CellsNo_line14)
            zzz114=[[]]*len(CellsNo_line14)
            mmm114=[[]]*len(CellsNo_line14)
            nnn114=[[]]*len(CellsNo_line14)
            for j in CellsNo_line14:
                kkk214=[]
                zzz214=[]
                mmm214=[]
                nnn214=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '14':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk214.append(vehAttributes[vehsAttNames['No']])
                                    kkk114[j]=kkk214

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '14':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz214.append(vehAttributes[vehsAttNames['No']])
                                        zzz114[j]=zzz214


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm214.append(vehAttributes[vehsAttNames['No']])
                                        mmm114[j]=mmm214


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn214.append(vehAttributes[vehsAttNames['No']])
                                        nnn114[j]=nnn214
                                
            f2= open("214.txt","a")
            f2.write(str(kkk114))
            f2.write("\n")
            f2.close()

            f2= open("2214.txt","a")
            f2.write(str(zzz114))
            f2.write("\n")
            f2.close()



            f2= open("22214.txt","a")
            f2.write(str(mmm114))
            f2.write("\n")
            f2.close()


            f2= open("222214.txt","a")
            f2.write(str(nnn114))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('014.txt', 'r')
        g014=[]
        for line in f.readlines():
            A014= ast.literal_eval(line)
            g014.append(A014)
        f.close()


        f = open('0014.txt', 'r')
        g0014=[]
        for line in f.readlines():
            A0014= ast.literal_eval(line)
            g0014.append(A0014)
        f.close()

        f = open('00014.txt', 'r')
        g00014=[]
        for line in f.readlines():
            A00014= ast.literal_eval(line)
            g00014.append(A00014)
        f.close()

        f = open('000014.txt', 'r')
        g000014=[]
        for line in f.readlines():
            A000014= ast.literal_eval(line)
            g000014.append(A000014)
        f.close()


        f = open('114.txt', 'r')
        g114=[]
        for line in f.readlines():
            A114= ast.literal_eval(line)
            g114.append(A114)
        f.close()

        f = open('1114.txt', 'r')
        g1114=[]
        for line in f.readlines():
            A1114= ast.literal_eval(line)
            g1114.append(A1114)
        f.close()


        f = open('11114.txt', 'r')
        g11114=[]
        for line in f.readlines():
            A11114= ast.literal_eval(line)
            g11114.append(A11114)
        f.close()


        f = open('111114.txt', 'r')
        g111114=[]
        for line in f.readlines():
            A111114= ast.literal_eval(line)
            g111114.append(A111114)
        f.close()


        f = open('1111114.txt', 'r')
        g1111114=[]
        for line in f.readlines():
            A1111114= ast.literal_eval(line)
            g1111114.append(A1111114)
        f.close()

        f = open('214.txt', 'r')
        g214=[]
        for line in f.readlines():
            A214= ast.literal_eval(line)
            g214.append(A214)
        f.close()

        f = open('2214.txt', 'r')
        g2214=[]
        for line in f.readlines():
            A2214= ast.literal_eval(line)
            g2214.append(A2214)
        f.close()

        f = open('22214.txt', 'r')
        g22214=[]
        for line in f.readlines():
            A22214= ast.literal_eval(line)
            g22214.append(A22214)
        f.close()

        f = open('222214.txt', 'r')
        g222214=[]
        for line in f.readlines():
            A222214= ast.literal_eval(line)
            g222214.append(A222214)
        f.close()


        Current_Number_CarCV_line14=[0]*len(CellsNo_line14)
        Current_Number_BusCV_line14=[0]*len(CellsNo_line14)
        Current_Number_Car_line14=[0]*len(CellsNo_line14)
        Current_Number_Bus_line14=[0]*len(CellsNo_line14)
        
        Arrival_CarCV_line14=[0]*len(CellsNo_line14)
        Arrival_BusCV_line14=[0]*len(CellsNo_line14)
        Arrival_Car_line14=[0]*len(CellsNo_line14)
        Arrival_Bus_line14=[0]*len(CellsNo_line14)

        Departure_CarCV_line14=[0]*len(CellsNo_line14)
        Departure_BusCV_line14=[0]*len(CellsNo_line14)
        Departure_Car_line14=[0]*len(CellsNo_line14)
        Departure_Bus_line14=[0]*len(CellsNo_line14)

        Average_speed_CarCV_line14=[0]*len(CellsNo_line14)
        Average_speed_BusCV_line14=[0]*len(CellsNo_line14)
        Average_speed_Car_line14=[0]*len(CellsNo_line14)
        Average_speed_Bus_line14=[0]*len(CellsNo_line14)



        Turn1_line14=[0]*len(CellsNo_line14)
        Turn2_line14=[0]*len(CellsNo_line14)






        for i in g1111114: 
            for j in CellsNo_line14:
                if len(i[j])>0:
                    k1=0
                    k2=0
                    for k in i[j]:
                        try:
                            if Vissim.Net.Vehicles.ItemByKey(k).AttValue('NextLink') == '10011':
                                k1=k1+1
                            if Vissim.Net.Vehicles.ItemByKey(k).AttValue('NextLink') == '10009':
                                k2=k2+1     
                            Turn1_line14[j]= k1/(k1+k2)
                            Turn2_line14[j]= k2/(k1+k2)

                        except:
                            Turn1_line14[j]= 0
                            Turn2_line14[j]= 0


                else:
                    Turn1_line14[j]= 0
                    Turn2_line14[j]= 0


        for i in g114: 
            for j in CellsNo_line14:
                Current_Number_CarCV_line14[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line14[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line14[j]= 0




        for i in g1114: 
            for j in CellsNo_line14:
                Current_Number_BusCV_line14[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line14[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line14[j]= 0





        for i in g11114: 
            for j in CellsNo_line14:
                Current_Number_Car_line14[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line14[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line14[j]= 0



        for i in g111114: 
            for j in CellsNo_line14:
                Current_Number_Bus_line14[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line14[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line14[j]= 0






        for i in range(len(g114)):          
            for j in CellsNo_line14:
                m=[]
                if len(g114[i][j])>0:
                    for k in g114[i][j]:
                        if k not in g014[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line14[j] = len(m)
                


        for i in range(len(g1114)):          
            for j in CellsNo_line14:
                m=[]
                if len(g1114[i][j])>0:
                    for k in g1114[i][j]:
                        if k not in g0014[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line14[j] = len(m)




        for i in range(len(g11114)):          
            for j in CellsNo_line14:
                m=[]
                if len(g11114[i][j])>0:
                    for k in g11114[i][j]:
                        if k not in g00014[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line14[j] = len(m)







        for i in range(len(g111114)):          
            for j in CellsNo_line14:
                m=[]
                if len(g111114[i][j])>0:
                    for k in g111114[i][j]:
                        if k not in g000014[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line14[j] = len(m)






        for i in range(len(g214)):          
            for j in CellsNo_line14:
                m=[]
                if len(g114[i][j])>0:
                    for k in g114[i][j]:
                        if k not in g214[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line14[j] = len(m)
                



        for i in range(len(g2214)):          
            for j in CellsNo_line14:
                m=[]
                if len(g1114[i][j])>0:
                    for k in g1114[i][j]:
                        if k not in g2214[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line14[j] = len(m)




        for i in range(len(g22214)):          
            for j in CellsNo_line14:
                m=[]
                if len(g11114[i][j])>0:
                    for k in g11114[i][j]:
                        if k not in g22214[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line14[j] = len(m)



        for i in range(len(g222214)):          
            for j in CellsNo_line14:
                m=[]
                if len(g111114[i][j])>0:
                    for k in g111114[i][j]:
                        if k not in g222214[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line14[j] = len(m)





        f2= open("Current_Number_CarCV_line14.txt","a")
        f2.write(str(Current_Number_CarCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line14.txt","a")
        f2.write(str(Current_Number_BusCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line14.txt","a")
        f2.write(str(Current_Number_Car_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line14.txt","a")
        f2.write(str(Current_Number_Bus_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line14.txt","a")
        f2.write(str(Average_speed_CarCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line14.txt","a")
        f2.write(str(Average_speed_BusCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line14.txt","a")
        f2.write(str(Average_speed_Car_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line14.txt","a")
        f2.write(str(Average_speed_Bus_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line14.txt","a")
        f2.write(str(Arrival_CarCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line14.txt","a")
        f2.write(str(Arrival_BusCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line14.txt","a")
        f2.write(str(Arrival_Car_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line14.txt","a")
        f2.write(str(Arrival_Bus_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line14.txt","a")
        f2.write(str(Departure_CarCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line14.txt","a")
        f2.write(str(Departure_BusCV_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line14.txt","a")
        f2.write(str(Departure_Car_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line14.txt","a")
        f2.write(str(Departure_Bus_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line14.txt","a")
        f2.write(str(Turn1_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line14.txt","a")
        f2.write(str(Turn2_line14))
        f2.write("\n")
        f2.write(",")
        f2.close()








    LinkLength13= Vissim.Net.Links.ItemByKey(13).AttValue('Length2D')
    CellsNo_line13=[]
    i=0
    k=0
    while i< truncate(LinkLength13,-1):
        CellsNo_line13.append(k)
        i=i+CellLength
        k+=1
    

    #first we just collect the infomation of CVs    
    for i in TimeNo:
        #It is the number of vehicles in each cell in the current time step



        if SimSec > (i)*deltaT and SimSec <= (i+1)*deltaT:
            k113=[[]]*len(CellsNo_line13)
            z113=[[]]*len(CellsNo_line13)
            m113=[[]]*len(CellsNo_line13)
            n113=[[]]*len(CellsNo_line13)
            T113=[[]]*len(CellsNo_line13)

            for j in CellsNo_line13:
                k213=[]
                z213=[]
                m213=[]
                n213=[]
                T213=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '13':                       
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:                                
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    k213.append(vehAttributes[vehsAttNames['No']])
                                    k113[j]=k213
                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:
                                    z213.append(vehAttributes[vehsAttNames['No']])
                                    z113[j]=z213
                        if vehAttributes[vehsAttNames['VehType\No']] in Car:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    m213.append(vehAttributes[vehsAttNames['No']])
                                    m113[j]=m213

                        if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    n213.append(vehAttributes[vehsAttNames['No']])
                                    n113[j]=n213

                        if vehAttributes[vehsAttNames['Pos']] != None:
                            Pos = vehAttributes[vehsAttNames['Pos']]                           
                            if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                T213.append(vehAttributes[vehsAttNames['No']])
                                T113[j]=T213                        


            f2= open("113.txt","a")
            f2.write(str(k113))
            f2.write("\n")
            f2.close()
            f2= open("1113.txt","a")
            f2.write(str(z113))
            f2.write("\n")
            f2.close()
            f2= open("11113.txt","a")
            f2.write(str(m113))
            f2.write("\n")
            f2.close()
            f2= open("111113.txt","a")
            f2.write(str(n113))
            f2.write("\n")
            f2.close()

            f2= open("1111113.txt","a")
            f2.write(str(T113))
            f2.write("\n")
            f2.close()


        # It is the number of vehicles in each cell in the previous time step
        elif SimSec > (i-1)*deltaT and SimSec <= (i)*deltaT:
            if i==0:
                kk113=[[]]*len(CellsNo_line13)
                f2= open("013.txt","a")
                f2.write(str(kk113))
                f2.write("\n")
                f2.close()

                zz113=[[]]*len(CellsNo_line13)
                f2= open("0013.txt","a")
                f2.write(str(zz113))
                f2.write("\n")
                f2.close()

                mm113=[[]]*len(CellsNo_line13)
                f2= open("00013.txt","a")
                f2.write(str(mm113))
                f2.write("\n")
                f2.close()

                nn113=[[]]*len(CellsNo_line13)
                f2= open("000013.txt","a")
                f2.write(str(nn113))
                f2.write("\n")
                f2.close()     
            
            else:
                kk113=[[]]*len(CellsNo_line13)
                zz113=[[]]*len(CellsNo_line13)
                mm113=[[]]*len(CellsNo_line13)
                nn113=[[]]*len(CellsNo_line13)
                for j in CellsNo_line13:
                    kk213=[]
                    zz213=[]
                    mm213=[]
                    nn213=[]
                    for vehAttributes in vehsAttributes:
                        if vehAttributes[vehsAttNames['Lane\Link']] == '13':
                            if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        kk213.append(vehAttributes[vehsAttNames['No']])
                                        kk113[j]=kk213
                            if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zz213.append(vehAttributes[vehsAttNames['No']])
                                        zz113[j]=zz213


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mm213.append(vehAttributes[vehsAttNames['No']])
                                        mm113[j]=mm213


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nn213.append(vehAttributes[vehsAttNames['No']])
                                        nn113[j]=nn213
                                        

                                        


                f2= open("013.txt","a")
                f2.write(str(kk113))
                f2.write("\n")
                f2.close()


                f2= open("0013.txt","a")
                f2.write(str(zz113))
                f2.write("\n")
                f2.close()


                f2= open("00013.txt","a")
                f2.write(str(mm113))
                f2.write("\n")
                f2.close()

                f2= open("000013.txt","a")
                f2.write(str(nn113))
                f2.write("\n")
                f2.close()  

        # It is the number of vehicles in each cell in thesubsequent time step
        elif SimSec > (i+1)*deltaT and SimSec <= (i+2)*deltaT:
            
            kkk113=[[]]*len(CellsNo_line13)
            zzz113=[[]]*len(CellsNo_line13)
            mmm113=[[]]*len(CellsNo_line13)
            nnn113=[[]]*len(CellsNo_line13)
            for j in CellsNo_line13:
                kkk213=[]
                zzz213=[]
                mmm213=[]
                nnn213=[]
                for vehAttributes in vehsAttributes:
                    if vehAttributes[vehsAttNames['Lane\Link']] == '13':
                        if vehAttributes[vehsAttNames['VehType\No']] in CarCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                Pos = vehAttributes[vehsAttNames['Pos']]                           
                                if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                    kkk213.append(vehAttributes[vehsAttNames['No']])
                                    kkk113[j]=kkk213

                        if vehAttributes[vehsAttNames['VehType\No']] in BusCV:
                            if vehAttributes[vehsAttNames['Pos']] != None:
                                if vehAttributes[vehsAttNames['Lane\Link']] == '13':
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        zzz213.append(vehAttributes[vehsAttNames['No']])
                                        zzz113[j]=zzz213


                            if vehAttributes[vehsAttNames['VehType\No']] in Car:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        mmm213.append(vehAttributes[vehsAttNames['No']])
                                        mmm113[j]=mmm213


                            if vehAttributes[vehsAttNames['VehType\No']] in Bus:
                                if vehAttributes[vehsAttNames['Pos']] != None:
                                    Pos = vehAttributes[vehsAttNames['Pos']]                           
                                    if Pos > (j)*CellLength and Pos <= (j+1)*CellLength:                                
                                        nnn213.append(vehAttributes[vehsAttNames['No']])
                                        nnn113[j]=nnn213
                                
            f2= open("213.txt","a")
            f2.write(str(kkk113))
            f2.write("\n")
            f2.close()

            f2= open("2213.txt","a")
            f2.write(str(zzz113))
            f2.write("\n")
            f2.close()



            f2= open("22213.txt","a")
            f2.write(str(mmm113))
            f2.write("\n")
            f2.close()


            f2= open("222213.txt","a")
            f2.write(str(nnn113))
            f2.write("\n")
            f2.close()  



    #Here, we retreive our data as lists
    if SimSec>=3:

        f = open('013.txt', 'r')
        g013=[]
        for line in f.readlines():
            A013= ast.literal_eval(line)
            g013.append(A013)
        f.close()


        f = open('0013.txt', 'r')
        g0013=[]
        for line in f.readlines():
            A0013= ast.literal_eval(line)
            g0013.append(A0013)
        f.close()

        f = open('00013.txt', 'r')
        g00013=[]
        for line in f.readlines():
            A00013= ast.literal_eval(line)
            g00013.append(A00013)
        f.close()

        f = open('000013.txt', 'r')
        g000013=[]
        for line in f.readlines():
            A000013= ast.literal_eval(line)
            g000013.append(A000013)
        f.close()


        f = open('113.txt', 'r')
        g113=[]
        for line in f.readlines():
            A113= ast.literal_eval(line)
            g113.append(A113)
        f.close()

        f = open('1113.txt', 'r')
        g1113=[]
        for line in f.readlines():
            A1113= ast.literal_eval(line)
            g1113.append(A1113)
        f.close()


        f = open('11113.txt', 'r')
        g11113=[]
        for line in f.readlines():
            A11113= ast.literal_eval(line)
            g11113.append(A11113)
        f.close()


        f = open('111113.txt', 'r')
        g111113=[]
        for line in f.readlines():
            A111113= ast.literal_eval(line)
            g111113.append(A111113)
        f.close()


        f = open('1111113.txt', 'r')
        g1111113=[]
        for line in f.readlines():
            A1111113= ast.literal_eval(line)
            g1111113.append(A1111113)
        f.close()

        f = open('213.txt', 'r')
        g213=[]
        for line in f.readlines():
            A213= ast.literal_eval(line)
            g213.append(A213)
        f.close()

        f = open('2213.txt', 'r')
        g2213=[]
        for line in f.readlines():
            A2213= ast.literal_eval(line)
            g2213.append(A2213)
        f.close()

        f = open('22213.txt', 'r')
        g22213=[]
        for line in f.readlines():
            A22213= ast.literal_eval(line)
            g22213.append(A22213)
        f.close()

        f = open('222213.txt', 'r')
        g222213=[]
        for line in f.readlines():
            A222213= ast.literal_eval(line)
            g222213.append(A222213)
        f.close()


        Current_Number_CarCV_line13=[0]*len(CellsNo_line13)
        Current_Number_BusCV_line13=[0]*len(CellsNo_line13)
        Current_Number_Car_line13=[0]*len(CellsNo_line13)
        Current_Number_Bus_line13=[0]*len(CellsNo_line13)
        
        Arrival_CarCV_line13=[0]*len(CellsNo_line13)
        Arrival_BusCV_line13=[0]*len(CellsNo_line13)
        Arrival_Car_line13=[0]*len(CellsNo_line13)
        Arrival_Bus_line13=[0]*len(CellsNo_line13)

        Departure_CarCV_line13=[0]*len(CellsNo_line13)
        Departure_BusCV_line13=[0]*len(CellsNo_line13)
        Departure_Car_line13=[0]*len(CellsNo_line13)
        Departure_Bus_line13=[0]*len(CellsNo_line13)

        Average_speed_CarCV_line13=[0]*len(CellsNo_line13)
        Average_speed_BusCV_line13=[0]*len(CellsNo_line13)
        Average_speed_Car_line13=[0]*len(CellsNo_line13)
        Average_speed_Bus_line13=[0]*len(CellsNo_line13)



        Turn1_line13=[0]*len(CellsNo_line13)
        Turn2_line13=[0]*len(CellsNo_line13)






        for i in g1111113: 
            for j in CellsNo_line13:
                if len(i[j])>0:
                    Turn1_line13[j]= 1
                    Turn2_line13[j]= 0


                else:
                    Turn1_line13[j]= 0
                    Turn2_line13[j]= 0


        for i in g113: 
            for j in CellsNo_line13:
                Current_Number_CarCV_line13[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_CarCV_line13[j]= kgh/len(i[j])

                else:
                    Average_speed_CarCV_line13[j]= 0




        for i in g1113: 
            for j in CellsNo_line13:
                Current_Number_BusCV_line13[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_BusCV_line13[j]= kgh/len(i[j])

                else:
                    Average_speed_BusCV_line13[j]= 0





        for i in g11113: 
            for j in CellsNo_line13:
                Current_Number_Car_line13[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Car_line13[j]= kgh/len(i[j])

                else:
                    Average_speed_Car_line13[j]= 0



        for i in g111113: 
            for j in CellsNo_line13:
                Current_Number_Bus_line13[j] = len(i[j])
                if len(i[j])>0:
                    kgh=0
                    for k in i[j]:
                        try:
                            kgh=kgh+Vissim.Net.Vehicles.ItemByKey(k).AttValue('Speed')
                        except:
                            kgh=kgh+0
                    Average_speed_Bus_line13[j]= kgh/len(i[j])

                else:
                    Average_speed_Bus_line13[j]= 0






        for i in range(len(g113)):          
            for j in CellsNo_line13:
                m=[]
                if len(g113[i][j])>0:
                    for k in g113[i][j]:
                        if k not in g013[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_CarCV_line13[j] = len(m)
                


        for i in range(len(g1113)):          
            for j in CellsNo_line13:
                m=[]
                if len(g1113[i][j])>0:
                    for k in g1113[i][j]:
                        if k not in g0013[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_BusCV_line13[j] = len(m)




        for i in range(len(g11113)):          
            for j in CellsNo_line13:
                m=[]
                if len(g11113[i][j])>0:
                    for k in g11113[i][j]:
                        if k not in g00013[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Car_line13[j] = len(m)







        for i in range(len(g111113)):          
            for j in CellsNo_line13:
                m=[]
                if len(g111113[i][j])>0:
                    for k in g111113[i][j]:
                        if k not in g000013[i][j]:
                            m.append(k)
                else:
                    m=[]
                Arrival_Bus_line13[j] = len(m)






        for i in range(len(g213)):          
            for j in CellsNo_line13:
                m=[]
                if len(g113[i][j])>0:
                    for k in g113[i][j]:
                        if k not in g213[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_CarCV_line13[j] = len(m)
                



        for i in range(len(g2213)):          
            for j in CellsNo_line13:
                m=[]
                if len(g1113[i][j])>0:
                    for k in g1113[i][j]:
                        if k not in g2213[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_BusCV_line13[j] = len(m)




        for i in range(len(g22213)):          
            for j in CellsNo_line13:
                m=[]
                if len(g11113[i][j])>0:
                    for k in g11113[i][j]:
                        if k not in g22213[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Car_line13[j] = len(m)



        for i in range(len(g222213)):          
            for j in CellsNo_line13:
                m=[]
                if len(g111113[i][j])>0:
                    for k in g111113[i][j]:
                        if k not in g222213[i][j]:
                            m.append(k)
                else:
                    m=[]
                Departure_Bus_line13[j] = len(m)





        f2= open("Current_Number_CarCV_line13.txt","a")
        f2.write(str(Current_Number_CarCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_BusCV_line13.txt","a")
        f2.write(str(Current_Number_BusCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Car_line13.txt","a")
        f2.write(str(Current_Number_Car_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Current_Number_Bus_line13.txt","a")
        f2.write(str(Current_Number_Bus_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()



        f2= open("Average_speed_CarCV_line13.txt","a")
        f2.write(str(Average_speed_CarCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_BusCV_line13.txt","a")
        f2.write(str(Average_speed_BusCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Car_line13.txt","a")
        f2.write(str(Average_speed_Car_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Average_speed_Bus_line13.txt","a")
        f2.write(str(Average_speed_Bus_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Arrival_CarCV_line13.txt","a")
        f2.write(str(Arrival_CarCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_BusCV_line13.txt","a")
        f2.write(str(Arrival_BusCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Car_line13.txt","a")
        f2.write(str(Arrival_Car_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Arrival_Bus_line13.txt","a")
        f2.write(str(Arrival_Bus_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()




        f2= open("Departure_CarCV_line13.txt","a")
        f2.write(str(Departure_CarCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_BusCV_line13.txt","a")
        f2.write(str(Departure_BusCV_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Car_line13.txt","a")
        f2.write(str(Departure_Car_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()

        f2= open("Departure_Bus_line13.txt","a")
        f2.write(str(Departure_Bus_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn1_line13.txt","a")
        f2.write(str(Turn1_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()


        f2= open("Turn2_line13.txt","a")
        f2.write(str(Turn2_line13))
        f2.write("\n")
        f2.write(",")
        f2.close()






















