# Vincit

## Description
VincitApplication is a Flask project made with Python. The application returns wanted data in JSON form depending on the given input written in the URL (dates separated by the pipe symbol "|"). 

## Authors
Boris Hiltunen ([BorisHiltunen](https://github.com/BorisHiltunen))

## Tools and Libraries
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [JSON](https://www.json.org/json-en.html)
- You can find required packets from requirements.txt

## Setup
- pip install -r requirements.txt

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
    
    For example: localhost:5000/get/downward_trend/25-11-2021|30-11-2021/
    
    ```python 
        {
            "text": "In bitcoin's historical data from CoinGecko, the price decreased 3 days in a row from 2021-11-25 to 2021-11-27",
            "data": {
                "input": "25-11-2021|30-11-2021",
                "first_date": "25-11-2021",
                "second_date": "30-11-2021",
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
    
    For example: localhost:5000/get/highest_trading_volume/25-11-2021|30-11-2021/
    
    ```python 
        {
            "text": "Highest trading volume date: 15:00:00, Highest trading volume: 37420994605.317085",
            "data": {
                "input": "25-11-2021|30-11-2021",
                "first_date": "25-11-2021",
                "second_date": "30-11-2021",
                "highest_trading_volume_date": "2021-11-26",
                "highest_trading_volume_time": "15:00:00",
                "highest_trading_volume": 37420994605.317085
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
            "text": "Buy date: 2021-11-27, Sell date: 2021-11-29",
            "data": {
                "input": "25-11-2021|30-11-2021",
                "first_date": "25-11-2021",
                "second_date": "30-11-2021",
                "buy_date": "2021-11-27",
                "sell_date": "2021-11-29",
                "buy_time": "00:00:00",
                "sell_time": "19:00:00",
                "buy_price": 47551,
                "sell_price": 52161,
                "profit": 4610.8124336957335
            }
        }
    ```
