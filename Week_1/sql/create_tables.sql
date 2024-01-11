
CREATE TABLE ny_taxi (
  id INT PRIMARY KEY,
  pickup_datetime DATE,
  dropoff_datetime DATE,
  passenger_count INT,
  trip_distance FLOAT,
  pickup_longitude FLOAT,
  pickup_latitude FLOAT,
  dropoff_longitude FLOAT,
  dropoff_latitude FLOAT,
  fare_amount FLOAT,
  tip_amount FLOAT,
  total_amount FLOAT
);
