#1
j = 795

bbm = j/12

print(bbm)

#2
import math

jarak=795

bbm=jarak/12

kapasitas=50

bbm_yg_digunakan=bbm/50

minimal=math.ceil(bbm_yg_digunakan)

print('Jumlah bensin yang diperlukan dalam perjalanan tersebut adalah', bbm, 'liter')
print('Jumlah minimal pak Budi harus mengisi bensin hingga penuh adalah', minimal, 'kali' )

#3
def nilai():
    while True:
        mapel = [int(input(f"Masukkan Nilai {n_mapel} : ")) for n_mapel in ['Bindo', 'IPA', 'MTK']]
        Bindo, IPA, MTK = mapel[0], mapel[1], mapel[2]
        
        if all(0 <= nilai <= 100 for nilai in mapel):
            break
        else:
            print("Nilai harus antara 0 dan 100. Silakan masukkan kembali.")

    if MTK > 70 and Bindo > 60 and IPA > 60:
        status = "lulus"
        print("Kamu dinyatakan " + status)
    else:
        status = "tidak lulus"
        print("Kamu dinyatakan : " + status)

nilai()

#4
for i in range(0,100):
    if i%2 != 0:
        print(i)

#5
a =0
for i in range(0,100):
    if i%2 == 1:
        print(a)
        a += 1
        
print(len(a))
        

#6
#   import library
import math
def kombinasi(n, r):
    return math.comb(n, r)
def permutation(n, r):
    return math.perm(n, r)

hasilComb = kombinasi(5, 3)
hasilperm = permutation(10, 7)

print(hasilComb)
print(hasilperm)

#   Manual
c = [5, 3]
p = [10, 7]

def faktorial(n):
    factor = 1
    for i in range(1, n+1):
        factor *= i
    return factor
        
c1 = faktorial(c[0])
c2 = faktorial(c[0]-c[1])
c3 = faktorial(c[1])

p1 = faktorial(p[0])
p2 = faktorial(p[0]-p[1])

kombinasi = (c1/(c2*c3))
permutasi = (p1/p2)

print(kombinasi)
print(permutasi)

#7
def isPythagoras(a,b,c):
    if a**2 + b**2 == c**2:
        print(True)
    else:
        print(False)
    
isPythagoras(3,4,5)
isPythagoras(5, 9, 12)
isPythagoras(8, 6, 10)
isPythagoras(7, 8, 11)

#8
jam_sewa = 23-6

tarif_12 = 200000
tarif_jalan = 10000
tarif_bayar = (jam_sewa - 12) * tarif_jalan if jam_sewa > 12 else 0
bayar = tarif_bayar + tarif_12

print(f"Total bayar yang harus dibayarkan adalah Rp {bayar}")

#9
def waktu_sampai_kota_C():
    jarak_A_B = 125  
    kecepatan_A_B = 62  
    jarak_B_C = 256  
    kecepatan_B_C = 70  
    waktu_istirahat = 45 / 60  

    waktu_A_B = jarak_A_B / kecepatan_A_B 
    waktu_B_C = jarak_B_C / kecepatan_B_C
    total_waktu = waktu_A_B + waktu_B_C + waktu_istirahat

    waktu_berangkat = 6 
    waktu_sampai_C = waktu_berangkat + total_waktu 


    jam = int(waktu_sampai_C)
    menit = int((waktu_sampai_C - jam) * 60)

    return jam, menit

jam, menit = waktu_sampai_kota_C()
print(f"Pak Amir sampai di kota C pada pukul {jam}:{menit}")

#10
import random

angka = random.randint(0, 100)
print("Hai! Nama saya Mr.Number, saya telah memilih sebuah bilangan bulat secara acak antara 0 s/d 100. Silahkan tebak saya!")

while True:
    try:
        tebak = int(input("Tebakan Anda : "))
    except ValueError:
        print("Input tidak valid. Harap masukkan angka.")
        continue
    
    if tebak == angka:
        print("Tebakan Anda BENAR ~ !")
        break
    elif tebak > angka:
        print("Angka tebakan terlalu tinggi")
    elif tebak < angka:
        print("Angka tebakan terlalu rendah")
