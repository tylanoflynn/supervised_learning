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
At the moment the model achieves an R**2 on the testing data of 0.624 and a RMSE of $165,028.67. This is a great deal more error than could be considered useful in terms of predicting a house's sale price.

## Challenges 
We definitely have insufficient data. The city with the most 

## Future Goals
(what would you do if you had more time?)
