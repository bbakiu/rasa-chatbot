# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from typing import Text, List, Any, Dict
from rasa_sdk.events import SlotSet
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests
import json
import pathlib

languages = pathlib.Path("data/languages.txt").read_text().split("\n")

class ValidateTranslateForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_translate_form"

    def validate_language_source(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `language_source` value."""

        # If the name is super short, it might be wrong.
        print(f"language_source given = {slot_value} length = {len(slot_value)}")
        language = slot_value
        if language not in languages:
            dispatcher.utter_message(text=f"That's a language I don't understand. Check if you mis-spelled it.")
            return {"language_source": None}
        else:
            return {"language_source": slot_value}

    def validate_language_target(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `language_target` value."""

        # If the name is super short, it might be wrong.
        print(f"language_target given = {slot_value} length = {len(slot_value)}")
        language = slot_value
        if language not in languages:
            dispatcher.utter_message(text=f"That's a language I don't understand. Check if you mis-spelled it.")
            return {"language_target": None}
        else:
            return {"language_target": slot_value}

class ActionSayTranslate(Action):

    def name(self) -> Text:
        return "action_say_translate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        translate_text = tracker.get_slot("translate_text")
        language_source = tracker.get_slot("language_source")
        language_target = tracker.get_slot("language_target")
        chuck_norris_url = "https://api.chucknorris.io/jokes/random"
        response_json = requests.get(chuck_norris_url)

        fact = json.loads(response_json.text)["value"]
        if not fact:
            dispatcher.utter_message(text="I don't know what you want to translate.")
        else:
            dispatcher.utter_message(text=f"Chuck fact: {fact}!")
            dispatcher.utter_message(text=f"To translate from {language_source} to {language_target}: {translate_text}!")
        return []