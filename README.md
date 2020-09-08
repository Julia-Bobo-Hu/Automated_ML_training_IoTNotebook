# Automated_ML_training_IoTNotebook
This is the repository to show how to achieve automated ML model training by using a containerized IoT Notebook.
In the past, model re-training requires specialized ML knowledge to decide when the re-training can be initiated, 
and when the new ML model outperformed the old ML model, and therefore can replace the original ML model for inference.

This repository is establishing an automatic ML model re-training framework by using AWS IoT Analytics service.
It will demonstrate (1) how to setup the notebook as an IoT notebook, (2) how to containerize the notebook and 
(3) How to register the Sagemaker notebook image to Elastic Container Registry(ECR) with one-click operation. 
(4) Last but not least, how to setup trigger by using IoT Dataset to automatically trigger the IoT Notebook run.
(5) Write the final output as IoT container dataset back to S3 bucket for record-keeping of model accuracy history and final model deployment. 

## Step 1: Unzip the input data csv file from "data" folder, "jh_demo_batch_ml_train_dataset.csv". 

## Step 2: Go to AWS Sagemaker console, and choose "notebook instance", setup proper "SageMakerExecution" role, 
and choose a relatively large instance size, M5.4XLarge for this training job. 

## Step 3: Go to AWS IoT Analytics console, click on "Notebooks" tab, click on "Create" tab, select "Blank Notebook",
Select data set source, in this example, IoT dataset generated from the other repository is used as input, https://github.com/Julia-Bobo-Hu/Automated-Historian-IoT-Data-Exploration
However, a supplement csv file is also available for loading as: "jh_demo_batch_ml_train_dataset.csv". 
Next, select a notebook instance with the sagemaker notebook instance from step 2. Finally select "Create Notebook".

## Step 4: After the IoT Notebook created, there is a folder: "IoT Analytics" available in your sagemaker notebook. 
You can save the example notebook provided in this repository: "IoTAnalytics_jh_demo.ipynb" under "IoT Analytics" folder.

## Step 5: When first open the notebook, please make sure the kernel of this notebook is: "Containerized Python 3".
Without this kernel, the containerization step will fail.

## Step 6, Run through the notebook step by step, to understand the data loading, feature engineering, and ML model building procedures.
Highlights of this notebook are: (1) All feature engineering steps are quantitatively measured by using wrapper classes. 
The wrapper class used SKLearn Pipeline as base class, and then pass flag indicator as a class member to turn on and off specific feature engineering.
(2) The impact of different feature engineering steps are summarized in the following figure:
(3) After each training job, the accuracy of the training job and final training model as pkl file are dumped into a specific S3 bucket. 
The Object key of these documents contains the date timestamp to allow data scientist to access and make suitable deployment decisions.

## Step 7: After successfully run the IoT notebook, click on the "Containerize" tab on the top of your IoT Notebook. 
Please note, this step significantly reduce most painful steps listed in AWS IoTAnalytics documents to containerize the IoT Notebook.
https://docs.aws.amazon.com/iotanalytics/latest/userguide/automate-proceed.html
Most important improvement by using this API, is to avoid the manual ECR registration. 
This one-click operation will achieve image creation and ECR registration together. This process will take 30 minutes.

## Step 8: After step 7 completion, return to IoT Analytics platform, to create the Container Data Set.

    (1) Click on Data Sets → Create
    (2) Choose Container Data Sets → Create Container
    (3) Choose a unique ID for the Container Data Set → container_dataset, click Next
    (4) Choose the option → Link an existing data set’s query → Link
    (5) Select a trigger for your analysis → Choose mydataset → Schedule will be automatically populated, click Next
    (6) Select from your ECR Repository → Choose the repository container-app-ia (as per screenshot below)
    (7) Select your image → Choose the image with latest tag
    (8) Configure the input variables if you have any input variable, such as IoT dataset name. You don't need to provide any input variable with this notebook.
    (9) Select a Role → Choose the IAM Role → search & select iotAContainerRole. Please note, you need to attach the S3 bucket access policy with this role for this notebook.
    (10) Configure the capacity for container (container size need to be similar to M5.4Xlarge.
    (11) Configure the results retention period

## Step 9: After setup the above IoT container dataset, you can click in, and run the container dataset. The output should be written to relevant S3 bucket.

AWS IoT Analytics enabled you to trigger your training job with new IoT data ingestion, and use your custom training code in a container to analyze, 
process and enrich IoT thing data. It also allow you to combine data sources from various AWS Services. 
You can try different Sciki Learn ML models, MXnet, and other deep learning frameworks in Sagemaker Notebook environment. 
This automated training job will be automatically triggered, ran and sent quantitative training results to S3 Bucket without adding other extra AWS services (such as Lambda function to send results back).

There is also a notebook example to demonstrate autoML on this data. 
The motivation is to improve the model performance by using AutoGluon framework to leverage the stacking of model zoo. From our limited experience, the AutoGluon can improve the model accuracy by another 10%. 
Unfortunately, there is still dependancies conflict between AutoGluon and Containerized AWS Sagemaker notebook, and the AutoGluon model creation notebook cannot be containerized as IoTNotebook.   



