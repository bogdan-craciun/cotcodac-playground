# cotcodac-playground

sudo apt-get install i2c-tools
sudo apt-get install python3-pip

i2cdetect -l
i2cdetect -y 1

python -m venv my-venv
cd my-venv
./bin/pip install rpi_lcd
