# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc, webrepl, network
import ujson as json

webrepl.start()

sta_if = network.WLAN(network.STA_IF)
if not sta_if.active():
    sta_if.active(True)
    
available_networks = sta_if.scan()

with open("networks.json", "r") as f:
    network_data = json.load(f)

ap_if = network.WLAN(network.AP_IF)
if not ap_if.active():
    ap_if.active(True)

with open("accesspoint.json", "r") as f:
    access_point = json.load(f)
    ap_if.config(
        essid=access_point["essid"], 
        channel=access_point["channel"],
        password=access_point["password"])

for network in available_networks:
    network_name = network[0].decode()
    if network_name in network_data.keys():
        sta_if.connect(network_name, network_data[network_name])
        break

gc.collect()
