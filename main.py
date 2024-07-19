import unittest
from abc import ABC, abstractmethod
import json
import xml.etree.ElementTree as ET

class NetworkDevice(ABC):
    def __init__(self, name, ip_address):
        self.name = name
        self.ip_address = ip_address

    @abstractmethod
    def configure(self):
        pass

    @abstractmethod
    def get_config(self):
        pass

class Router(NetworkDevice):
    def configure(self):
        print(f"Konfiguriere Router {self.name} mit IP {self.ip_address}")

    def get_config(self):
        return {"name": self.name, "ip": self.ip_address, "type": "Router"}

class Switch(NetworkDevice):
    def configure(self):
        print(f"Konfiguriere Switch {self.name} mit IP {self.ip_address}")

    def get_config(self):
        return {"name": self.name, "ip": self.ip_address, "type": "Switch"}

class NetworkAutomation:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def configure_all_devices(self):
        for device in self.devices:
            device.configure()

    def get_all_configs(self):
        return [device.get_config() for device in self.devices]

    def export_config_json(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.get_all_configs(), f, indent=2)

    def export_config_xml(self, filename):
        root = ET.Element("network_config")
        for config in self.get_all_configs():
            device = ET.SubElement(root, "device")
            for key, value in config.items():
                ET.SubElement(device, key).text = str(value)
        tree = ET.ElementTree(root)
        tree.write(filename)

class TestNetworkAutomation(unittest.TestCase):
    def setUp(self):
        self.na = NetworkAutomation()
        self.na.add_device(Router("R1", "192.168.1.1"))
        self.na.add_device(Switch("S1", "192.168.1.2"))

    def test_configure_all_devices(self):
        self.na.configure_all_devices()
        # In einem echten Test würden wir hier die tatsächliche Konfiguration überprüfen

    def test_get_all_configs(self):
        configs = self.na.get_all_configs()
        self.assertEqual(len(configs), 2)
        self.assertEqual(configs[0]["name"], "R1")
        self.assertEqual(configs[1]["name"], "S1")

if __name__ == "__main__":
    # Beispielverwendung
    na = NetworkAutomation()
    na.add_device(Router("MainRouter", "10.0.0.1"))
    na.add_device(Switch("CoreSwitch", "10.0.0.2"))
    na.configure_all_devices()
    na.export_config_json("network_config.json")
    na.export_config_xml("network_config.xml")
    
    # Führe Tests aus
    unittest.main()