from utils import banner,parses
from  apk_parser.decompiler import Decompiler
from core import cli
import argparse



print(banner.banner)
menu = argparse.ArgumentParser(description="[*] Exploit missconfigured firebase instances")
menu.add_argument("-t", "--target", required=False, type=str, help="[*] target firebase https://<abc>.firebaseio.com")
menu.add_argument("-a", "--apk", required=False, type=str, help="[*] APK to decompile and search for firebase misconfiguration")
args = menu.parse_args()


apk_file = args.apk
target = args.target


if target != None:
    parses.verify_url(target)
    cli_object = cli.Core(target)
    cli_object.is_alive()


if apk_file != None:
    apk_obj = Decompiler(apk_file)
    apk_obj.decompile_phase_one()
