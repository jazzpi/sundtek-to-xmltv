# Sundtek XMLTV Grabber

This script grabs EPG data from a Sundtek media server, converts it to XMLTV
data and upload (optional) the XMLTV data file to a ftp server.
The XMLTV data file can be used e.g. by the Kodi's Simple IPTV addon.

## install

``` sh
sudo git clone https://github.com/jazzpi/sundtek-to-xmltv.git /opt/sundtek-to-xmltv
sudo chown -R user:user /opt/sundtek-to-xmltv
```

## configure
Edit the `*** CONFIGURATION ***` section in [sundtek-grab.py](sundtek-grab.py)
and replace the `USERNAME` in [sundtek_xmltv.service](sundtek_xmltv.service).

### configure Upload (optional)
Remove the `#` in [run-grabber.sh](run-grabber.sh) before `"$GRABBER_DIR/upload-epg-file.sh"` 
and replace `USERNAME`, `PASSWORD` and `URL` in [upload-epg-file.sh](upload-epg-file.sh).

### install Service
``` sh
sudo cp /opt/sundtek-to-xmltv/sundtek_xmltv.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/sundtek_xmltv.service
sudo systemctl daemon-reload
sudo systemctl enable --now sundtek_xmltv.service
```
