from multiprocessing import Pool as Poolx
from functools import partial
import time
import numpy as np
import json
from multiprocessing.pool import ThreadPool as Pool


liste = []
def olustur(boyut,komutlar,duzlem):
    global liste
    denemeko = komutlar[:]
    if boyut == 1:
        a = komutlar[:]
        liste.append(a)
        return
    dugum_Sayisi = boyut-1
    for kacinci_dugum in range(dugum_Sayisi):
        kacinci_dugum += 1
        y_ekseni = ['yukarı','aşağı']
        for z,y_komut in enumerate(y_ekseni):
            x_ekseni = ['sağa','sola']
            for y,x_komut in enumerate(x_ekseni):
                if x_komut == "sağa":
                    sagimdakiler = boyut - kacinci_dugum
                    solumdakiler = kacinci_dugum
                    if solumdakiler > sagimdakiler:
                        x_komut = "sola"
                        y_komut = y_ekseni[(z+1)%len(y_ekseni)]
                        gonderilecek_boyut = boyut - sagimdakiler
                    else:
                        gonderilecek_boyut = boyut - kacinci_dugum
                elif x_komut == "sola":
                    sagimdakiler = boyut - kacinci_dugum
                    solumdakiler = kacinci_dugum
                    if sagimdakiler > solumdakiler:
                        x_komut = "sağa"
                        y_komut = y_komut = y_ekseni[(z+1)%len(y_ekseni)]
                        gonderilecek_boyut = boyut - solumdakiler
                    else:
                        gonderilecek_boyut = boyut - sagimdakiler
                olustur(gonderilecek_boyut,denemeko+[f" {str(kacinci_dugum)}. Düğümü {duzlem} eksende {x_komut} doğru  {y_komut} katlayın"],duzlem)



def uniquex(list1):
    x = np.array(list1)
    try:
        return np.unique(x,axis=0)
    except:
        return np.unique(x)


perm_list = []
def donder(liste1,list2,templist):
    global perm_list
    if len(liste1) == 0 and len(list2) == 0:
        perm_list.append(templist)
        return
    if len(liste1) == 0:
        perm_list.append(templist+list2)
        return
    if len(list2) == 0:
        perm_list.append(templist+liste1)
        return
    for i in range(2):
        temp_list = templist[:]
        list_one = liste1[:]
        list_two = list2[:]
        if i == 0:
            if len(list_one) != 0:
                temp_list.append(list_one[0])
                list_one = list_one[1:]
                donder(list_one,list_two,temp_list)
            elif len(list_two) != 0:
                temp_list.append(list_two[0])
                list_two = list_two[1:]
                donder(list_one,list_two,temp_list)
        if i == 1:
            if len(list_two) != 0:
                temp_list.append(list_two[0])
                list_two = list_two[1:]
                donder(list_one,list_two,temp_list)
            elif len(list_one) != 0:
                temp_list.append(list_one[0])
                list_one = list_one[1:]
                donder(list_one,list_two,temp_list)



def komut_isle(komut_list: list,matrix: list):
    komut_list = komut_list[:]
    for komut in komut_list:
        komut_splitted = komut.split()
        dugum = int(komut_splitted[0][:-1])
        eksen = komut_splitted[2]
        sag_sol = komut_splitted[4]
        yon = komut_splitted[6]

        if eksen == "dikey" and sag_sol == "sağa":
            if yon == "yukarı":
                for i in range(dugum):
                    for z in range(len(matrix[i])):
                        degisken = matrix[i][z].reverse()
                        matrix[(2*dugum)-1-i][z] = matrix[i][z] + matrix[(2*dugum)-1-i][z]
                del matrix[:dugum]
            elif yon == "aşağı":
                for i in range(dugum):
                    for z in range(len(matrix[i])):
                        degisken = matrix[i][z].reverse()
                        matrix[i+dugum][z] = matrix[i+dugum][z] + matrix[i][z]
                del matrix[:dugum]
        elif eksen == "dikey" and sag_sol == "sola":
            if yon == "yukarı":
                for i in range(len(matrix[dugum:])):
                    for z in range(len(matrix[i])):
                        sayi = len(matrix[dugum:]) - z
                        degisken = matrix[-(i+1)][z].reverse()
                        matrix[dugum-i-1][z] = matrix[-(i+1)][z] + matrix[dugum-i-1][z]
                    del matrix[-(i+1)]
            if yon == "aşağı":
                for i in range(len(matrix[dugum:])):
                    for z in range(len(matrix[i])):
                        degisken = matrix[-(i+1)][z].reverse()
                        matrix[dugum-(i+1)][z] = matrix[dugum-(i+1)][z] + matrix[-(i+1)][z]
                    del matrix[-(i+1)]
        elif eksen == "yatay" and sag_sol == "sağa":
            if yon == "yukarı":
                for i in range(len(matrix)):
                    for z in range(dugum):
                        degisken = matrix[i][z].reverse()
                        matrix[i][(2*dugum)-1-z] = matrix[i][z] + matrix[i][(2*dugum)-1-z]
                        del matrix[i][z]
            elif yon == "aşağı":
                for i in range(len(matrix)):
                    for z in range(dugum):
                        degisken = matrix[i][z].reverse()
                        matrix[i][(2*dugum)-1-z] = matrix[i][(2*dugum)-1-z] + matrix[i][z]
                        del matrix[i][z]
        elif eksen == "yatay" and sag_sol == "sola":
            if yon == "yukarı":
                for i in range(len(matrix)):
                    for z in range(len(matrix[i][dugum:])):
                        sayi = dugum - len(matrix[i][dugum:]) + z
                        degisken = matrix[i][-z-1].reverse()
                        matrix[i][sayi] = matrix[i][-z-1] + matrix[i][sayi]
                    del matrix[i][dugum:]
            if yon == "aşağı":
                for i in range(len(matrix)):
                    for z in range(len(matrix[i][dugum:])):
                        sayi = dugum - len(matrix[i][dugum:]) + z
                        degisken = matrix[i][-z-1].reverse()
                        matrix[i][sayi] = matrix[i][sayi] + matrix[i][-z-1]
                        del matrix[i][-z-1]
    return(matrix[0][0])



def sorgu():
    global perm_list
    while True:
        aranacak_siralama = input("Lütfen Aranacak Sıralamayı Giriniz (1 3 5 4 2 6) Gibi : ")
        indexler = []
        for single_command in (perm_list):
            if aranacak_siralama.strip() == single_command[-1].strip():
                indexler.append(single_command)
        
        for komuts in indexler:
            print("*"*45)
            for komut in komuts[:-1]:
                print(komut)
        
        print("\n"+str(len(indexler))+ " Adet Eşleşme Bulundu.")
        indexler = []




def worker(dikey,yatay):
    try:
        donder(dikey,yatay,[])
    except:
        print('error with item')


def main_func(soru_dikey,soru_yatay,x):
    sayac = 1
    matrix = []
    for i in range(soru_dikey):
        matrix.append([])
        for z in range(soru_yatay):
            matrix[i].append([sayac])
            sayac += 1
    sonuc = komut_isle(x,matrix[:])
    sonuc_str = ""
    for ss in sonuc:
        sonuc_str += str(ss) +" "
    sonuc.append(sonuc_str)
    return sonuc_str



if __name__ == "__main__":
    soru_dikey = int(input('Dikeyde Kaç Tane Nokta Olsun? :'))
    soru_yatay = int(input('Yatayda Kaç Tane Nokta Olsun? : '))

    start_time = time.time()
    olustur(soru_dikey,[],"dikey")
    dikey_liste = uniquex(liste).tolist()
    liste = []

    olustur(soru_yatay,[],"yatay")
    yatay_liste = uniquex(liste).tolist()

    pool = Pool(1)
    for dikey in dikey_liste:
        for yatay in yatay_liste:
            pool.apply_async(worker, (dikey,yatay,))
    pool.close()
    pool.join()

    print("--- Geçen süre: %s saniye ---" % (time.time() - start_time))


    px = Poolx()
    func = partial(main_func,soru_dikey,soru_yatay)
    result = px.map_async(func,perm_list)

    px.close()
    px.join()

    
    for i,veri in enumerate(result._value):
        perm_list[i].append(veri)
    
    sonuc_strx = uniquex(result._value).tolist()

    print("Özgün Sıralama Sayısı %d" % (len(sonuc_strx)))
    print("Toplam Komut Dizisi: " + str(len(perm_list)))
    print("--- Geçen süre: %s saniye ---" % (time.time() - start_time))

    with open("komutlar.txt","w",encoding="utf-8") as file:
        json.dump(perm_list,file,ensure_ascii=False,indent=4)

    sorgu()