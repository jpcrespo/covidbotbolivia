#!/bin/bash

cd core/
sudo rm -r vacunas covid19-bolivia pics
git clone https://github.com/mauforonda/vacunas
git clone -b opsoms https://github.com/mauforonda/covid19-bolivia
mkdir pics
cd ..
cd ..

source bin/activate


cd /home/pi/Desktop/telebot/covidbotbolivia/core/

python recopilador.py
#python notifi.py


