import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

df = pd.read_csv("earshells.csv")

df.describe()
outliers = {}
for column in df:
    if df[column].dtype == np.float64:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers[column] = df[(df[column] < lower_bound) | (df[column] > upper_bound)].index

#Create visualization
visualizations = {}
#for column in df:
#    visualizations[column] = df.plot(kind='box', x=column)
#plt.show()


# Data Cleaning
#def fill_missing_values(dataset, missing_values):
df.fillna(df.mean(), inplace=True)


#dataset = fill_missing_values(dataset, missing_values)



# Fix outliers
outliers_out = []
for column in outliers:
    outliers_in_column = outliers[column]
    outliers_out.extend(outliers_in_column)


df.drop(outliers_out, axis=0, inplace=True)

# Calculate average price for ear shells with diameter falling outside the interquartile range (IQR) of diameter
diameter = df["diameter"]
Q1_diameter = diameter.quantile(0.25)
Q3_diameter = diameter.quantile(0.75)
IQR_diameter = Q3_diameter - Q1_diameter
diameter_lower_bound = Q1_diameter - 1.5 * IQR_diameter
diameter_upper_bound = Q3_diameter + 1.5 * IQR_diameter

df_outside_IQR = df[(diameter >= diameter_lower_bound) | (diameter <= diameter_upper_bound)]

if df_outside_IQR.empty:
    print("Data frame is empty")
else:
    average_price = df_outside_IQR["price"].mean()
    print("Average price for ear shells with diameter falling outside the interquartile range (IQR) of diameter: ",
          average_price)



sns.pairplot(df, x_vars=['diameter', 'height', 'weight_whole'], y_vars='price', kind='reg')
#plt.show()


#training


# Split the data into feature and target variables
X = df[['sex', 'length', 'diameter', 'height', 'weight_whole', 'weight_shucked', 'weight_viscera', 'weight_shell', 'price']]
y = df['rings']

# One-hot encode the sex column
one_hot = pd.get_dummies(df, prefix='sex')

# Add the one-hot encoded columns to the dataframe
df = pd.concat([df, one_hot], axis=1)

# Drop the original "sex" column
df.drop('sex', axis=1, inplace=True)

#print(X, y)

# Split the data into training and testing sets
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
train_features, test_features, train_target, test_target = train_test_split(df.drop('rings', axis=1), df['rings'], test_size=0.2)

# Train the model using the training data
model = RandomForestRegressor(n_estimators=100)
#model.fit(X_train, y_train)
model.fit(train_features, train_target)

# Make predictions on the test data
#predictions = model.predict(X_test)
predictions = model.predict(test_features)


# Calculate the mean absolute error of the predictions
#mae = mean_absolute_error(y_test, predictions)
mae = mean_absolute_error(test_target, predictions)

# Print the mean absolute error
print("Mean Absolute Error:", mae)


"""

# Split the data into training and testing sets
train_features, test_features, train_target, test_target = train_test_split(df['test'], df['train'], test_size=0.2)

# Train the model using the training data
model = RandomForestRegressor(n_estimators=100)
model.fit(train_features, train_target)

# Make predictions on the test data
predictions = model.predict(test_features)

# Calculate the mean absolute error of the predictions
mae = mean_absolute_error(test_target, predictions)

# Print the mean absolute error
print("Mean Absolute Error:", mae)

"""