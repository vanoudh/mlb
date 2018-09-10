"""Created on Mon Jul  9 12:54:44 2018."""

import time
import pandas as pd
import sys
from automl import get_best_model
from sklearn.model_selection import train_test_split
from storage import DocStore, FileStore


ds = DocStore()
fs = FileStore()


def run(user_id, model):
    """Doc."""
    target = ds.get(user_id, 'target')
    path = fs.get_path(user_id, 'dataset')
    df = pd.read_csv(path)
    predictors = [v for v in target if target[v] == 'predictor']
    targets = [v for v in target if target[v] == 'target']
    X = df[predictors]
    y = df[targets[0]]
    print(X.head())
    print(y.head())
    if model == 'mock':
        time.sleep(5)
        score = 0.0099
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                            random_state=1)
        best_model = get_best_model(X_train, y_train, None, None, 0.1,
                                    verbose=1)
        # y_hat = best_model.predict(X_test)
        score = best_model.best_score_
    print("Score", score)
    ds.put(user_id, 'result', {model: score}, overwrite=True)


if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])