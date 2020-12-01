# Pinspiring MQTT Configuration

mqttconfig = {"broker": {"host": "WDDrivePi.localdomain",
                         "port": 8883,
                         "keepalive": 60,
                         "transport": "tcp",
                         "tlsversion": 2,
                         "certfile": "/home/pi/Pinspiring/mqtt-serv.crt"},
              "thisclient": {"devicetypes": ["Pinspiring"],
                        "username": "Pinspiring",
                        "password": "Pinspiring",
                        "deviceid": "Pinspiring",
                        "version": 1.1},
              "subscribeto": [{"name": "pinspiring", "definition": {"topic": "weather/temperature", "qos": 2}}],
              "publishto": []
              }
