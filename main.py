import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz #Bulanık kuralları ve kümeleri ifade etmek için gereken python kütüphanesi
from skfuzzy import control as ctrl #Kontrol oluşturmak için import edildi


#Antecedent =Bir bulanık kontrol sistemi için öncül (giriş/sensör) değişkeni.
#np.arange = Numpy kütüphanesini kullanarak belirtilen aralıklarda sayısal dizi oluşturur
oda_Sicakligi = ctrl.Antecedent(np.arange(16, 36, 1), 'oda_Sicakligi')
sicaklik = ctrl.Antecedent(np.arange(16, 36, 1), 'sicaklik')
nem = ctrl.Antecedent(np.arange(10, 70, 1), 'nem')
fan_hizi = ctrl.Consequent(np.arange(0, 1800, 1), 'fan_hizi')
kompresör_hizi = ctrl.Consequent(np.arange(0, 1800, 1), 'kompresör_hizi')


#Trimf = Üçgen Üyelik Fonksiyonu oluşturur.
#Belirtilen kümeler için aralık değerleri

oda_Sicakligi['cok-soguk'] = fuzz.trimf(sicaklik.universe, [0, 0, 20])
oda_Sicakligi['soguk'] = fuzz.trimf(sicaklik.universe, [16, 20, 24])
oda_Sicakligi['ilik'] = fuzz.trimf(sicaklik.universe, [20, 24, 28])
oda_Sicakligi['sicak'] = fuzz.trimf(sicaklik.universe, [24, 28, 32])
oda_Sicakligi['cok-sicak'] = fuzz.trimf(sicaklik.universe, [28, 32, 36])


sicaklik['cok-soguk'] = fuzz.trimf(sicaklik.universe, [0, 0, 20])
sicaklik['soguk'] = fuzz.trimf(sicaklik.universe, [16, 20, 24])
sicaklik['ilik'] = fuzz.trimf(sicaklik.universe, [20, 24, 28])
sicaklik['sicak'] = fuzz.trimf(sicaklik.universe, [24, 28, 32])
sicaklik['cok-sicak'] = fuzz.trimf(sicaklik.universe, [28, 32, 36])


nem['kuru'] = fuzz.trimf(nem.universe, [0, 0, 40])
nem['ferah'] = fuzz.trimf(nem.universe, [30, 40, 50])
nem['rahat'] = fuzz.trimf(nem.universe, [40, 50, 60])
nem['nemli'] = fuzz.trimf(nem.universe, [50, 60, 70])


fan_hizi['cok-yavas'] = fuzz.trimf(fan_hizi.universe, [0, 0, 600])
fan_hizi['yavas'] = fuzz.trimf(fan_hizi.universe, [300, 600, 900])
fan_hizi['orta'] = fuzz.trimf(fan_hizi.universe, [600, 900, 1200])
fan_hizi['hizli'] = fuzz.trimf(fan_hizi.universe, [900, 1200, 1500])
fan_hizi['cok-hizli'] = fuzz.trimf(fan_hizi.universe, [1200, 1500, 1800])


kompresör_hizi['cok-yavas'] = fuzz.trimf(fan_hizi.universe, [0, 0, 600])
kompresör_hizi['yavas'] = fuzz.trimf(fan_hizi.universe, [300, 600, 900])
kompresör_hizi['orta'] = fuzz.trimf(fan_hizi.universe, [600, 900, 1200])
kompresör_hizi['hizli'] = fuzz.trimf(fan_hizi.universe, [900, 1200, 1500])
kompresör_hizi['cok-hizli'] = fuzz.trimf(fan_hizi.universe, [1200, 1500, 1800])




def get_fan_hizi_control_kurallari(): #fan hızı için kurallar
    kural1a = ctrl.Rule( oda_Sicakligi['cok-sicak'] & sicaklik['cok-soguk'] & nem['nemli'],  fan_hizi['cok-hizli'] )
    kural1b = ctrl.Rule(  oda_Sicakligi['cok-sicak'] & sicaklik['cok-soguk'] & nem['rahat'], fan_hizi['hizli'] )
    kural1c = ctrl.Rule( oda_Sicakligi['cok-sicak'] & sicaklik['cok-soguk'] & nem['ferah'],  fan_hizi['orta']  )
    kural1d = ctrl.Rule( oda_Sicakligi['cok-sicak'] | sicaklik['cok-soguk'] | nem['kuru'], fan_hizi['yavas'] )

    kural2a = ctrl.Rule(oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['nemli'],  fan_hizi['cok-hizli'] )
    kural2b = ctrl.Rule(oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['rahat'],fan_hizi['hizli'])
    kural2c = ctrl.Rule(oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['ferah'], fan_hizi['orta'] )
    kural2d = ctrl.Rule( oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['kuru'], fan_hizi['yavas'])

    kural3a = ctrl.Rule( oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['nemli'],  fan_hizi['cok-hizli'])
    kural3b = ctrl.Rule( oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['rahat'],  fan_hizi['hizli'])
    kural3c = ctrl.Rule(  oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['ferah'],fan_hizi['orta'] )
    kural3d = ctrl.Rule( oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['kuru'],fan_hizi['yavas'] )

    kural4a = ctrl.Rule(  oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['nemli'], fan_hizi['cok-hizli'])
    kural4b = ctrl.Rule(oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['rahat'], fan_hizi['hizli'] )
    kural4c = ctrl.Rule(oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['ferah'], fan_hizi['orta'] )
    kural4d = ctrl.Rule( oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['kuru'], fan_hizi['yavas'])

    kural5a = ctrl.Rule( oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['nemli'], fan_hizi['cok-hizli'] )
    kural5b = ctrl.Rule( oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['rahat'],fan_hizi['hizli'])
    kural5c = ctrl.Rule( oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['ferah'], fan_hizi['orta'])
    kural5d = ctrl.Rule(  oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['kuru'], fan_hizi['yavas'] )

    return [
        kural1a, kural1b, kural1c, kural1d,
        kural2a, kural2a, kural2b, kural2d,
        kural3a, kural3b, kural3c, kural3d,
        kural4a, kural4b, kural4c, kural4d,
        kural5a, kural5b, kural5c, kural5d
    ]


def get_kompresör_hizi_control_kurallari(): #Komposor hizi için kurallar
    #Rule() Bulanık sistem için kural oluşturur

    kural1a = ctrl.Rule( oda_Sicakligi['cok-sicak'] & sicaklik['cok-soguk'] & nem['nemli'],  kompresör_hizi['cok-hizli'] )
    kural1b = ctrl.Rule(  oda_Sicakligi['cok-sicak'] & sicaklik['cok-soguk'] & nem['rahat'],  kompresör_hizi['cok-hizli'])
    kural1c = ctrl.Rule(  oda_Sicakligi['cok-sicak'] & sicaklik['cok-soguk'] & nem['ferah'],  kompresör_hizi['cok-hizli'])
    kural1d = ctrl.Rule( oda_Sicakligi['cok-sicak'] | sicaklik['cok-soguk'] | nem['kuru'],   kompresör_hizi['cok-hizli'])

    kural2a = ctrl.Rule(  oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['nemli'], kompresör_hizi['hizli'])
    kural2b = ctrl.Rule(  oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['rahat'],  kompresör_hizi['hizli'] )
    kural2c = ctrl.Rule(  oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['ferah'],  kompresör_hizi['hizli'])
    kural2d = ctrl.Rule(  oda_Sicakligi['cok-sicak'] | sicaklik['soguk'] | nem['kuru'],  kompresör_hizi['hizli'])

    kural3a = ctrl.Rule(  oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['nemli'], kompresör_hizi['hizli'])
    kural3b = ctrl.Rule(  oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['rahat'],  kompresör_hizi['hizli'] )
    kural3c = ctrl.Rule(   oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['ferah'],    kompresör_hizi['hizli']  )
    kural3d = ctrl.Rule(       oda_Sicakligi['sicak'] | sicaklik['soguk'] | nem['kuru'],  kompresör_hizi['hizli']  )

    kural4a = ctrl.Rule( oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['nemli'], kompresör_hizi['orta'])
    kural4b = ctrl.Rule(   oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['rahat'],  kompresör_hizi['orta'] )
    kural4c = ctrl.Rule( oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['ferah'], kompresör_hizi['orta'] )
    kural4d = ctrl.Rule(oda_Sicakligi['ilik'] | sicaklik['soguk'] | nem['kuru'], kompresör_hizi['orta'])

    kural5a = ctrl.Rule(     oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['nemli'],    kompresör_hizi['orta'] )
    kural5b = ctrl.Rule(    oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['rahat'],    kompresör_hizi['orta'])
    kural5c = ctrl.Rule(   oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['ferah'],    kompresör_hizi['orta'] )
    kural5d = ctrl.Rule(    oda_Sicakligi['soguk'] | sicaklik['ilik'] | nem['kuru'],    kompresör_hizi['orta'])

    return [
        kural1a, kural1b, kural1c, kural1d,
        kural2a, kural2a, kural2b, kural2d,
        kural3a, kural3b, kural3c, kural3d,
        kural4a, kural4b, kural4c, kural4d,
        kural5a, kural5b, kural5c, kural5d
    ]

#ctrl.ControlSystem = Bulanık Kontrol Sistemi içeren en üst sınıf
ac_ctrl = ctrl.ControlSystem( #iki parametreyi alıp(fan_....._control, kompresör_...._control), bulanık sistemde kullanması için gereken değişken
    get_fan_hizi_control_kurallari() + get_kompresör_hizi_control_kurallari()  
    
)

#İnput alanları (degeri girmeden önce küme aralılarının grafiklerini gösterir)
oda_Sicakligi.view()
in_rt = input("Oda sıcaklığını girin:") #sıcaklık için input alma

sicaklik.view()
in_tt = input("Hedef sıcaklığı girin:") # hedef sıcaklıgı için için input alma

nem.view()
in_hd = input("Nemi girin:")#nem için input alma


# fan_hizi.view()
# kompresör_hizi.view()

input('İşleme Kuralları İçin Entera Basın')
speed = ctrl.ControlSystemSimulation(ac_ctrl) #Control Sisteminin (ctrl) sonucunu hesaplar, speed değişkenine atar
speed.input['oda_Sicakligi'] = int(in_rt) # Girilen değeri int yapma
speed.input['sicaklik'] = int(in_tt) # Girilen değeri int yapma
speed.input['nem'] = int(in_hd) # Girilen değeri int yapma 
speed.compute() #Hız hesaplamasını yapar

input('Fan Hızını Görmek için Entera Bas')
print("Fan Hızı", f"{speed.output['fan_hizi']} RPM") #konsola hızı yazdırma
fan_hizi.view(sim=speed) # Fan Hızı Grafiğini gösterme (referans olarak speed değişkenini alır)

input('Kompresör Hızını Görmek için Entera bas') 
print("Kompresör Hızı", f"{speed.output['kompresör_hizi']} RPM") #konsola hızı yazdırma
kompresör_hizi.view(sim=speed) #Kompresör hızı grafiği gösterme (referans olarak speed değişkenini alır)

input('Bitirmek için herhangi bir tuşa basın')
