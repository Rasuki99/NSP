@echo off
Py get-pip.py %*
pip install pynput %*
pip install opencv-python %*
pause
