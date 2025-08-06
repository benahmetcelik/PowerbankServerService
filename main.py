#!/usr/bin/env python3
import subprocess
import json
import requests


def get_lsusb_devices():
    devices = []
    try:
        output = subprocess.check_output(['lsusb']).decode('utf-8').strip()
        lines = output.split('\n')
        for line in lines:
            parts = line.split()
            bus = parts[1]
            device = parts[3].rstrip(':')
            id_vendor_product = parts[5]
            description = ' '.join(parts[6:])

            detailed = subprocess.check_output(['lsusb', '-v', '-s', f'{bus}:{device}'],
                                               stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')

            devices.append({
                'bus': bus,
                'device': device,
                'id': id_vendor_product,
                'description': description,
                'details': detailed
            })
    except Exception as e:
        devices.append({'error': str(e)})
    return devices


def post_data(data):
    url = "http://192.168.1.9:8000/api/station-info"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error posting data: {e}")


def main():
    devices = get_lsusb_devices()
    post_data({
        "device_count": len(devices),
        "devices": devices
    })


if __name__ == "__main__":
    main()
