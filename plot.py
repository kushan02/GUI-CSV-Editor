import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy as np

girls_grades = ['abcs', 'abcs', 'abcs', 'abcsdf', 'abcasdasdas', 'abcaewass', 'abcssasad']
boys_grades = ['xxabcs', 'xxansaabcs', 'xxabdfcs', 'axxxbcsdf', 'xabcasdasdas', 'axbcaewass', 'abxcssasad']
# grades_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# plt.scatter(grades_range, girls_grades, color='r')
# plt.scatter(grades_range, boys_grades, color='g')
# plt.scatter(girls_grades, boys_grades, color = 'b')

data_x_axis = [6,7,8,9,10]
data_y_axis = [1312,124813,418893,34891,71238]

#T = np.array([6, 7, 8, 9, 10, 11, 12])
#power = np.array([1.53E+03, 5.92E+02, 2.04E+02, 7.24E+01, 2.72E+01, 1.10E+01, 4.70E+00])

T = np.array(data_x_axis)
power = np.array(data_y_axis)

xnew = np.linspace(T.min(), T.max(), 300)  # 300 represents number of points to make between T.min and T.max

spl = make_interp_spline(T, power, k=3)  # BSpline object
power_smooth = spl(xnew)

plt.plot(xnew, power_smooth)
# ax.plot(data_x_axis, data_y_axis)
# plt.plot(x_smooth, y_smooth)
plt.show()
