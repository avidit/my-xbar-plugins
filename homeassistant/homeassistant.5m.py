#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3

# <xbar.title>Homeassistant</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author.github>avidit</xbar.author.github>
# <xbar.desc>Control Homeassistant</xbar.desc>
# <xbar.image>https://raw.githubusercontent.com/avidit/my-xbar-plugins/develop/homeassistant/homeassistant.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>

# Variables:
# <xbar.var>string(HOMEASSISTANT_URL="http://homeassistant.local:8123/"): Home assistant URL.</xbar.var>
# <xbar.var>string(HOMEASSISTANT_TOKEN="ey..."): Long Lived Access Token. See: https://www.home-assistant.io/docs/authentication/</xbar.var>

# Installation:
# 1. Copy this script to your xbar plugin folder
# 2. Ensure the plugin file is executable by running chmod +x homeassistant.5m.py

import json
import argparse
from requests import get, post

ha_url = os.environ['HOMEASSISTANT_URL']
ha_token = os.environ['HOMEASSISTANT_TOKEN']
api_url = f"{ha_url}api/"
headers = {"Authorization": f"Bearer {ha_token}", "content-type": "application/json"}
ha_icon = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QAAAAAAAD5Q7t/AAAACXBIWXMAAABgAAAAYADwa0LPAAABL0lEQVQ4y8WUPS+DYRSGrwodlYhIqFWEnbBWrF34IQz9D34Cg48gpJtRRHTSxaYdDNhMTfyEy+A03r7efgVxJyfPk/Nx5z7n+YD/gJpTc4PkjgxANg7UgFrsf6RsXK37hQd18idk90H0HGb4hlOaIjtWp8NOwldXX9XGsGSqZfU8rGwnGoOQ1VNFFwmFl6nYW9f2u5C1sRyWhe8zTZG11DV1Qj3IINxXC+p65HaQtu/hDjAGvAOnwDxwB1QymqnweS/ngLOoyQO7WW1X1Wu1qG6pebWZUNgM33bk3KjVJEfWS9kEDoFVYAooAa2wUvhWgCNgo98pV1MDf1JnE/GZUJlEX4VJLAC3cQiFmN1Sr4JR+mMRKCb2PdH3txkWaYVXwEtGXivWvYzY42+L+lt8AFUJtvq22mzaAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIyLTAyLTA3VDE5OjUyOjEzKzAwOjAwOfvcFAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMi0wMi0wN1QxOTo1MjoxMyswMDowMEimZKgAAAAASUVORK5CYII="

print(f"|templateImage={ha_icon}")
print("---")

def is_up():
    try:
        response = get(api_url, headers=headers)
        if response.ok:
            return True
    except:
        pass


def get_states():
    try:
        states_url = f"{api_url}states"
        response = get(states_url, headers=headers)
        return response.json()
    except:
        pass


def get_state(entity_id):
    try:
        state_url = f"{api_url}states/{entity_id}"
        response = get(state_url, headers=headers)
        return response.json()
    except:
        pass


def call_service(domain, service, data):
    try:
        service_url = f"{api_url}services/{domain}/{service}"
        response = post(service_url, headers=headers, json=data)
    except:
        pass


def toggle_light(entity_id):
    state = get_state(entity_id)["state"]
    if state == "on":
        call_service("light", "turn_off", {"entity_id": entity_id})
    else:
        call_service("light", "turn_on", {"entity_id": entity_id})


def toggle_switch(entity_id):
    state = get_state(entity_id)["state"]
    if state == "on":
        call_service("switch", "turn_off", {"entity_id": entity_id})
    else:
        call_service("switch", "turn_on", {"entity_id": entity_id})


def list_lights():
    print("Lights")
    try:
        states = get_states()
        lights = [item for item in states if item["entity_id"].startswith("light.")]
        for light in lights:
            state = light["state"]
            entity_id = light["entity_id"]
            name = light["attributes"]["friendly_name"]
            icon = "💡" if state == "on" else "⚫"
            params = f'refresh=true terminal=false shell="{__file__}" param1="--entity_id={entity_id}" param2="--service=toggle_light"'
            print(f"--{icon} {name} | {params}")
    except:
        print("--Failed to get lights")


def list_switches():
    print("Switches")
    try:
        states = get_states()
        switches = [item for item in states if item["entity_id"].startswith("switch.")]
        for switch in switches:
            state = switch["state"]
            entity_id = switch["entity_id"]
            name = switch["attributes"]["friendly_name"]
            icon = "💡" if state == "on" else "⚫"
            params = f'refresh=true terminal=false shell="{__file__}" param1="--entity_id={entity_id}" param2="--service=toggle_switch"'
            print(f"--{icon} {name} | {params}")
    except:
        print("--Failed to get switches")


if __name__ == "__main__":
    if not is_up():
        print("🔴 Failed to connect")
    else:
        print("🟢 Connected")
        list_lights()
        list_switches()
        parser = argparse.ArgumentParser()
        parser.add_argument("--entity_id", required=False)
        parser.add_argument("--service", required=False)
        args = parser.parse_args()

        if args.entity_id:
            if args.service == "toggle_light":
                toggle_light(args.entity_id)
            elif args.service == "toggle_switch":
                toggle_switch(args.entity_id)
            else:
                pass

    print("---")
    print(f"Open Home Assistant | href={ha_url}")
