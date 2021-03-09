# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

#
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class HealthForm(FormAction):

    def name(self):
        return "health_form"

    @staticmethod
    def required_slots(tracker):

        if tracker.get_slot('confirm_exercise') == True:
            return ["confirm_exercise", "exercise", "sleep",
             "diet", "stress", "goal"]
        else:
            return ["confirm_exercise", "sleep",
             "diet", "stress", "goal"

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "confirm_exercise": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                self.from_intent(intent="inform", value=True),
            ],
            "sleep": [
                self.from_entity(entity="sleep"),
                self.from_intent(intent="deny", value="None"),
            ],
            "diet": [
                self.from_text(intent="inform"),
                self.from_text(intent="affirm"),
                self.from_text(intent="deny"),
            ],
            "goal": [
                self.from_text(intent="inform"),
            ],
        }

from rasa_sdk.forms import FormValidationAction

class ValidateHealthForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_health_form"

    async def validate_confirm_exercise(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value:
            return {"confirm_exercise": True}
        else:
            return {"exercise": "None", "confirm_exercise": False }

class ActionSubmitResults(Action):
    def name(self) -> Text:
        return "action_submit_results"
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        confirm_exercise = tracker.get_slot("confirm_exercise")
        exercise = tracker.get_slot("exercise")
        sleep = tracker.get_slot("sleep")
        stress = tracker.get_slot("stress")
        diet = tracker.get_slot("diet")
        goal = tracker.get_slot("goal")

        response = create_health_log(
                confirm_exercise=confirm_exercise,
                exercise=exercise,
                sleep=sleep,
                stress=stress,
                diet=diet,
                goal=goal
            )

        dispatcher.utter_message("Thanks, your answers have been recorded!")
        return []