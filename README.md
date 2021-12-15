# Vincit

## Description
VincitApplication is a Flask project made with Python. The application returns wanted data in JSON form depending on the given input written in the URL (dates separated by the pipe symbol "|"). 

## Authors
Boris Hiltunen ([BorisHiltunen](https://github.com/BorisHiltunen))

## Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [JSON](https://www.json.org/json-en.html)
- You can find required packets from Requirements.txt

## Setup
- pip install -r Requirements.txt

## Api endpoints:

```html 
localhost:5000/
```
<b>GET</b>
  - **/get**
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
    
    For example: localhost:5000/get/downward_trend/25-11-2021|30-11-2021/
    
    ```python 
        {
            "text": "In bitcoin's historical data from CoinGecko, the price decreased 7 days in a row for the inputs from 2021-11-25 02:00:00 and to 2021-11-30 03:00:00",
            "data": {
                "input": "25-11-2021|30-11-2021",
                "first_date": 1637798400.0,
                "second_date": 1638230400.0,
                "days": "7 days"
            }
        }
    ```
    
  - **/get/highest_trading_volume/date1|date2/**
  
    ```python 
    Returns highest trading volume data in JSON form
    ```
    
    For example: localhost:5000/get/highest_trading_volume/25-11-2021|30-11-2021/
    
    ```python 
        {
            "text": "2021-11-30 02:00:00:27436802911.974957",
            "data": {
                "input": "25-11-2021|30-11-2021",
                "first_date": "2021-11-25 02:00:00",
                "second_date": "2021-11-30 02:00:00",
                "highest_trading_volume_date": "2021-11-30 02:00:00",
                "highest_trading_volume": 27436802911.974957
            }
        }
    ```
    
  - **/get/buy_and_sell_dates/date1|date2/**
  
    ```python 
    Returns buy and sell date data in JSON form
    ```

    For example: localhost:5000/get/buy_and_sell_dates/25-11-2021|30-11-2021/
    
    ```python 
        {
            "text": "2021-11-27 02:00:00, 2021-11-29 21:00:00",
            "data": {
                "input": "25-11-2021|30-11-2021",
                "first_date": "2021-11-25 02:00:00",
                "second_date": "2021-11-30 02:00:00",
                "buy_date": "2021-11-27 02:00:00",
                "sell_date": "2021-11-29 21:00:00",
                "buy_price": 47551,
                "sell_price": 52161
            }
        }
    ```
