import pandas as pd
import numpy as np
import os
import json

class JSONFramer:
    #initialize a single instance of JSONFramer
    def __init__(self, dir):
        self.directory = dir
        self.file_list = self._get_file_list()
        self.dataframe = pd.DataFrame()

    def print_stuff(self):
        print("stuff")
    
    #defining function to be used to pull values by indexed key from JSON files 
    def _get_nested_value(self, data, *keys):
        try:
            for key in keys:
                data = data[key]
            return data
        except (TypeError, KeyError):
            return None

    #returns list of files in the given directory
    def _get_file_list(self):
        return os.listdir(self.directory)
    
    #drop all rows where model's target variable ('sold_price') is null
    def dropna_target(self):
        self.dataframe.dropna(subset=['sold_price'], inplace=True)
        self.dataframe.reset_index(drop=True, inplace=True)
        return self.dataframe
    
    #Create dataframe, loop through json files to and iterate through JSON data to assign dataframe columns and values
    def frame(self, eda = False, eda_limit = 5):
        #loop to limit data used in exploratory data analysis
        i = 0
        for file in self.file_list:
            i += 1
            if eda == True:
                if i == eda_limit:
                    break
            try:
                #load json object
                with open('../data/' + file) as f:
                    nested_json = json.load(f)
                    response_data = nested_json['data']['results']
                    # List to store data from file
                    extracted_data = []
                    
                    for result in response_data:  
                        row = { 
                            'baths': self._get_nested_value(result, 'description', 'baths'),
                            'baths_full': self._get_nested_value(result, 'description', 'baths_full'),
                            'baths_half': self._get_nested_value(result, 'description', 'baths_half'),
                            'beds': self._get_nested_value(result, 'description', 'beds'),
                            'garage': self._get_nested_value(result, 'description', 'garage'),
                            'lot_sqft': self._get_nested_value(result, 'description', 'lot_sqft'),
                            'sold_date': self._get_nested_value(result, 'description', 'sold_date'),
                            'sold_price': self._get_nested_value(result, 'description', 'sold_price'),
                            'sqft': self._get_nested_value(result, 'description', 'sqft'),
                            'stories': self._get_nested_value(result, 'description', 'stories'),
                            'type': self._get_nested_value(result, 'description', 'type'),
                            'year_built': self._get_nested_value(result, 'description', 'year_built'),                    
                            'is_price_reduced': self._get_nested_value(result, 'flags', 'is_price_reduced'),
                            'show_contact_an_agent': self._get_nested_value(result, 'lead_attributes', 'show_contact_an_agent'),
                            'list_date': self._get_nested_value(result, 'list_date'),
                            'list_price': self._get_nested_value(result, 'list_price'),
                            'listing_id': self._get_nested_value(result, 'listing_id'),
                            'city': self._get_nested_value(result, 'location', 'address', 'city'),
                            'lat': self._get_nested_value(result, 'location', 'address', 'coordinate', 'lat'),
                            'lon': self._get_nested_value(result, 'location', 'address', 'coordinate', 'lon'),
                            'line': self._get_nested_value(result, 'location', 'address', 'line'),
                            'postal_code': self._get_nested_value(result, 'location', 'address', 'postal_code'),
                            'state': self._get_nested_value(result, 'location', 'address', 'state'),
                            'state_code': self._get_nested_value(result, 'location', 'address', 'state_code'),  
                            'price_reduced_amount': self._get_nested_value(result, 'price_reduced_amount'),  
                            'property_id': self._get_nested_value(result, 'property_id'),           
                            'tags': self._get_nested_value(result, 'tags')
                        }
                        extracted_data.append(row)
                if not eda:
                    extracted_dataframe = pd.DataFrame(extracted_data).drop_duplicates("property_id")
                else:
                    extracted_dataframe = pd.DataFrame(extracted_data)
                self.dataframe = pd.concat([self.dataframe, extracted_dataframe])
            except:
                continue
        return self.dataframe
    
