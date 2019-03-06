import matplotlib.pyplot as plt
import pandas as pd
girls_grades = ['abcs','abcs','abcs','abcsdf','abcasdasdas','abcaewass','abcssasad']
boys_grades = ['xxabcs','xxansaabcs','xxabdfcs','axxxbcsdf','xabcasdasdas','axbcaewass','abxcssasad']
#grades_range = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
#plt.scatter(grades_range, girls_grades, color='r')
#plt.scatter(grades_range, boys_grades, color='g')
#plt.scatter(girls_grades, boys_grades, color = 'b')


plt.plot(girls_grades, boys_grades)

plt.xlabel('Grades Range')
plt.ylabel('Grades Scored')
plt.show()