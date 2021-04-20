#1/bin/bash

sudo rm -r vacunas covid19-bolivia
git clone https://github.com/mauforonda/vacunas
git clone -b opsoms https://github.com/mauforonda/covid19-bolivia
sudo rm /pics/vac* /pics/nac*
python recopilador.py

