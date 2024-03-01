# Data Science Midterm Project

## Project/Goals

The goal of this project is to create a robust predictor of housing prices in American cities based on a dataset containing features such as location, size, and amenities.
## Process
### Data Processing and EDA
The regressor's purpose is to predict the ultimate sale price of a house. To that end, the dataset is refined to exclude features that enhance performance but cannot be accurately determined when a house is listed. For example, "list_price" is a near perfect predictor of "sale_price", but this is mainly due to the list price being determined by a domain expert (real estate agent) during listing. Similarly, "discounted_price_amount"(?) is excluded because it cannot be known during listing and is a pretty strong predictor of the overall sale_price, given that the discount tends to be in the 5-10% sale price range.
### Feature Engineering
### Pipeline Building and Tuning
The pipeline includes basic preprocessing of data as well as some custom transformers. [TargetAverager](notebooks/modules/TargetAverager.py) replaces a feature with the average over the target of that feature in the training data during fitting. It then appends the same average (only calculated over the training data) to the testing data when making predictions. We used this transformer to replace the "city" column with the average house price by city, as well as the state column with the average by state.

After preprocessing the only categorical variable that remains is "type", which is one-hot encoded. SKBest is used to filter the numerical features, with the k-number of features tuned along with model hyperparameters. The models that are tested and tuned during grid search are sklearn's ridge and lasso regression, random forest, gradient boost, and xgboost (xgboost.XGBRegressor, the xgboost libraries regressor with a sklearn wrapper placed on top). 

## Results
At the moment the [tuned model](notebooks/models) achieves an average R**2 on the testing data of 0.657 and a average RMSE of $139,096.67 over 5 runs with a fixed train/test split. This is a great deal more error than could be considered useful in terms of predicting a house's sale price.

## Challenges 
We definitely have insufficient data. The city with the largest amount of data in our current dataset is Dover, Delaware with 46 entries. This likely explains a lot of the variance in our model. We also had to restrict our dataset to ignore certain types of sales (very expensive sales, sales of land containing no houses, etc.) in order to to achieve useful results. The sale of bare land should probably be covered in a separate model since so few of the features in this model apply to bare land (baths, stories, sqft, many of the tags, etc.), but accurate results for very expensive, or very inexpensive, properties could probably be achieved if the dataset was more robust. 

## Future Goals
1. Data Collection: We need to obtain more data from the API in order to build a more robust model. It would also be useful to find a reliable source for average house price by city instead of relying on computation in the training data.
2. Try more computationally expensive models: We were somewhat limited by computing power while working on these initial models. There could be value in trying models such as SVM or FNN. We would also like to try DBSCAN for identifying more fine-tuned structure in the geographic distribution of the houses (latitude, longitude) and see if this grouping provides interesting results.
3. While many tuning passes were made, we were limited by time in how many we could make. It is possible that more passes would yield better results. Although, the difference between out-of-the-box random forest and tuned random forest is around $4000 RMSE, so maybe tuning will be more relevant for other models. At the moment, random forest is the best performing.

{'model': RandomForestRegressor(min_samples_split=5), 'model__min_samples_split': 5, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 44}
R2:0.7056662139280132
RMSE:155464.50029859363

{'model': RandomForestRegressor(min_samples_split=6), 'model__min_samples_split': 6, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 44}
R2:0.7177127158606593
RMSE:150527.32391236164

{'model': RandomForestRegressor(min_samples_split=7), 'model__min_samples_split': 7, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 52}
R2:0.6679173185988708
RMSE:161533.5962821743

{'model': RandomForestRegressor(min_samples_split=4), 'model__min_samples_split': 4, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 44}
R2:0.7050026593780689
RMSE:153513.3676749753

{'model': RandomForestRegressor(min_samples_split=7), 'model__min_samples_split': 7, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 44}
R2:0.698748484423361
RMSE:149447.15241166018

{'model': RandomForestRegressor(min_samples_split=6), 'model__min_samples_split': 6, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 36}
R2:0.6744893502133642
RMSE:158758.89152011194

{'model': RandomForestRegressor(min_samples_split=8), 'model__min_samples_split': 8, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 28}
R2:0.6290417250587398
RMSE:174231.6083363113

{'model': RandomForestRegressor(min_samples_split=7), 'model__min_samples_split': 7, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 60}
R2:0.6681815043143517
RMSE:170342.76141113337

{'model': RandomForestRegressor(min_samples_split=7), 'model__min_samples_split': 7, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 52}
R2:0.7048233196700822
RMSE:162046.60142513548

{'model': RandomForestRegressor(min_samples_split=5), 'model__min_samples_split': 5, 'model__n_estimators': 100, 'preprocessing__num__skbest__k': 44}
R2:0.6699809527674909
RMSE:163549.83377448845













