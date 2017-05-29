#!/usr/bin/env python

import sys, urllib, urllib2, re, logging, json, uuid, ast, datetime, os, requests, time, collections
from redten.shellprinting import lg, good, boom, mark, anmt, info
from redten.redten_client import RedTenClient, ppj

"""
More documentation and samples:

- Forecast: https://github.com/jay-johnson/sci-pype/blob/master/red10/Red10-SPY-Multi-Model-Price-Forecast.ipynb
- Predictions with the IRIS dataset: https://github.com/jay-johnson/sci-pype/blob/master/red10/Red10-IRIS-Predictions.ipynb

"""

# Login to red10
rt = RedTenClient()

csv_file = ""
rloc = ""
sloc = ""

ds_name = "SPY"
if len(sys.argv) > 1:
    ds_name = str(sys.argv[1]).upper()

# What column do you want to predict values?
target_column_name = "FClose"

# possible values in the Target Column
target_column_values = [ "GoodBuys", "BadBuys", "Not Finished" ] 

# What columns can the algorithms use for training and learning?
feature_column_names = [ "FHigh", "FLow", "FOpen", "FClose", "FVolume" ]

ignore_features = [ # Prune non-int/float columns as needed: 
                "Ticker",
                "Date",
                "FDate",
                "FPrice",
                "DcsnDate",
                "Decision"
            ]

train_xgb = {
                "learning_rate" : 0.20, 
                "num_estimators" : 50, 
                "sub_sample" : 0.20, 
                "col_sample_by_tree" : 0.90, 
                "col_sample_by_level" : 1.0, 
                "objective" : "reg:linear",
                "max_depth" : 3,
                "max_delta_step" : 0,
                "min_child_weight" : 1, 
                "reg_alpha" : 0, 
                "reg_lambda" : 1,
                "base_score" : 0.6,
                "gamma" : 0,
                "seed" : 42, 
                "silent" : True
            } 

predict_row = {
                "FHigh"   : 5.4,
                "FLow"    : 3.4,
                "FOpen"   : 1.7,
                "FClose"  : 0.2,
                "FVolume" : 0
            }

units_ahead_set = [ 5, 10, 15, 20, 25, 30 ]
units_ahead_type = "Days"

algo_name = "xgb-regressor"
title = str(ds_name) + " Forecast v5 - " + str(rt.uni_key())
desc = "Forecast simulation"
label_column_name = target_column_name
test_ratio = 0.1
sample_filter_rules = {}

# list of emails to send the analysis to on successful completion
send_to_email = []

# Allow a list of comma separated emails to be passed in 
# example: email1@email.com,email2@email.com
# note no spaces between them
if str(os.getenv("ENV_REDTEN_FORECAST_EMAILS", "")).strip().lstrip() != "":
    send_to_email = str(os.getenv("ENV_REDTEN_FORECAST_EMAILS", "")).strip().lstrip().split(",")

# allow the target dataset to load from the env for automation with docker
if csv_file == "" and sloc == "" and rloc == "":
    csv_file = str(os.getenv("ENV_REDTEN_CSV_FILE", "")).strip().lstrip()

post_data = {
            "predict_this_data" : predict_row,
            "title" : title,
            "desc" : desc,
            "ds_name" : ds_name,
            "feature_column_names" : feature_column_names,
            "ignore_features" : ignore_features,
            "csv_file" : csv_file,
            "rloc" : rloc,
            "sloc" : sloc,
            "algo_name" : algo_name,
            "test_ratio" : test_ratio,
            "target_column_values" : target_column_values,
            "target_column_name" : target_column_name,
            "label_column_name" : label_column_name,
            "user_id" : rt.get_uid(),
            "train" : train_xgb,
            "max_features" : 10,
            "tracking_type" : "",
            "units_ahead_set" : units_ahead_set,
            "units_ahead_type" : units_ahead_type,
            "prediction_type" : "Forecast",
            "ml_type" : "Playbook-UnitsAhead",
            "forecast_type" : "ETFPriceForecasting",
            "forecast_version" : 5,
            "valid_forecast_threshold" : 0.3,
            "sample_filters" : sample_filter_rules,
            "predict_units_back" : 90,
            "bypass_trading_day" : 1,
            "send_to_email" : send_to_email,
            "version" : 1
        }


"""

Wait on the job to finish

"""

anmt("Launching Job")

job_data = {}
job_report = {}
job_res = {}
job_response = rt.run_job(post_data=post_data)

if job_response["status"] != "valid":
    boom("Forecast job failed with error=" + str(job_response["status"]))
    sys.exit(1)
else:
    if "id" not in job_response["data"]:
        boom("Failed to create new forecast job")
        sys.exit(1)
    else:
        job_id = job_response["data"]["id"]
        job_status = job_response["data"]["status"]
        lg("Started Forecast job=" + str(job_id) + " with current status=" + str(job_status))
# end of if job was valid or not

lg("Started Forecast=" + str(ds_name) + " job=" + str(job_id), 6)


"""

Wait on the job to finish

"""


if job_id == None:
    boom("Failed to start a new job")
else:
    lg("Waiting on results", 6)
    job_res = rt.wait_on_job(job_id)

    if job_res["status"] != "SUCCESS":
        boom("Job=" + str(job_id) + " failed with status=" + str(job_res["status"]) + " err=" + str(job_res["error"]))
    else:
        job_data = job_res["record"]
        anmt("Job Report:")
        lg(ppj(job_data), 5)
# end of waiting


"""

Get Job Analysis

"""


job_report = {}
if job_id == None:
    boom("Failed to start a new job")
else:
    # Get the analysis, but do not auto-show the plots
    job_report = rt.get_job_analysis(job_id, show_plots=False)
    if len(job_report) == 0:
        boom("Job=" + str(job_id) + " failed")
        sys.exit(1)
    else:
        lg("")
    # if the job failed
# end of get job analysis


"""

Build Forecast Results

"""

lg("Building Forecast=" + str(ds_name) + " Results for job=" + str(job_id), 6)

# Build the forecast accuracy dictionary from the analysis
# and show the forecast dataframes
acc_results = rt.build_forecast_results(job_report)
for col in acc_results:
    col_node = acc_results[col]
    
    predictions_df = col_node["predictions_df"]
    date_predictions_df = col_node["date_predictions_df"]
    train_predictions_df = col_node["train_predictions_df"]
    
    lg("--------------------------------------------------")
    # for all columns in the accuracy dictionary:  
    lg("Column=" + str(col) + " accuracy=" + str(col_node["accuracy"]) + " mse=" + str(col_node["mse"]) + " num_predictions=" + str(len(col_node["date_predictions_df"].index)))
    # end of header line
    
    # show the timeseries forecast
    lg(date_predictions_df.head(5), 6)
    
    lg("")
# end of showing prediction results



"""

Get Analysis Images

"""

lg("Getting Forecast=" + str(ds_name) + " Analysis Images for job=" + str(job_id), 6)

# unless matplotlib is installed this will fail showing plots:
job_res = rt.get_job_analysis(job_id, show_plots=False)

sys.exit(0)
