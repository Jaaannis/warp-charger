#!/bin/sh

# status

python3 screenshot.py -o manual/img_warp2/resized/web_status.png -H $1 -c '#sidebar-evse-group' '#sidebar-network-group' '#sidebar-interfaces-group' '#sidebar-users-group' '#sidebar-system-group' --full 1280

# evse group
python3 screenshot.py -o manual/img_warp2/resized/web_evse2.png -H $1 --crop -c '#sidebar-evse-group' '#sidebar-evse' -e '#evse' -l '#evse > div:nth-child(29)' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_evse2_settings.png -H $1 --crop -c '#sidebar-evse-group' '#sidebar-evse-settings' -e '#evse-settings' --full 1280

python3 screenshot.py -o manual/img_warp2/resized/web_meter.png -H $1 --crop -c '#sidebar-evse-group' '#sidebar-meter' -e '#meter' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_charge_tracker.png -H $1 --crop -c '#sidebar-evse-group' '#sidebar-charge_tracker' -e '#charge_tracker' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_charge_manager.png -H $1 --crop -c '#sidebar-evse-group' '#sidebar-charge_manager' -e '#charge_manager' --full 1280

# network group
python3 screenshot.py -o manual/img_warp2/resized/web_network.png -H $1 --crop -c '#sidebar-network-group' '#sidebar-network' -e '#network' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_wifi_ap.png -H $1 --crop -c '#sidebar-network-group' '#sidebar-wifi-ap' -e '#wifi-ap' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_wifi_sta.png -H $1 --crop -c '#sidebar-network-group' '#sidebar-wifi-sta' -e '#wifi-sta' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_ethernet.png -H $1 --crop -c '#sidebar-network-group' '#sidebar-ethernet' -e '#ethernet' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_wireguard.png -H $1 --crop -c '#sidebar-network-group' '#sidebar-wireguard' -e '#wireguard' --full 1280

# interfaces group

python3 screenshot.py -o manual/img_warp2/resized/web_mqtt.png -H $1 --crop -c '#sidebar-interfaces-group' '#sidebar-mqtt' -e '#mqtt' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_modbus_tcp.png -H $1 --crop -c '#sidebar-interfaces-group' '#sidebar-modbus_tcp' -e '#modbus_tcp' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_ocpp.png -H $1 --crop -c '#sidebar-interfaces-group' '#sidebar-ocpp' -e '#ocpp' --full 1280

# users group

python3 screenshot.py -o manual/img_warp2/resized/web_nfc.png -H $1 --crop -c '#sidebar-users-group' '#sidebar-nfc' -e '#nfc' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_users.png -H $1 --crop -c '#sidebar-users-group' '#sidebar-users' -e '#users' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_users_new.png -H $1 --crop -c '#sidebar-users-group' '#sidebar-users' '#users_config_form > div:nth-child(4) > div:nth-child(2) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)' -e 'div.modal.show' --style "div.modal.show {height: 630px}" -w 2560


# system group
python3 screenshot.py -o manual/img_warp2/resized/web_ntp.png -H $1 --crop -c '#sidebar-system-group' '#sidebar-ntp' -e '#ntp' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_event_log.png -H $1 --crop -c '#sidebar-system-group' '#sidebar-event_log' -e '#event_log' --full 1280
python3 screenshot.py -o manual/img_warp2/resized/web_firmware_update.png -H $1 --crop -c '#sidebar-system-group' '#sidebar-flash' -e '#flash' --full 1280

cp manual/img_warp2/resized/web_status_full.png warp-charger.com/img_warp2/impressions/web3.png
cp manual/img_warp2/resized/web_meter_full.png warp-charger.com/img_warp2/impressions/web1.png
cp manual/img_warp2/resized/web_wifi_sta_full.png warp-charger.com/img_warp2/impressions/web2.png
echo "Manually crop web_users_new.png"
