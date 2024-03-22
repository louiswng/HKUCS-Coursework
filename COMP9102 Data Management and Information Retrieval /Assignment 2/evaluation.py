import matplotlib.pyplot as plt

# eps = [0.1, 0.2, 0.4, 0.8]

# naive_comp = [10000, 10000, 10000, 10000]
# pivot_comp = [10.03, 16.71, 726.98, 7847.76]
# iDis_comp = [980.35, 2079.085, 4727.515, 10203.015]

# naive_time = [3.26, 3.27, 3.25, 3.34]
# pivot_time = [1.68, 1.85, 2.64, 6.41]
# iDis_time = [1.34, 1.83, 2.76, 5.31]

k = [1, 5, 10, 50, 100]
naive_time = [3.36, 3.42, 3.52, 3.93, 4.52]
pivot_time = [3.46, 4.52, 4.98, 6.40, 7.28]
iDis_time = [5.32, 5.63, 5.05, 5.61, 5.56]

# naive_comp = [10000, 10000, 10000, 10000, 10000]
# pivot_comp = [1325.075, 3156.76, 4139.145, 6653.57, 7663.865]
# iDis_comp = [9527.23, 9906.48, 9963.425, 10010.0, 10010.0]

# ax1 = plt.subplot(1, 2, 1)
plt.plot(k, naive_time, label='naive_time')
plt.plot(k, pivot_time, label='pivot_time')
plt.plot(k, iDis_time, label='iDis_time')
plt.legend(loc='upper right')
plt.xlabel('k')
plt.ylabel('total time (s)')
plt.show()
