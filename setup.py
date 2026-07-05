

"""
auto install requirements
install every need and run main.py 
"""

import os
import sys
import subprocess

def install_requirements():
    """install requirements with pip"""
    try:
        print("در حال نصب وابستگی‌ها...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ نصب وابستگی‌ها با موفقیت انجام شد.")
    except subprocess.CalledProcessError as e:
        print(f"❌ خطا در نصب وابستگی‌ها: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        sys.exit(1)

def run_main():
    """Run main.py"""
    main_script = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.exists(main_script):
        print(f"❌ فایل main.py در مسیر {main_script} یافت نشد.")
        sys.exit(1)
    try:
        subprocess.check_call([sys.executable, main_script])
    except KeyboardInterrupt:
        print("\nبرنامه با دخالت کاربر متوقف شد.")
    except Exception as e:
        print(f"❌ خطا در اجرای برنامه: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
    run_main()