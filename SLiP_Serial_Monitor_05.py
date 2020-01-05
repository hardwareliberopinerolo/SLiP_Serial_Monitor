#!/usr/bin/env python3

import sys
import serial
import time

from PyQt5 import QtCore, uic, QtWidgets

from pathlib import Path
p = Path(__file__).resolve().parent
print(p)
 
qtCreatorFile = str(p) + "/Arduino_Serial_Monitor_01.ui" # Enter file here
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#---Form Principale----------------------------------------------------

class Principale(QtWidgets.QMainWindow, Ui_MainWindow):

	
	
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		
		#Posizione e dimensione della finestra.
		self.setMinimumSize(600,600)
		self.setMaximumSize(1800,1200)
		self.setGeometry(200, 200, 800, 600)#pos & dim 

		
		#definizione segnali interfaccia

		self.B_quit.clicked.connect(fine_sessione)
		self.B_con.clicked.connect(Connessione_on)
		self.B_nocon.clicked.connect(Connessione_off)
		self.B_Send.clicked.connect(Inv_text)
		
		self.LW_Texts.itemClicked.connect(Inv_LW_text)
		
		#Timer per lettura da seriale
		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(Legge_Seriale)
		self.timer.start(100) #Verificare il tempo di timer 
		
		
		USB_items = ("/dev/ttyUSB0","/dev/ttyUSB1","/dev/ttyACM0","/dev/ttyACM1")
		self.CB_USB.addItems(USB_items)
		Vel_items= ("9600", "57600", "115200")
		self.CB_Vel.addItems(Vel_items)

#---Legge da Arduino-----------------------------------------
def Legge_Seriale():
	#da completare
	global con_status

	
	if con_status == 1:
		#print("Echo on")
		app.processEvents()
		if conn.inWaiting() > 1:
			ret = conn.readline().decode().strip( "\r\n" )
			#print(ret)
			if len(ret) > 1:
				#ret_ascii = ret.encode('ascii',errors='ignore')
				#window_a.ui.T_ser.append(ret_ascii)
				#app.processEvents()
				window_a.T_ser.append(ret)


#---Attiva Connessione---------------------------------------
def Connessione_on():
	# Apre connesione seriale con Arduino
	global conn
	global con_status
	

	A_ser_port=window_a.CB_USB.currentText()
	#print(A_ser_port)
	A_ser_vel=window_a.CB_Vel.currentText()
	#print(A_ser_vel)
	try:
		#A_ser_port="/dev/ttyUSB0"
		#A_ser_vel="9600"
		#conn=serial.Serial(str(A_ser_port), A_ser_vel,timeout=0.1, rtscts=False)
		conn=serial.Serial(A_ser_port, A_ser_vel,timeout=0.1, rtscts=False)
		window_a.T_note.setText("Connessione con Arduino avvenuta")
		con_status=1
		window_a.B_con.hide()
		window_a.B_nocon.show()
		
	except serial.serialutil.SerialException:
		window_a.T_note.setText("Controllare la connessione con Arduino")
		con_status=0
	time.sleep(2)

#---Chiude connessione---------------------------------------
def Connessione_off():
	global con_status
	#print con_status
	if con_status == 1:
		conn.close()
		con_status=0
		window_a.T_note.setText("Connessione Off")
		window_a.B_con.show()
		window_a.B_nocon.hide()

	
#---Fine lavoro, chiude tutto------------------------------------------
def fine_sessione():
	if con_status == 1:
		conn.close()
	quit()
	

		
#---Invia Text------------------------------------------
def Inv_text():
	sCmd=window_a.TE_command.toPlainText()
	#window_a.T_note.setText(sCmd)
	window_a.LW_Texts.addItem(sCmd)
	
	if con_status == 1:
		#conn.write( str(sCmd) + "\r\n")
		conn.write( (sCmd + "\r\n").encode() )

#---Invia Text------------------------------------------
def Inv_LW_text(item):
	#sCmd=window_a.LW_Texts.at(item.text())
	sCmd=item.text()
	#print(sCmd)
	
	if con_status == 1:
		#conn.write( str(sCmd) + "\r\n")
		conn.write( (sCmd + "\r\n").encode() )


#---Funzione principale------------------------------------------------
if __name__ == '__main__':
	global con_status
	con_status=0
	app = QtWidgets.QApplication(sys.argv)
	window_a = Principale()
	window_a.show()
	window_a.B_nocon.hide()
	sys.exit(app.exec_())
