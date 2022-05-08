import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import normalize

def train_model():
  cars_data = pd.read_csv('data/autos.csv', encoding="cp1252")
  cars_data.head(10)
  cars_data.describe(include='all')
  cars_data.dtypes
  cars_data.isnull().sum() * 100 / len(cars_data)
  column_new_names = {
    "dateCreated": "ad_created",
    "dateCrawled": "date_crawled",
    "fuelType": "fuel_type",
    "lastSeen": "last_seen",
    "monthOfRegistration": "registration_month",
    "notRepairedDamage": "unrepaired_damage",
    "nrOfPictures": "num_of_pictures",
    "offerType": "offer_type",
    "postalCode": "postal_code",
    "powerPS": "power_ps",
    "vehicleType": "vehicle_type",
    "yearOfRegistration": "registration_year"
  }
  cars_data.rename(columns=column_new_names, inplace=True)
  cars_data[["ad_created", "date_crawled", "last_seen"]] = cars_data[["ad_created", "date_crawled", "last_seen"]].apply(pd.to_datetime)
  cars_data[["ad_created", "date_crawled", "last_seen"]].info()
  cars_data["price"] = cars_data["price"].str.strip().str.replace("[,$]", "", regex=True)
  cars_data["odometer"] = cars_data["odometer"].str.strip().str.replace("[,km]", "", regex=True)
  cars_data[["price", "odometer"]] = cars_data[["price", "odometer"]].apply(pd.to_numeric)
  unique_ratio_limit = 0.5
  data_string_columns = cars_data.select_dtypes(include=[object])
  string_columns_unique_ratio = data_string_columns.nunique()/data_string_columns.count()
  droppable_string_columns = columns_unique_ratio[string_columns_unique_ratio > unique_ratio_limit]
  cars_data = cars_data.drop(columns=droppable_string_columns.index)
  data_numeric_columns = cars_data.select_dtypes(include=[np.number])
  numeric_columns_unique_count = data_numeric_columns.nunique()
  droppable_numeric_columns = numeric_columns_unique_count[numeric_columns_unique_count <= 1]
  cars_data = cars_data.drop(columns=droppable_numeric_columns.index, errors='ignore')
  cars_data = cars_data.drop(columns=["name", "postal_code"], errors='ignore')
  cars_data['price'].groupby(pd.cut(cars_data['price'], np.arange(0, 100000, 100))).count()
  cars_data = cars_data[(cars_data['price'] >= 500) & (cars_data['price'] <= 40000)] # Inputkan kode disini
  print(cars_data['price'].sort_values())
  for column in cars_data.columns:
      if cars_data[column].dtype == 'object':
          cars_data[column] = cars_data[column].fillna(cars_data[column].mode()[0])
      elif cars_data[column].dtype == 'int64':
          cars_data[column] = cars_data[column].fillna(cars_data[column].median())
      else:
          cars_data[column] = cars_data[column].fillna('na')
  cars_data.info()
  data_numeric_columns = cars_data.select_dtypes(include=[np.number]).drop(columns=['price'])
  normalized_array = normalize(X=data_numeric_columns, norm="l2", axis=1)
  normalized_data = pd.DataFrame(normalized_array, columns=data_numeric_columns.columns)
  cars_data[data_numeric_columns.columns] = normalized_data
  cars_data

  def categorical_encoder(column, type):
      if type == 'nominal':
          data_dummies = pd.get_dummies(cars_data[column], columns=[column], prefix=[column] )
          data_with_dummy = cars_data.join(data_dummies)
      elif type == 'ordinal':
          label_encoder = preprocessing.LabelEncoder()
          label_encoder.fit(cars_data[column].values)
          cars_data[column + '_encoded'] = label_encoder.transform(cars_data[column].values)

  for column in cars_data.select_dtypes(include=[object]).columns:
      category_type = 'nominal'
      if column == 'unrepaired_damage':
          category_type = 'ordinal'
      categorical_encoder(column, category_type)

  cars_data
  
if __name__ == "__main__":
    print("START RUNNING PIPELINE")
    train_model()
    print("FINISHED RUNNING PIPELINE")