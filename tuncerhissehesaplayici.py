
#pip install streamlit

#%%writefile deneme.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd


#streamlit.config.theme.base = "dark"
st.title(":blue[TUNCER YATIRIM]")
st.subheader(":chart::blue[**HİSSE HESAPLAMA UYGULAMASI**]:chart:", divider='rainbow')
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
      OdenmisSermaye = veri[veri['itemDescTr'] == '  Ödenmiş Sermaye']
      OdenmisSermaye = OdenmisSermaye.iloc[0,1]
      NetDonemKarı = veri[veri['itemDescTr'] == 'DÖNEM KARI (ZARARI)']
      NetDonemKarı = NetDonemKarı.iloc[0,1]

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
          st.write(f"**ÖZKAYNAKLAR:**  {float(ozkaynaklar1):,.0f}") #", box = True)
          st.write(f"**ÖDENMİŞ SERMAYE:**  {float(OdenmisSermaye):,.0f}") #, box = True)
          st.write(f"**NET DÖNEM KARI:**  {float(NetDonemKarı):,.0f}") #, box = True)
      except KeyError:
          #print("Hisse bulunamadı.") # Stock not found in the dictionary
          st.write("Hisse bulunamadı.")
  else:
      #print("Bir sorun var!")  # Stock not found in any of the dictionaries
      st.write(":red[Veri eksikliği var. Lütfen hisseyi kontrol ediniz!]")

  st.write(" İş Yatırım Sayfası İçin Tıklayın: [link](https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx)")
  st.write(" Tradingview Grafik Sayfası İçin Tıklayın: [link](https://tr.tradingview.com/chart/)")


  #import streamlit_tags as tags

  #st.write("Hisse Hedef Fiyat Hesaplayıcı")

  # Hisse Fiyatı
  #c3 = st.number_input("Hisse Fiyatı:" )
  #c3 = float(kapanıs)
  c3 = float(kapanıs.replace(",", "."))  # Replace comma with dot

  #c10 = float(st.number_input("Hisse F/K Oranı:"))
  c10 = float(fk_value.replace(",", "."))
  if c10 <= 0:
    st.write("F/K Değeri Bulunmamaktadır!")

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
  c4 = float(OdenmisSermaye)
  #c4 = ("{float(OdenmisSermaye):,.2f}")
  #c4 = OdenmisSermaye

  # Yıllık Net Kar
  #c7 = st.number_input("Yıllık Net Kar: ")
  C7 = float(NetDonemKarı.replace(",", "."))
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
  st.subheader(":one:**HİSSE HEDEF FİYAT HESAPLAYICI**", divider='rainbow')

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


  st.write("Not: Ödenmiş Sermaye, Özsermaye Karlılığı ve Potansiyel Karlılık Hedef Fiyat Hesaplamaları İçin Aşağıdaki Bölümü Kullanın:arrow_down:")
  # MANUEL VERİ GİRİŞİ İLE HEDEF FİYAT HESAPLAMA

  #st.subheader(f":two:** HİSSE HESAPLAMA BÖLÜMÜ**", divider='rainbow')

  st.write(f"**ÖZKAYNAKLAR:**  {float(ozkaynaklar1):,.0f}") #", box = True)
  st.write(f"**ÖDENMİŞ SERMAYE:**  {float(OdenmisSermaye):,.0f}") #, box = True)
  st.write(f"**NET DÖNEM KARI:**  {float(NetDonemKarı):,.0f}")


    # Özsermaye
  c8 = st.number_input(f"**Özkaynaklar (Özsermaye):**", value=None, placeholder="Özkaynaklar (Özsermaye) tutarını bu alana yazın") #{float(ozkaynaklar1):,.0f}")

    # Ödenmiş Sermaye
  c4 = st.number_input("**Ödenmiş Sermaye:**", value=None, placeholder="Ödenmiş Sermaye tutarını bu alana yazın")

    # Yıllık Net Kar
  c7 = st.number_input("**Yıllık Net Kar:**", value=None, placeholder="Yıllık Net Kar tutarını bu alana yazın")


  operation = st.selectbox("İşlem Seçimi:", ["İŞLEM SEÇİN", "F/K HEDEF FİYAT", "PD/DD HEDEF FİYAT", "ÖDENMİŞ SERMAYEYE GÖRE HEDEF FİYAT", "ÖZSERMAYE KARLILIĞINA GÖRE HEDEF FİYAT", "TÜM HESAPLAMALARIN SONUÇLARINI GÖSTER"])
  #if operation == "Tüm Hedef Fiyatları Göster":
  if operation == "İŞLEM SEÇİN":
    st.write(f"İŞLEM SEÇİN")
    st.write(f":red[Aşağıdaki kırmızı uyarı yazısı veriler girilmediği için çıkmaktadır. Lütfen verileri girip yapmak istediğiniz işlemi seçin.]")

  elif operation == "F/K HEDEF FİYAT":
    if c10 != 0:      fk_hedef_fiyat = c3 / c10 * c12
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
    st.write(f" :chart:**:blue[HİSSE FİYATI:]**  {kapanıs}")
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
    st.write(f":red[Not: Hisse verilerini kontrol ediniz. Eksik veri nedeniyle altta kırmızı alanda hata mesajı çıkmaktadır]")


else:
  st.write(":arrow_up:","Lütfen Yukarıdaki Alana Hisse Yazınız",":arrow_up:")
  st.write(":red[(Not: Bankalar İşleme Dahil Değildir)]")

    #if __name__ == "__main__":
    #  st.run()


#!streamlit run deneme.py & npx localtunnel --port 8501
