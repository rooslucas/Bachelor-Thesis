import matplotlib.pyplot as plt
import numpy as np

features_1 = ['chest', 'forehead', 'pinna', 'mastoid', 'finger', 'nose', 'DPG_finger-chest', 'DPG_nose-forehead',
              'DPG_pinna-mastoid', 'FLIR_forehead', 'FLIR_nose', 'FLIR_DPG_nose-forehead']
performance_1 = [0.030, 0.055, 0.030, 0.027, 0.081, 0.056, 0.088, 0.076, 0.035, 0.191, 0.169, 0.162]
plt.figure(figsize=(20,8))
plt.rcParams.update({'font.family':'Times'})
plt.rcParams.update({'font.size':12})

plt.barh( features_1, performance_1, color="coral")
plt.xlabel("Gini Importance")
plt.ylabel('Features')
#plt.title('Model 1: Gini Importance per feature')
plt.savefig("Model1_gi")
plt.show()

features_2 = ['Age', 'Gender', 'PSQI', 'MEQ_type']
performance_2 = [0.257, 0.095, 0.118, 0.529]
plt.figure(figsize=(20,8))
plt.barh( features_2, performance_2, color="lightseagreen")
plt.xlabel("Gini Importance")
plt.ylabel('Features')
#plt.title('Model 2: Gini Importance per feature')
plt.savefig("Model2_gi")
plt.show()

features_3 = ['Age', 'Gender', 'PSQI', 'MEQ_type', 'chest', 'forehead', 'pinna', 'mastoid', 'finger', 'nose', 'DPG_finger-chest', 'DPG_nose-forehead',
              'DPG_pinna-mastoid', 'FLIR_forehead', 'FLIR_nose', 'FLIR_DPG_nose-forehead']
performance_3 = [0.005, 0.001, 0.003, 0.016, 0.027, 0.052, 0.026, 0.023, 0.085, 0.047, 0.090, 0.074, 0.034, 0.187, 0.164, 0.165]
plt.figure(figsize=(20,8))
plt.barh( features_3, performance_3, color="darkolivegreen")
plt.xlabel("Gini Importance")
plt.ylabel('Features')
#plt.title('Model 3: Gini Importance per feature')
plt.savefig("Model3_gi")
plt.show()

data = ['Train', 'Test']
y_pos = np.arange(len(data))
accuracy_1 = [1.0, 0.7413]
accuracy_2 = [0.7709, 0.8023]
accuracy_3 = [1.0, 0.744]

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

y_ps2 = [0.77, 0.80]
plt.bar(data, y_ps2, color='slateblue')
plt.xlabel("Data set")
plt.ylim(0, 1)
plt.ylabel('Hit percentage')
#plt.title('Hit percentage in training and testing set')
plt.savefig("Hit_rate")
plt.show()
