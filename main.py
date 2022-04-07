import pytube  # youtube videolarını indirmek için gerekli kütüphane
from selenium import webdriver  # veri kazıma yapmak için gerekli kütüphane
from bs4 import BeautifulSoup  # veri/tag/etiket bulmak için gerekli kütüphane
import moviepy.editor as mp  # mp3'e eçvirmek için gerekli kütüphane
import time  # time sleep vermek için ekledik
import re
import os  # dosya işlemleri için ekledik
import shutil  # dosyaları taşımamızı sağlayan kütüphanemiz
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip  # kırpma yapmak için gerekli kütüphane

dosyaIsmi = "kemence"  # Oluşturulacak Dosya Adı Ve Eklenecek Klasör İsmi
Url = 'https://www.youtube.com/results?search_query=kemence+instrument&sp=EgQQARgB'
time_sleep = 10  # sistemi duraklatmak istediğimiz süre(saniye cinsinden)

# region linkleri toplama ve indirme kısmı
def main():
    driver = webdriver.Chrome(executable_path=R"C:\Users\YakupAkdin\PycharmProjects\chromedriver.exe")
    driver.get(Url)
    time.sleep(time_sleep)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, 'html.parser')
    titles = soup.findAll('a', id='video-title')
    print(len(titles))
    i = 1
    for tags in titles:
        link = ('https://www.youtube.com' + tags['href'])  # video yolunu değişkene atıyoruz
        # print(tags['href'])

        yt = pytube.YouTube(link)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        try:
            stream.download()
            print(i, ". Dosya İndirildi : ", link)
            i += 1
        except:
            print('İndirmede Sorun Oluştu ', link)
# endregion
# region kaynak yolu oluşturma ve dosyaya ekleme kısmı
def kaynak():
    kaynakYolu = './'
    sourceFiles = os.listdir(kaynakYolu)
    indirmeDosyasi = dosyaIsmi
    CHECK_FOLDER = os.path.isdir(indirmeDosyasi)

    if not CHECK_FOLDER:
        os.mkdir(indirmeDosyasi)
        print("Klasör Oluşturuldu.")
    else:
        print(indirmeDosyasi, " Adlı Klasör Zaten Oluşturuldu.")
    hedef = './' + dosyaIsmi

    for file in sourceFiles:
        if file.endswith('.mp4'):
            shutil.move(os.path.join(kaynakYolu, file), os.path.join(hedef, file))  # dosyayı taşıyan kısım
            print(file, ",", indirmeDosyasi, " İsimli Klasöre Eklendi")


# endregion
# region mp3'e dönüştürülen kısmı
def convert_to_mp3():
    folder = "./" + dosyaIsmi

    for file in os.listdir(folder):
        if re.search('mp4', file):
            mp4_path = os.path.join(folder, file)
            mp3_path = os.path.join(folder, os.path.splitext(file)[0] + '.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)


# endregion
# region 10 saniyelik kırpma yapan kısım
def cut_the_mp3():
    folder = "./" + dosyaIsmi
    for file in os.listdir(folder):
        if re.search('mp3', file):
            print(file)
            add = os.path.splitext(file)[0]
            ffmpeg_extract_subclip(os.path.join(folder, file), 3, 13,
                                   targetname=os.path.join(folder, add + "_exctract.mp3"))
            os.remove(os.path.join(folder, file))


# endregion


main()
kaynak()
convert_to_mp3()
cut_the_mp3()
