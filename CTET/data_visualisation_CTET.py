# Written by Rosalie Lucas

import matplotlib.pyplot as plt
import numpy as np

performance_1 = [0.067, 0.111, 0.061, 0.045, 0.163, 0.121, 0.179, 0.168, 0.084]
optimised_1 = [0.055, 0.098, 0.121, 0.055, 0.120, 0.159, 0.132, 0.122, 0.139]
plt.figure(figsize=(20, 20))
plt.rcParams.update({'font.family': 'Times'})
plt.rcParams.update({'font.size': 12})
fig, ax = plt.subplots()
index = np.arange(9)
bar_width = 0.4
opacity = 0.8
mod_1 = plt.barh(index + bar_width, performance_1, bar_width, color='red', alpha=opacity, label="Before")
mod_2 = plt.barh(index, optimised_1, bar_width, color="lightcoral", label="After")
plt.xlabel("Gini Importance")
plt.yticks(index + bar_width, ('chest','forehead', 'pinna', 'mastoid', 'finger', 'nose', 'DPG_finger-chest', 'DPG_nose-forehead', 'DPG_pinna-mastoid'))
plt.ylabel('Features')
plt.legend()
plt.tight_layout()
# plt.title('Model 1: Gini Importance per feature')
plt.savefig("Model_CTET_1.png", dpi=300, bbox_inches='tight')
plt.show()

features_2 = ['Age', 'Gender', 'MEQ_type', 'PSQI']
performance_2 = [0.415, 0.036, 0.114, 0.435]
optimised_2 = [0.410, 0.031, 0.136, 0.423]

fig2, ax2 = plt.subplots()
index2 = np.arange(4)

mod_3 = plt.barh(index2 + bar_width, performance_2, bar_width, color="green", alpha=opacity, label="Before")
mod_4 = plt.barh(index2, optimised_2, bar_width, color="lightgreen", label="After")
plt.xlabel("Gini Importance")
plt.yticks(index2 + bar_width, ('Age', 'Gender', 'MEQ_type', 'PSQI'))
plt.ylabel('Features')
plt.legend()
plt.tight_layout()
# plt.title('Model 2: Gini Importance per feature')
plt.savefig("Model_CTET_2.png", dpi=300, bbox_inches='tight')
plt.show()


performance_3 = [0.015, 0.002, 0.004, 0.012, 0.068, 0.109, 0.061, 0.043, 0.159, 0.116, 0.174, 0.160, 0.076]
optimised_3 = [0.065, 0.009, 0.023, 0.056, 0.057, 0.069, 0.094, 0.050, 0.106, 0.135, 0.115, 0.101, 0.121]

fig3, ax3 = plt.subplots()
index3 = np.arange(13)

mod_5 = plt.barh(index3 + bar_width, performance_3, bar_width, color="blue", alpha=opacity, label="Before")
mod_6 = plt.barh(index3, optimised_3, bar_width, color="lightskyblue", label="After")
plt.xlabel("Gini Importance")
plt.yticks(index3 + bar_width, ('Age', 'Gender', 'MEQ_type', 'PSQI', 'chest',
                               'forehead', 'pinna', 'mastoid', 'finger', 'nose', 'DPG_finger-chest',
                               'DPG_nose-forehead', 'DPG_pinna-mastoid'))
plt.ylabel('Features')
plt.tight_layout()
plt.legend()
# plt.title('Model 3: Gini Importance per feature')
plt.savefig("Model_CTET_3.png", dpi=300, bbox_inches='tight')
plt.show()



data = ['Train', 'Test']
y_pos = np.arange(len(data))
accuracy_1 = [0.8672, 0.58395]
accuracy_2 = [0.64351, 0.641975]
accuracy_3 = [0.867, 0.5802]

# create plot
fig_2, ax_2 = plt.subplots()
index_2 = np.arange(2)
bar_width = 0.3

model_1 = plt.bar(index_2, accuracy_1, bar_width,
                  color='red',
                  label='Model 1', alpha=opacity)

model_2 = plt.bar(index_2 + bar_width, accuracy_2, bar_width,
                  color='green',
                  label='Model 2', alpha=opacity)

model_3 = plt.bar(index_2 + bar_width * 2, accuracy_3, bar_width,
                  color='blue',
                  label='Model 3', alpha=opacity)

plt.ylabel('Accuracy')
plt.xlabel('Data')
#plt.title('Accuracy per model')
plt.xticks(index_2 + bar_width, ('Train', 'Test'))
plt.legend()
plt.ylim(0, 1)
#plt.tight_layout()
plt.savefig('accuracy_plot_CTET.png', dpi=300, bbox_inches='tight')
plt.show()

accuracy_1 = [0.6682, 0.63086]
accuracy_2 = [0.643209, 0.6444444444444444]
accuracy_3 = [0.658333333333, 0.6333333333]

# create plot
fig_5, ax_5 = plt.subplots()
index_2 = np.arange(2)
bar_width = 0.3

model_4 = plt.bar(index_2, accuracy_1, bar_width,
                  color='lightcoral',
                  label='Model 1')

model_5 = plt.bar(index_2 + bar_width, accuracy_2, bar_width,
                  color='lightgreen',
                  label='Model 2')

model_6 = plt.bar(index_2 + bar_width * 2, accuracy_3, bar_width,
                  color='lightskyblue',
                  label='Model 3')

plt.ylabel('Accuracy')
plt.xlabel('Data')
#plt.title('Accuracy per model')
plt.xticks(index_2 + bar_width, ('Train', 'Test'))
plt.legend()
plt.ylim(0,1)
#plt.tight_layout()
plt.savefig('accuracy_plot_CTET_2.png', dpi=300, bbox_inches='tight')
plt.show()



