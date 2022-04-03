import threading
import time
import random


class upr_naredbe:
     def __init__(self) -> None:
          self.liftSmjer1 = 0
          self.liftSmjer2 = 0
          self.liftKreni1 = 0
          self.liftKreni2 = 0
          self.liftKatovi1 = [0, 0, 0, 0]
          self.liftKatovi2 = [0, 0, 0, 0]

     # naredbe za liftove: smjer = {-1 = D, 0 = N, 1 = U}, kreni = {0, 1}, katovi - na kojem katu lift staje


class stanje_liftova:
     def __init__(self) -> None:
          self.brPutnikaKat = [0, 0, 0, 0]
          self.zeljeniKatSa = [[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]]

          self.liftLokacija1 = 0
          self.liftLokacija2 = 0
          self.liftPutnici1 = 0
          self.liftPutnici2 = 0

          self.liftZauzet1 = 0
          self.liftZauzet2 = 0

          self.liftVrata1 = 0
          self.liftVrata2 = 0
          self.liftSmjer1 = 0
          self.liftSmjer2 = 0

     # naredbe za liftove: smjer = {-1 = D, 0 = N, 1 = U}, kreni = {0, 1}, katovi - na kojem katu lift staje


S = [[' ', 'K', 'a', 't', ' ', '|', ' ', 'L', ' ', '0', ' ', '|', 'L', ' ', '0', '|'],  # 0
     ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '='],  # 1
     ['3', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],  # 2
     ['=', '=', '=', '=', '=', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],  # 3
     ['2', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],  # 4
     ['=', '=', '=', '=', '=', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],  # 5
     ['1', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],  # 6
     ['=', '=', '=', '=', '=', '|', ' ', ' ', ' ', ' ', ' ', '|', ' ', ' ', ' ', '|'],  # 7
     ['0', ' ', ' ', ' ', ' ', '|', '[', ' ', '0', ' ', ']', '|', '[', '0', ']', '|'],  # 8
     ['=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=']]  # 9
     # 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15




kljuc = threading.Lock()
printKljuc = threading.Lock()
uprNaredbe = upr_naredbe()
stanje = stanje_liftova()


def prikazStanja() -> None:
     while 1 == 1:
          kljuc.acquire()
          kat0 = [int(a) for a in str(stanje.brPutnikaKat[0])]
          kat1 = [int(a) for a in str(stanje.brPutnikaKat[1])]
          kat2 = [int(a) for a in str(stanje.brPutnikaKat[2])]
          kat3 = [int(a) for a in str(stanje.brPutnikaKat[3])]

          S[8][2] = ' '
          S[8][3] = ' '
          S[6][2] = ' '
          S[6][3] = ' '
          S[4][2] = ' '
          S[4][3] = ' '
          S[2][2] = ' '
          S[2][3] = ' '

          if stanje.brPutnikaKat[0] == 0:
               S[8][2] = ' '
               S[8][3] = ' '
          elif stanje.brPutnikaKat[0] <= 9:
               S[8][2] = ' '
               S[8][3] = stanje.brPutnikaKat[0]
          else:
               S[8][2] = kat0[0]
               S[8][3] = kat0[1]

          if stanje.brPutnikaKat[1] == 0:
               S[6][2] = ' '
               S[6][3] = ' '
          elif stanje.brPutnikaKat[1] <= 9:
               S[6][2] = ' '
               S[6][3] = stanje.brPutnikaKat[1]
          else:
               S[6][2] = kat1[0]
               S[6][3] = kat1[1]

          if stanje.brPutnikaKat[2] == 0:
               S[4][2] = ' '
               S[4][3] = ' '
          elif stanje.brPutnikaKat[2] <= 9:
               S[4][2] = ' '
               S[4][3] = stanje.brPutnikaKat[2]
          else:
               S[4][2] = kat2[0]
               S[4][3] = kat2[1]

          if stanje.brPutnikaKat[3] == 0:
               S[2][2] = ' '
               S[2][3] = ' '
          elif stanje.brPutnikaKat[3] <= 9:
               S[2][2] = ' '
               S[2][3] = stanje.brPutnikaKat[3]
          else:
               S[2][2] = kat3[0]
               S[2][3] = kat3[1]

          for i in range(2, 9, 1):
               S[i][6] = ' '
               S[i][8] = ' '
               S[i][10] = ' '
               S[i][12] = ' '
               S[i][13] = ' '
               S[i][14] = ' '

          S[8-stanje.liftLokacija1][6] = '['
          S[8-stanje.liftLokacija1][8] = stanje.liftPutnici1
          S[8-stanje.liftLokacija1][10] = ']'

          S[8 - stanje.liftLokacija2][12] = '['
          S[8 - stanje.liftLokacija2][13] = stanje.liftPutnici2
          S[8 - stanje.liftLokacija2][14] = ']'


          if stanje.liftSmjer1 == -1:
               S[0][9] = 'D'
          if stanje.liftSmjer1 == 0:
               S[0][9] = '-'
          if stanje.liftSmjer1 == 1:
               S[0][9] = 'G'

          if stanje.liftSmjer2 == -1:
               S[0][14] = 'D'
          if stanje.liftSmjer2 == 0:
               S[0][14] = '-'
          if stanje.liftSmjer2 == 1:
               S[0][14] = 'G'

          kljuc.release()

          printKljuc.acquire()
          printS()
          printKljuc.release()
          time.sleep(0.5)

def lift1() -> None:
     while 1 == 1:
          kljuc.acquire()
          if uprNaredbe.liftKreni1 == 0:
               kljuc.release()
               time.sleep(2)
               kljuc.acquire()

          if uprNaredbe.liftKreni1 == 1:
               stanje.liftZauzet1 = 1
               pocetniKat = 0
               zavrsniKat = 0

               if uprNaredbe.liftSmjer1 == 1:
                    for i in range(4):
                         if uprNaredbe.liftKatovi1[i] == 1:
                              pocetniKat = i
                              break
                    for i in range(3, pocetniKat, -1):
                         if uprNaredbe.liftKatovi1[i] == 1:
                              zavrsniKat = i
                              break
                    kljuc.release()
                    time.sleep(2.5)
                    kljuc.acquire()
                    stanje.liftLokacija1 = pocetniKat*2
                    stanje.liftSmjer1 = 1
                    stanje.liftVrata1 = 1
                    kljuc.release()
                    time.sleep(5)
                    kljuc.acquire()
                    stanje.liftVrata1 = 0
                    uprNaredbe.liftKatovi1[pocetniKat] = 0

                    while 1 == 1:
                         stanje.liftVrata1 = 0
                         stanje.liftLokacija1 += 1
                         kljuc.release()
                         time.sleep(5)
                         kljuc.acquire()
                         stanje.liftLokacija1 += 1

                         if uprNaredbe.liftKatovi1[int(stanje.liftLokacija1/2)] == 1:
                              stanje.liftVrata1 = 1
                              kljuc.release()
                              time.sleep(5)
                              kljuc.acquire()
                              stanje.liftVrata1 = 0
                              uprNaredbe.liftKatovi1[int(stanje.liftLokacija1/2)] = 0
                         if int(stanje.liftLokacija1/2) == zavrsniKat:
                              uprNaredbe.liftKreni1 = 0
                              uprNaredbe.liftSmjer1 = 0
                              stanje.liftSmjer1 = 0
                              stanje.liftZauzet1 = 0
                              break

               if uprNaredbe.liftSmjer1 == -1:
                    for i in range(3, -1, -1):
                         if uprNaredbe.liftKatovi1[i] == 1:
                              pocetniKat = i
                              break
                    for i in range(0, pocetniKat, 1):
                         if uprNaredbe.liftKatovi1[i] == 1:
                              zavrsniKat = i
                              break
                    kljuc.release()
                    time.sleep(2.5)
                    kljuc.acquire()
                    stanje.liftLokacija1 = pocetniKat * 2
                    stanje.liftSmjer1 = -1
                    stanje.liftVrata1 = 1
                    kljuc.release()
                    time.sleep(5)
                    kljuc.acquire()
                    stanje.liftVrata1 = 0
                    uprNaredbe.liftKatovi1[pocetniKat] = 0

                    while 1 == 1:
                         stanje.liftVrata1 = 0
                         stanje.liftLokacija1 -= 1
                         kljuc.release()
                         time.sleep(5)
                         kljuc.acquire()
                         stanje.liftLokacija1 -= 1

                         if uprNaredbe.liftKatovi1[int(stanje.liftLokacija1 / 2)] == 1:
                              stanje.liftVrata1 = 1
                              kljuc.release()
                              time.sleep(5)
                              kljuc.acquire()
                              stanje.liftVrata1 = 0
                              uprNaredbe.liftKatovi1[int(stanje.liftLokacija1 / 2)] = 0
                         if int(stanje.liftLokacija1 / 2) == zavrsniKat:
                              uprNaredbe.liftKreni1 = 0
                              uprNaredbe.liftSmjer1 = 0
                              stanje.liftSmjer1 = 0
                              stanje.liftZauzet1 = 0
                              break

          kljuc.release()

def lift2() -> None:
     while 1 == 1:
          kljuc.acquire()
          if uprNaredbe.liftKreni2 == 0:
               kljuc.release()
               time.sleep(2)
               kljuc.acquire()

          if uprNaredbe.liftKreni2 == 1:
               stanje.liftZauzet2 = 1
               pocetniKat = 0
               zavrsniKat = 0

               if uprNaredbe.liftSmjer2 == 1:
                    for i in range(4):
                         if uprNaredbe.liftKatovi2[i] == 1:
                              pocetniKat = i
                              break
                    for i in range(3, pocetniKat, -1):
                         if uprNaredbe.liftKatovi2[i] == 1:
                              zavrsniKat = i
                              break
                    kljuc.release()
                    time.sleep(2.5)
                    kljuc.acquire()
                    stanje.liftLokacija2 = pocetniKat*2
                    stanje.liftSmjer2 = 1
                    stanje.liftVrata2 = 1
                    kljuc.release()
                    time.sleep(5)
                    kljuc.acquire()
                    stanje.liftVrata2 = 0
                    uprNaredbe.liftKatovi2[pocetniKat] = 0

                    while 1 == 1:
                         stanje.liftVrata2 = 0
                         stanje.liftLokacija2 += 1
                         kljuc.release()
                         time.sleep(2.5)
                         kljuc.acquire()
                         stanje.liftLokacija2 += 1

                         if uprNaredbe.liftKatovi2[int(stanje.liftLokacija2/2)] == 1:
                              stanje.liftVrata2 = 1
                              kljuc.release()
                              time.sleep(5)
                              kljuc.acquire()
                              stanje.liftVrata2 = 0
                              uprNaredbe.liftKatovi2[int(stanje.liftLokacija2/2)] = 0
                         if int(stanje.liftLokacija2/2) == zavrsniKat:
                              uprNaredbe.liftKreni2 = 0
                              uprNaredbe.liftSmjer2 = 0
                              stanje.liftSmjer2 = 0
                              stanje.liftZauzet2 = 0
                              break

               if uprNaredbe.liftSmjer2 == -1:
                    for i in range(3, 0, -1):
                         if uprNaredbe.liftKatovi2[i] == 1:
                              pocetniKat = i
                              break
                    for i in range(0, pocetniKat, 1):
                         if uprNaredbe.liftKatovi2[i] == 1:
                              zavrsniKat = i
                              break
                    kljuc.release()
                    time.sleep(2.5)
                    kljuc.acquire()
                    stanje.liftLokacija2 = pocetniKat * 2
                    stanje.liftSmjer2 = -1
                    stanje.liftVrata2 = 1
                    kljuc.release()
                    time.sleep(8)
                    kljuc.acquire()
                    stanje.liftVrata2 = 0
                    uprNaredbe.liftKatovi2[pocetniKat] = 0

                    while 1 == 1:
                         stanje.liftVrata2 = 0
                         stanje.liftLokacija2 -= 1
                         kljuc.release()
                         time.sleep(8)
                         kljuc.acquire()
                         stanje.liftLokacija2 -= 1

                         printKljuc.acquire()
                         print()
                         print("idem dolje" + str(stanje.liftLokacija2))
                         print()
                         printKljuc.release()

                         if uprNaredbe.liftKatovi2[int(stanje.liftLokacija2 / 2)] == 1:
                              stanje.liftVrata2 = 1
                              kljuc.release()
                              time.sleep(8)
                              kljuc.acquire()
                              stanje.liftVrata2 = 0
                              uprNaredbe.liftKatovi2[int(stanje.liftLokacija2 / 2)] = 0
                         if int(stanje.liftLokacija2 / 2) == zavrsniKat:
                              uprNaredbe.liftKreni2 = 0
                              uprNaredbe.liftSmjer2 = 0
                              stanje.liftSmjer2 = 0
                              stanje.liftZauzet2 = 0
                              break

          kljuc.release()

def putnik() -> None:
     lokacija = random.randint(0, 3)
     odrediste = random.randint(0, 3)

     if lokacija == odrediste:
          return None

     # lokacija = 2
     # odrediste = 1

     lokacija *= 2
     odrediste *= 2

     mojSmjer = 0
     if lokacija < odrediste:
          mojSmjer = 1
     if lokacija > odrediste:
          mojSmjer = -1

     kljuc.acquire()
     stanje.brPutnikaKat[int(lokacija/2)] += 1
     stanje.zeljeniKatSa[int(lokacija/2)][int(odrediste/2)] += 1

     while 1 == 1:
          if stanje.liftLokacija1 == lokacija or stanje.liftLokacija2 == lokacija:
               if stanje.liftVrata1 == 1 and stanje.liftPutnici1 <= 8 and uprNaredbe.liftKatovi1[int(odrediste/2)] == 1:
                    stanje.liftPutnici1 += 1
                    stanje.brPutnikaKat[int(lokacija/2)] -= 1
                    stanje.zeljeniKatSa[int(lokacija / 2)][int(odrediste / 2)] -= 1
                    while 1 == 1:
                         if stanje.liftVrata1 == 1 and stanje.liftLokacija1 == odrediste:
                              stanje.liftPutnici1 -= 1
                              # stanje.zeljeniKatSa[int(lokacija/2)][int(odrediste/2)] -= 1
                              kljuc.release()
                              return None
                         else:
                              kljuc.release()
                              time.sleep(1.5)
                              kljuc.acquire()

               if stanje.liftVrata2 == 1 and stanje.liftPutnici2 <= 4 and uprNaredbe.liftKatovi2[int(odrediste/2)] == 1:
                    stanje.liftPutnici2 += 1
                    stanje.brPutnikaKat[int(lokacija/2)] -= 1
                    stanje.zeljeniKatSa[int(lokacija / 2)][int(odrediste / 2)] -= 1
                    while 1 == 1:
                         if stanje.liftVrata2 == 1 and stanje.liftLokacija2 == odrediste:
                              stanje.liftPutnici2 -= 1
                              # stanje.zeljeniKatSa[int(lokacija/2)][int(odrediste/2)] -= 1
                              kljuc.release()
                              return None
                         else:
                              kljuc.release()
                              time.sleep(1.5)
                              kljuc.acquire()

          kljuc.release()
          time.sleep(2.5)
          kljuc.acquire()

def upr() -> None:
     while 1 == 1:

          sumaGore = 0
          sumaDole = 0

          kljuc.acquire()
          for i in range(0, 4, 1):
               for j in range(i+1, 4, 1):
                    sumaGore += stanje.zeljeniKatSa[i][j]
                    sumaDole += stanje.zeljeniKatSa[j][i]

          #rijesi se zombija
          if stanje.liftPutnici1 > 0 and stanje.liftSmjer1 == 0 and stanje.liftZauzet1 == 0:
               for i in range(4):
                    uprNaredbe.liftKatovi1[i] = 1
               uprNaredbe.liftSmjer1 = 1
               uprNaredbe.liftKreni1 = 1
               stanje.liftZauzet1 = 1

               printKljuc.acquire()
               print("Zombie - Saljem Lift1, smjer = " + str(uprNaredbe.liftSmjer1) + ", kreni = " + str(
                    uprNaredbe.liftKreni1) + ", katovi = " + str(uprNaredbe.liftKatovi1))
               printKljuc.release()

          if stanje.liftPutnici2 > 0 and stanje.liftSmjer2 == 0 and stanje.liftZauzet2 == 0:
               for i in range(4):
                    uprNaredbe.liftKatovi2[i] = 1
               uprNaredbe.liftSmjer2 = 1
               uprNaredbe.liftKreni2 = 1
               stanje.liftZauzet2 = 1

               printKljuc.acquire()
               print("Zombie - Saljem Lift2, smjer = " + str(uprNaredbe.liftSmjer2) + ", kreni = " + str(
                    uprNaredbe.liftKreni2) + ", katovi = " + str(uprNaredbe.liftKatovi2))
               printKljuc.release()

          #dole
          if (1 <= sumaDole <= 5) and stanje.liftZauzet2 == 0:
               for i in range(0, 4, 1):
                    if i <= 2:
                         for j in range(i+1, 4, 1):
                              if stanje.zeljeniKatSa[j][i] > 0:
                                   uprNaredbe.liftKatovi2[i] = 1
                                   uprNaredbe.liftKatovi2[j] = 1
               uprNaredbe.liftSmjer2 = -1
               uprNaredbe.liftKreni2 = 1
               stanje.liftZauzet2 = 1

               printKljuc.acquire()
               print("Saljem Lift2, smjer = " + str(uprNaredbe.liftSmjer2) + ", kreni = " + str(
                    uprNaredbe.liftKreni2) + ", katovi = " + str(uprNaredbe.liftKatovi2))
               printKljuc.release()

          elif sumaDole >= 6 and stanje.liftZauzet1 == 0:
               for i in range(0, 4, 1):
                    if i <= 2:
                         for j in range(i+1, 4, 1):
                              if stanje.zeljeniKatSa[j][i] > 0:
                                   uprNaredbe.liftKatovi1[i] = 1
                                   uprNaredbe.liftKatovi1[j] = 1
               uprNaredbe.liftSmjer1 = -1
               uprNaredbe.liftKreni1 = 1
               stanje.liftZauzet1 = 1

               printKljuc.acquire()
               print("Saljem Lift1, smjer = " + str(uprNaredbe.liftSmjer1) + ", kreni = " + str(
                    uprNaredbe.liftKreni1) + ", katovi = " + str(uprNaredbe.liftKatovi1))
               printKljuc.release()

          # gore
          if (1 <= sumaGore <= 5) and stanje.liftZauzet2 == 0:
               for i in range(0, 4, 1):
                    if i <= 2:
                         for j in range(i+1, 4, 1):
                              if stanje.zeljeniKatSa[i][j] > 0:
                                   uprNaredbe.liftKatovi2[i] = 1
                                   uprNaredbe.liftKatovi2[j] = 1
               uprNaredbe.liftSmjer2 = 1
               uprNaredbe.liftKreni2 = 1
               stanje.liftZauzet2 = 1

               printKljuc.acquire()
               print("Saljem Lift2, smjer = " + str(uprNaredbe.liftSmjer2) + ", kreni = " + str(
                    uprNaredbe.liftKreni2) + ", katovi = " + str(uprNaredbe.liftKatovi2))
               printKljuc.release()

          elif sumaGore >= 6 and stanje.liftZauzet1 == 0:
               for i in range(0, 4, 1):
                    if i <= 2:
                         for j in range(i+1, 4, 1):
                              if stanje.zeljeniKatSa[i][j] > 0:
                                   uprNaredbe.liftKatovi1[i] = 1
                                   uprNaredbe.liftKatovi1[j] = 1
               uprNaredbe.liftSmjer1 = 1
               uprNaredbe.liftKreni1 = 1
               stanje.liftZauzet1 = 1

               printKljuc.acquire()
               print("Saljem Lift1, smjer = " + str(uprNaredbe.liftSmjer1) + ", kreni = " + str(
                    uprNaredbe.liftKreni1) + ", katovi = " + str(uprNaredbe.liftKatovi1))
               printKljuc.release()

          kljuc.release()
          time.sleep(0.5)

def printS() -> None:
     for i in range(10):
          for j in range(16):
               print(S[i][j], " ", end="")
          print()
     print("==================================================")
     return None


def main():
     printDretva = threading.Thread(target=prikazStanja, args=())
     uprDretva = threading.Thread(target=upr, args=())
     lift1Dretva = threading.Thread(target=lift1, args=())
     lift2Dretva = threading.Thread(target=lift2, args=())

     printDretva.start()
     uprDretva.start()
     lift1Dretva.start()
     lift2Dretva.start()

     while 1 == 1:
          threading.Thread(target=putnik, args=()).start()
          time.sleep(2)



if __name__ == '__main__':
    main()
