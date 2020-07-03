from utils import banner,parses
from core import cli
import argparse



print(banner.banner)
menu = argparse.ArgumentParser(description="[*] Exploit missconfigured firebase instances")
menu.add_argument("-t", "--target", required=True, type=str, help="[*] target firebase https://<abc>.firebaseio.com")
menu.add_argument("-a", "--apk", required=False, type=str, help="[*] APK to decompile and search for firebase misconfiguration")
args = menu.parse_args()

target = parses.verify_url(args.target)

cli_object = cli.Core(target)
cli_object.is_alive()



