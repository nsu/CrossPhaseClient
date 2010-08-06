import avahi
import dbus

__all__ = ["ZeroconfService"]

class Zeroconf:
    """A simple class to publish a network service with zeroconf using
    avahi.
        
    """

    def __init__(self, name, port, stype="_http._tcp",
                 domain="", host="", text=""):
        self.name = name
        self.stype = stype
        self.domain = domain
        self.host = host
        self.port = port
        self.text = text
    
    def publish(self):
        bus = dbus.SystemBus()
        
        avahiServer = bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER)
        server = dbus.Interface(avahiServer, avahi.DBUS_INTERFACE_SERVER)
        
        serviceGroup = bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew())
        self.group = dbus.Interface(serviceGroup, avahi.DBUS_INTERFACE_ENTRY_GROUP)

        self.group.AddService(avahi.IF_UNSPEC, avahi.PROTO_UNSPEC,dbus.UInt32(0),
                     self.name, self.stype, self.domain, self.host,
                     dbus.UInt16(self.port), self.text)

        self.group.Commit()
    
    def unpublish(self):
        self.group.Reset()
