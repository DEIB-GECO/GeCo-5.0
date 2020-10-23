from .abstract_action import AbstractAction
from .start_action import StartAction

class ProjectMetaAction(AbstractAction):

    def help_message(self):
        return []

    def on_enter(self):
        pass

    def logic(self, message, intent, entities):
        self.context.workflow.add_gmql('project_metadata',{'Dataset':self.context.data_extraction.datasets[-1]})