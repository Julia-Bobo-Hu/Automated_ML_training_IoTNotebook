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
