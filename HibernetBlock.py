import urllib.request, re, os, time, random
from bs4 import BeautifulSoup


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


def initcheck():
	if os.getuid() != 0: # controlla se e' stato eseguito come root
		print("You need to run this program as root.\n")
		exit(0) # se come utente normale, esce dal programma
	else: # se come root, continua e va avanti
		pass

	if os.path.isfile("/sbin/ipset"): # controlla se ipset e' installato sul sistema
		varchoice()
	else: # altrimenti cerca di installarlo (non e' detto che ci riesca)
		try:
			os.system("apt-get install ipset")
			varchoice()
		except OSError:
			try:
				os.system("pacman -S ipset")
				varchoice()
			except OSError:
				try:
					os.system("dnf install ipset")
					varchoice()
				except OSError: # se non riesce a installarlo da solo, printa che si deve installare
					print ("You need to install ipset.\n")
					exit(0)

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
		os.system("iptables -F") # flush rules iptables
	else:
		print ("")
		exit(0)

	try: # set del time di refresh del download dei proxy.
		refresh = int(input ("\nSet the time of proxies download refresh in minutes (5): "))
		refreshsec = refresh * 60 # conversione in secondi
	except: # il default e' 5 min
		print ("5 minutes set!")
		refreshsec = 5 * 60

	choice2 = input ("\nDo you want to block also tor-exit-nodes? (y/N): ") # la scelta del blocco dei tor-exit-nodes
	if choice2 == "y" or choice2 == "Y":
		pass
	elif choice2 == "n" or choice2 == "N":
		pass
	else:
		print ("")
		exit(0)

	choice3 = input ("\nDo you want to start protection? (Y/n): ")
	if choice3 == "y" or choice3 == "Y":
		loop()
	elif choice3 == "n" or choice3 == "N":
		print("")
		exit(0)
	else:
		print ("")
		exit(0)

def proxyget():
	req = urllib.request.Request(url) # url corrisponde a una serie di urls impostati sotto.
	req.add_header("User-Agent", random.choice(useragents)) # aggiunge uno user agent a caso dalla lista sopra
	sourcecode = urllib.request.urlopen(req, timeout = 10) # scaricamento sourcecode pagina + timeout impostato a 10
	for line in sourcecode :
			ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # cerca ip proxy
			ipf = list(filter(lambda x: x if not x.startswith("0.") else None, ip)) # evita di cattutrare anche ip inutili
			ipff = list(filter(lambda x: x if not x.startswith("985.") else None, ipf)) # evita di cattutrare anche ip inutili #2
			ipfff = list(set(ipff)) # cancella i doppioni
			if ipfff: # se trova ip prosegue
				for x in ipfff:
					out_file = open("blacklist.txt","a")
					while True:
						out_file.write(x+"\n") # scrive ip uno per uno nel file blacklist.txt
						out_file.close()
						break # appena finisce ferma il ciclo

def inforgeget(): # funzione dedicata solo al sito inforge.net che ha un meccanismo diverso
	req = urllib.request.Request("https://www.inforge.net/xi/forums/liste-proxy.1118/")
	req.add_header("User-Agent", random.choice(useragents))
	print ("\nIGNORE THIS WARNING:")
	soup = BeautifulSoup(urllib.request.urlopen(req, timeout = 10)) # trasformazione in "zuppa" del sourcecode
	print ("\nDownloading from inforge.net in progress...")
	base = "https://www.inforge.net/xi/"
	for tag in soup.find_all("a", {"class":"PreviewTooltip"}):
		links = tag.get("href") # trova i links
		final = base + links # tutti i link trovati
		result = urllib.request.urlopen(final) # apre i links
		for line in result :
			ip = re.findall("(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})", str(line)) # trova ip proxies
			ipf = list(filter(lambda x: x if not x.startswith("1.5.") else None, ip)) # non grabba il "falsoip" che spunta sempre e che comincia con 1.5
			if ipf: # se trova ip
				for x in ipf:
					out_file = open("blacklist.txt","a")
					while True:
						out_file.write(x+"\n") # scrive ip trovati
						out_file.close()
						break # quando finisce ferma il ciclo

def proxylist():
	global proxies
	entries = open("blacklist.txt").readlines()
	proxies = [x.strip().split(":") for x in entries] # crea la lista di tutti i proxy raccolti
	print ("\nBlacklist Updated!\n")

def loop():
	while True:
		try:
			global url
			out_file = open("blacklist.txt","w")
			out_file.write("")
			out_file.close()

			try:
				inforgeget() # all'inizio scarica da inforge
				print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except: # se si verifica un errore printa questa scritta:
				print("An error occurred, skipping to the next website.")
			if choice2 == "y": # se si è scelto di bloccare i tor-exit-nodes esegue il procedimento
				url = "https://torstatus.rueckgr.at/index.php?SR=Uptime&SO=Desc" # imposto url sito exit nodes
				try:
					print ("\nDownloading from torstatus.rueckgr.at in progress...")
					proxyget()
					print("Current IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
				except:
					print("An error occurred, skipping to the next website.")
			else: # altrimenti lo passa
				pass
			url = "http://free-proxy-list.net/"
			try:
				proxyget()
				print("\nCompleted downloads: (3/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://www.socks-proxy.net/"
			try:
				proxyget()
				print("Completed downloads: (4/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/"
			try:
				proxyget()
				print("Completed downloads: (5/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=64#list"
			try:
				proxyget()
				print("Completed downloads: (6/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=128#list"
			try:
				proxyget()
				print("Completed downloads: (7/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=192#list"
			try:
				proxyget()
				print("Completed downloads: (8/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=256#list"
			try:
				proxyget()
				print("Completed downloads: (9/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=320#list"
			try:
				proxyget()
				print("Completed downloads: (10/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=384#list"
			try:
				proxyget()
				print("Completed downloads: (11/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=448#list"
			try:
				proxyget()
				print("Completed downloads: (12/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=512#list"
			try:
				proxyget()
				print("Completed downloads: (13/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=576#list"
			try:
				proxyget()
				print("Completed downloads: (14/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=640#list"
			try:
				proxyget()
				print("Completed downloads: (15/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "https://incloak.com/proxy-list/?start=704#list"
			try:
				proxyget()
				print("Completed downloads: (16/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "http://www.gatherproxy.com/"
			try:
				proxyget()
				print("Completed downloads: (17/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "http://sockslist.net/proxy/server-socks-hide-ip-address#proxylist"
			try:
				proxyget()
				print("Completed downloads: (18/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "http://sockslist.net/proxy/server-socks-hide-ip-address/2#proxylist"
			try:
				proxyget()
				print("Completed downloads: (19/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "http://sockslist.net/proxy/server-socks-hide-ip-address/3#proxylist"
			try:
				proxyget()
				print("Completed downloads: (20/21)\nCurrent IPs in blacklist: %s" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next website.")
			url = "http://sockslist.net/proxy/server-socks-hide-ip-address/4#proxylist"
			try:
				proxyget()
				print("Completed downloads: (21/21)\nCurrent IPs in blacklist: %s\n" % (len(open("blacklist.txt").readlines())))
			except:
				print("An error occurred, skipping to the next phase.\n")

			proxylist() # e alla fine esegue questa funzione che crea la lista

			print ("\nImporting Blacklisted IPs...\n")
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
			elif choice3 == "n" or choice3 == "N":
				print ("")
				exit(0)
			else:
				print ("")
				exit(0)


print ("\n\nWARNING: This program will erase ALL current iptables rules.")
print ("TIP: Press Ctrl+C during sleeping time to exit and flush iptables rules.\n")
initcheck() # per far partire la funzione loop() e quindi il programma
