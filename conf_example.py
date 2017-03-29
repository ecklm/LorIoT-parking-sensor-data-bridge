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