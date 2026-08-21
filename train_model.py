import pandas as pd 

data = pd.read_csv('/home/matias/turtlebot3_ws/turtlebot3_data.csv')

print(data.shape)
print(data.columns)
data.head()

from sklearn.model_selection import train_test_split

X = data.iloc[:, 2:-2]
y = data.iloc[:, -2:]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.2, random_state = 42     
)