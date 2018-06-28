pip install -U -q PyDrive

python3 /content/Reinforcement_Learning-101-demo/scripts/get_drive_files.py $1

# dependencies
chmod +x /content/Reinforcement_Learning-101-demo/scripts/install_dependencies.sh
/content/Reinforcement_Learning-101-demo/scripts/install_dependencies.sh

# ngrok
chmod +x /content/Reinforcement_Learning-101-demo/scripts/install_ngrok.sh
/content/Reinforcement_Learning-101-demo/scripts/install_ngrok.sh

# novnc
chmod +x Reinforcement_Learning-101-demo/scripts/install_novnc.sh
bash Reinforcement_Learning-101-demo/scripts/install_novnc.sh 1>/dev/null


cp /content/Reinforcement_Learning-101-demo/A3C_helper_functions.py /content/

echo "web_addr: 4045" > /content/config.yml

cat <<EoF>/usr/local/bin/run
#!/bin/bash
python3 /content/Reinforcement_Learning-101-demo/display_game.py -g \$1
EoF

chmod +x /usr/local/bin/run