# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import random  
import time as t
import json

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1z60dayqonw5-ats.iot.us-west-2.amazonaws.com"
CLIENT_ID = "MyTestDevicePV1"
PATH_TO_CERTIFICATE = "certificates/da375ed26871c32952438a9243d8d9493cf1f16d33490eb88bfb5ee7c0f884dd-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "certificates/da375ed26871c32952438a9243d8d9493cf1f16d33490eb88bfb5ee7c0f884dd-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "certificates/root.pem"

TOPIC = "/sample/topic"
RANGE = 100

# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')
for i in range (RANGE):
    # data = "{} [{}]".format(MESSAGE, i+1)
    # message = {"message" : data}
    randomtemp = random.randint(0, 101) 
    randomwaterLevel = random.randint(0, 201) 
    MESSAGE = {"temp": randomtemp, "waterLevel": randomwaterLevel, "state": "reporting" }
    mqtt_connection.publish(topic=TOPIC, payload=json.dumps(MESSAGE), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(MESSAGE) + "' to the topic: " + "'/sample/topic'")
    t.sleep(5)
print('Publish End')
disconnect_future = mqtt_connection.disconnect()
disconnect_future.result()