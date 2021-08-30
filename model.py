import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split #For splitting the data into train & test
from sklearn.linear_model import LinearRegression #Linear regression model
#from sklearn.metrics import mean_squared_error #Metric for regression MSE

df=pd.read_csv("Student Database Final.csv")
df=df.dropna()
le=LabelEncoder()
df[["gender","school_type"]]=df[["gender","school_type"]].apply(lambda col : le.fit_transform(col))
x=df[["math_1","math_2","math_3","phy_1","phy_2","phy_3","chem_1","chem_2","chem_3","gender","sleeping_hours","distance_to_school (kms)","school_type","income(Rs)"]]
y=df["final_zscore"]
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)
regressor=LinearRegression()
regressor.fit(x_train,y_train)

pickle.dump(regressor, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
#print(model.predict([[100,100,100,100,95,100,100,95,100,1,5,50,1,250]]))