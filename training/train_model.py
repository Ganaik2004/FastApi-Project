import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from training.training_util import DATA_FILE_PATH, MODEL_PATH, MODEL_DIR

data = (
    pd.read_csv(DATA_FILE_PATH)
    .drop_duplicates()
    .drop(columns = ['name','model','edition'])
)

X = data.drop(columns = ['selling_price'])
Y = data.selling_price.copy()

X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

num_col = X_train.select_dtypes(include='number').columns.to_list()
cat_col = X_train.select_dtypes(include='object').columns.to_list()


num_pipe = Pipeline(steps=[
    ('imputer',SimpleImputer(strategy='median')), 
    ('scaler',StandardScaler())
])

cat_pipe = Pipeline(steps=[
    ('imputer',SimpleImputer(strategy='constant',fill_value='missing')),
    ('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))
])
preprocessor = ColumnTransformer(transformers=[
    ('num',num_pipe,num_col),
    ('cat',cat_pipe,cat_col)
])

preprocessor.fit_transform(X_train)
regressor =     RandomForestRegressor(
    n_estimators = 10,
    max_depth = 5,
    random_state = 42
)
rf_model = Pipeline(steps=[
    ('preprocessor',preprocessor),
    ('regressor',regressor)
])

rf_model.fit(X_train,Y_train)


os.makedirs(MODEL_DIR,exist_ok=True)
joblib.dump(rf_model,MODEL_PATH)