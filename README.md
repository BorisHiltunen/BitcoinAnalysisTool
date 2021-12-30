# Vincit

## Description
Vincit Application is a Flask project made with Python. The application returns wanted data in JSON form depending on the given input written in the URL (dates separated by the pipe symbol "|"). 

## Authors
Boris Hiltunen ([BorisHiltunen](https://github.com/BorisHiltunen))

## Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [JSON](https://www.json.org/json-en.html)
- [Datetime](https://docs.python.org/3/library/datetime.html)
- You can find required packets from requirements.txt

## Setup
- Clone or fork the repository.

- Install virtualenv if not already
-> (pip install virtualenv)

- Make an Virtual Environment
-> (virtualenv env Mac)

- Access it
-> (Windows -> .\env\Scripts\activate -> Mac source env/bin/activate)

- Install requirements.txt
-> (pip install -r requirements.txt)

- Run
-> (python runner.py)

## Application's structure
```GAP
- ├── app
- |   ├── helpers
- |   |   ├── __init__.py
- |   |   ├── timestamp_engine.py
- |   ├── json_formatters
- |   |   ├── __init__.py
- |   |   ├── buy_and_sell_dates_json_formatter.py
- |   |   ├── downward_trend_json_formatter.py
- |   |   ├── incorrect_input_json_formatter.py
- |   |   ├── trading_volume_json_formatter.py
- |   ├── __init__.py
- |   ├── buy_and_sell_dates.py
- |   ├── data_bank.py
- |   ├── data_updater.py
- |   ├── downward_trend.py
- |   ├── highest_trading_volume.py
- |   ├── price_iterator.py
- |   ├── sum_difference_iterator.py
- ├── env
- ├── .qitignore
- ├── README.md
- ├── requirements
- ├── runner.py
```

## Api endpoints:

```html 
localhost:5000/
```
<b>GET</b>
  - **/get/**
    ```python 
    Returns options
    ```
    
    For example: localhost:5000/get/
    
    ```python 
    1. downward_trend 2. highest_trading_volume 3. buy_and_sell_dates
    ```
    
  - **/get/downward_trend/date1|date2/**
    ```python 
    Returns downward trend data in JSON form 
    ```
    
    For example: localhost:5000/get/downward_trend/2021-11-25|2021-11-30/
    
    ```python 
        {
            "text":"In bitcoin's historical data from CoinGecko, the price decreased 3 days in a row from 2021-11-25 to 2021-11-27",
            "data": {
                "input":"2021-11-25|2021-11-30",
                "first_date":"2021-11-25",
                "second_date":"2021-11-30",
                "downward_trend_start_date": "2021-11-25",
                "downward_trend_end_date": "2021-11-27",
                "days": 3
            }
        }
    ```
    
  - **/get/highest_trading_volume/date1|date2/**
  
    ```python 
    Returns highest trading volume data in JSON form
    ```
    
    For example: localhost:5000/get/highest_trading_volume/2021-11-25|2021-11-30/
    
    ```python 
        {
            "text": "Highest trading volume date: 2021-11-26, Highest trading volume: 37420994605.317085",
            "data": {
                "input": "2021-11-25|2021-11-30",
                "first_date": "2021-11-25",
                "second_date": "2021-11-30",
                "highest_trading_volume_date": "2021-11-26",
                "highest_trading_volume_time": "15:00:00",
                "highest_trading_volume": 37420994605.317085
            }
        }
    ```
    
  - **/get/buy_and_sell_dates/date1|date2/**
  
    ```python 
    Returns buy and sell date data in JSON form
    
    Important
    -> The estimated wait time will be 1 Minute And 14 Seconds
       if you try to retrieve data from the start of bitcoin's history to the end.
    ```

    For example: localhost:5000/get/buy_and_sell_dates/2021-11-25|2021-11-30/
    
    ```python 
        {
            "text": "Buy date: 2021-11-27, Sell date: 2021-11-25",
            "data": {
                "input": "2021-11-25|2021-11-30",
                "first_date": "2021-11-25",
                "second_date": "2021-11-30",
                "buy_date": "2021-11-27",
                "sell_date": "2021-11-25",
                "buy_time": "00:00:00",
                "sell_time": "18:00:00",
                "buy_price": 47551,
                "sell_price": 52814,
                "profit": 5263.345551691731
            }
        }

    ```
