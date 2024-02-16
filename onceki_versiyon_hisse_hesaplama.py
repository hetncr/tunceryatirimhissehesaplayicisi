
#pip install streamlit

#%%writefile deneme.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd


#streamlit.config.theme.base = "dark"
st.title("**HOCALAR HİSSE HESAPLIYOR**")
st.subheader("**:blue[Road to Kıbrıs]** :airplane_departure::sunglasses:", divider='rainbow')
#st.set_page_config(
# page_title="Hisse Hedef Fiyat Hesaplayıcı",
#  page_icon="https://example.com/icon.png",
#  layout="centered",
#)

# Kullanıcıdan hisse senedi adı almak için input fonksiyonu kullanın
#hisse_adi = input("Hisse Adı : ").upper()
hisse_input = st.text_input("**Hisse Adı (Sadece Borsadaki Kısaltma Adını Girin):**").upper()
hisse_adi = hisse_input

if hisse_adi:
  # hisse_adi değişkenini url1 değişkeninde hisse parametresine atayın
  url1="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse="+hisse_adi
  #time.sleep(0.01)
  # web sitesinden yıl ve dönem bilgilerini çekmek için BeautifulSoup kullanın
  r1=requests.get(url1)
  s1=BeautifulSoup(r1.text, "html.parser")
  secim=s1.find("select", id="ddlMaliTabloFirst")
  secim2=s1.find("select", id="ddlMaliTabloGroup")

  #print(secim2)

  # yıl ve dönem bilgilerini listelere atayın
  grup=[]
  tarihler=[]
  yıllar=[]
  donemler=[]

  # try to find the elements with BeautifulSoup
  try:
    cocuklar=secim.findChildren("option")
    grup=secim2.find("option")["value"]


    for i in cocuklar:
      tarihler.append(i.string.rsplit("/"))

    for j in tarihler:
      yıllar.append(j[0])
      donemler.append(j[1])


    if len(tarihler)>=4:
      # parametreler değişkenini oluşturun
      parametreler=(
          ("companyCode",hisse_adi),
          ("exchange","TRY"),
          ("financialGroup",grup),
          ("year1",yıllar[0]),
          ("period1",donemler[0]),
          ("year2",yıllar[1]),
          ("period2",donemler[1]),
          ("year3",yıllar[2]),
          ("period3",donemler[2]),
          ("year4",yıllar[3]),
          ("period4",donemler[3])
      )
      #print(tarihler)
      # web servisine istek gönderin ve veriyi alın
      url2="https://www.isyatirim.com.tr/_layouts/15/IsYatirim.Website/Common/Data.aspx/MaliTablo"
      r2= requests.get(url2,params=parametreler).json()["value"]

      # veriyi bir veri çerçevesine dönüştürün
      veri=pd.DataFrame.from_dict(r2)

      # gereksiz sütunları kaldırın
      veri.drop(columns=["itemCode","itemDescEng"],inplace=True)
      # Select the first row by its index
      Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
      ozkaynaklar1 = Ozkaynaklar.iloc[0,1]
      Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
      ozkaynaklar_3 = Ozkaynaklar.iloc[0,2]
      Ozkaynaklar =  veri[veri['itemDescTr'] == 'Özkaynaklar']
      ozkaynaklar_2 = Ozkaynaklar.iloc[0,4]
      OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']
      OdenmisSermaye1 = OdenmisSermaye.iloc[0,1]
      OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']
      OdenmisSermaye_2 = OdenmisSermaye.iloc[0,4]
      NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
      NetDonemKarı1 = NetDonemKarı.iloc[0,1]
      NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
      NetDonemKarı_3 = NetDonemKarı.iloc[0,2]
      NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
      NetDonemKarı_2 = NetDonemKarı.iloc[0,4]

      #print("Özkaynaklar:", ozkaynaklar1)
      #print("Ödenmiş Sermaye:", OdenmisSermaye)
      ###print(f"Özkaynaklar: {float(ozkaynaklar1):,.2f}") # comma and dot separators
      ###print(f"Ödenmiş Sermaye: {float(OdenmisSermaye):,.2f}")

  # Print the desired data
      #print(ozkaynaklar)
      #print(OdenmisSermaye)
      # veriyi ekrana yazdırın
      #print(veri)

  except AttributeError:
    # print a message
    print("An AttributeError occurred")
    # skip the iteration
    #continue

  st.write(" İş Yatırım Sayfası İçin Tıklayın: [link](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx)")
  st.write(" Tradingview Grafik Sayfası İçin Tıklayın: [link](https://tr.tradingview.com/chart/)")
  
  with st.sidebar:
  #Gelecek Özkaynak Tahmini Miktarı
  #Gelecek Özkaynak Tahmini Miktarı
    c22 = st.number_input(f"**Güncel Dönem Tutarı:**", value=None, placeholder="Güncel dönem tutarını bu alana yazın")
    c24 = st.number_input(f"**Geçmiş Dönem Tutarı:**", value=None, placeholder="Geçmiş dönem tutarını bu alana yazın")
    #c22 = st.number_input(f"**Geçmiş Dönem Özkaynaklar (Özsermaye):**", value=None, placeholder="Özkaynaklar (Özsermaye) tutarını bu alana yazın")
    #c24 = st.number_input(f"**Geçmiş Dönem Net Kar:**", value=None, placeholder="Geçmiş Dönem Net Kar tutarını bu alana yazın")
    islem_1 = st.selectbox("Gelecek Özkaynak ve Net Kar Tahmini Miktarı:", ["Gelecek Dönem Tahmini Miktarı"])
    if islem_1 == "Gelecek Dönem Tahmini Miktarı":
      # Ensure both c8 and c22 have valid numerical values before calculation
        if c22 is not None and c24 is not None:
            c25 = c22 + (c22 - c24)  # Calculate the future equity amount
            st.write(f"**Gelecek Dönem Tahmini Miktarı:** {c25}")
        else:
            st.write("Hesaplama için Güncel ve Geçmiş Dönem tutarlarını giriniz.")
    #else:
        #st.write("Hesaplama Yapılamadı")
    #elif islem_1 == " Gelecek Net Kar Tahmini Miktarı":
        # Ensure both c7 and c24 have valid numerical values before calculation
        #if c7 is not None and c24 is not None:
            #c26 = c7 + (c7 - c24)  # Calculate the future equity amount
            #st.write(f"**Gelecek Net Kar Tahmini Miktarı:** {c26}")
        #else:
            #st.write("Hesaplama için Güncel Net Kar ve Geçmiş Dönem Net Kar tutarlarını giriniz.")
    #else:
        #st.write("Hesaplama Yapılamadı")
    
#with sidebar:
    st.subheader(f":blue[**Manuel Hisse Hesaplayıcı**]", divider="rainbow")
    st.write("Hisse Hedef Fiyat Hesaplayıcı")
# Hisse Fiyatı
    c3_1 = st.number_input("Hisse Fiyatı:" )
# Hisse F/K Oranı
    c10_1 = float(st.number_input("Hisse F/K Oranı:"))
# HİSSE PD/DD ORANI
    c11_1 = st.number_input("Hisse PD/DD Oranı: ")
# BİST100 /SEKTÖR GÜNCEL F/K ORANI
    c12_1 = st.number_input("BİST100 / Sektör Güncel F/K Oranı: ")
# BIST100 / Sektör Güncel P/D Oranı
    c13_1 = float(st.number_input("BİST100 / Sektör Güncel PD/DD Oranı:"))
# Ödenmiş Sermaye
    c4_1 = st.number_input("Ödenmiş Sermaye: ")
# Yıllık Net Kar
    c7_1 = st.number_input("Yıllık Net Kar: ")
# Özsermaye
    c8_1 = st.number_input("Özkaynaklar (Özsermaye): ")
    operation_manuel = st.selectbox(":blue[**HİSSE FİYAT HESAPLAMARI İÇİN İŞLEM SEÇİN:**]", ["İŞLEM SEÇİN","TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER"])
  #if operation == "Tüm Hedef Fiyatları Göster":
    if operation_manuel == "İŞLEM SEÇİN":
      st.write(f"İŞLEM SEÇİN")
    elif operation_manuel == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
      c21_1 = (c7_1*7)+(c8_1*0.5)
      potansiyel_fiyat_1 = c21_1/c4_1
      st.write(f":blue[**POTANSİYEL DEĞERİNE GÖRE HİSSE FİYATI:**] {potansiyel_fiyat_1:,.2f}")
    #st.write(f":red[Not: Hisse verilerini kontrol ediniz. Eksik veri nedeniyle altta kırmızı alanda hata mesajı çıkmaktadır]")
  #operation = st.selectbox("[ORTALAMA HEDEF FİYAT]")
      fk_hedef_fiyat_1 = c3_1 / c10_1 * c12_1
      pd_hedef_fiyat_1 = c3_1 / c11_1 * c13_1
      ozsermaye_hf_1 = (c7_1/c8_1)*10/c11_1*c3_1
      odenmis_hedef_fiyat_1 = (c7_1 / c4_1) * c10_1
      c21_1 = (c7_1*7)+(c8_1*0.5)
      potansiyel_fiyat_1 = c21_1/c4_1
      ortalama_hesap_1 = ( fk_hedef_fiyat_1 + pd_hedef_fiyat_1 + odenmis_hedef_fiyat_1 + ozsermaye_hf_1 + potansiyel_fiyat_1 ) / 5
    #if operation == "ORTALAMA HEDEF FİYAT":
    #st.write(ortalama_hesap)
    #if ortalama_hesap < kapanıs :
      #st.write(f":blue[**TÜM HESAPLAMALARIN ORTALAMA FİYATI:**] {ortalama_hesap:,.2f}")
    #else :
      #st.write(f"**TÜM HESAPLAMALARIN ORTALAMA FİYATI:** :green[{ortalama_hesap:,.2f}]")
    #elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
      st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat_1:,.2f}")
      st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat_1:,.2f}")
      st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat_1:,.2f}")
      st.write(f":blue[**ÖZKAYNAK (ÖZSERMAYE) KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf_1:,.2f}")
      st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap_1:,.2f}")
      st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {c3_1}")
  #c22 = st.number_input(f"**Geçmiş Dönem Özkaynaklar (Özsermaye):**", value=None, placeholder="Özkaynaklar (Özsermaye) tutarını bu alana yazın") #{float(ozkaynaklar1):,.0f}")
  #c22 = float((ozkaynaklar_2).replace(",", "."))
  #st.write("Gelecek Özkaynak Tahmini Miktarı", c22)
  #islem_1 = st.selectbox("Gelecek Özkaynak Tahmini Miktarı:", ["Gelecek Özkaynak Tahmini Miktarı"])
  #if islem_1 == "Gelecek Özkaynak Tahmini Miktarı":
    #c25 = c8-c22+c8
    #st.write(f"**Gelecek Özkaynak Tahmini Miktarı:** {c25}")
  #else:
    #st.write("Hesaplama Yapılamadı")  

  ### KODUN 2. KISMI BURADAN BAŞLIYOR

  # URL for the initial page
  url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?"

  # Fetch the initial page content
  response = requests.get(url)
  temeldegerler = BeautifulSoup(response.text, "html.parser")

  # Find the tables containing the stock data
  table = temeldegerler.find("tbody", id="temelTBody_Ozet")
  f_oranlar = temeldegerler.find("tbody", id="temelTBody_Finansal")

  sektorkodu = temeldegerler.find("select", id="ddlSektor")

  # Create dictionaries to store stock information
  hisse_sektor = {}
  hisse_oran = {}
  sektor_numara = {}

  # Iterate over the first table to extract stock names and sectors
  for row in table.find_all("tr"):
      cells = row.find_all("td")
      hisse = cells[0].find("a").text.upper()
      sektor = cells[2].text
      hisse_sektor[hisse] = sektor
      ###sektor_output = hisse_sektor[hisse_input]

  # Iterate over the options in the select element
  for option in sektorkodu.find_all("option"):
      # Get the sector row number
      sektor_numarasi = option["value"]
      # Get the sector name
      sektor_ismi  = option.text
      # Add the pair to the dictionary
      sektor_numara[sektor_ismi] = sektor_numarasi

  # Iterate over the second table to extract financial ratios
  for r in f_oranlar.find_all("tr"):
      hucre = r.find_all("td")
      hisse_adi_1 = hucre[0].find("a").text.upper()
      kapanıs = hucre[1].text
      #c3 = float(kapanıs)
      f_k = hucre[2].text
      #c10 = float(fk_value)
      pd_dd = hucre[5].text
      #c11 = float(pd_value)
      hisse_oran[hisse_adi_1] = {"kapanıs": kapanıs, "f_k": f_k, "pd_dd": pd_dd}

  # Get the stock name from the user
  stock_name = hisse_adi #input("Hisse Adı Giriniz: ").upper()

  st.subheader(":one:**:blue[HİSSE VERİLERİ]**", divider='rainbow')
  
  if stock_name:
      # Check if the input is in the dictionary
      if stock_name in hisse_sektor:
          # Get the sector name from the dictionary
          sektor_output = hisse_sektor[stock_name]
          # Display the sector name
          st.write("**SEKTÖR ALANI:**",  sektor_output)
          #print("Sektör Alanı:", sektor_output)
          # Get the sector row number from the dictionary
          sektor_numarasi = sektor_numara[sektor_output]
          # Add the sector row number to the url
          url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/Temel-Degerler-Ve-Oranlar.aspx?sektor="+sektor_numarasi
          # Make a new request with the updated url
          response = requests.get(url)
          temeldegerler = BeautifulSoup(response.text, "html.parser")
          sek_ortalama = temeldegerler.find("sectorArea", id="sectorAreaBigData")
          sek_ortalama = temeldegerler.find("div", id="sectorAreaBigData")
          sek_ortalama_fk = temeldegerler.find("div", "second-item text-right")
          sek_ortalama_pd = temeldegerler.find("div", "fifth-item text-right")
          # Ensure elements are found before extracting values
          if sek_ortalama_fk and sek_ortalama_pd:
              # Get and clean the values
              sek_ortalama_fk_value = sek_ortalama_fk.text.strip().replace(",", ".")
              sek_ortalama_pd_value = sek_ortalama_pd.text.strip().replace(",", ".")

              # Convert to floats
              sek_ortalama_fk_float = float(sek_ortalama_fk_value)
              sek_ortalama_pd_float = float(sek_ortalama_pd_value)

              # Print the results
              #print(sek_ortalama)
              st.write(f"**Sektör F/K Oranı:** {sek_ortalama_fk_float}") #, box=True)
              st.write(f"**Sektör PD/DD Oranı:** {sek_ortalama_pd_float}")#, box=True)
          else:
              print("Error: Elements not found. Check website structure or selectors.")


  # Check if the stock exists in the dictionary
  if stock_name in hisse_oran:
      try:
          # Access the stock data and extract the F/K value
          kapanıs = hisse_oran[stock_name]["kapanıs"].replace(",", ".")
          fk_value = hisse_oran[stock_name]["f_k"].replace(",", ".")  # Format with dots as decimal separators
          pd_value = hisse_oran[stock_name]["pd_dd"].replace(",", ".")
          st.write(f"   :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}") #, box = True)
          st.write(f"**HİSSE F/K ORANI:**  {fk_value}") #, box = True)
          st.write(f"**HİSSE PD/DD ORANI:**  {pd_value}") #, box = True)
                  #print(f"{stock_name} Hisse Fiyatı: {kapanıs}")
          #print(f"{stock_name} F/K Oranı:  {fk_value}")
          #print(f"{stock_name} PD/DD Oranı:  {pd_value}")
          st.subheader(f"**Bilanço Verileri:**", divider='grey')
          st.write(f"**Güncel Dönem Bilanço Verileri:**")
          st.write(f"**:blue[ÖZKAYNAKLAR:]**  {float(ozkaynaklar1):,.0f}") #", box = True)
          st.write(f"**:blue[ÖDENMİŞ SERMAYE:]**  {float(OdenmisSermaye1):,.0f}") #, box = True)
          st.write(f"**:blue[NET DÖNEM KARI:]**  {float(NetDonemKarı1):,.0f}") #, box = True)
          st.write(f"**Geçmiş Dönem Bilanço Verileri:**")
          st.write(f"**ÖZKAYNAKLAR(Bir Önceki Çeyrek):**  {float(ozkaynaklar_3):,.0f}")
          st.write(f"**NET DÖNEM KARI(Bir Önceki Çeyrek):**  {float(NetDonemKarı_3):,.0f}")
          st.write(f"**ÖZKAYNAKLAR(Geçmiş Yıl ):**  {float(ozkaynaklar_2):,.0f}") #", box = True)
          st.write(f"**ÖDENMİŞ SERMAYE(Geçmiş Yıl):**  {float(OdenmisSermaye_2):,.0f}") #, box = True)
          st.write(f"**NET DÖNEM KARI(Geçmiş Yıl):**  {float(NetDonemKarı_2):,.0f}") #, box = True)      
      except KeyError:
          #print("Hisse bulunamadı.") # Stock not found in the dictionary
          st.write("Hisse bulunamadı.")
  else:
      #print("Bir sorun var!")  # Stock not found in any of the dictionaries
      st.write(":red[Veri eksikliği var. Lütfen hisseyi kontrol ediniz!]")
    
  #import streamlit_tags as tags

  #st.write("Hisse Hedef Fiyat Hesaplayıcı")

  # Hisse Fiyatı
  #c3 = st.number_input("Hisse Fiyatı:" )
  #c3 = float(kapanıs)
  c3 = float(kapanıs.replace(",", "."))  # Replace comma with dot

  #c10 = float(st.number_input("Hisse F/K Oranı:"))
  c10 = float(fk_value.replace(",", "."))
  #if c10 != "A/D":
  #  c10 = st.number_input("F/K Değeri Bulunmamaktadır. Lütfen F/K Değeri Giriniz")

  ##if stock_name in hisse_oran:
    #try:
    # fk_value = hisse_oran[stock_name]["f_k"].replace(",", ".")
    ##c10 = float(fk_value.replace(",", "."))
    #except KeyError:
      #print("Hisse bulunamadı.") # Stock not found in the dictionary
      #st.write("F/K Verisi Bulunamadı")
  ##else:
    #print("Bir sorun var!") # Stock not found in any of the dictionaries
    #st.write()
    ##c10 = st.number_input("F/K Değeri Bulunmamaktadır. Lütfen F/K Değeri Giriniz")


  # HİSSE PD/DD ORANI
  #c11 = st.number_input("Hisse PD/DD Oranı: ")
  c11 = float(pd_value)

  # BİST100 /SEKTÖR GÜNCEL F/K ORANI
  #c12 = float(st.number_input("BİST100 / Sektör Güncel F/K Oranı: "))
  c12 = sek_ortalama_fk_float

  # BIST100 / Sektör Güncel P/D Oranı
  #c13 = float(st.number_input("BİST100 / Sektör Güncel PD/DD Oranı:"))
  c13 = sek_ortalama_pd_float

  # Ödenmiş Sermaye
  #c4 = st.number_input("Ödenmiş Sermaye: ")
  c4 = float(OdenmisSermaye1)
  #c4 = ("{float(OdenmisSermaye):,.2f}")
  #c4 = OdenmisSermaye

  # Yıllık Net Kar
  #c7 = st.number_input("Yıllık Net Kar: ")
  c7 = float(NetDonemKarı1.replace(",", "."))
  #c7 = ("{float(NetDonemKarı):,.2f}")
  #c7 = NetDonemKarı
  #c15 = c7*2
  #st.write(c15)

  # Özsermaye
  #c8 = st.number_input("Özsermaye : ")
  c8 = float(ozkaynaklar1)
  #c8 = (f"{float(ozkaynaklar1):,.2f}")
  #c8 = ozkaynaklar1


  # Güncel Piyasa Değeri
  #c9 = st.number_input("Güncel Piyasa Değeri: ")

  # HİSSE HESAPLAYICISI SELECT BOX İLE F/K VE PD/DD ORANLARINA GÖRE HESAPLAMA
  #st.write("**HİSSE HEDEF FİYAT HESAPLAYICI**")
  st.subheader(":two:**HİSSE HEDEF FİYAT HESAPLAYICI**", divider='rainbow')

  #operation = st.selectbox("İşlem Seçimi:", ["F/K Hedef Fiyat", "P/D Hedef Fiyat"])

  # Calculate the target price based on the selected operation
  #if operation == "F/K Hedef Fiyat":
  #  if c10 != 0:
  #    fk_hedef_fiyat = c3 / c10 * c12
  #  else:
  #    fk_hedef_fiyat = 0

  #elif operation == "P/D Hedef Fiyat":
  #  if c11 != 0:
  #    pd_hedef_fiyat = c3 / c11 * c13
  #  else:
  #    pd_hedef_fiyat = 0

  # F/K HEDEF FİYAT VE PD/DD HEDEF FİYAT İŞLEM HESAPLAMALARI
  #if operation == "F/K Hedef Fiyat":
  #  st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
  #  st.write(f"    :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")

  #elif operation == "P/D Hedef Fiyat":
  #  st.write(f":blue[**P/D HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
  #  st.write(f"    :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
  st.write()
  st.write()
  st.write()

  #st.write("Not: Ödenmiş Sermaye, Özsermaye Karlılığı ve Potansiyel Karlılık Hedef Fiyat Hesaplamaları İçin Aşağıdaki Bölümü Kullanın:arrow_down:")
  # MANUEL VERİ GİRİŞİ İLE HEDEF FİYAT HESAPLAMA

  #st.subheader(f":two:** HİSSE HESAPLAMA BÖLÜMÜ**", divider='rainbow')

  #st.write(f"**ÖZKAYNAKLAR:**  {float(ozkaynaklar1):,.0f}") #", box = True)  
  #st.write(f"**ÖDENMİŞ SERMAYE:**  {float(OdenmisSermaye1):,.0f}") #, box = True)
  #st.write(f"**NET DÖNEM KARI:**  {float(NetDonemKarı1):,.0f}")
  
  #st.write(f"**ÖZKAYNAKLAR(Geçmiş Yıl):**  {float(ozkaynaklar_2):,.0f}") #", box = True)
  #st.write(f"**NET DÖNEM KARI(Geçmiş Yıl):**  {float(NetDonemKarı_2):,.0f}") #, box = True)

    # Özsermaye
  c8 = st.number_input(f"**Özkaynaklar (Özsermaye):**", value=None, placeholder="Özkaynaklar (Özsermaye) tutarını bu alana yazın") #{float(ozkaynaklar1):,.0f}")

    # Ödenmiş Sermaye
  c4 = st.number_input("**Ödenmiş Sermaye:**", value=None, placeholder="Ödenmiş Sermaye tutarını bu alana yazın")

    # Yıllık Net Kar
  c7 = st.number_input("**Yıllık Net Kar:**", value=None, placeholder="Yıllık Net Kar tutarını bu alana yazın")
  #with st.sidebar:
    
  operation = st.selectbox(":blue[**HİSSE FİYAT HESAPLAMARI İÇİN İŞLEM SEÇİN:**]", ["İŞLEM SEÇİN", "F/K HEDEF FİYAT", "PD/DD HEDEF FİYAT", "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT", "ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT", "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER"])
  #if operation == "Tüm Hedef Fiyatları Göster":
  if operation == "İŞLEM SEÇİN":
    st.write(f"İŞLEM SEÇİN")
    #st.write(f":red[Aşağıdaki kırmızı uyarı yazısı veriler girilmediği için çıkmaktadır. Lütfen verileri girip yapmak istediğiniz işlemi seçin.]")

  elif operation == "F/K HEDEF FİYAT":
    if c10 != 0:
      fk_hedef_fiyat = c3 / c10 * c12
    else:
      fk_hedef_fiyat = 0
    st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
    st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")

  elif operation == "PD/DD HEDEF FİYAT":
    if c11 != 0:
      pd_hedef_fiyat = c3 / c11 * c13
    else:
      pd_hedef_fiyat = 0
    st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
    st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")

  elif operation == "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT":
    if c4 != 0:
      odenmis_hedef_fiyat = (c7 / c4) * c10
    #else:
      #odenmis_hedef_fiyat = 0
      st.write(f":blue[ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:] {odenmis_hedef_fiyat:,.2f}")
      st.write(f"   :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
  #elif operation == "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT":
    #st.write(f"ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT: {odenmis_hedef_fiyat:,.2f}")
      st.write(f":red[Not: Hisse verilerini kontrol ediniz. Eksik veri nedeniyle altta kırmızı alanda hata mesajı çıkmaktadır]")
  elif operation == "ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT":
    #if c10 != 0:
    ozsermaye_hf = (c7/c8)*10/c11*c3
    st.write(f":blue[ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT]: {ozsermaye_hf:,.2f}")
    st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
    st.write(f":red[Not: Hisse verilerini kontrol ediniz. Eksik veri nedeniyle altta kırmızı alanda hata mesajı çıkmaktadır]")
  elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
    c21 = (c7*7)+(c8*0.5)
    potansiyel_fiyat = c21/c4
    st.write(f":blue[**POTANSİYEL DEĞERİNE GÖRE HİSSE FİYATI:**] {potansiyel_fiyat:,.2f}")
    #st.write(f":red[Not: Hisse verilerini kontrol ediniz. Eksik veri nedeniyle altta kırmızı alanda hata mesajı çıkmaktadır]")
  #operation = st.selectbox("[ORTALAMA HEDEF FİYAT]")
    fk_hedef_fiyat = c3 / c10 * c12
    pd_hedef_fiyat = c3 / c11 * c13
    ozsermaye_hf = (c7/c8)*10/c11*c3
    odenmis_hedef_fiyat = (c7 / c4) * c10
    c21 = (c7*7)+(c8*0.5)
    potansiyel_fiyat = c21/c4
    ortalama_hesap = ( fk_hedef_fiyat + pd_hedef_fiyat + odenmis_hedef_fiyat + ozsermaye_hf + potansiyel_fiyat ) / 5
  #if operation == "ORTALAMA HEDEF FİYAT":
  #st.write(ortalama_hesap)
  #if ortalama_hesap < kapanıs :
    #st.write(f":blue[**TÜM HESAPLAMALARIN ORTALAMA FİYATI:**] {ortalama_hesap:,.2f}")
  #else :
    #st.write(f"**TÜM HESAPLAMALARIN ORTALAMA FİYATI:** :green[{ortalama_hesap:,.2f}]")
  #elif operation == "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER":
    st.write(f":blue[**F/K HEDEF FİYAT:**] {fk_hedef_fiyat:,.2f}")
    st.write(f":blue[**PD/DD HEDEF FİYAT:**] {pd_hedef_fiyat:,.2f}")
    st.write(f":blue[**ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT:**] {odenmis_hedef_fiyat:,.2f}")
    st.write(f":blue[**ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT**]: {ozsermaye_hf:,.2f}")
    st.write(f":chart:**:blue[TÜM HESAPLAMALARIN ORTALAMA FİYATI:]** {ortalama_hesap:,.2f}")
    st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
   

else:
  st.write(":arrow_up:","Lütfen Yukarıdaki Alana Hisse Yazınız",":arrow_up:")
  st.write("(Not: Bankalar İşleme Dahil Değildir)")



    #if __name__ == "__main__":
    #  st.run()


#!streamlit run deneme.py & npx localtunnel --port 8501