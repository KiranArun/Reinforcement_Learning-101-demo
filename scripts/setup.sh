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

POSITIONAL=()
while [[ \$# -gt 0 ]]
do
key="\$1"

case \$key in
    -g|--gap)
    GAP="\$2"
    shift # past argument
    shift # past value
    ;;
    -mc|--model-checkpoint)
    MODELCHECKPOINT="\$2"
    shift # past argument
    shift # past value
    ;;
    *)    # unknown option
    POSITIONAL+=("\$1") # save it in an array for later
    shift # past argument
    ;;
esac
done
set -- "\${POSITIONAL[@]}" # restore positional parameters

if [[ \${GAP} = "" ]]
then
	GAP="0.0"
fi

if [[ \${MODELCHECKPOINT} = "" ]]
then
	MODELCHECKPOINT="logdir/run_01-lr_0.0001-nw_24-tmax_50/final_model.ckpt"
fi

python3 /content/Reinforcement_Learning-101-demo/display_game.py -g \${GAP} -mc \${MODELCHECKPOINT}
EoF

chmod +x /usr/local/bin/run