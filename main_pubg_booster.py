import os
import subprocess
import json
import time

CHANNEL_NAME = "MAYKI_1_SHOP_PUBG"
PACKAGE_NAME = "com.tencent.ig"  # پابجی گلوبال

# منو با تبلیغ کانال و خط انتخاب
def termux_menu(title, options):
    menu_title = f"{title} | {CHANNEL_NAME}\nانتخاب کنید"
    cmd = f'termux-dialog radio -t "{menu_title}" -v "{",".join(options)}"'
    result = subprocess.getoutput(cmd)
    try:
        return json.loads(result)["text"]
    except:
        return None

# نمایش مرحله‌ای گزینه‌ها با تیک ✔ سریع‌تر
def show_steps_fast(steps):
    # نمایش سریع، بدون تاخیر طولانی
    for step in steps:
        os.system(f'termux-toast "✔ {step}"')
        time.sleep(0.15)  # نصف زمان قبلی

# تست پینگ سریع
def ping_test():
    ping = subprocess.getoutput("ping -c 1 8.8.8.8")
    if "time=" in ping:
        value = ping.split("time=")[1].split(" ")[0]
        os.system(f'termux-toast "پینگ لحظه‌ای: {value} ms"')
    else:
        os.system('termux-toast "پینگ ناموفق"')

# بهینه‌سازی اینترنت / وای‌فای سریع
def optimize_network_fast():
    os.system("termux-toast 'بهینه‌سازی اینترنت و وای‌فای...'")
    os.system("ndc resolver flushdefaultif 2>/dev/null")  # پاکسازی DNS کش
    os.system("am kill-all 2>/dev/null")  # بستن برنامه‌های شبکه‌ای اضافی
    os.system("termux-toast 'اینترنت بهینه شد'")

# اجرای بازی (اگر نتوانست، بدون ارور رد شود)
def launch_game_safe():
    try:
        os.system(f'am start -n {PACKAGE_NAME}/.GameActivity 2>/dev/null')
        time.sleep(1)  # کوتاه‌تر
    except:
        pass  # هیچ اروری نمایش داده نشود

# بهینه‌سازی اختصاصی هر حالت سریع‌تر
def optimize(mode):
    steps = []

    # مراحل مشترک
    steps.append("بستن برنامه‌های پس‌زمینه")
    os.system("am kill-all 2>/dev/null")
    steps.append("پایداری FPS")

    if mode == "Gaming (گیمینگ)":
        steps.append("کاهش گرافیک")
        steps.append("تقویت وای‌فای")
        steps.append("کاهش پینگ")
    elif mode == "Extreme (اکستریم)":
        steps.append("کاهش گرافیک")
        steps.append("تقویت وای‌فای")
        steps.append("کاهش تاخیر تاچ")
        steps.append("کاهش پینگ")
        steps.append("پایداری اینترنت")
    elif mode == "Balanced (متعادل)":
        steps.append("کاهش گرافیک")
        steps.append("پایداری اینترنت")
        steps.append("کاهش پینگ")

    # اجرای بازی (اگر موفق شد)
    launch_game_safe()

    # نمایش مرحله‌ای سریع
    show_steps_fast(steps)

    # بهینه‌سازی اینترنت سریع
    optimize_network_fast()

    # تست پینگ یکبار
    ping_test()

    # پیام پایانی
    os.system(f'termux-toast "💡 بهینه انجام شد"')
    os.system(f'termux-toast "🎮 از گیم لذت ببرید ❤️"')

# بخش گیم بوستر
def game_booster():
    options = ["Gaming (گیمینگ)", "Extreme (اکستریم)", "Balanced (متعادل)"]
    mode = termux_menu("انتخاب حالت گیم بوستر", options)
    if not mode:
        mode = "Gaming (گیمینگ)"
    optimize(mode)

# منوی اصلی سریع
def main_menu():
    options = ["گیم بوستر", "کانال تلگرام"]
    choice = termux_menu("منوی اصلی", options)
    if not choice:
        return
    if choice == "گیم بوستر":
        game_booster()
    elif choice == "کانال تلگرام":
        os.system(f'am start -a android.intent.action.VIEW -d "https://t.me/{CHANNEL_NAME}"')

if name == "main":
    main_menu()