import os
import importlib.util
import subprocess
import sys

def check_and_install_requirements(requirements_file):
    """Check and install requirements from a requirements.txt file"""
    if os.path.exists(requirements_file):
        try:
            with open(requirements_file, 'r') as f:
                requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not requirements:
                return
                
            for req in requirements:
                try:
                    module_name = req.split('==')[0].split('>=')[0].split('<=')[0].strip()
                    importlib.import_module(module_name)
                except ImportError:
                    print(f"[QHNodes] Installing: {req}")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except Exception as e:
            print(f"[QHNodes] Error installing requirements: {e}")

def install_dependencies(base_dir):
    """Install dependencies for main repo and all submodules"""
    # Check main repo requirements
    main_requirements = os.path.join(base_dir, "requirements.txt")
    check_and_install_requirements(main_requirements)
    
    # Check submodule requirements
    external_nodes_dir = os.path.join(base_dir, "external_nodes")
    if os.path.exists(external_nodes_dir):
        submodules = [d for d in os.listdir(external_nodes_dir) 
                     if os.path.isdir(os.path.join(external_nodes_dir, d))]
        
        if submodules:
            for submodule in submodules:
                requirements_file = os.path.join(external_nodes_dir, submodule, "requirements.txt")
                check_and_install_requirements(requirements_file)

def ensure_dependencies():
    """Ensure all dependencies are installed"""
    try:
        print("[QHNodes] Checking dependencies...")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        install_dependencies(base_dir)
    except Exception as e:
        print(f"[QHNodes] Error during dependency installation: {e}")
        print("[QHNodes] Please try installing dependencies manually")
