# Sundtek XMLTV Grabber

This script grabs EPG data from a Sundtek media server and converts it to XMLTV
data for further use (e.g. by Kodi's Simple IPTV add-on).

## Installation

``` sh
sudo git clone https://github.com/jazzpi/sundtek-to-xmltv.git /opt/sundtek-to-xmltv
sudo chown -R user:user /opt/sundtek-to-xmltv
```

Edit the `*** CONFIGURATION ***` section in [sundtek-grab.py](sundtek-grab.py)
and the lines marked by `EDIT_THIS` in
[sundtek_xmltv.service](sundtek_xmltv.service).

``` sh
sudo cp /opt/sundtek-to-xmltv/sundtek_xmltv.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/sundtek_xmltv.service
sudo systemctl daemon-reload
sudo systemctl enable --now sundtek_xmltv.service
```
