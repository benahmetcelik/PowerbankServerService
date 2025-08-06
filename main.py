#!/usr/bin/env python3
import requests
import socket
import psutil
import platform
import json

def get_system_info():
    info = {
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "uptime": psutil.boot_time(),
        "os": platform.platform(),
    }
    return info

def post_data():
    url = "http://localhost:8000/api/station-info"
    headers = {'Content-Type': 'application/json'}
    data = get_system_info()
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(f"Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    post_data()
