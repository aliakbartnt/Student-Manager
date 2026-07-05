"""
auto install requirements
install every need and run main.py 
"""

import os
import sys
import subprocess

def install_requirements():
    """install requirements with pip"""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_file = os.path.join(script_dir, "requirements.txt")
    
    
    if not os.path.exists(req_file):
        print(f"⚠️ requirements.txt not found at {req_file}")
        print("ℹ️ Skipping installation (maybe already installed)...")
        return
    
    try:
        print("📦 Installing requirements from:", req_file)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("✅ Installation successful")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        sys.exit(1)

def run_main():
    """Run main.py"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "main.py")
    
    if not os.path.exists(main_script):
        print(f"❌ main.py not found at {main_script}")
        sys.exit(1)
    
    try:
        print("🚀 Running main.py...")
        subprocess.check_call([sys.executable, main_script])
    except KeyboardInterrupt:
        print("\n⚠️ User cancelled execution")
    except Exception as e:
        print(f"❌ Error running main.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements()
    run_main()