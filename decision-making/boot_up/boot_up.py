import os

os.chdir("/home/pi/product-name-tbd/decision-making")
os.system("source venv/bin/activate")
os.system("sudo python src/workflow_manager.py &")
