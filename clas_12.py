#
# Copyright 2005-2018 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#
 
from __future__ import print_function
import traceback
import sys
import requests
import bz2
import os
import datetime
import math
import ephem
import io
import psycopg2
from psycopg2 import connect, sql
from psycopg2.extras import RealDictCursor
import time
from datetime import timedelta
from bz2 import decompress
from eccodes import *
from threading import Thread

class DownParam:

    
    def __init__(self,pathpart,firstpart,zeropart,lastpart,httppart,name,slash,extpart):
        self.pathpart=pathpart
        self.firstpart=firstpart
        self.zeropart=zeropart
        self.lastpart=lastpart
        self.httppart=httppart
        self.name=name
        self.slash=slash
        self.extpart=extpart

        while True:
            try:
                self.conn = psycopg2.connect(host="localhost",database="test", user="user1", password="123456")
            except:
                print("Не удалось")#есть ошибка
            else:
                break;#все хорошо
            time.sleep(5)

    def sunpos_utc(self,lon, lat, timeutc):
        someplace = ephem.Observer()
        someplace.lon, someplace.lat = str(lon), str(lat)
        someplace.date = timeutc
        sun = ephem.Sun()
        sun.compute(someplace)
        return math.degrees(sun.alt), math.degrees(sun.az) 


    def timecor(self,numberhour):
        self.numberhour=numberhour
        now = datetime.datetime.now()
        intdays=int (numberhour)//24
        remday=(int (numberhour)%24)+3  
        result=now+timedelta(days=intdays,hours=-now.hour+remday,minutes=-now.minute)
        return result

    def downandwrite(self,filename,url):
        self.filename=filename
        self.url=url
        stations=[0,0,0]
        r=requests.get(url)
        gribfile=bz2.decompress(r.content)
        f=open(filename,"wb") #открываем файл для записи, в режиме wb
        f.write(gribfile) #записываем содержимое в файл; как видите - content запроса
        f.close()
        points = ((44.28882798, 33.59823831), (45.23847542, 33.67488499), (44.94879052,33.93747816))
        f=open(filename, 'rb')
        gid = codes_grib_new_from_file(f)
        i=0
        for lat, lon in points:
            nearest = codes_grib_find_nearest(gid, lat, lon)[0]
            stations[i]=round(nearest.value,4)
            i=i+1	
        os.remove(filename)
        codes_release(gid)
        return stations

    def downloadbadfiles(self,conn):
        self.conn=conn
        stations=[0,0,0]    
        cur=conn.cursor()
        while True:            
            cur.execute('SELECT * FROM bad_files_12')
            if cur.rowcount==0:
                break
            else:
                rows=cur.fetchmany(cur.rowcount)
                for row in rows:
                    try:
                        r=requests.head(row[0],timeout=5)
                        if(r.status_code==200):
                            stations=self.downandwrite(row[1],row[0])
                            if self.name=="t" or self.name=="t_2m" or self.name=="tmax_2m" or self.name=="tmin_2m":
                                stations[0]=round(stations[0]-273.15,4)
                                stations[1]=round(stations[1]-273.15,4)
                                stations[2]=round(stations[2]-273.15,4)
                            cur.execute('SELECT '+str(row[2])+' FROM forecast_omao_12 WHERE date=%s',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),))
                            if cur.rowcount==0:
                                s=self.sunpos_utc(33.59823831, 44.28882798,self.timecor(row[3]-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)

                                cur.execute('INSERT INTO forecast_omao_12 (date,'+str(row[2])+',altitude,azimuth) VALUES(%s,%s,%s,%s)',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),stations[0],round(s[0],4),round(s[1],4)))
                            else:

                                cur.execute('UPDATE forecast_omao_12 SET '+str(row[2])+'=%s WHERE date=%s',(stations[0],self.timecor(row[3]).strftime("%Y%m%d %H%M")))  
                
                            
                            cur.execute('SELECT '+str(row[2])+' FROM forecast_ospriy_12 WHERE date=%s',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),))
                            if cur.rowcount==0:
                                s=self.sunpos_utc(33.59823831, 44.28882798,self.timecor(row[3]-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)

                                cur.execute('INSERT INTO forecast_ospriy_12 (date,'+str(row[2])+',altitude,azimuth) VALUES(%s,%s,%s,%s)',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),stations[0],round(s[0],4),round(s[1],4)))
                            else:

                                cur.execute('UPDATE forecast_ospriy_12 SET '+str(row[2])+'=%s WHERE date=%s',(stations[0],self.timecor(row[3]).strftime("%Y%m%d %H%M")))                  

                            
                            cur.execute('SELECT '+str(row[2])+' FROM forecast_oul_12 WHERE date=%s',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),))
                            if cur.rowcount==0:
                                s=self.sunpos_utc(33.67488499, 45.23847542,self.timecor(row[3]-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)

                                cur.execute('INSERT INTO forecast_oul_12 (date,'+str(row[2])+',altitude,azimuth) VALUES(%s,%s,%s,%s)',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),stations[1],round(s[0],4),round(s[1],4)))
                            else:
                                cur.execute('UPDATE forecast_oul_12 SET '+str(row[2])+'=%s WHERE date=%s',(stations[1],self.timecor(row[3]).strftime("%Y%m%d %H%M")))                  

                            cur.execute('SELECT '+str(row[2])+' FROM forecast_delta_12 WHERE date=%s',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),))
                            if cur.rowcount==0:
                                s=self.sunpos_utc(33.93747816,44.94879052,self.timecor(row[3]-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)

                                cur.execute('INSERT INTO forecast_delta_12 (date,'+str(row[2])+',altitude,azimuth) VALUES(%s,%s,%s,%s)',(self.timecor(row[3]).strftime("%Y%m%d %H%M"),stations[2],round(s[0],4),round(s[1],4)))
                            else:
                                cur.execute('UPDATE forecast_delta_12 SET '+str(row[2])+'=%s WHERE date=%s',(stations[2],self.timecor(row[3]).strftime("%Y%m%d %H%M")))                  
     
                            cur.execute('DELETE FROM bad_files_12 WHERE address=%s',(row[0],))  
                            conn.commit()
                    except:                                            
                        conn.commit()                  
            #time.sleep(5)
        conn.close()        
 

    def downloadfiles(self,conn):
        stations=[0,0,0]
        self.conn=conn
        cur=conn.cursor()

        for j in range(26,67):
            if (j>=26 and j<43) or (j>=50 and j<67):
                try:                
                    now=datetime.datetime.now()              
                    r=requests.head(self.httppart+self.name+self.slash+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart+self.extpart,timeout=5)          
                    if(r.status_code==200):
                        stations=self.downandwrite(self.pathpart+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart,self.httppart+self.name+self.slash+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart+self.extpart) 
                        if self.name=="t" or self.name=="t_2m" or self.name=="tmax_2m" or self.name=="tmin_2m":
                            stations[0]=round(stations[0]-273.15,4)
                            stations[1]=round(stations[1]-273.15,4)
                            stations[2]=round(stations[2]-273.15,4)
                        cur.execute('SELECT * FROM forecast_omao_12 WHERE date=%s',(self.timecor(j).strftime("%Y%m%d %H%M"),))

                        if cur.rowcount==0:

                            s=self.sunpos_utc(33.59823831, 44.28882798,self.timecor(j-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)
                            cur.execute('INSERT INTO forecast_omao_12 (date,'+str(self.name)+',altitude,azimuth)'+' VALUES(%s,%s,%s,%s)',(self.timecor(j).strftime("%Y%m%d %H%M"),stations[0],round(s[0],4),round(s[1],4)))
                        else:

                            cur.execute('UPDATE forecast_omao_12 SET '+str(self.name)+'=%s WHERE date=%s',(stations[0],self.timecor(j).strftime("%Y%m%d %H%M")))        



                        cur.execute('SELECT * FROM forecast_ospriy_12 WHERE date=%s',(self.timecor(j).strftime("%Y%m%d %H%M"),))

                        if cur.rowcount==0:

                            s=self.sunpos_utc(33.59823831, 44.28882798,self.timecor(j-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)
                            cur.execute('INSERT INTO forecast_ospriy_12 (date,'+str(self.name)+',altitude,azimuth)'+' VALUES(%s,%s,%s,%s)',(self.timecor(j).strftime("%Y%m%d %H%M"),stations[0],round(s[0],4),round(s[1],4)))
                        else:

                            cur.execute('UPDATE forecast_ospriy_12 SET '+str(self.name)+'=%s WHERE date=%s',(stations[0],self.timecor(j).strftime("%Y%m%d %H%M")))        
 

                        cur.execute('SELECT * FROM forecast_oul_12 WHERE date=%s',(self.timecor(j).strftime("%Y%m%d %H%M"),))
                        if cur.rowcount==0:

                            s=self.sunpos_utc(33.67488499, 45.23847542,self.timecor(j-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)
                            cur.execute('INSERT INTO forecast_oul_12 (date,'+str(self.name)+',altitude,azimuth)'+' VALUES(%s,%s,%s,%s)',(self.timecor(j).strftime("%Y%m%d %H%M"),stations[1],round(s[0],4),round(s[1],4)))
                        else:
   
                            cur.execute('UPDATE forecast_oul_12 SET '+str(self.name)+'=%s WHERE date=%s',(stations[1],self.timecor(j).strftime("%Y%m%d %H%M")))         

                        cur.execute('SELECT * FROM forecast_delta_12 WHERE date=%s',(self.timecor(j).strftime("%Y%m%d %H%M"),))
                        if cur.rowcount==0:
                            s=self.sunpos_utc(33.93747816,44.94879052,self.timecor(j-3).strftime("%Y/%m/%d %H:%M"))#долгота(-запад) широта(+север)
  
                            cur.execute('INSERT INTO forecast_delta_12 (date,'+str(self.name)+',altitude,azimuth)'+' VALUES(%s,%s,%s,%s)',(self.timecor(j).strftime("%Y%m%d %H%M"),stations[2],round(s[0],4),round(s[1],4)))
                        else:
   
                            cur.execute('UPDATE forecast_delta_12 SET '+str(self.name)+'=%s WHERE date=%s',(stations[2],self.timecor(j).strftime("%Y%m%d %H%M")))         

               	        
        
                    else:
                        cur.execute('INSERT INTO bad_files_12 VALUES(%s,%s,%s,%s)',(self.httppart+self.name+self.slash+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart+self.extpart,self.pathpart+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart,self.name,j))                
                except:
                    cur.execute('INSERT INTO bad_files_12 VALUES(%s,%s,%s,%s)',(self.httppart+self.name+self.slash+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart+self.extpart,self.pathpart+self.firstpart+str(now.strftime("%Y%m%d"))+self.zeropart+str(j)+self.lastpart,self.name,j))                      
                conn.commit()
    
    def makeall(self):  
        self.downloadfiles(self.conn)
        self.downloadbadfiles(self.conn)
   

def thrALBRAD():
    param1 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_ALB_RAD.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","alb_rad","/",".bz2")
    param1.makeall()

def thrASOBS():
    param2 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_ASOB_S.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","asob_s","/",".bz2")
    param2.makeall()

def thrASWDIFDS():
    param3 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_ASWDIFD_S.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","aswdifd_s","/",".bz2")
    param3.makeall()

def thrASWDIFUS():
    param4 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_ASWDIFU_S.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","aswdifu_s","/",".bz2")
    param4.makeall()

def thrASWDIRS():
    param5 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_ASWDIR_S.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","aswdir_s","/",".bz2")
    param5.makeall()

def thrCAPECON():
    param6 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_CAPE_CON.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","cape_con","/",".bz2")
    param6.makeall()

def thrCLCH():
    param7 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_CLCH.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","clch","/",".bz2")
    param7.makeall()

def thrCLCL():
    param8 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_CLCL.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","clcl","/",".bz2")
    param8.makeall()


def thrCLCM():
    param9 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_CLCM.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","clcm","/",".bz2")
    param9.makeall()

def thrCLCT():
    param10 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_CLCT.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","clct","/",".bz2")
    param10.makeall()

def thrCLCTMOD():
    param11 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_CLCT_MOD.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","clct_mod","/",".bz2")
    param11.makeall()

def thrHBASCON():
    param12 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_HBAS_CON.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","hbas_con","/",".bz2")
    param12.makeall()

def thrMH():
    param13 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_MH.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","mh","/",".bz2")
    param13.makeall()

def thrQV2M():
    param14 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_QV_2M.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","qv_2m","/",".bz2")
    param14.makeall()

def thrQVS():
    param15 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_QV_S.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","qv_s","/",".bz2")
    param15.makeall()

def thrRAINCON():
    param16 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_RAIN_CON.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","rain_con","/",".bz2")
    param16.makeall()

def thrRAINGSP():
    param17 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_RAIN_GSP.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","rain_gsp","/",".bz2")
    param17.makeall()

def thrRELHUM2M():
    param18 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_RELHUM_2M.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","relhum_2m","/",".bz2")
    param18.makeall()

def thrSNOWCON():
    param19 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_SNOW_CON.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","snow_con","/",".bz2")
    param19.makeall()

def thrSNOWGSP():
    param20 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_SNOW_GSP.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","snow_gsp","/",".bz2")
    param20.makeall()

def thrT2M():
    param21 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_T_2M.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","t_2m","/",".bz2")
    param21.makeall()

def thrTMAX2M():
    param22 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_TMAX_2M.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","tmax_2m","/",".bz2")
    param22.makeall()

def thrTMIN2M():
    param23 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_single-level_","12_0","_TMIN_2M.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","tmin_2m","/",".bz2")
    param23.makeall()
#Bad below!!
def thrOMEGA():
    param24 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_pressure-level_","12_0","_1000_OMEGA.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","omega","/",".bz2")
    param24.makeall()

def thrCLC():
    param25 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_pressure-level_","12_0","_1000_CLC.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","clc","/",".bz2")
    param25.makeall()

def thrT():
    param26 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_T.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","t","/",".bz2")
    param26.makeall()

def thrU():
    param27 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_U.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","u","/",".bz2")
    param27.makeall()

def thrV():
    param28 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_V.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","v","/",".bz2")
    param28.makeall()

def thrP():
    param29 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_P.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","p","/",".bz2")
    param29.makeall()

def thrQV():
    param30 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_QV.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","qv","/",".bz2")
    param30.makeall()

def thrRELHUM():
    param31 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_pressure-level_","12_0","_1000_RELHUM.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","relhum","/",".bz2")
    param31.makeall()

def thrTKE():
    param32 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_TKE.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","tke","/",".bz2")
    param32.makeall()

def thrW():
    param33 = DownParam("/home/osboxes/","icon-eu_europe_regular-lat-lon_model-level_","12_0","_10_W.grib2","http://opendata.dwd.de/weather/nwp/icon-eu/grib/12/","w","/",".bz2")
    param33.makeall()



thr1=Thread(target=thrALBRAD)
thr2=Thread(target=thrASOBS)
thr3=Thread(target=thrASWDIFDS)
thr4=Thread(target=thrASWDIFUS)
thr5=Thread(target=thrASWDIRS)
thr6=Thread(target=thrCAPECON)
thr7=Thread(target=thrCLCH)
thr8=Thread(target=thrCLCL)
thr9=Thread(target=thrCLCM)
thr10=Thread(target=thrCLCT)
thr11=Thread(target=thrCLCTMOD)
thr12=Thread(target=thrHBASCON)
thr13=Thread(target=thrMH)
thr14=Thread(target=thrQV2M)
thr15=Thread(target=thrQVS)
thr16=Thread(target=thrRAINCON)
thr17=Thread(target=thrRAINGSP)
thr18=Thread(target=thrRELHUM2M)
thr19=Thread(target=thrSNOWCON)
thr20=Thread(target=thrSNOWGSP)
thr21=Thread(target=thrT2M)
thr22=Thread(target=thrTMAX2M)
thr23=Thread(target=thrTMIN2M)
thr24=Thread(target=thrOMEGA)
thr25=Thread(target=thrCLC)
thr26=Thread(target=thrT)
thr27=Thread(target=thrU)
thr28=Thread(target=thrV)
thr29=Thread(target=thrP)
thr30=Thread(target=thrQV)
thr31=Thread(target=thrRELHUM)
thr32=Thread(target=thrTKE)
thr33=Thread(target=thrW)


l=[thr1,thr2,thr3,thr4,thr5,thr6,thr7,thr8,thr9,thr10,thr11,thr12,thr13,thr14,thr15,thr16,thr17,thr18,thr19,thr20,thr21,thr22,thr23,thr24,thr25,thr26,thr27,thr28,thr29,thr30,thr31,thr32,thr33]
for i in range(0,33):
    l[i].start()
for i in range(0,33):
    l[i].join()


