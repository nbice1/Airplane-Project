# Airplane-Project
This program uses machine learning to predict the level of turbulence experienced by a plane based on data about that plane (altitude, speed, number of engines, etc.). It begins by gathering data about various planes and storing it in a PostgreSQL table named plane_table. The program is written to store the table in a database named planes, which must first be created by the user in PostgreSQL. After downloading data on various planes currently flying, the program compares various machine learning models, followed by using a Decision Tree Classifier to make predictions on a validation dataset. The program then downloads new data and attempts to predict turbulence level after being trained on the original dataset. 

The dataset downloaded is updated every 60 seconds and contains data on an average of 5000 planes currently flying. More information on the dataset can be found here: https://www.adsbexchange.com/data/. In particular, turbulence is split into 4 possible values: 0 - no turbulence, 1 - light turbulence, 2 - medium turbulence, 3 - heavy turbulence. A list of the available types of data for predicting turbulence can be found here: https://www.adsbexchange.com/datafields/. Check the database_setup code to see which types of data were used in this project (abbreviations are explained at the same website). 

## Set up local environment 

1. Install & start postgres server.

2. Create ```planes``` database. 

3. Run ```python database_setup.py``` to establish table schema in postgres database. 

4. Run ```python plane_data.py``` to update the table with new rows. Ideally, run this multiple times in order to construct a large dataset, although for greater variation wait several hours each time (since the same plane will often be in the air for several hours). (I'm currently considering adding a script to do this automatically every 24 hours.)

5. Optional: Run ```python machine_learning_test.py``` to compare the accuracy of various models using 10-fold cross validation and then check the accuracy of a Decision Tree Classifier against a validation dataset (20% of total dataset). The program will print the accuracy score of the various models, followed by the accuracy score, confusion matrix, and classification report of the Decision Tree Classifier trained on the training dataset and tested against the validation dataset. A Decision Tree Classifier model was chosen since it had the highest accuracy score after various tests. 

6. Run ```python predict.py``` to create a new table called 'predictions' to store new plane data and use a Decision Tree Classifier to attempt to predict the turbulence level of the new dataset after being trained on the original dataset (stored in plane_table). The program will print the model's accuracy score, confusion matrix, and classification report. 

7. For repeated trials, first log back into postgres and drop the table 'predictions'. Then, run ```python predict.py``` again in order to repeat the trial. 
