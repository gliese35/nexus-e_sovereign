import pandas as pd
import random

def generate_data():
    urunler = ['Akıllı Saat X1', 'RGB Klavye', 'USB-C Hub', 'Kablosuz Mouse', 'Dron Pro V9']
    data = []
    
    for _ in range(100):
        urun = random.choice(urunler)
        maliyet = random.randint(200, 1500)
        satis = maliyet + random.randint(100, 800)
        kar = satis - maliyet
        data.append([urun, maliyet, satis, kar])
        
    df = pd.DataFrame(data, columns=['Urun_Adi', 'Maliyet', 'Satis_Fiyati', 'Net_Kar'])
    df.to_csv("data/sales_data.csv", index=False)
    print("✅ E-Ticaret Veri Seti 'data/sales_data.csv' Olarak Oluşturuldu.")

if __name__ == "__main__":
    generate_data()