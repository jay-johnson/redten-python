#!/usr/bin/env python

import sys, urllib, urllib2, re, logging, json, uuid, ast, datetime, os, requests, time, collections
from redten.shellprinting import lg, good, boom, mark, anmt, info
from redten.redten_client import RedTenClient, ppj

"""
More documentation and samples:

- Predictions with the IRIS dataset: https://github.com/jay-johnson/sci-pype/blob/master/red10/Red10-IRIS-Predictions.ipynb
- Forecast: https://github.com/jay-johnson/sci-pype/blob/master/red10/Red10-SPY-Multi-Model-Price-Forecast.ipynb

"""

# Login to red10
rt = RedTenClient()

csv_file = "/opt/work/data/src/iris.csv"
rloc = ""
sloc = ""

ds_name = "iris"
title = "IRIS Predictions - " + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
desc = "This is a Description for - " + str(title)

# What column has the labeled targets as integers? (added-manually to the dataset)
target_column_name = "ResultLabel"                 
# possible values in the Target Column
target_column_values = [ "Iris-setosa", "Iris-versicolor", "Iris-virginica" ] 

# What columns can the algorithms use for training and learning?
feature_column_names = [ "SepalLength", "SepalWidth", "PetalLength", "PetalWidth", "ResultTargetValue" ] 

# What column holds string labels for the Target Column?
label_column_name = "ResultLabel"
ignore_features = [ # Prune non-int/float columns as needed: 
                    target_column_name
                ]
if target_column_name != label_column_name:
    ignore_features.append(label_column_name)

predict_row = {
                "SepalLength"       : 5.4,
                "SepalWidth"        : 3.4,
                "PetalLength"       : 1.7,
                "PetalWidth"        : 0.2,
                "ResultTargetValue" : 0
            }

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

label_column_name = target_column_name
test_ratio = 0.1
sample_filter_rules = {}
algo_name = "xgb-regressor"

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
            "target_column_values" : target_column_values,
            "target_column_name" : target_column_name,
            "label_column_name" : label_column_name,
            "prediction_type" : "Predict",
            "ml_type" : "Predict with Filter",
            "train" : train_xgb
    }

"""

Wait on the Job to finish

"""

anmt("Launching Job")

job_id = None
job_data = {}
job_report = {}
job_res = {}
job_response = rt.run_job(post_data=post_data)

if job_response["status"] != "valid":
    boom("Predict job failed with error=" + str(job_response["status"]))
    sys.exit(1)
else:
    if "id" not in job_response["data"]:
        boom("Failed to create new Predict job")
        sys.exit(1)
    else:
        job_id = job_response["data"]["id"]
        job_status = job_response["data"]["status"]
        lg("Started Predict job=" + str(job_id) + " with current status=" + str(job_status))
# end of if job was valid or not

lg("Started Predict=" + str(ds_name) + " job=" + str(job_id), 6)


"""

Wait on the Job to finish

"""

if job_id == None:
    boom("Failed to start a new job")
    sys.exit(1)
else:
    lg("Waiting on results", 6)
    job_res = rt.wait_on_job(job_id)

    if job_res["status"] != "SUCCESS":
        boom("Job=" + str(job_id) + " failed with status=" + str(job_res["status"]) + " err=" + str(job_res["error"]))
        sys.exit(1)
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
    sys.exit(1)
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

Build Prediction Results

"""

lg("Building Prediction=" + str(ds_name) + " Results for job=" + str(job_id), 6)

# Build the prediction accuracy dictionary from the analysis
# and show the Predict dataframes
acc_results = rt.build_prediction_results(job_report)

# for all columns in the accuracy dictionary:
for col in acc_results:
    col_node = acc_results[col]
    
    lg("Column=" + str(col) + " accuracy=" + str(col_node["accuracy"]) + " mse=" + str(col_node["mse"]) + " num_predictions=" + str(len(col_node["predictions_df"].index)))

    # show the predictions
    lg(col_node["predictions_df"].head(5))
    
    lg("")
# end of showing prediction results


anmt("Building a new prediction from pre-trained, cached models")

predict_row = {
                "SepalLength"       : 5.4,
                "SepalWidth"        : 3.4,
                "PetalLength"       : 1.7,
                "PetalWidth"        : 0.2,
                "ResultTargetValue" : 0
            }

post_data = {
            "use_cached_job_id" : job_id,
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
            "target_column_values" : target_column_values,
            "target_column_name" : target_column_name,
            "label_column_name" : label_column_name,
            "prediction_type" : "Predict",
            "ml_type" : "Predict with Filter",
            "user_id" : 2,
            "train" : train_xgb,
            "max_features" : 10,
            "version" : 1
    }

job_data = {}
job_report = {}
job_res = {}
job_response = rt.run_job(post_data=post_data)

if job_response["status"] != "valid":
    boom("Predict job failed with error=" + str(job_response["status"]))
    sys.exit(1)
else:
    if "id" not in job_response["data"]:
        boom("Failed to create new Predict job")
        sys.exit(1)
    else:
        job_id = job_response["data"]["id"]
        job_status = job_response["data"]["status"]
        lg("Started Predict job=" + str(job_id) + " with current status=" + str(job_status))
# end of if job was valid or not

lg("Started Predict=" + str(ds_name) + " job=" + str(job_id), 6)


"""

Wait on the New Prediction Job to finish

"""


if job_id == None:
    boom("Failed to start a new Prediction job")
else:
    lg("Waiting on new Prediction results", 6)
    job_res = rt.wait_on_job(job_id)

    if job_res["status"] != "SUCCESS":
        boom("New Prediction Job=" + str(job_id) + " failed with status=" + str(job_res["status"]) + " err=" + str(job_res["error"]))
    else:
        job_data = job_res["record"]
        anmt("New Prediction Job Report:")
        lg(ppj(job_data), 5)
# end of waiting


"""

Get New Prediction Job Analysis

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

Build New Prediction Results

"""

lg("Building New Prediction=" + str(ds_name) + " Results for job=" + str(job_id), 6)

# Build the prediction accuracy dictionary from the analysis
# and show the Predict dataframes
acc_results = rt.build_prediction_results(job_report)

# for all columns in the accuracy dictionary:
for col in acc_results:
    col_node = acc_results[col]
    
    lg("Column=" + str(col) + " accuracy=" + str(col_node["accuracy"]) + " mse=" + str(col_node["mse"]) + " num_predictions=" + str(len(col_node["predictions_df"].index)))

    # show the predictions
    lg(col_node["predictions_df"].head(5))
    
    lg("")
# end of showing prediction results



"""

Get New Prediction's Analysis Images

"""

lg("Getting Predict=" + str(ds_name) + " Analysis Images for job=" + str(job_id), 6)

# unless matplotlib is installed this will fail showing plots:
job_res = rt.get_job_analysis(job_id, show_plots=False)

sys.exit(0)
