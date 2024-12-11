# cotcodac-playground

```
sudo apt-get install i2c-tools git python3-pip

i2cdetect -l
i2cdetect -y 1

python -m venv my-venv
cd my-venv
./bin/pip install rpi_lcd
```

Mac:

clone it, then inside it run:

```
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
flask --app hello run --host=0.0.0.0 --port 5555
```
