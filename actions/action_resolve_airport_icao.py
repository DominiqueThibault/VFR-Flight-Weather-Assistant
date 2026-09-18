"""This files contains custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa-pro/concepts/custom-actions

# This is a custom action which resolves city names as user input to equivalent ICAO codes.
"""
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import airportsdata
import re

# Loads database when initializing the action server.
AIRPORTS = airportsdata.load('ICAO')

class ActionResolveAirportICAO(Action):
    def name(self) -> Text:
        return "action_resolve_airport_icao"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # If the slot airport_icao is already filled
        # its value will be used.
        airport_icao = tracker.get_slot("airport_icao")
        if isinstance(airport_icao, str) and re.fullmatch(r"[A-Za-z]{4}", airport_icao):
            icao = airport_icao.upper()
            #latitude, longitude = 0.0, 0.0
            if icao in AIRPORTS:
                airport_data = AIRPORTS.get(icao, {})
                try:
                    latitude = float(airport_data.get("lat")) if airport_data.get("lat") is not None else 0.0
                    longitude = float(airport_data.get("lon")) if airport_data.get("lon") is not None else 0.0
                except (ValueError, TypeError):
                    latitude, longitude = 0.0, 0.0

            return [
                SlotSet("resolved_airport_icao", None),
                SlotSet("airport_icao", icao),
                SlotSet("lat", latitude),
                SlotSet("lon", longitude),
            ]

        # 2. Search for city names in the database
        city = tracker.get_slot("city")
        if not isinstance(city, str):
            return [SlotSet("resolved_airport_icao", None)]
        if not city.strip():
            dispatcher.utter_message(text="Please name a city.")
            return [SlotSet("resolved_airport_icao", None)]

        search_city = city.lower().strip()
        matches = []

        for icao, data in AIRPORTS.items():
            # Filters for cities and ensures, that airport is valid and active.
            db_city_raw = data.get('city')
            if db_city_raw and isinstance(db_city_raw, str):
                db_city = db_city_raw.lower().strip()
                if search_city == db_city or search_city in db_city:
                    # Filters for common world region
                    if icao.startswith(('E', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'U', 'V', 'W', 'Y', 'Z')):
                        matches.append({
                            'icao': icao,
                            'name': data.get('name', 'Unknown Airport'),
                            'lat': data.get('lat'),
                            'lon': data.get('lon')
                        })

        # Case 1: No airports found
        if not matches:
            dispatcher.utter_message(text=f"Sorry, I could not find any airport for {city}. Please try again")
            return [SlotSet("airport_icao", None), SlotSet("resolved_airport_icao", None)]

        # Case 2: Exactly 1 match -> Set directly (incl. coordinates)
        elif len(matches) == 1:
            single_icao = matches[0]['icao']
            single_name = matches[0]['name']

            # Retrieves the coordinates from the global AIRPORTS database.
            airport_data = AIRPORTS.get(single_icao, {})
            try:
                latitude = float(airport_data.get('lat')) if airport_data.get('lat') is not None else 0.0
                longitude = float(airport_data.get('lon')) if airport_data.get('lon') is not None else 0.0
            except (ValueError, TypeError):
                latitude, longitude = 0.0, 0.0

            dispatcher.utter_message(text=f'For {city} I found the airport {single_name} ({single_icao})')
            # Saves the following parameters in slots.
            return [
                SlotSet("resolved_airport_icao", None),
                SlotSet("airport_icao", single_icao),
                SlotSet("lat", latitude),
                SlotSet("lon", longitude)
            ]

        # Case 3: Several airports where found
        else:
            return [
                SlotSet("airport_icao", None),
                SlotSet("resolved_airport_icao", matches)
            ]

class ActionAskAirportIcao(Action):
    def name(self) -> Text:
        return "action_ask_airport_icao"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        candidates = tracker.get_slot("resolved_airport_icao") or []

        # Creates dynamic buttons for the user
        buttons = []
        for c in candidates:
            # Important: The payload sets the slot directly when clicking the ICAO code
            payload_string = f'/SetSlots(airport_icao={c["icao"]})'
            buttons.append({
                'title': f"{c['name']} ({c['icao']})",
                'payload': payload_string
            })

        dispatcher.utter_message(
            text=f"I found {len(candidates)} airports matching your request. Please select one:",
            buttons=buttons
        )
        return []
