import os,sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1=pd.read_csv('vacunas/datos/primera.csv',sep=',').sort_values(by='fecha').set_index('fecha')
df2=pd.read_csv('vacunas/datos/segunda.csv',sep=',').sort_values(by='fecha').set_index('fecha')

df3=pd.read_csv('covid19-bolivia/confirmados.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')
df4=pd.read_csv('covid19-bolivia/decesos.csv',sep=',').sort_values(by='Fecha').set_index('Fecha')

departamentos_v=['Beni','Chuquisaca','Cochabamba','La Paz','Oruro','Pando','Potosi','Santa Cruz','Tarija']
departamentos_c=['La Paz','Cochabamba','Santa Cruz','Oruro','Potosí','Tarija','Chuquisaca','Beni','Pando']

data1 = df1.iloc[:,:].values.T
data2 = df2.iloc[:,:].values.T

data3 = df3.iloc[:,:].values.T
data4 = df4.iloc[:,:].values.T

# En el caso de la presentación de datos del Nacional
# se plantea obtener los nuevos casos diarios. Igual que en
# vacunaciones pero solo para obtener la última actualización del día.

var_c=np.zeros((9,len(data3[0])))
var_m=np.zeros((9,len(data4[0])))

for j in range(9):
    var_c[j,0]=data3[j,0]
    var_m[j,0]=data4[j,0]
    for i in range(1,len(data3[0])):
        var_c[j,i]=data3[j,i]-data3[j,i-1]
        var_m[j,i]=data4[j,i]-data4[j,i-1]
        
        
        
#Para encontrar solo el valor de vacunados día (en la gráfica solo interesa el acumulado)
#como dato díario se rescata pero no graficamos la variación diaria de vacunas 
var_v1=np.zeros(9)
var_v2=np.zeros(9)
for j in range(9):
    var_v1[j]=data1[j,-1]-data1[j,-2]
    var_v2[j]=data2[j,-1]-data2[j,-2]
    
y_v=df1.index.values       #Para los gráficos de las vacunas
y_c=df3.index.values       #Para los gráficos de los datos covid
    
# Ahora para que las gráficas de los datos covid se vean bien 
# sobre los puntos de los datos reportados ira un curva 
# pero de los promedios por semana. 

#promedio de 7 dias
mean_df_c = df3.rolling(7,min_periods=1).mean()
mean_df_m = df4.rolling(7,min_periods=1).mean()

mean_dc = mean_df_c.iloc[:,:].values.T   
mean_dm = mean_df_m.iloc[:,:].values.T   

var_mc=np.zeros((9,len(mean_dc[0])))
var_mm=np.zeros((9,len(mean_dm[0])))

for j in range(9):
    var_mc[j,0]=mean_dc[j,0]
    var_mm[j,0]=mean_dc[j,0]
    for i in range(1,len(data3[0])):
        var_mc[j,i]=mean_dc[j,i]-mean_dc[j,i-1]
        var_mm[j,i]=mean_dm[j,i]-mean_dm[j,i-1]
        
        
#Generador de imagenes  VACUNAS
plt.style.use('dark_background')

from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

bol = mpimg.imread('bol.jpg')
imagebox = OffsetImage(bol,zoom=1)


# These are the "Tableau 20" colors as RGB.    
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)   

for i in range(len(departamentos_v)):
    plt.figure(figsize=(20,15))
    
    plt.title('Vacunaciones en el Departamento: '+departamentos_v[i]+'\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=35)
    plt.plot(y_v,data1[i],linewidth=3,color=tableau20[0])
    plt.plot(y_v,data2[i],linewidth=3,color=tableau20[4])
    plt.xticks(y_v[::7],fontsize=15,rotation=45)
    plt.ylabel('Vacunados',fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim(0,np.max(data1[i]))
    plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(True)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)  
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.text(len(data1[0]), data1[i,-1],'1er Dosis',fontsize=20,color=tableau20[0])
    plt.text(len(data1[0]), data2[i,-1],'2da Dosis',fontsize=20,color=tableau20[4])
    plt.text(55,400,"Data source: https://github.com/mauforonda/vacunas"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado", fontsize=12)  
    plt.savefig('pics/vac'+departamentos_v[i]+'.png')


nacional1=data1[0]+data1[1]+data1[2]+data1[3]+data1[4]+data1[5]+data1[6]+data1[7]+data1[8]
nacional2=data2[0]+data2[1]+data2[2]+data2[3]+data2[4]+data2[5]+data2[6]+data2[7]+data2[8]

op=int(len(nacional1)/1.12)
firma = AnnotationBbox(imagebox,(20,nacional1[op]))

plt.figure(figsize=(20,15))
plt.title('Vacunación a nivel Nacional\n(último reporte en fuente: '+y_v[-1]+')\n',fontsize=35)
plt.plot(y_v,nacional1,linewidth=3,color=tableau20[0])
plt.plot(y_v,nacional2,linewidth=3,color=tableau20[4])
plt.xticks(y_v[::7],fontsize=15,rotation=45)
plt.ylabel('Vacunados',fontsize=20)
plt.ylim(0,np.max(nacional1))
plt.yticks(fontsize=20)
#plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.gca().add_artist(firma)
plt.text(len(data1[0]), nacional1[-1],'1er Dosis',fontsize=20,color=tableau20[0])
plt.text(len(data1[0]), nacional2[-1],'2da Dosis',fontsize=20,color=tableau20[4])
plt.text(55,8000,"Data source: https://github.com/mauforonda/vacunas"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado", fontsize=12)  
plt.savefig('pics/vacNac.png')



# ==============================================================
# =           Obteniendo el gráfico Variación Diaria           =
# ==============================================================

for i in range(len(departamentos_c)):
    plt.figure(figsize=(20,15))
    plt.title('Nuevos casos/día en el Departamento: '+departamentos_c[i]+'\n(último reporte en fuente: '+y_c[-1]+')\n',fontsize=35)
    plt.plot(y_c[:-2],var_c[i,:-2],label='Nuevos Casos/día',linewidth=0.5,color=tableau20[0],linestyle='-',marker='.', markersize=5,markeredgecolor='red',markerfacecolor='r')
    plt.plot(y_c,var_mc[i],label='Promedio 7 días',linewidth=5,color=tableau20[1],linestyle='-')
    plt.plot(y_c,var_m[i],label='Fallecimientos/día',linewidth=5,color=tableau20[7],linestyle='-')
    plt.legend(loc='upper left',fontsize=20)
    plt.yticks(fontsize=20)
    plt.xticks(y_c[::31],fontsize=15,rotation=45)
    plt.ylim(0,np.max(var_c[i]))  
    plt.ylabel('Casos/día',fontsize=20)
    plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
    plt.gca().spines["top"].set_visible(False)    
    plt.gca().spines["bottom"].set_visible(True)    
    plt.gca().spines["right"].set_visible(False)    
    plt.gca().spines["left"].set_visible(False)  
    plt.gca().get_xaxis().tick_bottom()    
    plt.gca().get_yaxis().tick_left()
    plt.text(10,np.max(var_c[i])/2,"Data source: https://github.com/mauforonda/covid19-bolivia"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado", fontsize=12) 
    plt.savefig('pics/cov'+departamentos_c[i]+'.png')
    

nacional1_=var_c[0]+var_c[1]+var_c[2]+var_c[3]+var_c[4]+var_c[5]+var_c[6]+var_c[7]+var_c[8]
nacional2_=var_mc[0]+var_mc[1]+var_mc[2]+var_mc[3]+var_mc[4]+var_mc[5]+var_mc[6]+var_mc[7]+var_mc[8]
nacional3_=var_mm[0]+var_mm[1]+var_mm[2]+var_mm[3]+var_mm[4]+var_mm[5]+var_mm[6]+var_mm[7]+var_mm[8]


plt.figure(figsize=(20,15))
plt.title('Nuevos casos/día a nivel Nacional'+'\n(último reporte en fuente: '+y_c[-1]+')\n',fontsize=35)
plt.plot(y_c[:-2],nacional1_[:-2],label='Nuevos Casos/día',linewidth=0.5,color=tableau20[0],linestyle='-',marker='.',markersize=5,markeredgecolor='red',markerfacecolor='r')
plt.plot(y_c,nacional2_,label='Promedio 7 días',linewidth=5,color=tableau20[1],linestyle='-')
plt.plot(y_c,nacional3_,label='Fallecimientos/día',linewidth=5,color=tableau20[7],linestyle='-')



bol1 = mpimg.imread('bol.jpg')
imagebox1 = OffsetImage(bol1,zoom=1)

firma1 = AnnotationBbox(imagebox1,(60,np.max(nacional1_)/1.2))




plt.legend(loc='upper right',fontsize=20)
plt.yticks(fontsize=20)
plt.xticks(y_c[::31],fontsize=15,rotation=45)
plt.ylim(0,np.max(nacional1_))  
plt.ylabel('Casos/día',fontsize=20)
#plt.gca().yaxis.grid(linestyle='--',linewidth=0.5,dashes=(5,15))
plt.gca().spines["top"].set_visible(False)    
plt.gca().spines["bottom"].set_visible(True)    
plt.gca().spines["right"].set_visible(False)    
plt.gca().spines["left"].set_visible(False)  
plt.gca().get_xaxis().tick_bottom()    
plt.gca().get_yaxis().tick_left()
plt.gca().add_artist(firma1)
plt.text(10,1800,"Data source: https://github.com/mauforonda/covid19-bolivia"    
       "\nAutor: Telegram Bot: @Bolivian_Bot"    
       "\nNota: Histórico acumulado", fontsize=12) 
plt.savefig('pics/covNac.png')

from datetime import date
from datetime import datetime
now = datetime.now()

with open('datos.py', 'a') as f:
    mss=str(now.day)+'/'+str(now.month)+'/'+str(now.year)
    mss1=str(now.day)+'/'+str(now.month)+'/'+str(now.year)+'-'+str(now.hour)+":"+str(now.minute)
    f.write("\n")
    f.write("flag_date = '" )    #ultima actualización de consulta a la fuente y generación de imagenes
    f.write(mss)
    f.write("'")
    f.write("\n")
    f.write("act_mss = '")          #las notificaciones que manda al admin con hora de ejecución.
    f.write(mss1)
    f.write("'")


#se guarda un array actualizado con los datos: 
# casos_dia     
# muertos_día    
# vacunados_1    
# vacunados_2    


muertos_dia=np.zeros(9)
casos_dia=np.zeros(9)
for j in range(9):
    muertos_dia[j]=data4[j,-1]-data4[j,-2]
    casos_dia[j]=data3[j,-1]-data3[j,-2]


estados =  [[casos_dia[0],casos_dia[1],casos_dia[2],casos_dia[3],casos_dia[4],casos_dia[5],casos_dia[6],casos_dia[7],casos_dia[8]],
            [muertos_dia[0],muertos_dia[1],muertos_dia[2],muertos_dia[3],muertos_dia[4],muertos_dia[5],muertos_dia[6],muertos_dia[7],muertos_dia[8]],
            [var_v1[3],var_v1[2],var_v1[7],var_v1[4],var_v1[6],var_v1[8],var_v1[1],var_v1[0],var_v1[5]],
            [var_v2[3],var_v2[2],var_v2[7],var_v2[4],var_v2[6],var_v2[8],var_v2[1],var_v2[0],var_v2[5]]]


uac = [y_c[-1],y_v[-1]]
np.save('estados.npy',estados)   #los valores de cada día actualizado y mostrar resumen.
np.save('fechas.npy',uac)        #Guarda las últimas fechas donde se llenaron las fuentes. 


