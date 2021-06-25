#!/usr/bin/env python3

import asyncio
import json
import paho.mqtt.client as mqtt
import queue
import websockets

# MQTT topics to subscribe to
MQTT_TOPICS = [('celidon/iloc', 0), ('celidon/poi', 0), ('celidon/hololens', 0)]

floor_dict_queues = {}

# offset [mm] of map coordinate system to localization coordinate system
coordinate_offset = [240, 2240, 0]


def create_floor_dict(pos_dict, topic):
    """
    function to create a floor based dictionary
    """

    # initialize empty floor dictionary
    floor_dict = {
        'topic': topic.split('/')[-1],  # remove celidon/ from topic
    }

    # map received positions to floors (based on z position)
    for key, value in pos_dict.items():
        if -2.76 <= value['pos'][2] < 0:
            if 'floor-1' not in floor_dict:
                floor_dict['floor-1'] = {}
            floor_dict['floor-1'][key] = value
        elif 0 <= value['pos'][2] < 3.510:
            if 'floor0' not in floor_dict:
                floor_dict['floor0'] = {}
            floor_dict['floor0'][key] = value
        elif 3.510 <= value['pos'][2] < 6.520:
            if 'floor1' not in floor_dict:
                floor_dict['floor1'] = {}
            floor_dict['floor1'][key] = value
        elif 6.520 <= value['pos'][2] < 9.530:
            if 'floor2' not in floor_dict:
                floor_dict['floor2'] = {}
            floor_dict['floor2'][key] = value
        else:
            if 'unknown' not in floor_dict:
                floor_dict['unknown'] = {}
            floor_dict['unknown'][key] = value

    return floor_dict


# mqtt callbacks
def on_message(mqtt_client, userdata, msg):
    """
    callback to handle received mqtt messages
    """

    # decode received mqtt message
    if msg.topic == 'celidon/iloc':
        iloc_dict = {}
        recv_data = json.loads(msg.payload.decode())

        # add received data to position dictionary
        for tag_id, data in recv_data.items():
            position_m = [p / 1000 for p in data['pos']]
            ofst_m = [o / 1000 for o in coordinate_offset]
            iloc_dict[data['alias']] = {'ts': data['ts'],
                                        'pos': position_m,
                                        'ofst': ofst_m}
            fl = create_floor_dict(iloc_dict, msg.topic)
            for q in floor_dict_queues.values():
                q.put(fl)

    elif msg.topic == 'celidon/poi' or msg.topic == 'celidon/hololens':
        poi_dict = {}
        recv_data = json.loads(msg.payload.decode())

        # add received data to position dictionary
        for poi_id, data in recv_data.items():
            position_m = [p / 1000 for p in data['pos']]
            ofst_m = [o / 1000 for o in coordinate_offset]
            poi_dict[data['alias']] = {'ts': data['ts'],
                                       'to': data['to'],
                                       'pos': position_m,
                                       'ofst': ofst_m,
                                       'text': data['text']}
            fl = create_floor_dict(poi_dict, msg.topic)
            for q in floor_dict_queues.values():
                q.put(fl)


def on_disconnect(mqtt_client, userdata, rc=0):
    mqtt_client.loop_stop()


async def webserver(websocket, port):
    q = queue.Queue()
    floor_dict_queues[websocket] = q
    while True:
        try:
            floor_dict = q.get_nowait()
            await websocket.send(json.dumps(floor_dict))
        except queue.Empty:
            await asyncio.sleep(0.001)
        except websockets.exceptions.ConnectionClosedOK:
            pass


def main():
    # setup mqtt
    mqtt_port = 1883  # default mqtt port: 1883
    mqtt_broker = '10.10.1.82'  # address of the MQTT broker
    mqtt_client = mqtt.Client('CelidonSub2')  # name of this MQTT subscriber
    mqtt_client.connect(mqtt_broker, mqtt_port)  # connect to MQTT broker
    mqtt_client.subscribe(MQTT_TOPICS)  # subscribe to MQTT topics
    mqtt_client.on_message = on_message  # configure callback for message reception
    mqtt_client.on_disconnect = on_disconnect  # configure callback for disconnection
    mqtt_client.loop_start()  # start MQTT client loop

    # setup webserver
    start_server = websockets.serve(webserver, host="localhost",
                                    port=1989, ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    try:
        main()
    except:
        import traceback
        traceback.print_exc()
        while True:
            pass
