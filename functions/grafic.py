import matplotlib
import matplotlib.pyplot as plt

#from configs.config_reader import get_config
#from framework.chat_checker import ChatChecker
#from rm import Rm

#def get_statistics():
x = [1, 2, 3, 4]
y = [1, 4, 9, 6]
labels = ['1', '2', '3', '4', '5']

plt.plot(x, y, 'ro')

plt.xticks(x, labels, rotation='horizontal')

plt.margins(0.5)

plt.subplots_adjust(bottom=0.20)
plt.show()
