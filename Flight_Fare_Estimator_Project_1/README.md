# Flight-Fare-Estimator-Project
Travelling through flights has become an integral part of today’s lifestyle as more and more people are opting for faster travelling options. The flight ticket prices increase or decrease every now and then depending on various factors like timing of the flights, destination, and duration of flights various occasions such as vacations or festive season. Therefore, having some basic idea of the flight fares before planning the trip will surely help many people save money and time.

# Approach
The main goal is to predict the fares of the flights based on different factors available in the dataset.
Data Collection : The data is collected from kaggle.
                  The data mainly consists of categorical column such as Airline,Source,Destination and etc.

Handling Categorical Columns: Using One Hot Encoding wasn't a good idea thats why i used lable Encoding Concept.
                              I give number of labels on the basis of mean price of Flightfare of each label.Refer LLD,HLD you will get it.

Model Creation: Model Creation is a crucial part of Machine learning project.Firstly I experimented using three Regression models that are
                SVR,RandomForestRegression,XGBRegressor and I did hyperparameter tuning of each model and XGBRegressor so i just kept only XGB 
                for my model Training approach.

Hyperparameter Tuning:I have done Hyperparameter tuning for XGB only and it helped me to get 89% r2 score and mean absolte error of 673

Model Saving: I saved my model using pickle as model.pickle

Webpage:Inside the webpage u will be able to see Enter Absolute path.There u have to paste the folder location in which your test data is present and then click on Input File Predict.
If you dont have test data u can basically download from Raw_Data_For_Testing in my github.
Results section will show you the results obtained and if it got any error it will also show it .
U can view logs section to checck what are the errors that occured.

# Project Interface
I have deployed this model to Google Cloud Platform
Link:http://ec2-3-141-18-169.us-east-2.compute.amazonaws.com:5000/
##### Type "Raw_Data_For_Testing" inside "Enter absolute file path." to check whether it is working or not
![web](https://user-images.githubusercontent.com/90147205/143179697-7077b188-49df-4561-bf82-e7f4fadf0f58.png)

# Technologies Used
1. Python
2. Sklearn
3. xgboost
4. Html,Css
5. Pandas,Numpy
6. Amazon Web Services
7. Flask and others

# Check out HLD,LLD for more info

# Help Me improve
Hello if you find any bug please consider raising issue. I will address them asap
