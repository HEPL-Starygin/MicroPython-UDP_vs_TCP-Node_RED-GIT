import network   #on importe la librairie network 
import usocket as socket
import urequests, ujson #on importe les librairie pour le http 
from machine import Pin #on importe Pin de la librairie machine
import time

tcp_port  = 1882
udp_port  = 1881
server_ip = 'ip'



led = Pin(2, Pin.OUT) #on configure la pin 16 comme sortie (la où est connecté la led)

#Connexion au  WIFI

SSID = 'nom' #nom du wifi 
PASSWORD = 'mdp'       #mdp du wifi 
wlan = network.WLAN(network.STA_IF) #Creer un objet WLAN et l'initialise
wlan.active(True)           #Permet d'activer la connexion

if not wlan.isconnected():  #si on est pas conneccté au wifi
    print('Connecting to Wi-Fi...')  #affiche qu'on se connecte
    wlan.connect(SSID, PASSWORD)     #se connecte au wifi en utilisant ssid et WiFi_pass
    while not wlan.isconnected():    #boucle tant qu'on est pas connecté
        pass
print('Connected to Wi-Fi:', SSID)   #affiche qu'on se connecte

#Pret à recevoir des données

led.value(0)    #Allume la led


def send_tcp_data(data):
    s = socket.socket()  #création d'un objet socket
    addr = socket.getaddrinfo(server_ip, tcp_port)[0][-1] #IP et port TCP
    s.connect(addr) #etablit la connexion 
    s.sendall(str(data).encode()) #envoie les données 
    s.close() #ferme la connexion

def send_udp_data(data): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #création d'un objet socket
    addr = socket.getaddrinfo(server_ip, udp_port)[0][-1] #IP et port UDP
    s.sendto(str(data).encode(), addr) #envoie les données
    s.close() #ferme la connexion

Valeur = 0

while True:
    led.value(0)  # Allume la LED pour indiquer l'envoi de données

    # Envoi des données sur la socket TCP
    try:
        send_tcp_data(Valeur) #envoie la valeur via tcp
        print("TCP: ", Valeur)
    except:
        print("Erreur TCP ")
    # Envoi des données sur la socket UDP
    try:
        send_udp_data(Valeur) #envoie la valeur via udp
        print("UDP: ", Valeur)
    except:
        print("Erreur UDP ")
        
    led.value(1) # Éteint la LED
    time.sleep(0.2)  # Ajoutez un délai en fonction de votre fréquence d'envoi
    Valeur += 1  #incrémentation de la valeur envoyé
      
