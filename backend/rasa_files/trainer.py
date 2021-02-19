from rasa.shared.nlu.training_data.loading import load_data
from rasa.nlu.model import Trainer
from rasa.nlu import config
import os
import shutil
from tensorflow.keras.callbacks import EarlyStopping

import warnings
warnings.filterwarnings('ignore')

print("You may need to run the following commands:")
print('>> python -m spacy download "en_core_web_md"')
print('>> python -m spacy link en_core_web_md en')

#training_data = load_data('./rasa_files/nlu.md')
#trainer = Trainer(config.load("./rasa_files/config.yml"))
training_data = load_data('nlu.yml')
trainer = Trainer(config.load("config.yml"))
trainer.train(training_data)
model_directory = trainer.persist('./../model_dir/')  # Returns the directory the model is stored in

# Move directory to latest directory
latest_model_directory = os.path.join(os.path.dirname(model_directory), "latest_model")
shutil.rmtree(latest_model_directory, ignore_errors=True)
os.rename(model_directory, latest_model_directory)
