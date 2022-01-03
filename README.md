# Overview
This is proto-type to filter the W3C format logs.
([Test format](https://help.sumologic.jp/07Sumo-Logic-Apps/04Microsoft-and-Azure/IIS_10/Collect_Logs_for_the_IIS_10_App#iis-%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9-%E3%83%AD%E3%82%B0-w3c-%E3%83%87%E3%83%95%E3%82%A9%E3%83%AB%E3%83%88%E5%BD%A2%E5%BC%8F))

# How to use

- input the log file at "./input" directory
- edit "setting.json"
- run the following command

``` cmd
python filterlog.py
```

- select filter format

0. Filter by term(yyy/mm/dd HH:MM)
1. Filter by each of "sc-status" and "time-taken" term after filtering term
2. Filter by "sc-status" after filtering term
3. Filter by "time-taken" term after filtering term
4. Filter by "sc-status"
5. Filter by "time-taken"

- check "output" directory

# pip modules

- os
- json
- statistics