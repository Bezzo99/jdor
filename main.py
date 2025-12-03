from dotenv import load_dotenv
from datetime import datetime
from app.service.git import check_for_updates
from app.service.auth import AuthInstance
from app.client.engsel import get_balance, get_tiering_info
from app.client.famplan import validate_msisdn
from app.client.registration import dukcapil
from app.menus.util import clear_screen, pause
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family, show_package_details
from app.menus.hot import show_hot_menu, show_hot_menu2
from app.menus.payment import show_transaction_history
from app.menus.famplan import show_family_info
from app.menus.circle import show_circle_info
from app.menus.notification import show_notification_menu
from app.menus.store.segments import show_store_segments_menu
from app.menus.store.search import show_family_list_menu, show_store_packages_menu
from app.menus.store.redemables import show_redeemables_menu
from app.menus.bookmark import show_bookmark_menu
from app.service.sentry import enter_sentry_mode
import sys, json, time

# === Warna ANSI ===
R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
M = "\033[35m"
C = "\033[36m"
W = "\033[37m"
RESET = "\033[0m"
BOLD = "\033[1m"

WIDTH = 60

def banner():
    """Menampilkan banner keren"""
    clear_screen()
    text = f"""
{R}{BOLD}
███╗   ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗  ██╗
████╗  ██║██╔═══██╗██║   ██║██╔══██╗████╗ ██║
██╔██╗ ██║██║   ██║██║   ██║███████║██╔██╗██║
██║╚██╗██║██║▄▄ ██║██║   ██║██╔══██║██║╚████║
██║ ╚████║╚██████╔╝╚██████╔╝██║  ██║██║ ╚███║
╚═╝  ╚═══╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚══╝
{Y}                N O V A N  S T O R E
{RESET}
    """
    print(text)
    print("=" * WIDTH)

def show_main_menu(profile):
    banner()
    expired_at_dt = datetime.fromtimestamp(profile["balance_expired_at"]).strftime("%Y-%m-%d")
    print(f"{C}Nomor: {W}{profile['number']} {C}| Type: {W}{profile['subscription_type']}")
    print(f"{C}Pulsa: {Y}Rp {profile['balance']} {C}| Aktif sampai: {Y}{expired_at_dt}")
    print(f"{M}{profile['point_info']}{RESET}")
    print("=" * WIDTH)
    print(f"""
{Y}{BOLD}Menu Utama:{RESET}
{G}1{W}. Login / Ganti akun
{G}2{W}. Lihat Paket Saya
{G}3{W}. 🔥 Beli Paket HOT
{G}4{W}. 🔥 Beli Paket HOT-2
{G}5{W}. Beli Paket berdasarkan Option Code
{G}6{W}. Beli Paket berdasarkan Family Code
{G}7{W}. Beli Semua Paket di Family Code (Loop)
{G}8{W}. Riwayat Transaksi
{G}9{W}. Family Plan / Akrab Organizer
{G}10{W}. Circle
{G}11{W}. Store Segments
{G}12{W}. Store Family List
{G}13{W}. Store Packages
{G}14{W}. Redeemables
{C}R{W}. Register
{C}N{W}. Notifikasi
{C}V{W}. Validate MSISDN
{C}00{W}. Bookmark Paket
{R}99{W}. Tutup Aplikasi
""")
    print("=" * WIDTH)

def main():
    try:
        print(f"{C}Checking for updates...{RESET}")
        need_update = check_for_updates()
        if need_update:
            pause()

        while True:
            active_user = AuthInstance.get_active_user()
            if active_user is not None:
                balance = get_balance(AuthInstance.api_key, active_user["tokens"]["id_token"])
                balance_remaining = balance.get("remaining")
                balance_expired_at = balance.get("expired_at")
                point_info = f"{Y}Points: N/A | Tier: N/A{RESET}"

                if active_user["subscription_type"] == "PREPAID":
                    tiering_data = get_tiering_info(AuthInstance.api_key, active_user["tokens"])
                    tier = tiering_data.get("tier", 0)
                    current_point = tiering_data.get("current_point", 0)
                    point_info = f"{Y}Points: {current_point} | Tier: {tier}{RESET}"

                profile = {
                    "number": active_user["number"],
                    "subscriber_id": active_user["subscriber_id"],
                    "subscription_type": active_user["subscription_type"],
                    "balance": balance_remaining,
                    "balance_expired_at": balance_expired_at,
                    "point_info": point_info
                }

                show_main_menu(profile)
                choice = input(f"{C}Pilih menu {W}> {RESET}")

                if choice == "1":
                    selected = show_account_menu()
                    if selected: AuthInstance.set_active_user(selected)
                elif choice == "2":
                    fetch_my_packages()
                elif choice == "3":
                    show_hot_menu()
                elif choice == "4":
                    show_hot_menu2()
                elif choice == "5":
                    code = input("Masukkan Option Code: ")
                    show_package_details(AuthInstance.api_key, active_user["tokens"], code, False)
                elif choice == "6":
                    fam = input("Masukkan Family Code: ")
                    get_packages_by_family(fam)
                elif choice == "7":
                    fam = input("Family Code: ")
                    purchase_by_family(fam, False, False, 0, 1)
                elif choice == "8":
                    show_transaction_history(AuthInstance.api_key, active_user["tokens"])
                elif choice == "9":
                    show_family_info(AuthInstance.api_key, active_user["tokens"])
                elif choice == "10":
                    show_circle_info(AuthInstance.api_key, active_user["tokens"])
                elif choice == "11":
                    show_store_segments_menu(False)
                elif choice == "12":
                    show_family_list_menu(profile["subscription_type"], False)
                elif choice == "13":
                    show_store_packages_menu(profile["subscription_type"], False)
                elif choice == "14":
                    show_redeemables_menu(False)
                elif choice == "00":
                    show_bookmark_menu()
                elif choice.lower() == "n":
                    show_notification_menu()
                elif choice.lower() == "r":
                    msisdn = input("MSISDN: ")
                    nik = input("NIK: ")
                    kk = input("KK: ")
                    res = dukcapil(AuthInstance.api_key, msisdn, kk, nik)
                    print(json.dumps(res, indent=2))
                    pause()
                elif choice.lower() == "v":
                    msisdn = input("Nomor untuk divalidasi: ")
                    res = validate_msisdn(AuthInstance.api_key, active_user["tokens"], msisdn)
                    print(json.dumps(res, indent=2))
                    pause()
                elif choice == "99":
                    print(f"{R}Keluar dari aplikasi...{RESET}")
                    sys.exit(0)
                else:
                    print(f"{R}Pilihan tidak valid!{RESET}")
                    pause()
            else:
                selected_user_number = show_account_menu()
                if selected_user_number:
                    AuthInstance.set_active_user(selected_user_number)
                else:
                    print(f"{R}Tidak ada akun aktif.{RESET}")
                    time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{R}Aplikasi dihentikan.{RESET}")
