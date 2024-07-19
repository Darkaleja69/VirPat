import matplotlib.pyplot as plt
import numpy as np

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute:d})"
fig1, ax1=plt.subplots()
labels=["train","dev","test"]
data=[99,11,19]
ax1.pie(data,labels=labels,autopct=lambda pct:func(pct,data))

plt.show()
#Resultados de la temperatura en las conversaciones 10-29

'''x=[]

i=0
while i<=1:
    x.append(str(i))
    i=round(i+0.05,2)

print(x)
y=[0.4075,0.4142,0.4217,0.4164,0.4171,0.4133,0.4133,0.4191,0.4116,0.4111,0.4145,0.4234,0.4103,0.4157,0.4018,0.4133,0.4021,0.4046,0.4025,0.4,0.3972]

fig2,ax2=plt.subplots()
plt.xlabel('Temperatura de ChatGPT',fontsize=15)
plt.ylabel('Precisión BLEU',fontsize=15)
ax2.plot(x,y)
plt.show()'''