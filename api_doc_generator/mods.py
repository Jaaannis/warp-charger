from evse import evse
from meter import meter
from nfc import nfc
from charge_manager import charge_manager
from mqtt import mqtt
from wifi import wifi
from ethernet import ethernet
from network import network
from ntp import ntp
from users import users
from charge_tracker import charge_tracker
from misc import misc
from info import info
from wireguard import wireguard
from rtc import rtc
from modbus_tcp import modbus_tcp
from ocpp import ocpp
from authentication import authentication
from energy_manager import energy_manager

mods = [evse, meter, charge_manager, users, charge_tracker, nfc, network, wifi, ethernet, ntp, mqtt, modbus_tcp, ocpp, wireguard, rtc, info, authentication, misc, energy_manager]
