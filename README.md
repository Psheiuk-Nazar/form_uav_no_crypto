# UAV Configuration Web App
This simple web application built with Flask allows users to configure parameters for a UAV (Unmanned Aerial Vehicle). 
Users can input various values through a form, and the configuration data is then saved to a JSON file.

# Clone
```
git clone https://github.com/uav8rivne/form_uav_no_crypto.git
```
# Venv
! If we use venv!!! be carefuller when use venv, change form_uav.sh
``` python
python -m venv venv
```
Windows
``` python
source venv//Scripts//activate
```
Ubunta
``` python
source venv/bin/activate
```

# Installs 
``` python

pip install -r requirements.txt

```


# Configuration
Open settings.json
Change parameters 
```json

    "form" : {
        "secret_key": Flask -project secret key
        "host": "localhost", -> host where program will work
        "port": 5000, -> port where program will work
        "mission_executor": python /way/to/mission/main.py -c /way/to/mission/config.json
        "logs_path": -> dir where logs will save
        "mission_save_path": -> dir where mission.json will save
        "gpio_buzzer": 26, -> buzzer gpio in raspberry pi
    }
```
## Usage
Run the Flask application:

Ubunta
```
sudo python main.py -c settings.json

```
Windows
``` python
python main.py -c settings.json
```

1. Open your web browser and go to http://{your_host_name}.
2. Fill out the configuration form
3. Click the "Save" button to save the configuration.
4. Check coordinates on map
5. Start mission 

How make service:
1. Navigate to the systemd directory by executing the following command:/etc/systemd/system/
2. Create a file named formuav.service with the following content: formuav.service
```formuav.service
[Unit]
Description=Form UAV service
Wants=network.target

[Service]
ExecStart=/bin/bash /home/owner/uav8rivne/forms/form_uav.sh
Restart=on-abort
User=root
WorkingDirectory=/home/owner/uav8rivne/forms/

[Install]
WantedBy=multi-user.target
```

3. Install Apache HTTP Server by executing the following commands: sudo apt install apache2
4. Start the Apache service: ```sudo systemctl start apache2```
5. Check its status: ``` sudo systemctl status apache2``` 
6. Enable Apache service to start automatically on system boot: ```sudo systemctl enable apache2```
7. Add a firewall rule to allow access to port 80, which is used by Apache:```sudo ufw allow 80/tcp```
8. Navigate to the Apache configuration directory by executing the following command: /etc/apache2/sites-enabled
9. Create a file named uav_m2.local.conf with the following content: uav_m2.local.conf
```uav_m2.local.conf
<VirtualHost *:80>
        ServerName 10.9.0.22
        ServerAdmin webmaster@localhost
                ProxyPass / "http://localhost:5000/"

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

10. Reload the systemd daemon to apply the changes made to the service file: ```sudo systemctl daemon-reload```
11. Start the Form UAV service::  ```sudo systemctl start formuav.service```
12. Enable the Form UAV service to start automatically on system boot: ```sudo systemctl enable formuav.service```
13. Check the status of the Form UAV service to ensure it's running properly: ```sudo systemctl status formuav.service```
14. Enable the Apache proxy modules to allow proxying requests to your Flask application:
    14.1. ```sudo a2enmod proxy```
    14.2. ```sudo a2enmod proxy_http```
15. Restart the Apache server to apply the changes: ```sudo systemctl restart apache2```
16. Verify the status of the Apache server to ensure it's running without errors ```sudo systemctl status apache2```

form_uav.sh with venv:
```
#!/bin/sh


PATH=/root/{your_dir}/.env/bin:/usr/local/bin:/usr/bin:/bin
PYTHONIOENCODING=utf-8
PYTHONPATH=/root/{your_dir}/.env/bin/python
VIRTUAL_ENV=/root/{your_dir}/.env

/root/{your_dir}/.env/bin/python3 web_form/form_uav.py -c web_form/mission/settings.json
```
form_uav.sh without venv:
````
#!/bin/sh

python3 web_form/form_uav.py -c web_form/mission/settings.json
```
