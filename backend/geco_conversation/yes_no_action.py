from .abstract_action import AbstractAction

class YesNoAction(AbstractAction):
    def __init__(self, context, next_action_yes, next_action_no):
        super().__init__(context)
        self.next_yes = next_action_yes
        self.next_no = next_action_no

    def help_message(self):
        pass

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        if intent == 'affirm':
            return self.next_yes, True
        else:
            return self.next_no, True