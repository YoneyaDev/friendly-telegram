# friendly-telegram

echo "1. UserBot | Kajitsu_Yoneya > запуск..."
cd ~/Telegram/KYoneya/UserBot/ && screen -AmdS -r python3.10 -m friendly-telegram --no-web
echo "2. UserBot | šveps > запуск..."
cd ~/Telegram/Dima/UserBot/ && screen -AmdS -r python3.10 -m friendly-telegram --no-web
echo "Ожидайте! Боты будут запущены в течении минуты!"
