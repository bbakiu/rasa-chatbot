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
class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_first_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `first_name` value."""

        # If the name is super short, it might be wrong.
        print(f"First name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"first_name": None}
        else:
            return {"first_name": slot_value}

    def validate_last_name(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `last_name` value."""

        # If the name is super short, it might be wrong.
        print(f"Last name given = {slot_value} length = {len(slot_value)}")
        if len(slot_value) <= 2:
            dispatcher.utter_message(text=f"That's a very short name. I'm assuming you mis-spelled.")
            return {"last_name": None}
        else:
            return {"last_name": slot_value}

class ActionReceiveTranslate(Action):

    def name(self) -> Text:
        return "action_receive_translate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        text = tracker.latest_message['text']
        dispatcher.utter_message(text=f"I'll save the text you want to translate: {text}!")
        return [SlotSet("translate_text", text)]

class ActionSayTranslate(Action):

    def name(self) -> Text:
        return "action_say_translate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        translate = tracker.get_slot("translate_text")
        chuck_norris_url = "https://api.chucknorris.io/jokes/random"
        response_json = requests.get(chuck_norris_url)

        fact = json.loads(response_json.text)["value"]
        if not fact:
            dispatcher.utter_message(text="I don't know what you want to translate.")
        else:
            dispatcher.utter_message(text=f"Chuck fact: {fact}!")
        return []