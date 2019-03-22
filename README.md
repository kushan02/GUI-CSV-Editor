# fsf_2019_screening_task2

This project done for the completion of screening task for python, FOSSEE 2019 fellowship. The task requirement was to implement a fully functional GUI CSV Editor by using Python and PyQT as open source project hosted on github.

<details>
<summary>Features (Click to expand)</summary>

    1. Load a CSV file and view it in table form
    2. Add data to the table as a new blank row
    3. Edit Data in the table
    4. Delete data from the table:
        1) Option to delete whole column or whole row and also individual cells
    5. show/hide Columns: Select which columns should be visible in the desired table
    6. Plot any two columns with following plots in a new tab:
        1) Plot scatter points
        2) Plot scatter points with smooth lines
        3) Plot lines
    7. Ability to add a custom title for the plot on the fly
    8. Ability to flip the X and Y axes on the fly
    9. Save the plot as PNG file
    10. Prompt for saving the file in case any modifications are made to the original file
</details>

<details>
<summary>Screening Task for fossee fellowship 2019, IITB internship.</summary>

#### Technologies/Libraries to use:
  1. Python
  2. PyQt/Kivy
  
#### Instructions:

  1. Create a Github Account or Use your existing one.

  2. Create a new Repository in your Github Account for this task called fsf_2019_screening_task2

  3. Commit your code at regular intervals by doing small incremental changes to your code (committing huge blobs of code all at once is not recommended).

  4. The steps in “Description” below are general, minimum and mandatory guidelines. You are free to add well documented features to your application.

#### Description:

Following functionalities should be present in the application.

User should be able to:

  1. Load a csv file using ‘Load’ option available under “File” menu

  2. Display the complete data from the loaded csv as a table

  3. Edit the existing data in the table using ‘Edit data’ option under “Edit” menu.

  4. Add new data to the table using ‘Add data’ option under “File” menu.

  5. Select any number of columns from the displayed table

  6. Plot the data from any two selected columns should be available as buttons as mentioned below:
  
     1. Plot scatter points
     
     2. Plot scatter points with smooth lines
     
     3. Plot lines

  7. Click on any of the plot button. Plot should be generated accordingly in a new tab.
  
  8. Label x-axis and y-axis accordingly.
  
  9. Add a title to the graph.
  
  10. Save the plot as .png file using ‘Save as png’ option under “File” menu.
  
#### Submissions:

  1. Create a Github Account or Use your existing one.

  2. Create a new Repository in your Github Account for this task called fsf_2019_screening_task2

  3. Send the Link of your github repository to contact-om[at]fossee[dot]in
  
</details>

<details>
<summary>Usage (Click to expand)</summary>

1. Download the project from github or clone the repo to your machine using:

     ```
     git clone https://github.com/kushan02/fsf_2019_screening_task2.git
  	```
2. Install the project requirements using pip:

	If on linux, type:
  ```pip3 install -r requirements.txt```
  <br>
  	If on windows type
    ```pip install -r requirements.txt```

3. <b>NOTE:</b> If you are on ubuntu, you may need an additional step to get everything working:
	<br>
```sudo apt-get install python3-tk```
<br>(Matplot lib internally requires this for plotting on GUI)
4. To run the app, navigate to src folder in the terminal using ```cd src```
	<br>
    Now execute the app by:
    <br>
    ```python3 app.py``` if on Linux
    <br>
    ```python app.py``` if on Windows
 
</details>

<details>
<summary>Screenshots (Click to expand)</summary>

![Screenshot_1](https://i.postimg.cc/CKXjF80D/1.png "Home Screen")
![Screenshot_2](https://i.postimg.cc/C5Vk8Vzx/2.png "Loading Screen 1")
![Screenshot_3](https://i.postimg.cc/G2Dv9p3f/3.png "Loading Screen 2")
![Screenshot_4](https://i.postimg.cc/C5HDH6qH/4.png "Loading Screen 3")
![Screenshot_5](https://i.postimg.cc/FsN0smMP/5.png "Show/hide column option")
![Screenshot_6](https://i.postimg.cc/K8YLBfvB/6.png "Plot options")
![Screenshot_7](https://i.postimg.cc/Y211HjsG/7.png "Plot 1")
![Screenshot_8](https://i.postimg.cc/hPsTX6gK/8.png "Plot 2")
![Screenshot_9](https://i.postimg.cc/wTpQyDmQ/9.png "Plot 3")
![Screenshot_10](https://i.postimg.cc/FHFbGmGf/10.png "Plot 4")
![Screenshot_11](https://i.postimg.cc/dVW2xXS5/11.png "Plot 5")
![Screenshot_12](https://i.postimg.cc/8CjRQH2N/12.png "Save plot as PNG 1")
![Screenshot_13](https://i.postimg.cc/ncGYvMKb/13.png "Save plot as PNG 2")


</details>












