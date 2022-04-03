import threading
import time
import random
from array import *

class upr_naredbe:

	def __init__(self) -> None:
		self.pin = 0
		self.pzn = 0
		self.psn = 0
		self.pjn = 0
		self.ain = [0, 0, 0]
		self.azn = [0, 0, 0]
		self.asn = [0, 0, 0]
		self.ajn = [0, 0, 0]

		# naredbe za semafor: 0 = crveno, 1 = zeleno


class sem_data:

	def __init__(self) -> None:
		self.pis = 0
		self.pzs = 0
		self.pss = 0
		self.pjs = 0
		self.ais = [0, 0, 0]
		self.azs = [0, 0, 0]
		self.ass = [0, 0, 0]
		self.ajs = [0, 0, 0]

		# stanje semafora: 0 = crveno, 1 = zeleno

class ras_data:

	def __init__(self) -> None:
		self.piCekaj = 0
		self.pzCekaj = 0
		self.psCekaj = 0
		self.pjCekaj = 0
		self.piKreni = 0
		self.pzKreni = 0
		self.psKreni = 0
		self.pjKreni = 0

		self.aiCekaj = [0, 0, 0]
		self.aiKreni = [0, 0, 0]
		self.azCekaj = [0, 0, 0]
		self.azKreni = [0, 0, 0]
		self.asCekaj = [0, 0, 0]
		self.asKreni = [0, 0, 0]
		self.ajCekaj = [0, 0, 0]
		self.ajKreni = [0, 0, 0]

		# podaci raskrizja: brojac trenutnih (aktivnih) pjesaka ili auta na pojednom dijelu







kljuc = threading.Lock()
printKljuc = threading.Lock()
uprNaredbe = upr_naredbe()
semData = sem_data()
rasData = ras_data()
R =[[' ', ' ', ' ', ' ', '|', ' ', ' ', 's', 's', ' ', ' ', '|', ' ', ' ', ' ', ' '],  # 0
	[' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' '],  # 1
	[' ', ' ', ' ', ' ', '|', '|', '|', '|', '|', '|', '|', '|', ' ', ' ', ' ', ' '],  # 2
	[' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' '],  # 3
	['-', '-', '-', '-', '+', ' ', ' ', ' ', ' ', ' ', ' ', '+', '-', '-', '-', '-'],  # 4
	[' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' '],  # 5
	[' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' '],  # 6
	['z', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', 'i'],  # 7
	['z', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', 'i'],  # 8
	[' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' '],  # 9
	[' ', ' ', '-', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-', ' ', ' '],  # 10
	['-', '-', '-', '-', '+', ' ', ' ', ' ', ' ', ' ', ' ', '+', '-', '-', '-', '-'],  # 11
	[' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' '],  # 12
	[' ', ' ', ' ', ' ', '|', '|', '|', '|', '|', '|', '|', '|', ' ', ' ', ' ', ' '],  # 13
	[' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' '],  # 14
	[' ', ' ', ' ', ' ', '|', ' ', ' ', 'j', 'j', ' ', ' ', '|', ' ', ' ', ' ', ' ']]  # 15
	# 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15


def upr() -> None:
	printKljuc.acquire()
	print("UPR dretva pokrenuta")
	printKljuc.release()
	while 1 == 1:
		# 1 faza - svima crveno
		kljuc.acquire()
		uprNaredbe.pin = 0
		uprNaredbe.pzn = 0
		uprNaredbe.psn = 0
		uprNaredbe.pjn = 0
		for i in range(3):
			uprNaredbe.ain[i] = 0
			uprNaredbe.azn[i] = 0
			uprNaredbe.asn[i] = 0
			uprNaredbe.ajn[i] = 0
		kljuc.release()
		time.sleep(3)

		# 2 faza - ZELENO - SJEVER JUG - ravno i desno
		kljuc.acquire()
		uprNaredbe.asn[1] = 1
		uprNaredbe.asn[2] = 1
		uprNaredbe.ajn[1] = 1
		uprNaredbe.ajn[2] = 1
		kljuc.release()
		time.sleep(10)
		kljuc.acquire()

		# pusti pjesake desno
		if rasData.pzCekaj >= rasData.asCekaj[2] and uprNaredbe.asn[1] == 1:
			uprNaredbe.asn[2] = 0
			kljuc.release()
			time.sleep(3)
			kljuc.acquire()
			uprNaredbe.pzn = 1
		if rasData.piCekaj >= rasData.ajCekaj[2] and uprNaredbe.ajn[1] == 1:
			uprNaredbe.ajn[2] = 0
			kljuc.release()
			time.sleep(3)
			kljuc.acquire()
			uprNaredbe.pin = 1

		kljuc.release()
		time.sleep(5)
		kljuc.acquire()
		uprNaredbe.pin = 0
		uprNaredbe.pzn = 0
		uprNaredbe.asn[1] = 0
		uprNaredbe.asn[2] = 0
		uprNaredbe.ajn[1] = 0
		uprNaredbe.ajn[2] = 0
		kljuc.release()
		time.sleep(4)

		# 3 faza - ZELENO - SJEVER JUG - lijevo
		kljuc.acquire()
		uprNaredbe.asn[0] = 1
		uprNaredbe.ajn[0] = 1
		kljuc.release()
		time.sleep(15)
		kljuc.acquire()
		uprNaredbe.asn[0] = 0
		uprNaredbe.ajn[0] = 0
		kljuc.release()
		time.sleep(3)

		# 4 faza - ZELENO - ISTOK ZAPAD - ravno i desno
		kljuc.acquire()
		uprNaredbe.ain[1] = 1
		uprNaredbe.ain[2] = 1
		uprNaredbe.azn[1] = 1
		uprNaredbe.azn[2] = 1
		kljuc.release()
		time.sleep(10)
		kljuc.acquire()

		# pusti pjesake desno
		if rasData.psCekaj >= rasData.aiCekaj[2] and uprNaredbe.ain[1] == 1:
			uprNaredbe.ain[2] = 0
			kljuc.release()
			time.sleep(3)
			kljuc.acquire()
			uprNaredbe.psn = 1
		if rasData.pjCekaj >= rasData.azCekaj[2] and uprNaredbe.azn[1] == 1:
			uprNaredbe.azn[2] = 0
			kljuc.release()
			time.sleep(3)
			kljuc.acquire()
			uprNaredbe.pjn = 1

		kljuc.release()
		time.sleep(5)
		kljuc.acquire()
		uprNaredbe.psn = 0
		uprNaredbe.pjn = 0
		uprNaredbe.ain[1] = 0
		uprNaredbe.ain[2] = 0
		uprNaredbe.azn[1] = 0
		uprNaredbe.azn[2] = 0
		kljuc.release()
		time.sleep(4)

		# 5 faza - ZELENO - ISTOK ZAPAD - lijevo
		kljuc.acquire()
		uprNaredbe.ain[0] = 1
		uprNaredbe.azn[0] = 1
		kljuc.release()
		time.sleep(15)
		kljuc.acquire()
		uprNaredbe.ain[0] = 0
		uprNaredbe.azn[0] = 0
		kljuc.release()
		time.sleep(3)

		# 6 faza - zeleno svim pjesacica
		kljuc.acquire()
		uprNaredbe.psn = 1
		uprNaredbe.pjn = 1
		uprNaredbe.pin = 1
		uprNaredbe.pzn = 1
		kljuc.release()
		time.sleep(5)
		kljuc.acquire()
		uprNaredbe.psn = 0
		uprNaredbe.pjn = 0
		uprNaredbe.pin = 0
		uprNaredbe.pzn = 0
		kljuc.release()
		time.sleep(5)

def sem() -> None:
	printKljuc.acquire()
	print("SEM dretva pokrenuta")
	printKljuc.release()
	while 1 == 1:
		kljuc.acquire()
		semData.pss = uprNaredbe.psn
		semData.pjs = uprNaredbe.pjn
		semData.pis = uprNaredbe.pin
		semData.pzs = uprNaredbe.pzn
		for i in range(3):
			semData.ass[i] = uprNaredbe.asn[i]
			semData.ajs[i] = uprNaredbe.ajn[i]
			semData.ais[i] = uprNaredbe.ain[i]
			semData.azs[i] = uprNaredbe.azn[i]
		kljuc.release()
		time.sleep(0.05)

def ras() -> None:
	printKljuc.acquire()
	print("RAS dretva pokrenuta")
	printKljuc.release()

	while 1 == 1:
		kljuc.acquire()

		# pjesaci ISTOK
		if(rasData.piCekaj == 0):
			R[3][13] = ' '
			R[12][13] = ' '
		if (rasData.piKreni == 0):
			R[5][13] = '-'
			R[6][13] = '-'
			R[7][13] = '-'
			R[8][13] = '-'
			R[9][13] = '-'
			R[10][13] = '-'
		if (rasData.piCekaj >= 1):
			R[3][13] = 'P'
			R[12][13] = 'P'
		if (rasData.piKreni >= 1):
			R[5][13] = 'P'
			R[6][13] = 'P'
			R[7][13] = 'P'
			R[8][13] = 'P'
			R[9][13] = 'P'
			R[10][13] = 'P'

		# pjesaci ZAPAD
		if (rasData.pzCekaj == 0):
			R[3][2] = ' '
			R[12][2] = ' '
		if (rasData.pzKreni == 0):
			R[5][2] = '-'
			R[6][2] = '-'
			R[7][2] = '-'
			R[8][2] = '-'
			R[9][2] = '-'
			R[10][2] = '-'
		if (rasData.pzCekaj >= 1):
			R[3][2] = 'P'
			R[12][2] = 'P'
		if (rasData.pzKreni >= 1):
			R[5][2] = 'P'
			R[6][2] = 'P'
			R[7][2] = 'P'
			R[8][2] = 'P'
			R[9][2] = 'P'
			R[10][2] = 'P'

		# pjesaci SJEVER
		if (rasData.psCekaj == 0):
			R[2][3] = ' '
			R[2][12] = ' '
		if(rasData.psKreni == 0):
			R[2][5] = '|'
			R[2][6] = '|'
			R[2][7] = '|'
			R[2][8] = '|'
			R[2][9] = '|'
			R[2][10] = '|'
		if (rasData.psCekaj >= 1):
			R[2][3] = 'P'
			R[2][12] = 'P'
		if(rasData.psKreni >= 1):
			R[2][5] = 'P'
			R[2][6] = 'P'
			R[2][7] = 'P'
			R[2][8] = 'P'
			R[2][9] = 'P'
			R[2][10] = 'P'

		# pjesaci JUG
		if (rasData.pjCekaj == 0):
			R[13][3] = ' '
			R[13][12] = ' '
		if(rasData.pjKreni == 0):
			R[13][5] = '|'
			R[13][6] = '|'
			R[13][7] = '|'
			R[13][8] = '|'
			R[13][9] = '|'
			R[13][10] = '|'
		if (rasData.pjCekaj >= 1):
			R[13][3] = 'P'
			R[13][12] = 'P'
		if(rasData.pjKreni >= 1):
			R[13][5] = 'P'
			R[13][6] = 'P'
			R[13][7] = 'P'
			R[13][8] = 'P'
			R[13][9] = 'P'
			R[13][10] = 'P'

		# cisti SVE AUTE
		if (rasData.aiKreni[0] == 0):
			R[7][11] = ' '
			R[7][10] = ' '
			R[8][9] = ' '
			R[9][8] = ' '
			R[10][7] = ' '
			R[11][7] = ' '
		if (rasData.aiKreni[1] == 0):
			R[6][11] = ' '
			R[6][10] = ' '
			R[6][9] = ' '
			R[6][8] = ' '
			R[6][7] = ' '
			R[6][5] = ' '
			R[6][4] = ' '
		if (rasData.aiKreni[2] == 0):
			R[5][11] = ' '
			R[5][10] = ' '
			R[4][10] = ' '
		if (rasData.azKreni[0] == 0):
			R[8][4] = ' '
			R[8][5] = ' '
			R[7][6] = ' '
			R[6][7] = ' '
			R[5][8] = ' '
			R[4][8] = ' '
		if (rasData.azKreni[1] == 0):
			R[9][11] = ' '
			R[9][10] = ' '
			R[9][9] = ' '
			R[9][8] = ' '
			R[9][7] = ' '
			R[9][5] = ' '
			R[9][4] = ' '
		if (rasData.azKreni[2] == 0):
			R[10][4] = ' '
			R[10][5] = ' '
			R[11][5] = ' '
		if (rasData.asKreni[0] == 0):
			R[4][7] = ' '
			R[5][7] = ' '
			R[6][8] = ' '
			R[7][9] = ' '
			R[8][10] = ' '
			R[8][11] = ' '
		if (rasData.asKreni[1] == 0):
			R[4][6] = ' '
			R[5][6] = ' '
			R[6][6] = ' '
			R[7][6] = ' '
			R[8][6] = ' '
			R[9][6] = ' '
			R[10][6] = ' '
		if (rasData.asKreni[2] == 0):
			R[4][5] = ' '
			R[5][5] = ' '
			R[5][4] = ' '
		if (rasData.ajKreni[0] == 0):
			R[11][8] = ' '
			R[10][8] = ' '
			R[9][7] = ' '
			R[8][6] = ' '
			R[7][5] = ' '
			R[7][4] = ' '
		if (rasData.ajKreni[1] == 0):
			R[11][9] = ' '
			R[10][9] = ' '
			R[9][9] = ' '
			R[8][9] = ' '
			R[7][9] = ' '
			R[6][9] = ' '
			R[5][9] = ' '
		if (rasData.ajKreni[2] == 0):
			R[11][10] = ' '
			R[10][10] = ' '
			R[10][11] = ' '


		# auti ISTOK
		if (rasData.aiCekaj[0] == 0):
			R[7][14] = ' '
		if (rasData.aiCekaj[0] >= 1):
			R[7][14] = 'A'
		if (rasData.aiCekaj[1] == 0):
			R[6][14] = ' '
		if (rasData.aiCekaj[1] >= 1):
			R[6][14] = 'A'
		if (rasData.aiCekaj[2] == 0):
			R[5][14] = ' '
		if (rasData.aiCekaj[2] >= 1):
			R[5][14] = 'A'
		# L
		if (rasData.aiKreni[0] >= 1):
			R[7][11] = 'A'
			R[7][10] = 'A'
			R[8][9] = 'A'
			R[9][8] = 'A'
			R[10][7] = 'A'
			R[11][7] = 'A'
		# R
		if (rasData.aiKreni[1] >= 1):
			R[6][11] = 'A'
			R[6][10] = 'A'
			R[6][9] = 'A'
			R[6][8] = 'A'
			R[6][7] = 'A'
			R[6][6] = 'A'
			R[6][5] = 'A'
		# D
		if (rasData.aiKreni[2] >= 1):
			R[5][11] = 'A'
			R[5][10] = 'A'
			R[4][10] = 'A'


		# auti ZAPAD
		if (rasData.azCekaj[0] == 0):
			R[8][1] = ' '
		if (rasData.azCekaj[0] >= 1):
			R[8][1] = 'A'
		if (rasData.azCekaj[1] == 0):
			R[9][1] = ' '
		if (rasData.azCekaj[1] >= 1):
			R[9][1] = 'A'
		if (rasData.azCekaj[2] == 0):
			R[10][1] = ' '
		if (rasData.azCekaj[2] >= 1):
			R[10][1] = 'A'
		# L
		if (rasData.azKreni[0] >= 1):
			R[8][4] = 'A'
			R[8][5] = 'A'
			R[7][6] = 'A'
			R[6][7] = 'A'
			R[5][8] = 'A'
			R[4][8] = 'A'
		# R
		if (rasData.azKreni[1] >= 1):
			R[9][10] = 'A'
			R[9][9] = 'A'
			R[9][8] = 'A'
			R[9][7] = 'A'
			R[9][6] = 'A'
			R[9][5] = 'A'
			R[9][4] = 'A'
		# D
		if (rasData.azKreni[2] >= 1):
			R[10][4] = 'A'
			R[10][5] = 'A'
			R[11][5] = 'A'


		# auti SJEVER
		if (rasData.asCekaj[0] == 0):
			R[1][7] = ' '
		if (rasData.asCekaj[0] >= 1):
			R[1][7] = 'A'
		if (rasData.asCekaj[1] == 0):
			R[1][6] = ' '
		if (rasData.asCekaj[1] >= 1):
			R[1][6] = 'A'
		if (rasData.asCekaj[2] == 0):
			R[1][5] = ' '
		if (rasData.asCekaj[2] >= 1):
			R[1][5] = 'A'
		# L
		if (rasData.asKreni[0] >= 1):
			R[4][7] = 'A'
			R[5][7] = 'A'
			R[6][8] = 'A'
			R[7][9] = 'A'
			R[8][10] = 'A'
			R[8][11] = 'A'
		# R
		if (rasData.asKreni[1] >= 1):
			R[4][6] = 'A'
			R[5][6] = 'A'
			R[6][6] = 'A'
			R[7][6] = 'A'
			R[8][6] = 'A'
			R[9][6] = 'A'
			R[10][6] = 'A'
		# D
		if (rasData.asKreni[2] >= 1):
			R[4][5] = 'A'
			R[5][5] = 'A'
			R[5][4] = 'A'


		# auti JUG
		if (rasData.ajCekaj[0] == 0):
			R[14][8] = ' '
		if (rasData.ajCekaj[0] >= 1):
			R[14][8] = 'A'
		if (rasData.ajCekaj[1] == 0):
			R[14][9] = ' '
		if (rasData.ajCekaj[1] >= 1):
			R[14][9] = 'A'
		if (rasData.ajCekaj[2] == 0):
			R[14][10] = ' '
		if (rasData.ajCekaj[2] >= 1):
			R[14][10] = 'A'
		# L
		if (rasData.ajKreni[0] >= 1):
			R[11][8] = 'A'
			R[10][8] = 'A'
			R[9][7] = 'A'
			R[8][6] = 'A'
			R[7][5] = 'A'
			R[7][4] = 'A'
		# R
		if (rasData.ajKreni[1] >= 1):
			R[11][9] = 'A'
			R[10][9] = 'A'
			R[9][9] = 'A'
			R[8][9] = 'A'
			R[7][9] = 'A'
			R[6][9] = 'A'
			R[5][9] = 'A'
		# D
		if (rasData.ajKreni[2] >= 1):
			R[11][10] = 'A'
			R[10][10] = 'A'
			R[10][11] = 'A'

		kljuc.release()

		# print raskrizje
		printKljuc.acquire()
		printR()
		printKljuc.release()
		time.sleep(0.5)

def auto() -> None:
	lokacija = random.randint(0, 11)
	skretanje = lokacija % 3

	# JUG
	if lokacija >= 0 and lokacija <= 2:
		# DODI NA SEM
		kljuc.acquire()
		rasData.ajCekaj[skretanje] += 1
		kljuc.release()

		# CEKAJ SEM I PROMET ISPRED SEBE
		kljuc.acquire()
		cekaj = semData.ajs[skretanje] == 0 or rasData.ajKreni[skretanje] >= 3
		kljuc.release()
		while cekaj == 1:
			kljuc.acquire()
			cekaj = semData.ajs[skretanje] == 0 or rasData.ajKreni[skretanje] >= 3
			kljuc.release()
			time.sleep(1)

		# UDI U RASKRIZJE
		kljuc.acquire()
		rasData.ajCekaj[skretanje] -= 1
		rasData.ajKreni[skretanje] += 1
		kljuc.release()

		# BUDI U RASKRIZJU
		time.sleep(2)

		# IZADI IZ RASKRIZJA
		kljuc.acquire()
		rasData.ajKreni[skretanje] -= 1
		kljuc.release()

	# SJEVER
	if lokacija >= 3 and lokacija <= 5:
		# DODI NA SEM
		kljuc.acquire()
		rasData.asCekaj[skretanje] += 1
		kljuc.release()

		# CEKAJ SEM I PROMET ISPRED SEBE
		kljuc.acquire()
		cekaj = semData.ass[skretanje] == 0 or rasData.asKreni[skretanje] >= 3
		kljuc.release()
		while cekaj == 1:
			kljuc.acquire()
			cekaj = semData.ass[skretanje] == 0 or rasData.asKreni[skretanje] >= 3
			kljuc.release()
			time.sleep(1)

		# UDI U RASKRIZJE
		kljuc.acquire()
		rasData.asCekaj[skretanje] -= 1
		rasData.asKreni[skretanje] += 1
		kljuc.release()

		# BUDI U RASKRIZJU
		time.sleep(3)

		# IZADI IZ RASKRIZJA
		kljuc.acquire()
		rasData.asKreni[skretanje] -= 1
		kljuc.release()

	# ISTOK
	if lokacija >= 6 and lokacija <= 8:
		# DODI NA SEM
		kljuc.acquire()
		rasData.aiCekaj[skretanje] += 1
		kljuc.release()

		# CEKAJ SEM I PROMET ISPRED SEBE
		kljuc.acquire()
		cekaj = semData.ais[skretanje] == 0 or rasData.aiKreni[skretanje] >= 3
		kljuc.release()
		while cekaj == 1:
			kljuc.acquire()
			cekaj = semData.ais[skretanje] == 0 or rasData.aiKreni[skretanje] >= 3
			kljuc.release()
			time.sleep(1)

		# UDI U RASKRIZJE
		kljuc.acquire()
		rasData.aiCekaj[skretanje] -= 1
		rasData.aiKreni[skretanje] += 1
		kljuc.release()

		# BUDI U RASKRIZJU
		time.sleep(3)

		# IZADI IZ RASKRIZJA
		kljuc.acquire()
		rasData.aiKreni[skretanje] -= 1
		kljuc.release()



	# ZAPAD
	if lokacija >= 9 and lokacija <= 11:
		# DODI NA SEM
		kljuc.acquire()
		rasData.azCekaj[skretanje] += 1
		kljuc.release()

		# CEKAJ SEM I PROMET ISPRED SEBE
		kljuc.acquire()
		cekaj = semData.azs[skretanje] == 0 or rasData.azKreni[skretanje] >= 3
		kljuc.release()
		while cekaj == 1:
			kljuc.acquire()
			cekaj = semData.azs[skretanje] == 0 or rasData.azKreni[skretanje] >= 3
			kljuc.release()
			time.sleep(1)

		# UDI U RASKRIZJE
		kljuc.acquire()
		rasData.azCekaj[skretanje] -= 1
		rasData.azKreni[skretanje] += 1
		kljuc.release()

		# BUDI U RASKRIZJU
		time.sleep(3)

		# IZADI IZ RASKRIZJA
		kljuc.acquire()
		rasData.azKreni[skretanje] -= 1
		kljuc.release()

	return None

def pjesak() -> None:
	lokacija = random.randint(1, 4)

	# ISTOK
	if lokacija == 1:
		# DODI NA SEMAFOR
		kljuc.acquire()
		rasData.piCekaj += 1
		kljuc.release()

		# CEKAJ SEMAFOR
		while semData.pis == 0:
			time.sleep(1)

		# PRELAZI CESTU
		kljuc.acquire()
		rasData.piCekaj -= 1
		rasData.piKreni += 1
		kljuc.release()

		# NA CESTI
		time.sleep(4)

		# MAKNI SE SA CESTE
		kljuc.acquire()
		rasData.piKreni -= 1
		kljuc.release()


	# SJEVER
	if lokacija == 2:
		kljuc.acquire()
		rasData.psCekaj += 1
		kljuc.release()

		# CEKAJ SEMAFOR
		while semData.pss == 0:
			time.sleep(1)

		# PRELAZI CESTU
		kljuc.acquire()
		rasData.psCekaj -= 1
		rasData.psKreni += 1
		kljuc.release()

		# NA CESTI
		time.sleep(4)

		# MAKNI SE SA CESTE
		kljuc.acquire()
		rasData.psKreni -= 1
		kljuc.release()

	# ZAPAD
	if lokacija == 3:
		kljuc.acquire()
		rasData.pzCekaj += 1
		kljuc.release()

		# CEKAJ SEMAFOR
		while semData.pis == 0:
			time.sleep(1)

		# PRELAZI CESTU
		kljuc.acquire()
		rasData.pzCekaj -= 1
		rasData.pzKreni += 1
		kljuc.release()

		# NA CESTI
		time.sleep(4)

		# MAKNI SE SA CESTE
		kljuc.acquire()
		rasData.pzKreni -= 1
		kljuc.release()

	# JUG
	if lokacija == 4:
		kljuc.acquire()
		rasData.pjCekaj += 1
		kljuc.release()

		# CEKAJ SEMAFOR
		while semData.pis == 0:
			time.sleep(1)

		# PRELAZI CESTU
		kljuc.acquire()
		rasData.pjCekaj -= 1
		rasData.pjKreni += 1
		kljuc.release()

		# NA CESTI
		time.sleep(4)

		# MAKNI SE SA CESTE
		kljuc.acquire()
		rasData.pjKreni -= 1
		kljuc.release()

	return None

def printR() -> None:
	for i in range(16):
		for j in range(16):
			print(R[i][j], " ", end="")
		print()
	print("==================================================")
	return None


def main():
	uprDretva = threading.Thread(target=upr, args=())
	semDretva = threading.Thread(target=sem, args=())
	rasDretva = threading.Thread(target=ras, args=())
	uprDretva.start()
	semDretva.start()
	rasDretva.start()


	while 1 == 1:
		threading.Thread(target=auto, args=()).start()
		threading.Thread(target=pjesak, args=()).start()
		time.sleep(0.2)


if __name__ == '__main__':
	main()

