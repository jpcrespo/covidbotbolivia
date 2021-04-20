
import os,sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha')
df3=pd.read_csv('covid19-bolivia/confirmados.csv',sep=',').sort_values(by='Fecha')
df4=pd.read_csv('covid19-bolivia/decesos.csv',sep=',').sort_values(by='Fecha')


departamentos=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']
departamentos1=['La Paz','Cochabamba','Santa Cruz','Oruro','Potosí','Tarija','Chuquisaca','Beni','Pando']

y  = df1['fecha']
y1 = df3['Fecha']

data1 = df1.iloc[:,1:].values.T
data2 = df2.iloc[:,1:].values.T

data3 = df3.iloc[:,1:].values.T
data4 = df4.iloc[:,1:].values.T


for i in range(len(departamentos)):
    plt.figure(figsize=(10,5))
    plt.title('Vacunaciones en el Departamento\n del '+departamentos[i],fontsize=15)
    plt.plot(y,data1[i],label='Primera dosis')
    plt.plot(y,data2[i],label='Segunda dosis')
    plt.xticks(y[::7],fontsize=6)
    plt.ylabel('Número de dosis aplicadas')
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend(loc='upper left')
    plt.text(51,0,"Data source: https://github.com/mauforonda/vacunas"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Históricos acumulado", fontsize=6.5)  
    plt.savefig('pics/vac'+departamentos[i]+'.png')

nacional1=data1[0]+data1[1]+data1[2]+data1[3]+data1[4]+data1[5]+data1[6]+data1[7]+data1[8]
nacional2=data2[0]+data2[1]+data2[2]+data2[3]+data2[4]+data2[5]+data2[6]+data2[7]+data2[8]
plt.figure(figsize=(10,5))
plt.title('Vacunaciones en el Nacional',fontsize=15)
plt.plot(y,nacional1,label='Primera dosis')
plt.plot(y,nacional2,label='Segunda dosis')
plt.xticks(y[::7],fontsize=6)
plt.ylabel('Número de dosis aplicadas')
plt.xticks(rotation=45)
plt.grid()
plt.legend(loc='upper left')
plt.text(51,0,"Data source: https://github.com/mauforonda/vacunas"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Históricos acumulado", fontsize=6.5)   
plt.savefig('pics/vacNac.png')



# ==============================================================
# =           Obteniendo el gráfico Variación Diaria           =
# ==============================================================

var_d=np.zeros((9,len(data3[0])))
var_d_m=np.zeros((9,len(data3[0])))

for j in range(9):
	for i in range(len(data3[0])-1):
		var_d[j,i]=data3[j,i+1]-data3[j,i]
		var_d_m[j,i]=data4[j,i+1]-data4[j,i]


# # # ======  End of Obteniendo eláfico Variación Diaria  =======
	

for i in range(len(departamentos1)):
    plt.figure(figsize=(10,5))
    plt.title('Variación Diaria en el Departamento\n del '+departamentos1[i],fontsize=15)
    plt.plot(y1,var_d[i],label='Variación nuevos casos por día')
    plt.plot(y1,var_d_m[i],label='Variación fallecimientos por día')
    plt.xticks(y1[::30],fontsize=6)
    plt.ylabel('Casos nuevos por día')
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend(loc='upper right')
    plt.savefig('pics/cov'+departamentos1[i]+'.png')

nacional1_=var_d[0]+var_d[1]+var_d[2]+var_d[3]+var_d[4]+var_d[5]+var_d[6]+var_d[7]+var_d[8]
nacional2_=var_d_m[0]+var_d_m[1]+var_d_m[2]+var_d_m[3]+var_d_m[4]+var_d_m[5]+var_d_m[6]+var_d_m[7]+var_d_m[8]
plt.figure(figsize=(10,5))
plt.title('Variación Diaria Nacional',fontsize=15)
plt.plot(y1,nacional1_,label='Variación nuevos casos por día')
plt.plot(y1,nacional2_,label='Variación fallecimientos por día')
plt.xticks(y1[::30],fontsize=6)
plt.ylabel('Número de dosis aplicadas')
plt.xticks(rotation=45)
plt.grid()
plt.legend(loc='upper right')
plt.text(-5,2600,"Data source: https://github.com/mauforonda/covid19-bolivia"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Históricos acumulado", fontsize=6.3)   
plt.savefig('pics/covNac.png')




from datetime import date
from datetime import datetime
now = datetime.now()

with open('datos.py', 'a') as f:
    mss=str(now.day)+'/'+str(now.month)+'/'+str(now.year)
    f.write("\n")
    f.write("flag_date = '" )
    f.write(mss)
    f.write("'")
