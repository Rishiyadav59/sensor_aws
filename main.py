from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging
#from  sensor.utils import dump_csv_file_to_mongodb_collecton
#from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig

from sensor.pipeline.training_pipeline import TrainPipeline

# def test_exception():
#     try:
#         logging.info("ki yaha p bhaiaa ek error ayegi diveision by zero wali error ")
#         a=1/0
#     except Exception as e:
#        raise SensorException(e,sys) 



if __name__ == "__main__":

    training_pipeline = TrainPipeline()
    training_pipeline.run_pipeline()
    # try:
    #     test_exception()
    # except Exception as e:
    #     print(e)