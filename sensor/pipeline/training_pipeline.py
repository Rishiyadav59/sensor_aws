from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.exception import SensorException
from sensor.entity.artifact_entity import DataIngestionArtifact
from sensor.logger import logging
import os,sys
from sensor.components.data_ingestion import DataIngestion
from sensor.components.data_validation import DataValidation
from sensor.components.data_validation import DataValidationArtifact
from sensor.components.data_validation import DataValidationConfig

class TrainPipeline:

    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:

            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)

            logging.info("starting data ingestion")

            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)

            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()

            logging.info(f"data ingestion completed and artifacts:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)
        

    def start_data_validaton(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        logging.info("1")
        
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("2")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config = data_validation_config
            )
            logging.info("3")

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("4")
            return data_validation_artifact
    
        except  Exception as e:
            logging.info("aab")
            raise  SensorException(e,sys)

        
    
        
        
    def run_pipeline(self):
        try:

            data_ingestion_artifact:DataIngestionArtifact=self.start_data_ingestion()

            data_validation_artifact=self.start_data_validaton(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            raise Exception(e,sys)