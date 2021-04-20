#!/bin/bash


sudo rm -r vacunas covid19-bolivia

git clone https://github.com/mauforonda/vacunas
git clone -b opsoms https://github.com/mauforonda/covid19-bolivia.git
sudo rm core/pics/vac* core/pics/cov*
python recopilador.py
