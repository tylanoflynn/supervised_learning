import pandas as pd
import numpy as np
import os
import json

class JSONFramer:
    def __init__(self, dir):
        self.directory = dir
        self.file_list = self._get_file_list()
        self.dataframe = pd.DataFrame()

    def _get_nested_value(self, data, *keys):
        try:
            for key in keys:
                data = data[key]
            return data
        except (TypeError, KeyError):
            return None
        
    def frame(self, eda = False, eda_limit = 5):
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
                            'branding_name': nested_json['data']['results'][0]['branding'][0]['name'],  
                            'baths': self._get_nested_value(result, 'description', 'baths'),
                            'baths_1qtr': self._get_nested_value(result, 'description', 'baths_1qtr'),
                            'baths_3qr': self._get_nested_value(result, 'description', 'baths_3qr'),
                            'baths_full': self._get_nested_value(result, 'description', 'baths_full'),
                            'baths_half': self._get_nested_value(result, 'description', 'baths_half'),
                            'beds': self._get_nested_value(result, 'description', 'beds'),
                            'garage': self._get_nested_value(result, 'description', 'garage'),
                            'lot_sqft': self._get_nested_value(result, 'description', 'lot_sqft'),
                            'name': self._get_nested_value(result, 'description', 'name'),
                            'sold_date': self._get_nested_value(result, 'description', 'sold_date'),
                            'sold_price': self._get_nested_value(result, 'description', 'sold_price'),
                            'sqft': self._get_nested_value(result, 'description', 'sqft'),
                            'stories': self._get_nested_value(result, 'description', 'stories'),
                            'sub_type': self._get_nested_value(result, 'description', 'sub_type'),
                            'type': self._get_nested_value(result, 'description', 'type'),
                            'year_built': self._get_nested_value(result, 'description', 'year_built'),                    
                            'is_coming_soon': self._get_nested_value(result, 'flags', 'is_coming_soon'),
                            'is_contingent': self._get_nested_value(result, 'flags', 'is_contingent'),
                            'is_for_rent': self._get_nested_value(result, 'flags', 'is_for_rent'),
                            'is_foreclosure': self._get_nested_value(result, 'flags', 'is_foreclosure'),
                            'is_new_construction': self._get_nested_value(result, 'flags', 'is_new_construction'),
                            'is_new_listing': self._get_nested_value(result, 'flags', 'is_new_listing'),
                            'is_pending': self._get_nested_value(result, 'flags', 'is_pending'),
                            'is_plan': self._get_nested_value(result, 'flags', 'is_plan'),
                            'is_price_reduced': self._get_nested_value(result, 'flags', 'is_price_reduced'),
                            'is_subdivision': self._get_nested_value(result, 'flags', 'is_subdivision'),                   
                            'last_update_date': self._get_nested_value(result, 'last_update_date'),
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
                            'open_houses': self._get_nested_value(result, 'open_houses'),
                            'price_reduced_amount': self._get_nested_value(result, 'price_reduced_amount'),
                            'brand_name': self._get_nested_value(result, 'products', 'brand_name'),
                            'property_id': self._get_nested_value(result, 'property_id'),
                            'status': self._get_nested_value(result, 'status'),
                            'tags': self._get_nested_value(result, 'tags'),
                        }
                        extracted_data.append(row)
                if not eda:
                    extracted_dataframe = pd.DataFrame(extracted_data).drop_duplicates("property_id")
                else:
                    extracted_dataframe = pd.DataFrame(extracted_data)
                self.dataframe = pd.concat([self.dataframe, extracted_dataframe])
            except:
                continue
  
    def _get_file_list(self):
        return os.listdir(self.directory)
        
    
        