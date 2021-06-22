# Written by Rosalie Lucas
# Exploring Logistic regression models

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm
from scipy import stats
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

data_file_path = '/Users/roos/Data/all_trials_noNaN_CTET.csv'
data_file = pd.read_csv(data_file_path)

# x_norm = stats.zscore(X_train)
# logistic = LogisticRegression()
# logistic.fit(x_norm, Y_train)
# y_pred = logistic.predict(x_norm)
#
# confusion_matrix = pd.crosstab(Y_test, y_pred, rownames=['Actual'], colnames=['Predicted'])
# print('Accuracy: ',metrics.accuracy_score(Y_test, y_pred))
# print(confusion_matrix)
# plt.show()
data_l = data_file[['reaction_times', '9A00000045146841',
                    'F9000000452CCF41', '76000000452C9741', '7200000045201D41', '4B0000004516B141', 'CB000000452D7441',
                    'results']]
# data_l = data_file[['reaction_times', 'Age', 'Gender', 'PSQI', 'MEQ_type', 'results']]
# data_l = data_file[['reaction_times', 'Age', 'Gender', 'PSQI', 'MEQ_type', '9A00000045146841',
#                      'F9000000452CCF41', '76000000452C9741', '7200000045201D41', '4B0000004516B141', 'CB000000452D7441',
#                      'results']]
#
# encoder = LabelEncoder()
# label_encoder_gender = encoder.fit(data_l['Gender'])
# print("gender classes:", label_encoder_gender.classes_)
# integer_classes_gender = label_encoder_gender.transform(label_encoder_gender.classes_)
# print("Gender integer classes", integer_classes_gender)
# code = label_encoder_gender.transform(data_l['Gender'])
# data_l['Gender'] = code
#
# # MEQ_type
# label_encoder_MEQ = encoder.fit(data_l['MEQ_type'])
# print("MEQ classes:", label_encoder_MEQ.classes_)
# integer_classes_MEQ = label_encoder_MEQ.transform(label_encoder_MEQ.classes_)
# print("MEQ> integer classes", integer_classes_MEQ)
# code_MEQ = label_encoder_MEQ.transform(data_l['MEQ_type'])
# data_l['MEQ_type'] = code_MEQ

data_l['reaction_times'] = 1.0
Xl = data_l.drop('results', axis=1).values
Yl = data_l['results'].values
print('X shape: {}'.format(np.shape(Xl)))
print('Y shape: {}'.format(np.shape(Yl)))
x_normm = Xl
print(x_normm)
for x in range(len(x_normm)):
    np.insert(x, 0, 1)
# x_normm = stats.zscore(Xl)
# print(Xl)
X_trainl, X_testl, Y_trainl, Y_testl = train_test_split(x_normm, Yl, train_size=0.8, test_size=0.2, random_state=0)

logit_model = sm.Logit(Yl, x_normm)
result = logit_model.fit(maxiter=3000)
print(result.summary())
cov = result.cov_params()
print(cov)

pca = PCA(n_components=4)
pca.fit(x_normm)
print(pca.singular_values_)

logistic = LogisticRegression()
logistic.fit(X_trainl, Y_trainl)
y_pred = logistic.predict(X_testl)
print(y_pred)
confusion_matrix = pd.crosstab(Y_testl, y_pred, rownames=['Actual'], colnames=['Predicted'])
print(confusion_matrix)
print('Accuracy: ', metrics.accuracy_score(Y_testl, y_pred))
print(logistic.predict_proba(X_testl))

fpr, tpr, _ = metrics.roc_curve(Y_testl,  y_pred)
auc2 = metrics.roc_auc_score(Y_testl, y_pred)
plt.plot(fpr, tpr, c='red', alpha=0.8, label=auc2)
plt.show()