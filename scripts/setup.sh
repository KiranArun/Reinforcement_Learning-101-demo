pip install -U -q PyDrive

python3 /content/Reinforcement_Learning-101-demo/scripts/get_drive_files.py $1

chmod +x /content/Reinforcement_Learning-101-demo/scripts/install_dependencies.sh
/content/Reinforcement_Learning-101-demo/scripts/install_dependencies.sh

chmod +x /content/Reinforcement_Learning-101-demo/scripts/install_ngrok.sh
/content/Reinforcement_Learning-101-demo/scripts/install_ngrok.sh

cp /content/Reinforcement_Learning-101-demo/A3C_helper_functions.py /content/