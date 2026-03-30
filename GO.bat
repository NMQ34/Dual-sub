@echo off
title Traducteur Stremio Turbo
echo Lancement du traducteur...
python -m pip uninstall googletrans -y >nul 2>&1
python -m pip install deep-translator pysubs2 >nul 2>&1
cls
python dual_sub.py
pause