import os

os.chdir("/home/user/product-name-tbd/decision-making") #not sure what our user is or if we log in as root
os.system("source venv/bin/activate")
os.system("sudo python src/workflow_manager.py")