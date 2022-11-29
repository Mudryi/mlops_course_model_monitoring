import os
import logging
import numpy as np
import datetime
import requests

from joblib import load


class Classifier(object):
    def __init__(self):
        self.model = load(os.environ['MODEL_PATH'])

    def predict(self, X, features_names):
        # logging.info(X, features_names)
        start_time = datetime.datetime.now()

        y_prob = self.model.predict_proba(X)[:,1]

        time_diff = (datetime.datetime.now() - start_time)
        self._run_time = int(time_diff.total_seconds() * 1000)
        self.had_quotes = X[0, 3]>0
        self.score = float(np.round(y_prob , 3))

        self.send_to_evidently_service(X)
        return np.round(y_prob , 3)

    def send_to_evidently_service(self, record):
        cols = ['fico_score', 'lead_sold', 'dayofweek_created_at', 'successful_quote_count', 'age']
        rec = dict(zip(cols, record[0]))
        rec['prediction'] = self.score

        requests.post("http://192.168.49.2:30008/iterate/leads",  json=[rec])

    def metrics(self):
        metrics = [
            {"type": "COUNTER", "key": "model_calls", "value": 1},
            {"type": "GAUGE", "key": "gauge_runtime", "value": self._run_time},
            {"type": "TIMER", "key": "timer_runtime", "value": self._run_time},
            {"type": "TIMER", "key": "timer_scores", "value": self.score},
        ]
        if self.score > 0.5:
            metrics.append({"type": "COUNTER", "key": "predict_relevant", "value": 1})
        
        if self.had_quotes:
            metrics.append({"type": "GAUGE", "key": "scores_with_quotes", "value": self.score})
        
        return metrics
