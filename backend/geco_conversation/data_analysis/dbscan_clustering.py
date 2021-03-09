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
            self.context.add_bot_msg(Utils.chat_message(
                "Ok! You have to define 2 parameters: the maximum distance between 2 samples and the number of samples in a neighborhood for a point to be considered as a core point."))
            self.context.add_bot_msg(Utils.chat_message(
                "Start with the max distance, the default is 0.5. Do you want to change it? If yes, please provide me the number."))

            return EpsilonAction(self.context), False

        else:
            self.context.add_bot_msg(Utils.chat_message(
                "Ok! You have to tell me the ranges to try for the two parameters: the maximum distance (epsilon) between 2 samples and the number of samples in a neighborhood for a point to be considered as a core point."))

            self.context.add_bot_msg(Utils.chat_message(
                "Which is the minimum epsilon you want to try? If you don't know, please tell me 0."))
            return TuningDBScan(self.context), False


class EpsilonAction(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        return None, False

    def logic(self, message, intent, entities):

        if intent == 'deny':
            self.context.payload.insert('epsilon', 0.5)
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

        self.context.workflow.add(
            DBScan(self.context.workflow[-1], epsilon=self.status['epsilon'], min_samples=self.status['min_samples']))
        self.context.workflow.add(PCA(self.context.workflow[-1], 2))
        self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
        self.context.workflow.run(self.context.workflow[-1], self.context.session_id)
        print(self.context.workflow[-1].result.__dict__)
        self.context.add_bot_msg(
            Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                          self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
        self.context.add_bot_msg(Utils.chat_message(
            f"Ok, I did DBScan clustering using {self.status['epsilon']} and {self.status['min_samples']}."))

        return ByeAction(self.context), True


class TuningDBScan(AbstractAction):
    def help_message(self):
        pass

    def on_enter(self):
        return None, False

    def logic(self, message, intent, entities):
        if 'min_eps' not in self.status:
            min = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('min_eps', min)
            self.context.add_bot_msg(Utils.chat_message(
                "Which is the maximum epsilon you want to try?"))
            return TuningDBScan(self.context), False
        elif 'max_eps' not in self.status:
            max = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('max_eps', max)
            self.context.add_bot_msg(Utils.chat_message(
                "Which is the minimum number of samples you want to try?"))
            return TuningDBScan(self.context), False
        elif 'min_samp' not in self.status:
            min = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('min_samp', min)
            self.context.add_bot_msg(Utils.chat_message(
                "Which is the maximum number of samples you want to try?"))
            return TuningDBScan(self.context), False
        else:
            max = int(''.join(filter(str.isdigit, message)))
            self.context.payload.insert('max_samp', max)

        self.context.workflow.add(
            DBScan(self.context.workflow[-1], tuning=True, min_eps=self.status['min_eps'],
                   max_eps=self.status['max_eps'], min_samp=self.status['min_samp'], max_samp=self.status['max_samp']))
        self.context.workflow.add(PCA(self.context.workflow[-1], 2))
        self.context.workflow.add(Scatter(self.context.workflow[-1], self.context.workflow[-2]))
        self.context.workflow.run(self.context.workflow[-1], self.context.session_id)
        print(self.context.workflow[-1].result.__dict__)
        self.context.add_bot_msg(
            Utils.scatter(self.context.workflow[-1].result.x, self.context.workflow[-1].result.y,
                          self.context.workflow[-1].result.labels, self.context.workflow[-1].result.u_labels))
        self.context.add_bot_msg(Utils.chat_message(
            f"Ok, I did DBScan clustering using parameter tuning with epsilon between [{self.status['min_eps']},{self.status['max_eps']}] and min_samples between [{self.status['min_samp']},{self.status['max_samp']}]."))
        return ByeAction(self.context), True
