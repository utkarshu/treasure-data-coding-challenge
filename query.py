import os
import csv
import argparse
import tdclient
from prettytable import PrettyTable

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--format", choices=["csv", "tabular"],
                        help="output format", default="tabular")
    parser.add_argument("-e", "--engine", choices=["hive", "presto"],
                        help="query engine", default="presto")
    parser.add_argument("-c", "--col_list", help="comma separated list of columns",
                        default="*")
    parser.add_argument("-l", "--limit", type=int, help="query limit",
                        default=100)
    parser.add_argument("-m", "--min_time", type=int, help="minimum timestamp",
                        default=None)
    parser.add_argument("-M", "--max_time", type=int, help="maximum timestamp",
                        default=None)
    parser.add_argument("db_name", help="database name")
    parser.add_argument("table_name", help="table name")
    args = parser.parse_args()
    return args

def validate_arguments(args):
    if args.min_time and args.max_time:
        if args.min_time > args.max_time:
            print("min_time cannot be higher than max_time")
            exit(1)

def generate_query(args):
    if args.min_time == None:
        args.min_time = "NULL"
    if args.max_time == None:
        args.max_time = "NULL"
        
    if args.min_time == "NULL" and args.max_time == "NULL":
        where_time_condition = ""
    else:
        where_time_condition = "WHERE TD_TIME_RANGE(time, " + str(args.min_time) + ", " + str(args.max_time) + ") "

    query_string = "SELECT " + args.col_list + " " + \
                       "FROM " + args.table_name + " " + \
                       where_time_condition + " " + \
                       "LIMIT " + str(args.limit)
    return query_string

def generate_data_model(apikey):
    data_model = {}
    with tdclient.Client(apikey) as client:
        databases = client.databases()
        db_names = [db.name for db in databases]
        for db in databases:
            data_model[db.name] = [table.name for table in db.tables()]
    return data_model

def validate_database_table_input(args, data_model):
    if args.db_name not in data_model:
        print("There is no database named ", args.db_name, "in your TreasureData account")
        exit(1)
    if args.table_name not in data_model[args.db_name]:
        print("There is no table named", args.table_name, "in the database", args.db_name)
        exit(1)

def run_query(apikey, args, query_string):
    with tdclient.Client(apikey) as client:
        job = client.query(args.db_name, query_string, type=args.engine)
        job.wait()
        return list(job.result())

def write_tabular(field_names, result):
    t= PrettyTable(field_names)
    for row in result:
        t.add_row(row)
    output_filename = "output.txt"
    with open(output_filename, "w") as file:
        file.write(str(t))
    return output_filename

def write_csv(field_names, result):
    output_filename = "output.csv"
    with open("output.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if field_names is not None:
            writer.writerow(field_names)
        writer.writerows(result)
    return output_filename
    
def output_results(args, result):
    if args.col_list ==  "*":
        field_names = None
    else:
        field_names = args.col_list.split(",")

    if args.format == "tabular":
        output_filename = write_tabular(field_names, result)
    else:
        output_filename = write_csv(field_names, result)

    with open(output_filename,"r") as file:
        for line in file:
            print(line, end="")
    print()

def main():
    try:
        args = parse_arguments()
        validate_arguments(args)
        apikey = os.getenv("TD_API_KEY")
        query_string = generate_query(args)
        data_model = generate_data_model(apikey)
        validate_database_table_input(args, data_model)
        print("Running the query:", query_string, sep="\n")
        result = run_query(apikey, args, query_string)
        if len(result) == 0:
            print("No rows returned!")
            exit(0)
        output_results(args, result)      
    except Exception as e:
        print(e)
        exit(1)
    else:
        print("Success!")

if __name__ == "__main__":
    main()
