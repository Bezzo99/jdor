from dotenv import load_dotenv
load_dotenv()

import sys, json
from datetime import datetime

# ==== WARNA ====
from colorama import init, Fore, Style
init(autoreset=True)
# ===============

from app.menus.util import clear_screen, pause
from app.client.engsel import (
    get_balance,
    get_tiering_info,
)
from app.client.famplan import validate_msisdn
from app.menus.payment import show_transaction_history
from app.service.auth import AuthInstance
from app.menus.bookmark import show_bookmark_menu
from app.menus.account import show_account_menu
from app.menus.package import fetch_my_packages, get_packages_by_family, show_package_details
from app.menus.hot import show_hot_menu, show_hot_menu2
from app.service.sentry import enter_sentry_mode
from app.menus.purchase import purchase_by_family
from app.menus.famplan import show_family_info
from app.menus.circle import show_circle_info
from app.menus.notification import show_notification_menu
from app.menus.store.segments import show_store_segments_menu
from app.menus.store.search import show_family_list_menu, show_store_packages_menu
from app.menus.store.redemables import show_redeemables_menu
from app.client.registration import dukcapil

WIDTH = 55

def show_main_menu(profile):
    clear_screen()

    print(Fore.CYAN + "=" * WIDTH)

    expired_at_dt = datetime.fromtimestamp(profile["balance_expired_at"]).strftime("%Y-%m-%d")

    print(Fore.YELLOW + f"Nomor: {profile['number']} | Type: {profile['subscription_type']}".center(WIDTH))
    print(Fore.GREEN + f"Pulsa: Rp {profile['balance']} | Aktif sampai: {expired_at_dt}".center(WIDTH))
    print(Fore.MAGENTA + f"{profile['point_info']}".center(WIDTH))

    print(Fore.CYAN + "=" * WIDTH)
    print(Fore.WHITE + "Menu:")

    # MENU WARNA
    print(Fore.GREEN + "1. Login/Ganti akun")
    print("2. Lihat Paket Saya")
    print("3. Beli Paket " + Fore.RED + "🔥 HOT 🔥")
    print("4. Beli Paket " + Fore.RED + "🔥 HOT-2 🔥")
    print("5. Beli Paket Berdasarkan Option Code")
    print("6. Beli Paket Berdasarkan Family Code")
    print("7. Beli Semua Paket di Family Code (loop)")
    print("8. Riwayat Transaksi")
    print("9. Family Plan/Akrab Organizer")
    print("10. Circle")
    print("11. Store Segments")
    print("12. Store Family List")
    print("13. Store Packages")
    print("14. Redemables")
    print(Fore.YELLOW + "R. Register")
    print(Fore.YELLOW + "N. Notifikasi")
    print(Fore.BLUE + "V. Validate msisdn")
    print(Fore.MAGENTA + "00. Bookmark Paket")
    print(Fore.RED + "99. Tutup aplikasi")

    print(Fore.CYAN + "-" * WIDTH)


def main():
    while True:
        active_user = AuthInstance.get_active_user()

        if active_user is not None:
            balance = get_balance(AuthInstance.api_key, active_user["tokens"]["id_token"])
            balance_remaining = balance.get("remaining")
            balance_expired_at = balance.get("expired_at")

            point_info = "Points: N/A | Tier: N/A"

            if active_user["subscription_type"] == "PREPAID":
                tiering_data = get_tiering_info(AuthInstance.api_key, active_user["tokens"])
                tier = tiering_data.get("tier", 0)
                current_point = tiering_data.get("current_point", 0)
                point_info = f"Points: {current_point} | Tier: {tier}"

            profile = {
                "number": active_user["number"],
                "subscriber_id": active_user["subscriber_id"],
                "subscription_type": active_user["subscription_type"],
                "balance": balance_remaining,
                "balance_expired_at": balance_expired_at,
                "point_info": point_info
            }

            show_main_menu(profile)

            choice = input(Fore.CYAN + "Pilih menu: " + Fore.WHITE)

            if choice.lower() == "t":
                pause()
            elif choice == "1":
                selected_user_number = show_account_menu()
                if not selected_user_number:
                    print(Fore.RED + "No user selected or failed to load user.")
                else:
                    AuthInstance.set_active_user(selected_user_number)
                continue

            elif choice == "2":
                fetch_my_packages()
                continue

            elif choice == "3":
                show_hot_menu()

            elif choice == "4":
                show_hot_menu2()

            elif choice == "5":
                option_code = input("Enter option code (or '99' to cancel): ")
                if option_code != "99":
                    show_package_details(AuthInstance.api_key, active_user["tokens"], option_code, False)

            elif choice == "6":
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code != "99":
                    get_packages_by_family(family_code)

            elif choice == "7":
                family_code = input("Enter family code (or '99' to cancel): ")
                if family_code == "99":
                    continue

                start_from_option = input("Start purchasing from option number (default 1): ")
                try:
                    start_from_option = int(start_from_option)
                except:
                    start_from_option = 1

                use_decoy = input("Use decoy package? (y/n): ").lower() == 'y'
                pause_on_success = input("Pause on each success? (y/n): ").lower() == 'y'

                delay_seconds = input("Delay seconds between purchases (0 = none): ")
                try:
                    delay_seconds = int(delay_seconds)
                except:
                    delay_seconds = 0

                purchase_by_family(
                    family_code, use_decoy, pause_on_success, delay_seconds, start_from_option
                )

            elif choice == "8":
                show_transaction_history(AuthInstance.api_key, active_user["tokens"])

            elif choice == "9":
                show_family_info(AuthInstance.api_key, active_user["tokens"])

            elif choice == "10":
                show_circle_info(AuthInstance.api_key, active_user["tokens"])

            elif choice == "11":
                is_enterprise = input("Is enterprise store? (y/n): ").lower() == 'y'
                show_store_segments_menu(is_enterprise)

            elif choice == "12":
                is_enterprise = input("Is enterprise? (y/n): ").lower() == 'y'
                show_family_list_menu(profile['subscription_type'], is_enterprise)

            elif choice == "13":
                is_enterprise = input("Is enterprise? (y/n): ").lower() == 'y'
                show_store_packages_menu(profile['subscription_type'], is_enterprise)

            elif choice == "14":
                is_enterprise = input("Is enterprise? (y/n): ").lower() == 'y'
                show_redeemables_menu(is_enterprise)

            elif choice == "00":
                show_bookmark_menu()

            elif choice == "99":
                print(Fore.RED + "Exiting the application.")
                sys.exit(0)

            elif choice.lower() == "r":
                msisdn = input("Enter msisdn (628xxxx): ")
                nik = input("Enter NIK: ")
                kk = input("Enter KK: ")
                res = dukcapil(AuthInstance.api_key, msisdn, kk, nik)
                print(json.dumps(res, indent=2))
                pause()

            elif choice.lower() == "v":
                msisdn = input("Enter the msisdn to validate (628xxxx): ")
                res = validate_msisdn(AuthInstance.api_key, active_user["tokens"], msisdn)
                print(json.dumps(res, indent=2))
                pause()

            elif choice.lower() == "n":
                show_notification_menu()

            elif choice == "s":
                enter_sentry_mode()

            else:
                print(Fore.RED + "Invalid choice. Please try again.")
                pause()

        else:
            selected_user_number = show_account_menu()
            if selected_user_number:
                AuthInstance.set_active_user(selected_user_number)
            else:
                print(Fore.RED + "No user selected or failed to load user.")


if __name__ == "__main__":
    try:
        print(Fore.YELLOW + "Checking for updates...")
        need_update = check_for_updates()
        if need_update:
            pause()
        main()

    except KeyboardInterrupt:
        print("\n" + Fore.RED + "Exiting the application.")
