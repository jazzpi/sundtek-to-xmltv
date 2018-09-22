# Sundtek XMLTV Grabber

This script grabs EPG data from a Sundtek media server, converts it to XMLTV
data and upload the XMLTV data file to a ftp server (optional).
The XMLTV data file can be used e.g. by the Kodi's Simple IPTV addon.

## install
``` sh
sudo git clone https://github.com/jazzpi/sundtek-to-xmltv.git /opt/sundtek-to-xmltv
sudo chown -R user:user /opt/sundtek-to-xmltv
```

### install as Service
``` sh
sudo cp /opt/sundtek-to-xmltv/sundtek_xmltv.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/sundtek_xmltv.service
sudo systemctl daemon-reload
sudo systemctl enable --now sundtek_xmltv.service
```

## configure
Edit [config.json](config.json) and replace the content of the [fields](#configuration-field-list).  
Replace `USERNAME` in [sundtek_xmltv.service](sundtek_xmltv.service) with the username of the local user.

### configure FTP Upload (optional)
If `SERVER` is not empty and `ENABLED` is set to true, the upload will be executed after fetching data.

### configuration field list
- `FETCH`
	- `SERVER`  
	  IP and PORT of sundtek server
	- `DAYS`  
	  How many days to fetch (including today)?  
	  Set to 0 to only fetch data from `now`. (`now` contains the current and the next 6 shows.)  
	  Beware that a couple days can already take a couple minutes, even with just 20 channels.
	- `CHANNEL_GROUPS`  
	  Which channel groups should be fetched e.g. `["SD", "HD"]`?  
	  If the array is empty, each channel whould be fetched.
	- `OUTPUT_FILE_PATH`  
	  Where to save the output (relative save filepath e.g. `../../home/shares/tv/epg.xml`)?
	- `DEBUG_OUTPUT`  
	  enable/disable DEBUG print
- `FTP_UPLOAD`
	- `ENABLED`  
	  enable/disable upload
	- `FILE_NAME`  
	  name of the file on the the Server
	- `SERVER`  
	  hostname of the Server
	- `USERNAME`  
	  username (for authentification)
	- `PASSWORD`  
	  password (for authentification)