# Pinspiring MQTT Configuration

mqttconfig = {"broker": {"host": "WDDrivePi.localdomain",
                         "port": 8883,
                         "keepalive": 60,
                         "transport": "tcp",
                         "tlsversion": 2,
                         "certfile": "/home/pi/mqtt-ca.crt"},
              "local": {"deviceid": "Pinspiring",
                        "username": "Pinspiring",
                        "password": "Pinspiring",
                        "device": "Pinspiring",
                        "version": 1},
              "queues": {"Pinspiring": {"name": "weather/temperature",
                                         "qos": 2}

                         }
              }
