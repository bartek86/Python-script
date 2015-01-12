#!/usr/bin/python

# Program zapisujący do pliku osoby występujące w polskojęzycznej wikipedii 
# na podstawie listy imion
#
# autor: Bartlomiej Lesniak
#
# Program zapisuje w liscie imiona z pliku txt. 
# Crawler przeszukuje serwis Wikipedia zapisujac wszystkie linki do odwiedzenia
# a jednoczesnie sprawdza czy w tytule strony znajduje sie wyraz bedacy w liscie imion.
# Każda osoba wystepujaca w wikipedii jest hasłem i posiada własną stronę, dlatego wystarczy
# przeszukiwac tytuly stron w tagach <title>.
# Odnalezione osoby sa zapisywane w slowniku, nastepnie sortowane i zapisywane do pliku.
#
# Wady programu:
# długi czas działania(100 osób/godzinę) (możliwa poprawa poprzez pomijanie nieznaczących linków np. obrazy img,png)
#
# anomalie w wynikach: 
#	kłopot z osobami mającymi liczbę w tytule np. Jan Paweł II 
#	kłopot z nazwiskami wieloczłonowymi np. Boy-Żeleński
#	wyświetlanie haseł mającymi imię w nazwie np. tytuły książek jak "Harry Potter"

import urllib
import re
import urlparse

url = 'http://pl.wikipedia.org/wiki/'
#--pobranie imion z pliku do listy-----------------------------

f=open("imiona.txt","r")
imiona = []
line=f.readline()
  
while line!="":
  n_line=line.strip('\n')
  imiona.append(n_line)
  line = f.readline()
  ###
f.close()
print("Lista imion pobrana")

#---robot przedgladajacy,tworzy liste stron---

urls = [url]
visited = [url]
link = re.compile(r'href="(.*?)"')          #wyrazenia regularne dla szukanych elementow
obraz = re.compile(r'href="(.*?)jpg"')#|href="(.*?)png"')
title = re.compile(r'<title>(.*?)</title>')
wyraz = re.compile(r'[A-Z][a-z]*')
end=0
t = {}

while len(urls) > 0 and end <= 100:	    #zmienna end - ograniczenie czasu działania
  
  htmltext = urllib.urlopen(urls[0]).read()
  
  urls.pop(0)
  #print len(urls)
  
  links = link.findall(htmltext)            #znalezienie wszystkich linkow
  nazwa = title.search(htmltext).group(0)   #znalezienie tytulu strony
  nazwa = wyraz.findall(str(nazwa))
  nazwa.remove('Wikipedia')                 #usuniecie stalej czesci tytulu wikipedii
                                            
  if nazwa != []:
    if nazwa[0] in imiona:                  #sprawdzenie czy pierwsze slowo w tytule jest imieniem
      nazwisko = nazwa[len(nazwa)-1]  
      imie = ''
      for i in range(len(nazwa)-1):         #formatowanie: nazwisko + imiona
        imie = imie + nazwa[i]+' '
     
      if len(imie) > 0 and nazwisko != 'Wikipedia':
        t.update({nazwisko: imie})            #zapis w slowniku
        end += 1
        print(nazwisko, imie, end)
    ###
  ###
  
  for l in links:
    l = urlparse.urljoin(url,l)             #dolaczenie linku do adresu glownego
                         
    if url in l and l not in visited:       #sprawdzenie czy nie wychodzimy poza link glowny
        urls.append(l)                      #oraz listy odwiedzonych
        visited.append(l)                   #oznacznie linku jako odwiedzonego i dodanie do kolejki
        

#sortowanie i zapis w pliku
sortowanie = sorted(t.items(), key=lambda tup: tup[0])
  
osoby=open("osoby_wikipedia.txt","w")
for k,w in sortowanie:
  os = k + ' ' + w + '\n'
  osoby.write(os)
osoby.close()  
  
  
