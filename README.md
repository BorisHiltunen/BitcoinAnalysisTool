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
  - **/get/downward_trend/date1|date2/**
    ```python 
    Returns downward trend data in JSON form 
    ```
  - **/get/highest_trading_volume/date1|date2/**
    ```python 
    Returns highest trading volume data in JSON form
    ```
  - **/get/buy_and_sell_dates/date1|date2/**
    ```python 
    Returns buy and sell date data in JSON form
    ```
