# This is an example config file which holds placeholders for the variables needed
# to connect to the LorIoT websocket service.
# To make it active, copy to a file named conf.py. For security reasons conf.py
# is ignored because it stores confidential data.

# LorIoT parameters
loriot_id = "" # AppID
loriot_token = "" # Token to the service
loriot_watched_ports = [] # List of port numbers to be watched

# AWS parameters
aws_host = "" # Host path provided by the AWS IoT platform thing inventory
aws_root_CA_path = "" # Path to Amazon root CA file
aws_certificate_path = "" # Path to the cert file
aws_private_key_path = "" # Path to the privete key file
aws_topic = "" # MQTT topic to publish to

# Lora Gateway paramteres
loragw_host = "" # Host to connect to
loragw_port = 0 # Port used to the connection
loragw_user = "" # Username
loragw_passwd = "" # Password
loragw_topics = [] # List of topics to subscribe
loragw_watched_ports = [] # List of port numbers to be watched

# SensorHUB parameters
sensorhub_host = "" # Host to connect to
sensorhub_port = 0 # Port used to the connection
sensorhub_user = "" # Username
sensorhub_passwd = "" # Password
sensorhub_topic = "" # MQTT topic to publish to
