from dialogue_manager2 import CheckDataset
from dialogue_manager2 import Pivot, Classification

kb = {'retrieve_annotations': [CheckDataset],
      'retrieve_experiments': [CheckDataset],
      'pivot': [CheckDataset, Pivot],
      'classification': [CheckDataset, Pivot, Classification]}