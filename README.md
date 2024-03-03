# Data Science Midterm Project
Alexandra Snelling and Tylan O’Flynn

## Project/Goals
The goal of this project is to create a robust predictor of housing prices in American cities based on a dataset containing features such as location, size, and amenities.

## Process
1. Load data to Pandas dataframes

2. Explore, clean and preprocess Data

3. Feature & External Data Engineering 

4. Perform Exploratory Data Analysis 

5. Save DataFrame to CSV

6. Load CSV into prediction pipeline

7. Perform train-test split on DataFrame

8. Replace city/state with average price 
    (training dataset only)

9. One-hot encode categorical features

10. Select (K=44) best numerical features


### Data Processing and EDA
The regressor's purpose is to predict the ultimate sale price of a house. To that end, the dataset is refined to exclude features that enhance performance but cannot be accurately determined when a house is listed. 
For example, "list_price" is a near perfect predictor of "sale_price", but this is mainly due to the list price being determined by a domain expert (real estate agent) during listing. 
Similarly, "discounted_price_amount"(?) is excluded because it cannot be known during listing and is a pretty strong predictor of the overall sale_price, given that the discount tends to be in the 5-10% sale price range.

1. Load data to Pandas dataframes:
**Loop through Real Estate data files and Parse JSONs to dataframe**

**Load US Cities Demographics Data from Open Data Soft CSV(2017):**
https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/

2. Explore, clean and preprocess your 
**Drop Columns:**
    Columns with 0 Non-Null Values 
    ‘branding_name’ column to Remove Unnecessary Duplication in Dataframe
    Columns with Unnecessary, Redundant and Rare Data: sub_type, last_update_date, last_update_date, 'is_new_listing, brand_name, status, show_contact_an_agent, is_foreclosure, 'line’, ‘listing_id’

**Explore Rows where target column is null:**
    Lack of NA sold_price represents significant data loss (appx. 18%)
    Perform Regression on sold_price and list_price
        Expected Slope: 1
        Actual Slope: 0.96
        RMSE: $86,375
    Impute sold_price from list_price
    Impute list_price from sold_price
    
**Drop any remaining rows where target column is null:**

**Encode nested list items in 'tags' columns using MultiLabelBinarizer from SKLearn**
    Drop binary tag columns represented in less that 5% of the data

**Fill N/A Values**
    Zeros: 'baths_full','baths_half', 'garage', 'price_reduced_amount'
    False: 'is_price_reduced'
    Mean, Median, etc.

**Drop Rows where value is NA for 'type' column**
    (*Drop Rows where value is NA for 'city' and ‘state’ column*)*should be performed

**Use Group By to Fill NA values with aggregate function in another column**
    Group By ‘type’ fill NA with Median for baths, beds, stories
    Group By ‘type’ fill NA with Mean for sqft, sqft_lot
    Group By ‘city’ fill NA with Median for ‘year_built’
    Group By 'state' and 'city' fill NA with median for 'lat' and 'lon' 

**Check for Duplicates in property_id**

**Fill all rows that still have NA values with Column Mean**

**Change column data types to facilitate EDA (most imported as object)**

**Drop columns not supplied as true predictive model input: 'list_price', 'price_reduced_amount'**


### Feature Engineering
3. Feature & External Data Engineering 
**Create Features using Datetime Values:**
    Convert 'sold_date' and 'list_date' to datetime values 
    remove timestamp from list_date
    Fill NA values for list_date with sold_date subtract 75days
    Create Columns from Datetime Values
        >Time on Market, 
        >Month/Year Sold/Listed
        >Drop ‘list_date', 'sold_date' following use in feature engineering

**Improve ‘type’ Feature:**
    Replace rare values with more general type for:
        condo, apartment, duplex_triplex, condo_townhome_rowhome_coop
    Drop rows where column = other
    Drop rows where type = Land due to lack of data
    (Note: Our model is not applicable to land value prediction)
    
**Join Real Estate Data with US Cities Demographics Data to add Features:**
        >Total Population
        >Median Age 
        >Household Count
    Fill ‘Total Population’ NA values with 33,000
    (Note: Demographics Data limited to cities with population >= 65,000)


### EDA
4. Perform Exploratory Data Analysis

**Explore Target Variable**
    Left Skewed (skewed value:  21.54)

**Perform Transformations: Log, Sqrt. Cbrt.**
    Log Transform (skewed value: -0.74)

**IQR Outlier Calculation for 'sold_price'**
(original target: skewed distribution)
    upper limit:   $ 943,937
    lower limit: - $ 226,562 
    outliers (all upper): 115 

**IQR Outlier Calculation for 'log_sold_price'**
(transformed target: normal distribution)
    upper limit: $1,851,713.00
    lower limit: $   57,918.00
    outliers (upper): 27 
    outliers (lower): 61

**Outlier Rows Dropped based on log transform limits**
**Original Data used without transformation as models could handle skewed data**

**Plots Correlation Matrix:**
    TOP 5 CORRELATED FEATURES:
         0.46 : baths
         0.38 : baths_full
         0.30 : beds
         0.32 : garage
         0.47 : sqft
    No individual feature correlation > 0.5


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













