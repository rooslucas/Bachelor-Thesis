import matplotlib.pyplot as plt
import numpy as np

performance_1 = [0.028, 0.055, 0.028, 0.023, 0.080, 0.054, 0.085, 0.072, 0.039, 0.197, 0.168, 0.171]
optimised_1 = [0.050, 0.060, 0.072, 0.046, 0.069, 0.110, 0.080, 0.069, 0.062, 0.179, 0.107, 0.097]
plt.figure(figsize=(20, 20))
plt.rcParams.update({'font.family': 'Times'})
plt.rcParams.update({'font.size': 12})
fig, ax = plt.subplots()
index = np.arange(12)
bar_width = 0.4
opacity = 0.8
mod_1 = plt.barh(index +bar_width, performance_1, bar_width, color="coral", alpha=opacity)
mod_2 = plt.barh(index, optimised_1, bar_width, color="darkcyan")
plt.xlabel("Gini Importance")
plt.yticks(index + bar_width, ('chest',
                               'forehead', 'pinna', 'mastoid', 'finger', 'nose', 'DPG_finger-chest',
                               'DPG_nose-forehead',
                               'DPG_pinna-mastoid', 'FLIR_forehead', 'FLIR_nose', 'FLIR_DPG_nose-forehead'))
plt.ylabel('Features')
plt.tight_layout()
# plt.title('Model 1: Gini Importance per feature')
plt.savefig("Model1_gi")
plt.show()

features_2 = ['Age', 'Gender', 'PSQI', 'MEQ_type']
performance_2 = [0.358, 0.064, 0.106, 0.472]
optimised_2 = [0.353, 0.065, 0.107, 0.474]

fig2, ax2 = plt.subplots()
index2 = np.arange(4)

mod_3 = plt.barh(index2 + bar_width, performance_2, bar_width, color="teal", alpha=opacity)
mod_4 = plt.barh(index2, optimised_2, bar_width, color="gold")
plt.xlabel("Gini Importance")
plt.yticks(index2 + bar_width, ('Age', 'Gender', 'PSQI', 'MEQ_type'))
plt.ylabel('Features')
plt.tight_layout()
# plt.title('Model 2: Gini Importance per feature')
plt.savefig("Model2_gi")
plt.show()


performance_3 = [0.005, 0.001, 0.002, 0.015, 0.025, 0.051, 0.027, 0.021, 0.081, 0.050, 0.087, 0.071, 0.035, 0.188, 0.168, 0.172]
optimised_3 = [0.021, 0.000, 0.005, 0.069, 0.034, 0.074, 0.058, 0.032, 0.060, 0.084, 0.061, 0.061, 0.072, 0.169, 0.106, 0.093]

fig3, ax3 = plt.subplots()
index3 = np.arange(16)

mod_5 = plt.barh(index3 + bar_width, performance_3, bar_width, color="chocolate", alpha=opacity)
mod_6 = plt.barh(index3, optimised_3, bar_width, color="mediumpurple")
plt.xlabel("Gini Importance")
plt.yticks(index3 + bar_width, ('Age', 'Gender', 'PSQI', 'MEQ_type', 'chest',
                               'forehead', 'pinna', 'mastoid', 'finger', 'nose', 'DPG_finger-chest',
                               'DPG_nose-forehead',
                               'DPG_pinna-mastoid', 'FLIR_forehead', 'FLIR_nose', 'FLIR_DPG_nose-forehead'))
plt.ylabel('Features')
plt.tight_layout()
# plt.title('Model 3: Gini Importance per feature')
plt.savefig("Model3_gi")
plt.show()



data = ['Train', 'Test']
y_pos = np.arange(len(data))
accuracy_1 = [1.0, 0.7383720930232558]
accuracy_2 = [0.7798833819241983, 0.7645348837209303]
accuracy_3 = [1.0, 0.7383720930232558]

# create plot
fig_2, ax_2 = plt.subplots()
index_2 = np.arange(2)
bar_width = 0.3

model_1 = plt.bar(index_2, accuracy_1, bar_width,
                  color='coral',
                  label='Model 1')

model_2 = plt.bar(index_2 + bar_width, accuracy_2, bar_width,
                  color='lightseagreen',
                  label='Model 2')

model_3 = plt.bar(index_2 + bar_width * 2, accuracy_3, bar_width,
                  color='darkolivegreen',
                  label='Model 3')

plt.ylabel('Accuracy')
plt.xlabel('Data')
#plt.title('Accuracy per model')
plt.xticks(index_2 + bar_width, ('Train', 'Test'))
plt.legend()
plt.tight_layout()
plt.savefig('accuracy_plot.png', dpi=300, bbox_inches='tight')
plt.show()

y_ps2 = [0.7798833819241983, 0.7645348837209303]
plt.bar(data, y_ps2, color='slateblue')
plt.xlabel("Data set")
plt.ylim(0, 1)
plt.ylabel('Hit percentage')
#plt.title('Hit percentage in training and testing set')
plt.savefig("Hit_rate")
plt.show()

accuracy_1 = [0.8112244897959183, 0.7761627906976745]
accuracy_2 = [0.7798833819241983, 0.7645348837209303]
accuracy_3 = [0.8061224489795918, 0.7790697674418605]

# create plot
fig_5, ax_5 = plt.subplots()
index_2 = np.arange(2)
bar_width = 0.3

model_4 = plt.bar(index_2, accuracy_1, bar_width,
                  color='coral',
                  label='Model 1')

model_5 = plt.bar(index_2 + bar_width, accuracy_2, bar_width,
                  color='lightseagreen',
                  label='Model 2')

model_6 = plt.bar(index_2 + bar_width * 2, accuracy_3, bar_width,
                  color='darkolivegreen',
                  label='Model 3')

plt.ylabel('Accuracy')
plt.xlabel('Data')
#plt.title('Accuracy per model')
plt.xticks(index_2 + bar_width, ('Train', 'Test'))
plt.legend()
#plt.tight_layout()
plt.savefig('accuracy_plot2.png', dpi=300, bbox_inches='tight')
plt.show()



