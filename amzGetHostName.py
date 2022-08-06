from zeroconf import ServiceBrowser, Zeroconf
def getHostIP():
    zeroconf = Zeroconf()

    info = zeroconf.get_service_info("_mqtt._tcp.local.", "AMZ MQTT._mqtt._tcp.local.")

        # If service registered #
    if info:
            #print(info.parsed_addresses()[0])
            return info.parsed_addresses()[0]
        # No named service registered #
    else:
            print("Service MQTT doesn't exist")
            return "Not Found"
    zeroconf.close()
