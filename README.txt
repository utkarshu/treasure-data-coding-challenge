How to run this script?

Pre-requisites
Python 3.6 is installed and the environemnt variable is setup
Treasure Data client key is stored as an environment variable ("TD_API_KEY")

Packages used:
os, csv, argparse, tdclient, prettytable

Please install argparse, tdclient and prettytable through pip or Anaconda

Sample Output:

C:\Users\Utkarsh\Documents\TreausreData>query.py -c "time,order_id,quantity,profit" -M 1510462800 sample_superstore orders -l 10
Running the query:
SELECT time,order_id,quantity,profit FROM orders WHERE TD_TIME_RANGE(time, NULL, 1510462800)  LIMIT 10
+------------+----------------+----------+----------+
|    time    |    order_id    | quantity |  profit  |
+------------+----------------+----------+----------+
| 1499572800 | US-2017-150070 |    2     | -28.2744 |
| 1499572800 | CA-2017-100335 |    9     | 26.4654  |
| 1499572800 | CA-2017-128783 |    4     | 46.5432  |
| 1499572800 | CA-2017-128783 |    5     |  37.884  |
| 1499572800 | CA-2017-103877 |    3     | 757.4112 |
| 1499572800 | CA-2017-124401 |    3     |  2.355   |
| 1499572800 | CA-2017-124401 |    7     | 80.4839  |
| 1499572800 | CA-2017-100160 |    5     |  9.8685  |
| 1499572800 | CA-2017-100160 |    3     |  5.4432  |
| 1499572800 | CA-2017-100160 |    3     |  1.6524  |
+------------+----------------+----------+----------+
Success!

C:\Users\Utkarsh\Documents\TreausreData>query.py -f csv -c "time,order_id,quantity,profit" -M 1510462800 sample_superstore orders -l 10
Running the query:
SELECT time,order_id,quantity,profit FROM orders WHERE TD_TIME_RANGE(time, NULL, 1510462800)  LIMIT 10
time,order_id,quantity,profit
1462766400,US-2016-148110,7,-24.843
1462766400,CA-2016-154536,5,-7.3255
1462766400,CA-2016-133319,4,92.2368
1462766400,CA-2016-139409,4,12.208
1462766400,CA-2016-164490,2,3.3524
1462766400,CA-2016-110366,2,10.35
1462766400,CA-2016-160815,3,80.736
1462766400,CA-2016-136231,3,7.6284
1462766400,CA-2016-136231,7,-63.1092
1462766400,CA-2016-136231,2,6.799

Success!

C:\Users\Utkarsh\Documents\TreausreData>query.py
usage: query.py [-h] [-f {csv,tabular}] [-e {hive,presto}] [-c COL_LIST]
                [-l LIMIT] [-m MIN_TIME] [-M MAX_TIME]
                db_name table_name
query.py: error: the following arguments are required: db_name, table_name

C:\Users\Utkarsh\Documents\TreausreData>query.py sample_superstore orders1
There is no table named orders1 in the database sample_superstore

C:\Users\Utkarsh\Documents\TreausreData>query.py sample_superstore1 orders
There is no database named  sample_superstore1 in your TreasureData account

C:\Users\Utkarsh\Documents\TreausreData>query.py -c "time,order_id,quantity,profit" -m 1545000000 -M 1510462800 sample_superstore orders -l 10
min_time cannot be higher than max_time

C:\Users\Utkarsh\Documents\TreausreData>query.py -e engine1 sample_superstore orders
usage: query.py [-h] [-f {csv,tabular}] [-e {hive,presto}] [-c COL_LIST]
                [-l LIMIT] [-m MIN_TIME] [-M MAX_TIME]
                db_name table_name
query.py: error: argument -e/--engine: invalid choice: 'engine1' (choose from 'hive', 'presto')

C:\Users\Utkarsh\Documents\TreausreData>query.py --format text sample_superstore orders
usage: query.py [-h] [-f {csv,tabular}] [-e {hive,presto}] [-c COL_LIST]
                [-l LIMIT] [-m MIN_TIME] [-M MAX_TIME]
                db_name table_name
query.py: error: argument -f/--format: invalid choice: 'text' (choose from 'csv', 'tabular')

C:\Users\Utkarsh\Documents\TreausreData>query.py --limit "abc" sample_superstore orders
usage: query.py [-h] [-f {csv,tabular}] [-e {hive,presto}] [-c COL_LIST]
                [-l LIMIT] [-m MIN_TIME] [-M MAX_TIME]
                db_name table_name
query.py: error: argument -l/--limit: invalid int value: 'abc'

C:\Users\Utkarsh\Documents\TreausreData>query.py -m 1850000000 --limit 10 sample_superstore orders
Running the query:
SELECT * FROM orders WHERE TD_TIME_RANGE(time, 1850000000, NULL)  LIMIT 10
No rows returned!