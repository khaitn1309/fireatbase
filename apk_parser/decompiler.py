import os
import sys
import shutil
import zipfile
from subprocess import call, DEVNULL
import xml.etree.ElementTree as ET
from core import cli

TOOLS_PATH = "./tools_decompiler/"
android_path  = "./decompiled_android_files/"
jadx_path = "tools_decompiler/jadx/bin/jadx"
DEX2J_PATH = "tools_decompiler/dex2jar/d2j-dex2jar.sh"

# subprocess call
stdout = None
stderr = None
stdout = DEVNULL
stderr = DEVNULL

class Decompiler():

    def __init__(self, file):
        self.file = file
        self.decompile_android_path = "./decompiled_android_files/"


    def decompile_phase_one(self):
        print(f"==> decompiling apk at path: {self.file}")

        if not os.path.exists(self.file):
            print(f"[!] error apk not exists: {self.file} ")
            sys.exit(1)

        apk_name = os.path.splitext(os.path.basename(self.file))[0]
        print(f"==> apk name: {apk_name}")

        if os.path.exists(android_path):
            print(f"==> android path found! {android_path}")
            self.decompile_phase_two(apk_name)
        else:
            print(f"[+] creating directory: [{android_path}]")
            os.makedirs(android_path)


    def decompile_phase_two(self, apk_name):
        print("[**] starting phase two..")
        self.unpacking(apk_name)
        self.generate_jar(apk_name)
        self.get_firebase_remote_config(apk_name)

    def unpacking(self, apk_name):
        print("==> unpacking files..")
        call([jadx_path, self.file])
        unpack_files = apk_name + "/"
        shutil.move(unpack_files, android_path)


    def generate_jar(self,apk_name):
            print("=> generate jar file..")
            dex_classes_path = android_path + apk_name + "/resources/" + "classes.dex"
            call([DEX2J_PATH, dex_classes_path])
            jar_file = "classes-dex2jar.jar"
            jar_file_new_name = apk_name + ".jar"
            os.rename(jar_file, jar_file_new_name)
            shutil.move(jar_file_new_name, android_path)

    def get_firebase_remote_config(self,apk_name):
        api_key = ""
        app_id = ""
        storage_bucket = ""
        firebase_url = ""

        print("=> try to get firebase remote config..")
        try:
            config_path = dex_classes_path = android_path + apk_name + "/resources/res/values/strings.xml"
            xml_tree = ET.parse(config_path)
            root = xml_tree.getroot()
            for data in root:
                if data.attrib['name'] == 'google_api_key':
                    api_key = data.text
                    print(f"[**] api key found: {api_key}\n")
                elif data.attrib['name'] == 'google_app_id':
                    app_id = data.text
                    print(f"[**]: app id found: {app_id}\n")
                elif data.attrib['name'] == 'google_storage_bucket':
                    storage_bucket = data.text
                    print(f"[**] storage bucket found: {storage_bucket}\n")
                elif data.attrib['name'] == 'firebase_database_url':
                    firebase_url = data.text
                    print(f"[**] Firebase URL found: {firebase_url}\n")
                else:
                    pass
        except FileNotFoundError as e:
            print(f"==> Erro while parsing the file at {config_path}:{e}")

        if firebase_url != "":
            fire_url = firebase_url
            cli_object = cli.Core(fire_url)
            cli_object.remote_config(api_key, app_id, storage_bucket)
            cli_object.is_alive()
