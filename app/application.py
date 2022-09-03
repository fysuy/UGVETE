from tkinter import *
import os
#from turtle import forward, right
import configparser
from functools import partial
import simulation as sim


simulation = sim.Simulacion('default.ini')   
algoritm = simulation.algoritm
episodes = simulation.episodes
timesteps = simulation.timesteps
movements = simulation.movements
foward = movements["Foward"]
left = movements["Left"]
right = movements["Right"]
turnleft = movements["TurnLeft"]
turnright = movements["TurnRight"]
stop = movements["Stop"]
   
window = Tk()
window.title("Configuracion de ambiente")
window.geometry('1024x720')
#window.configure(background = "grey")

a = Label(window ,text = "Algortimo:").grid(row = 1,column = 0,pady=10)
radioValue = IntVar()
if algoritm == '1':
   #print('Qlearning')
   radioValue.set(1)  
elif algoritm == '2': 
   #print('Sarsa')
   radioValue.set(2)  
rdioOne = Radiobutton(window, text='Qlearning',
                             variable=radioValue, value=1) 
rdioTwo = Radiobutton(window, text='Sarsa',
                             variable=radioValue, value=2) 

rdioOne.grid(column=1, row=1)
rdioTwo.grid(column=2, row=1)

b = Label(window ,text = "Cantidad de episodios:").grid(row = 3,column = 0)
vb1 = IntVar(window, value=episodes)
b1 = Entry(window,textvariable=vb1).grid(row = 3,column = 1)

c = Label(window ,text = "Cantidad de timesteps por episodio:").grid(row = 4,column = 0)
vc1 = IntVar(window, value=timesteps)
c1 = Entry(window,textvariable=vc1).grid(row = 4,column = 1)

movs = Label(window ,text = "Movimientos",font= ('Arial 12 bold')).grid(row = 5,column = 0,pady = 10)
vel = Label(window ,text = "Velocidad lineal",font= ('Arial 12 bold')).grid(row = 5,column = 1)
velAng = Label(window ,text = "Velocidad angular",font= ('Arial 12 bold')).grid(row = 5,column = 2)
rew = Label(window ,text = "Recompensa",font= ('Arial 12 bold')).grid(row = 5,column = 3)
Habi = Label(window ,text = "Habilitada",font= ('Arial 12 bold')).grid(row = 5,column = 4)

ade = Label(window ,text = "Adelante").grid(row = 6,column = 0)
vade1 = StringVar(window, value = foward.vel_linear)
#vade2 = StringVar(window, value = foward.vel_angular)
vade2 = StringVar(window)
vade2.set(foward.vel_angular)
vade3 = StringVar(window, value = foward.reward)
ade1 = Entry(window,textvariable = vade1).grid(row = 6,column = 1)
ade2 = Entry(window,textvariable = vade2).grid(row = 6,column = 2)
ade3 = Entry(window,textvariable = vade3).grid(row = 6,column = 3)

izq = Label(window ,text = "Izquierda").grid(row = 7,column = 0)
vizq1 = StringVar(window, value = left.vel_linear)
vizq2 = StringVar(window, value = left.vel_angular)
vizq3 = StringVar(window, value = left.reward)
izq1 = Entry(window,textvariable = vizq1).grid(row = 7,column = 1)
izq2 = Entry(window,textvariable = vizq2).grid(row = 7,column = 2)
izq3 = Entry(window,textvariable = vizq3).grid(row = 7,column = 3)

der = Label(window ,text = "Derecha").grid(row = 8,column = 0)
vder1 = StringVar(window, value = right.vel_linear)
vder2 = StringVar(window, value = right.vel_angular)
vder3 = StringVar(window, value = right.reward)
der1 = Entry(window,textvariable = vder1).grid(row = 8,column = 1)
der2 = Entry(window,textvariable = vder2).grid(row = 8,column = 2)
der3 = Entry(window,textvariable = vder3).grid(row = 8,column = 3)

gizq = Label(window ,text = "Giro izquierda").grid(row = 9,column = 0)
#vgizq1 = StringVar(window, value = turnleft.vel_linear)
vgizq2 = StringVar(window, value = turnleft.vel_angular)
vgizq3 = StringVar(window, value = turnleft.reward)
#gizq1 = Entry(window,textvariable = vgizq1).grid(row = 9,column = 1)
gizq2 = Entry(window,textvariable = vgizq2).grid(row = 9,column = 2)
gizq3 = Entry(window,textvariable = vgizq3).grid(row = 9,column = 3)

gder = Label(window ,text = "Giro derecha").grid(row = 10,column = 0)
#vgder1 = StringVar(window, value = turnright.vel_linear)
vgder2 = StringVar(window, value = turnright.vel_angular)
vgder3 = StringVar(window, value = turnright.reward)
#gder1 = Entry(window,textvariable = vgder1).grid(row = 10,column = 1)
gder2 = Entry(window,textvariable = vgder2).grid(row = 10,column = 2)
gder3 = Entry(window,textvariable = vgder3).grid(row = 10,column = 3)


par = Label(window ,text = "Frenar").grid(row = 11,column = 0)
#par1 = Entry(window).grid(row = 11,column = 1)
#par2 = Entry(window).grid(row = 11,column = 2)
vsto3 = StringVar(window, value = stop.reward)
sto3 = Entry(window,textvariable = vsto3).grid(row = 11,column = 3)


chkValue = BooleanVar() 
if foward.enabled == '1':
   chkValue.set(True)
else:
   chkValue.set(False)

chkValue1 = BooleanVar() 
if left.enabled == '1':
   chkValue1.set(True)
else:
   chkValue1.set(False)

chkValue2 = BooleanVar() 
if right.enabled == '1':
   chkValue2.set(True)
else:
   chkValue2.set(False)

chkValue3 = BooleanVar() 
if turnleft.enabled == '1':
   chkValue3.set(True)
else:
   chkValue3.set(False)

chkValue4 = BooleanVar() 
if turnright.enabled == '1':
   chkValue4.set(True)
else:
   chkValue4.set(False)

chkValue5 = BooleanVar() 
if stop.enabled == '1':
   chkValue5.set(True)
else:
   chkValue5.set(False)

adeCheck = Checkbutton(window,var=chkValue) 
adeCheck.grid(row = 6,column = 4)
izqCheck = Checkbutton(window, var=chkValue1) 
izqCheck.grid(row = 7,column = 4)
derCheck = Checkbutton(window, var=chkValue2) 
derCheck.grid(row = 8,column = 4)
gizqCheck = Checkbutton(window, var=chkValue3) 
gizqCheck.grid(row = 9,column = 4)
gderCheck = Checkbutton(window, var=chkValue4) 
gderCheck.grid(row = 10,column = 4)
parCheck = Checkbutton(window, var=chkValue5) 
parCheck.grid(row = 11,column = 4)

execution = False

def simulate():
   #Set values:
   algoritm = radioValue.get()
   episodes = vb1.get()
   timesteps = vc1.get()
   #s_foward = Movement("Foward",vade1.get(),vade2.get(),vade3.get(),chkValue.get())
   foward.vel_linear = vade1.get()
   foward.vel_angular = vade2.get()
   foward.reward = vade3.get()
   foward.enabled = chkValue.get()

   left.vel_linear = vizq1.get()
   left.vel_angular = vizq2.get()
   left.reward = vizq3.get()
   left.enabled = chkValue1.get()

   right.vel_linear = vder1.get()
   right.vel_angular = vder2.get()
   right.reward = vder3.get()
   right.enabled = chkValue2.get()

   turnleft.vel_linear = vgizq2.get()
   turnleft.reward = vgizq3.get()
   turnleft.enabled = chkValue3.get()

   turnright.vel_linear = vgder2.get()
   turnright.reward = vgder3.get()
   turnright.enabled = chkValue4.get()

   stop.reward = vsto3.get()
   stop.enabled = chkValue5.get()
   sim.save_simulation(algoritm,episodes,timesteps,foward,left,right,turnleft,turnright,stop)

   if (algoritm == 1):
      #/home/felipe/gym-gazebo/examples/turtlebot
      print("Qlearn")
      os.system("python $HOME/Libs/UGVETE/turtlebot/circuit2_turtlebot_lidar_qlearn.py")
   elif(algoritm== 2):
      print("Sarsa")
      os.system("python $HOME/Libs/UGVETE/turtlebot/circuit2_turtlebot_lidar_sarsa.py")
   print("simular")
   execution = True

def gzclient():
   #if execution == True:
   print('terminal')
   os.system('gnome-terminal --tab -e gzclient')
   print('new terminal')

btn = Button(window ,text="Simular",command = simulate).grid(row=20,column=0,pady=30)
#btn2 = Button(window ,text="Ver simulacion",command = gzclient).grid(row=20,column=1,pady=30)


window.mainloop()
