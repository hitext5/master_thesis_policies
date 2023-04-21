from dataclasses import dataclass
import paho.mqtt.client as mqtt


@dataclass
class MessageHandler:
    mqtt_id = "message_handler"
    broker: str = "127.0.0.1"
    port: int = 1883
    client = mqtt.Client(client_id=mqtt_id)
    rc = 1

    def on_connect(self, client, userdata, flags, rc):
        self.rc = rc
        if rc == 0:
            print("MessageHandler connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
        pass

    def on_message(self, client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)

    # TODO How can we tell the client to subscribe to a topic, when a new device is added?
    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload=None, qos=0, retain=False):
        self.client.publish(topic, payload=payload, qos=qos, retain=retain)
