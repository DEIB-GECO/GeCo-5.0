from geco_conversation import *


class DBScanClustering(AbstractAction):

    def help_message(self):
        pass

    def on_enter(self):
        self.context.add_bot_msg(
            Utils.chat_message("Do you want to apply parameter tuning?"))

        self.context.add_bot_msg(
            Utils.workflow("DBScan Clustering"))
        return None, False

    def logic(self, message, intent, entities):

        if intent == 'deny':
            self.context.add_bot_msg(Utils.chat_message("Ok! You have to define 2 parameters: the maximum distance between 2 samples and the number of samples in a neighborhood for a point to be considered as a core point."))
            self.context.add_bot_msg(Utils.chat_message("Start with the max distance, the default is 0.5. Do you want to change it? If yes, please provide me the number."))

            return EpsilonAction(self.context), False

        else:
            self.context.add_bot_msg(Utils.chat_message("Which is the minimum number of clusters you want to try?"))
            return TuningDBScan(self.context), False

class EpsilonAction(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        return None, False

    def logic(self, message, intent, entities):

        if intent == 'deny':
            self.context.payload.insert('epsilon',0.5)
        else:
            eps = float(message.strip())
            self.context.payload.insert('epsilon', eps)

        self.context.add_bot_msg(Utils.chat_message(
                "The minimum number of samples is 5 as default. Do you want to change it? If yes, please provide me the number."))
        return MinSamplesAction(self.context), True


class MinSamplesAction(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        return None, False

    def logic(self, message, intent, entities):

        if intent == 'deny':
            self.context.payload.insert('min_samples', 5)
        else:
            min_samples = int(message.strip())
            self.context.payload.insert('min_samples', min_samples)

        self.context.workflow.add(DBScan(self.context.workflow[-1], epsilon = self.status['epsilon'], min_samples=self.status['min_samples']))
        self.context.workflow.add(PCA(self.context.workflow[-1], 2))
        self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
        self.context.workflow.run(self.context.workflow[-1],self.context.session_id)
        print(self.context.workflow[-1].result.__dict__)
        self.context.add_bot_msg(
            Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                          self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
        self.context.add_bot_msg(Utils.chat_message(f"Ok, I did DBScan clustering using {self.status['epsilon']} and {self.status['min_samples']}."))

        return ByeAction(self.context), True

class TuningDBScan(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        return None, False

    def logic(self, message, intent, entities):

        if intent == 'deny':
            self.context.payload.insert('epsilon',0.5)
        else:
            eps = float(message.strip())
            self.context.payload.insert('epsilon', eps)

        self.context.add_bot_msg(Utils.chat_message(
                "The minimum number of samples is 5 as default. Do you want to change it? If yes, please provide me the number."))
        return MinSamplesAction(self.context), True