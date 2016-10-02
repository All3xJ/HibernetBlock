import urllib.request
import re
import os
import time
import random
import ipaddress
from bs4 import BeautifulSoup

# dichiarazione della lista degli useragents per evitare che il sito ci blocchi per le numerose richieste
useragents=["Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
			"Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
			"Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
			"Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
			"Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
			"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
			"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
			"Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.1 (KHTML, like Gecko) Maxthon/3.0.8.2 Safari/533.1",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
			"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
			"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7",
			"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",]

# siti creati con blogspot che hanno la stessa struttura
burls = ["http://sslproxies24.blogspot.it/", "http://proxyserverlist-24.blogspot.it/", "http://newfreshproxies24.blogspot.it/",
		"http://irc-proxies24.blogspot.it/", "http://getdailyfreshproxy.blogspot.it/", "http://www.proxyocean.com/",
		"http://www.socks24.org/",]

# urls vari
nurls = ["http://www.aliveproxy.com/socks5-list/", "http://www.aliveproxy.com/high-anonymity-proxy-list/", "http://www.aliveproxy.com/anonymous-proxy-list/",
		"http://www.aliveproxy.com/fastest-proxies/", "http://www.aliveproxy.com/us-proxy-list/", "http://www.aliveproxy.com/gb-proxy-list/",
		"http://www.aliveproxy.com/fr-proxy-list/", "http://www.aliveproxy.com/de-proxy-list/", "http://www.aliveproxy.com/jp-proxy-list/",
		"http://www.aliveproxy.com/ca-proxy-list/", "http://www.aliveproxy.com/ru-proxy-list/", "http://www.aliveproxy.com/proxy-list-port-80/",
		"http://www.aliveproxy.com/proxy-list-port-81/", "http://www.aliveproxy.com/proxy-list-port-3128/", "http://www.aliveproxy.com/proxy-list-port-8000/",
		"http://www.aliveproxy.com/proxy-list-port-8080/", "http://webanetlabs.net/publ/24", "http://www.proxz.com/proxy_list_high_anonymous_0.html",
		"http://free-proxy-list.net/", "https://www.socks-proxy.net/", "https://incloak.com/proxy-list/", "https://incloak.com/proxy-list/?start=64#list",
		"https://incloak.com/proxy-list/?start=128#list", "https://incloak.com/proxy-list/?start=192#list", "https://incloak.com/proxy-list/?start=256#list",
		"https://incloak.com/proxy-list/?start=320#list", "https://incloak.com/proxy-list/?start=384#list", "https://incloak.com/proxy-list/?start=448#list",
		"https://incloak.com/proxy-list/?start=512#list", "https://incloak.com/proxy-list/?start=576#list", "https://incloak.com/proxy-list/?start=640#list",
		"https://incloak.com/proxy-list/?start=704#list", "http://www.gatherproxy.com/", "http://sockslist.net/proxy/server-socks-hide-ip-address#proxylist",
		"http://sockslist.net/proxy/server-socks-hide-ip-address/2#proxylist", "http://sockslist.net/proxy/server-socks-hide-ip-address/3#proxylist", "http://sockslist.net/proxy/server-socks-hide-ip-address/4#proxylist",
		"http://skypegrab.net/proxy/http.txt", "http://skypegrab.net/proxy/socks.txt", "http://xseo.in/proxylist",
		"http://spys.ru/proxies/", "http://proxyb.net/",]

def initcheck():
	if os.getuid() != 0: # controlla se e' stato eseguito come root
		print("You need to run this program as root.\n\n") # printa questo
		exit(0) # se come utente normale, esce dal programma
	else: # se come root, continua e va avanti
		pass

	if os.path.isfile("/sbin/ipset"): # controlla se ipset e' installato sul sistema
		varchoice() # e va alla prossima funzione
	else: # altrimenti cerca di installarlo (non e' detto che ci riesca)
		try:
			os.system("apt-get install ipset") # per debian-based
			varchoice()
		except OSError:
			try:
				os.system("pacman -S ipset") # per arch-based
				varchoice()
			except OSError:
				try:
					os.system("dnf install ipset") # per redhat based
					varchoice()
				except OSError: # se non riesce a installarlo da solo, printa che bisogna installarlo
					print ("You need to install ipset.\n")
					exit(0) # ed esce dal programma

def varchoice():
	global choice1
	global choice2
	global choice3
	global refreshsec

	choice1 = input ("\nDo you want to implement some basic iptables rules to prevent DoS? (Y/n): ")
	if choice1 == "y" or choice1 == "Y": # se si risponde si, implementa delle rules di base
		os.system("iptables -F") # flusha tutte le rules di iptables
		# Limita il nuovo traffico sulla porta 80
		os.system("iptables -A INPUT -p tcp --dport 80 -m state --state NEW -m limit --limit 25/minute --limit-burst 100 -j ACCEPT")
		# Limita il traffico stabilito
		os.system("iptables -A INPUT -m state --state RELATED,ESTABLISHED -m limit --limit 25/second --limit-burst 25 -j ACCEPT")
		# Rifiuta i pacchetti spoofati
		os.system("iptables -A INPUT -s 10.0.0.0/8 -j DROP")
		os.system("iptables -A INPUT -s 169.254.0.0/16 -j DROP")
		os.system("iptables -A INPUT -s 224.0.0.0/4 -j DROP")
		os.system("iptables -A INPUT -d 224.0.0.0/4 -j DROP")
		os.system("iptables -A INPUT -s 240.0.0.0/5 -j DROP")
		os.system("iptables -A INPUT -d 240.0.0.0/5 -j DROP")
		os.system("iptables -A INPUT -s 0.0.0.0/8 -j DROP")
		os.system("iptables -A INPUT -d 0.0.0.0/8 -j DROP")
		os.system("iptables -A INPUT -d 239.255.255.0/24 -j DROP")
		os.system("iptables -A INPUT -d 255.255.255.255 -j DROP")
		# Ferma gli attacchi smurf
		os.system("iptables -A INPUT -p icmp -m icmp --icmp-type address-mask-request -j DROP")
		os.system("iptables -A INPUT -p icmp -m icmp --icmp-type timestamp-request -j DROP")
		# Butta tutti i pacchetti invalidi
		os.system("iptables -A INPUT -m state --state INVALID -j DROP")
		os.system("iptables -A FORWARD -m state --state INVALID -j DROP")
		os.system("iptables -A OUTPUT -m state --state INVALID -j DROP")
		# Blocca i tentativi di RST attack
		os.system("iptables -A INPUT -p tcp -m tcp --tcp-flags RST RST -m limit --limit 2/second --limit-burst 2 -j ACCEPT")
	elif choice1 == "n" or choice1 == "N": # altrimenti va avanti
		os.system("iptables -F") # flushando solamente le rules di iptables e non aggiungendone nessuna
	else: # se si commette un errore di battitura
		print ("")
		exit(0) # esce dal programma

	try: # set del time di refresh del download dei proxy.
		refresh = int(input ("\nSet the time of proxies download refresh in minutes (5): "))
		refreshsec = refresh * 60 # conversione in secondi
	except: # il default e' 5 min se si commettono errori di battitura
		print ("5 minutes set!")
		refreshsec = 5 * 60

	choice2 = input ("\nDo you want to block also tor-exit-nodes? (y/N): ") # la scelta del blocco dei tor-exit-nodes
	if choice2 == "y" or choice2 == "Y":
		pass # per adesso non fa niente... poi ci occuperemo di questa choice2
	elif choice2 == "n" or choice2 == "N":
		pass # per adesso non fa niente... poi ci occuperemo di questa choice2
	else: # se si e' commesso un errore di battitura
		print ("")
		exit(0) # esce

	choice3 = input ("\nDo you want to start protection? (Y/n): ")
	if choice3 == "y" or choice3 == "Y" or choice3 == "":
		print ("")
		loop() # se si digita si va al loop
	elif choice3 == "n" or choice3 == "N":
		print("")
		exit(0) # altrimenti esce
	else:
		print ("")
		exit(0) # altrimenti esce

def valid_ip(ip): # funzione per il check di validita' degli ip visto che alcuni ip che si grabban non lo sono
    try: # se
        ipaddress.IPv4Address(ip) # la libreria ipaddress processa quell'ip
    except ipaddress.AddressValueError: # e visualizza un errore
        return False # allora si elimina quell'ip
    else: # altrimenti l'ip e' vero e si lascia
        return True # con il return True

def inforgeget(): # funzione dedicata solo al sito inforge.net che ha un meccanismo diverso
	try:
		req = urllib.request.Request("https://www.inforge.net/xi/forums/liste-proxy.1118/") # composizione req
		req.add_header("User-Agent", random.choice(useragents)) # scelta useragent random
		soup = BeautifulSoup(urllib.request.urlopen(req, timeout = 10)) # apertura url e trasformazione in "zuppa" del sourcecode
		print ("\nDownloading from inforge.net in progress...")
		base = "https://www.inforge.net/xi/" # la base dei link, ci servira' piu' sotto
		for tag in soup.find_all("a", {"class":"PreviewTooltip"}):
			links = tag.get("href") # trova i links
			final = base + links # tutti i link trovati
			result = urllib.request.urlopen(final) # apre i links
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # trova ip proxies
				ipf = list(filter(lambda x: x if not x.startswith("1.5.") else None, ip)) # non grabba il "falsoip" che spunta sempre e che comincia con 1.5
				if ipf: # se trova ip
					for x in ipf:
						if valid_ip(x): # e l'ip e' valido dopo averlo processato nella funzione valid_ip
							ipfinal = x # allora ipfinal si prende l'ip
							out_file = open("blacklist.txt","a")
							while True:
								out_file.write(x+"\n") # scrive ip trovati
								out_file.close()
								break # quando finisce ferma il ciclo
	except: # se succede qualcosa di brutto
		print("An error occurred, skipping to the next website.")

def blogspotget(url): # anche questa funzione scarica proxy pero' dai siti blogspot
	try:
		soup = BeautifulSoup(urllib.request.urlopen(url)) # per strasformare in "zuppa" la source del sito
		for tag in soup.find_all("h3", "post-title entry-title"): # trova nel source la parte riguardante le proxylist
			links = tag.a.get("href")                             # prende i link delle proxylist
			result = urllib.request.urlopen(links)                # finalmente apre i link trovati
			for line in result :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # cerca gli ip:porta nelle pagine
				if ip: # se ha trovato gli ip prosegue
					for x in ip:
						if valid_ip(x): # se l'ip e' valido
							ipfinal = x # se lo prende ipfinal
							out_file = open("blacklist.txt","a") # scrittura singolo ip nella proxy.txt
							while True:
								out_file.write(x+"\n") # scrive ip uno per uno nel file blacklist.txt
								out_file.close()
								break # il ciclo si ferma non appena ha finito
	except: # se qualcosa va storto
		print("An error occurred, skipping to the next website.") # printa questo

def proxyget(url):
	try:
		req = urllib.request.Request(url) # url corrispondente a una serie di urls impostati sotto.
		req.add_header("User-Agent", random.choice(useragents)) # aggiunge uno user agent a caso dalla lista sopra
		sourcecode = urllib.request.urlopen(req, timeout = 10) # scaricamento sourcecode pagina + timeout impostato a 10
		for line in sourcecode :
				ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # cerca ip proxy
				ipf = list(filter(lambda x: x if not x.startswith("0.") else None, ip)) # evita di cattutrare anche ip inutili
				if ipf: # se trova ip prosegue
					for x in ipf:
						if valid_ip(x): # se l'ip e' valido
							ipfinal = x # se lo prende ipfinal
							out_file = open("blacklist.txt","a")
							while True:
								out_file.write(x+"\n") # scrive ip uno per uno nel file blacklist.txt
								out_file.close()
								break # appena finisce ferma il ciclo
	except:
		print("An error occurred, skipping to the next website.")

def proxylist(): # funzione per la creazione della proxylist
	global proxies
	print ("\nSetting up the blacklist...")
	entries = open("blacklist.txt").readlines() # la lista txt presenta doppioni, quindi:
	proxiesp = {tuple(x.strip().split(':')) for x in entries} # prima trasforma la lista in tupla
	proxies = list(set(proxiesp)) # e poi leva i doppioni
	print ("\nBlacklist Updated!\n")

def loop(): # funzione effettiva del programma.
	global url
	while True: # il ciclo infinito
		try:

			out_file = open("blacklist.txt","w") # prima di tutto
			out_file.write("") # cancella il contenuto precedente della blacklist.txt
			out_file.close()

			inforgeget() # all'inizio scarica da inforge
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines()))) # questa riga consente di visualizzare il numero di ip trovati

			if choice2 == "y": # se si e' scelto di bloccare i tor-exit-nodes esegue il procedimento
				print ("\nDownloading from torstatus.rueckgr.at in progress...")
				url = "https://torstatus.rueckgr.at/index.php?SR=Uptime&SO=Desc" # imposto url sito exit nodes
				try:
					proxyget(url) # e lo manda a proxyget
					print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
				except: # a volte fa capricci
					try:
						proxyget(url) # e lo manda a proxyget
						print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
					except:
						try:
							proxyget(url) # e lo manda a proxyget
							print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
						except: # se in questi 3 tentativi non riesce allora printa che non e' riuscito e passa al next download
							print ("Tor exit nodes download failed.")
			else: # altrimenti lo passa
				pass

			print ("\nDownloading from blogspot in progress...")
			for position, url in enumerate(burls): # enumerate serve per numerare appunto il numero del sito corrente
				blogspotget(url) # manda url a blogspotget
				print("Completed downloads: (%s/%s)\nCurrent IPs in blacklist: %s" % (position+1, len(burls), len(open("blacklist.txt").readlines())))

			print ("\nDownloading from various mirrors in progress...")
			for position, url in enumerate(nurls):
				proxyget(url)
				print("Completed downloads: (%s/%s)\nCurrent IPs in blacklist: %s" % (position+1, len(nurls), len(open("blacklist.txt").readlines())))

			print ("\nDownloading from proxymore in progress...")
			proxymore = ['http://www.proxymore.com/proxy-list-%d.html' % n for n in range(1, 15)] # per prendere ip di tutte e 15 le pagine
			for position, url in enumerate(proxymore):
				proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			print ("\nDownloading from foxtools in progress...")
			foxtools = ['http://api.foxtools.ru/v2/Proxy.txt?page=%d' % n for n in range(1, 6)] # per prendere ip di tutte e 6 le pagine
			for position, url in enumerate(foxtools):
				proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			print ("\nDownloading from nntime in progress...")
			numbers = ["01","02","03","04","05","06","07","08","09",] # i numeri del nome della pagina web
			for n in numbers:
				nntime = ("http://nntime.com/proxy-updated-%s.htm" % n)
				proxyget(nntime)
				print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			nntime = ("http://nntime.com/proxy-updated-%s.htm" % n for n in range(10, 31)) # e da 10 in poi sono numeri senza 0 davanti quindi procede normalmente
			proxyget(nntime)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			print ("\nDownloading from proxylistplus in progress...")
			url = "http://list.proxylistplus.com/Fresh-HTTP-Proxy"
			proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			proxylistplus = ['http://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%s' % n for n in range(2, 6)] # per prendere tutti ip dalla pagina 2 a 6
			for position, url in enumerate(proxylistplus):
				proxyget(url)
			print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))

			proxylist() # e alla fine esegue questa funzione che crea la lista

			print ("\nImporting Blacklisted IPs... (It can take a while)\n")
			os.system("ipset create evil_ips iphash -!") # qua creiamo il table "evil_ips" e il comando -! serve per non dare l'output degli errori
			os.system("ipset flush evil_ips -!") # qua flusha tutti i vecchi ip salvati su evil_ips
			for proxy in proxies:
				os.system("ipset add evil_ips %s -!" % (proxy)) # qua mette tutti i proxy scaricati su evil_ips
			os.system("iptables -A INPUT -m set --match-set evil_ips src -j DROP") # inserimento degli ip blacklisted sia nell'INPUT
			os.system("iptables -A OUTPUT -m set --match-set evil_ips dst -j DROP")
			os.system("iptables -A FORWARD -m set --match-set evil_ips src -j DROP") # sia nel FORWARD
			os.system("iptables -A FORWARD -m set --match-set evil_ips dst -j DROP")
			print ("\nBlacklisted IPs Imported!")
			print ("\nSleeping for the time set.")
			time.sleep(refreshsec) # aspetta per il tempo stabilito prima (refreshsec), e ricomincia :D
			print ("\n\nRestarting cycle...")

		except KeyboardInterrupt: # se si chiude il programma con Ctrl+C
			choice3 = input ("\nDo you want to flush iptables rules? (y/n): ")
			if choice3 == "y" or choice3 == "Y": # se si decide di flushare
				print ("\nFlushing iptables before exit...\n")
				os.system("iptables -F") # flusha tutte le rules di iptables
				os.system("ipset flush evil_ips") # e le tavole di ipset
				exit(0) # e si chiude.
			elif choice3 == "n" or choice3 == "N": # se non si vuole flushare
				print ("")
				exit(0) # esce
			else: # se si digita male
				print ("")
				exit(0) # esce


print ("\n\nWARNING: This program will erase ALL current iptables rules.")
print ("TIP: Press Ctrl+C during sleeping time to exit and flush iptables rules.\n")
initcheck() # per far partire la funzione loop() e quindi il programma
