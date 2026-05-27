#!/data/data/com.termux/files/usr/bin/bash

clear

echo "================================="
echo "      CODE PAY OO BACKUP"
echo "================================="

DATE=$(date +"%Y-%m-%d_%H-%M-%S")

zip -r CodePayOo_$DATE.zip CodePayOo

echo ""
echo "Backup Complete ✅"

mv CodePayOo_$DATE.zip /storage/emulated/0/

echo ""
echo "Saved To Phone Storage ✅"
echo ""
