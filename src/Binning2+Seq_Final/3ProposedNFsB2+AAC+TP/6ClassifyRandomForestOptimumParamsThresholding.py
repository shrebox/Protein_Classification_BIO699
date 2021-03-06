import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, roc_auc_score, accuracy_score, matthews_corrcoef, f1_score
import pandas as pd

iterations = 4
cvCount = 10
threshold = 0.490526315789474

best_params = [[False, 1, 66, 4, 'sqrt', 23], [False, 1, 59, 5, 'sqrt', 74],
               [False, 2, 66, 5, 'sqrt', 23], [False, 1, 218, 6, 'sqrt', 47]]

def getPredictionsGivenThreshold(myMatrix, th):
    myList = []
    for i in range(myMatrix.shape[0]):
        p1 = myMatrix[i, 1]
        if p1>= th:
            myList.append(1)
        else:
            myList.append(0)
    return np.asarray(myList)


overallPrecision = 0
overallRecall = 0
overallAuroc = 0
overallAccuracy = 0
overallMc = 0
overallF1 = 0
for i in range(iterations):
    X_train = np.load('X_train_' + str(i) + '.npy')
    Y_train = np.load('Y_train_' + str(i) + '.npy')
    skf = StratifiedKFold(n_splits=cvCount, random_state=42)
    foldPrecision = 0
    foldRecall = 0
    foldAuroc = 0
    foldAccuracy = 0
    foldMc = 0
    foldF1 = 0
    for train_index, test_index in skf.split(X_train, Y_train):
        X_tr, X_te = X_train[train_index], X_train[test_index]
        Y_tr, Y_te = Y_train[train_index], Y_train[test_index]
        bp = best_params[i]
        clf = RandomForestClassifier(bootstrap=bp[0], min_samples_leaf=bp[1], n_estimators=bp[2],
                                     min_samples_split=bp[3], max_features=bp[4], max_depth=bp[5],
                                     random_state=42).fit(X_tr, Y_tr.ravel())
        predictionsProb = clf.predict_proba(X_te)
        predictions = getPredictionsGivenThreshold(predictionsProb, threshold)
        precision = precision_score(Y_te, predictions)
        recall = recall_score(Y_te, predictions)
        auroc = roc_auc_score(Y_te, predictionsProb[:, 1])
        accuracy = accuracy_score(Y_te, predictions)
        matthewsCoeff = matthews_corrcoef(Y_te, predictions)
        f1score = f1_score(Y_te, predictions)

        foldPrecision += precision
        foldRecall += recall
        foldAuroc += auroc
        foldAccuracy += accuracy
        foldMc += matthewsCoeff
        foldF1 += f1score
    overallPrecision = overallPrecision + (foldPrecision/cvCount)
    overallRecall = overallRecall + (foldRecall/cvCount)
    overallAuroc = overallAuroc + (foldAuroc / cvCount)
    overallAccuracy = overallAccuracy + (foldAccuracy/cvCount)
    overallMc = overallMc + (foldMc/cvCount)
    overallF1 = overallF1 + (foldF1/cvCount)
print('Precision: ' + str(overallPrecision/iterations))
print('Recall: ' + str(overallRecall/iterations))
print('F1: ' + str(overallF1/iterations))
print('Accuracy: ' + str(overallAccuracy/iterations))
print('AUROC: ' + str(overallAuroc / iterations))
print('MCC: ' + str(overallMc/iterations))
print('Done')
