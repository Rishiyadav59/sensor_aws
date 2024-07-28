from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging

from sensor.pipeline.training_pipeline import TrainPipeline

from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import load_object
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR

from  fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, File, UploadFile, Response
import pandas as pd


app = FastAPI()



origins = ["*"]
#Cross-Origin Resource Sharing (CORS) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",tags=["authentication"])
async def  index():
    return RedirectResponse(url="/docs")





@app.get("/train")
async def train():
    try:

        training_pipeline = TrainPipeline()

        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        training_pipeline.run_pipeline()
        return Response("Training successfully completed!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")
        




@app.get("/predict")
async def predict():
    try:

    # get data and from the csv file 
    # covert it into dataframe 
        a=16,18.0,16.0,0.0,0.0,0.0,0.0,0.0,0.0,5968.0,1440.0,1192.0,0.0,0.0,0.0,2922.0,0.0,156.0,0.0,892.0,1272.0,13512.0,12376.0,6820.0,142.0,0.0,0.0,0.0,0.0,8.0,6.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2484.0,6116.0,0.0,1224.0,2.0,2.0,6.0,8.0,6184.0,1174.0,0.0,0.0,0.0,6830.0,398.0,348.0,166.0,586.0,178.0,88.0,6.0,0.0,0.0,21260.0,2.0,2.0,0.0,0.0,2922.0,150.0,5040.0,1754.0,,,,6600.0,16.97,21260.0,21260.0,22008.0,25.0,0.0,2016.0,21060.0,8658.0,1209600.0,308.0,0.0,4.0,0.0,2232.96,0.0,5285.76,0.0,16.0,0.0,0.0,4508.0,1780.0,2246.0,66.0,0.0,0.0,0.0,0.0,10.0,44.0,21260.0,1224.0,10.0,14.0,18.0,10.0,1742.0,4946.0,632.0,4.0,0.0,14.0,18.0,1796.0,36.0,0.0,78.0,0.0,0.0,2452.0,40.0,112.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,164.0,0.0,0.0,0.0,0.0,32.0,16.0,1420.0,142.0,0.0,0.0,0.0,0.0,0.0,134.64,56.0,6556.0,1596.0,156.0,68.0,120.0,44.0,42.0,18.0,0.0,0.0,0.0,0.0

        df =pd.DataFrame (a)

        Model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not Model_resolver.is_model_exists():
            return Response("Model is not available")
        
        best_model_path = Model_resolver.get_best_model_path()
        model= load_object(file_path=best_model_path)
        y_pred=model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping,inplace=True)


        # get the prediction output as you wnat 


    except  Exception as e:
        raise  SensorException(e,sys)





def main():
    try:
            
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__ == "__main__":

    app_run(app ,host=APP_HOST,port=APP_PORT)
