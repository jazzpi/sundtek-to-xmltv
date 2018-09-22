# Sundtek XMLTV Grabber

This script grabs EPG data from a Sundtek media server, converts it to XMLTV
data and upload the XMLTV data file to a ftp server (optional).
The XMLTV data file can be used e.g. by the Kodi's Simple IPTV addon.

## install
``` sh
sudo git clone https://github.com/jazzpi/sundtek-to-xmltv.git /opt/sundtek-to-xmltv
sudo chown -R user:user /opt/sundtek-to-xmltv
```

## configure
Edit [config.json](config.json) and replace the content of the fields.
With `"CHANNEL_GROUPS"` you can restrict the fetched groups (e.g. `"CHANNEL_GROUPS": ["FreeTV"]`).

### configure FTP Upload (optional)
If `SERVER` and `ENABLED` in `FTP_UPLOAD` is set, the upload will be executed after fetching data.

### install as Service
``` sh
sudo cp /opt/sundtek-to-xmltv/sundtek_xmltv.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/sundtek_xmltv.service
sudo systemctl daemon-reload
sudo systemctl enable --now sundtek_xmltv.service
```
