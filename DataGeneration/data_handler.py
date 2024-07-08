from abc import ABC, abstractmethod
import yaml
import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)

persona = ["man", "woman"]


def sanitize_model_name(model_name: str):
    model_name = model_name.split("/")[0]
    model_name = model_name.replace(".", "_").replace("-", "_")
    return model_name


class DataHandlerBase(ABC):
    @abstractmethod
    def get_model_name(self):
        pass

    @abstractmethod
    def get_prompt_version(self):
        pass

    @abstractmethod
    def return_data_point(self, total=-1):
        pass

    @abstractmethod
    def save_generated_data(self, content, persona, index, filepath=None):
        pass


class DataHandler(DataHandlerBase):
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.__read_config_file()

    def __read_config_file(self):
        with open(self.config_file_path, "r") as f:
            self.config = yaml.safe_load(f)

    def readfile(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error occurred while reading file: {e}\n")
            pass

    def __read_emotion_data(self):
        emotion_df = pd.read_csv(self.config["emotion_data_path"])
        print(f"Selected data points length: {len(emotion_df)}")
        return emotion_df

    def __is_datapoint_eligible(self, index, reject_for_one_response=True):
        # skip if the response already exists
        model_name = sanitize_model_name(self.config["model"])
        for per in persona:
            response_file_path = os.path.join(
                self.config["storage_folder_path"],
                str(index),
                f"{per}_{model_name}_response.txt",
            )
            if reject_for_one_response and os.path.exists(response_file_path):
                logger.info(f"Response already exist for index: {index}")
                return False

        return True

    def __create_valid_data_points(self):
        emotion_df = self.__read_emotion_data()
        emotion_df_valid_mask = emotion_df["ID"].apply(
            lambda x: self.__is_datapoint_eligible(x)
        )
        emotion_df_valid = emotion_df[emotion_df_valid_mask]
        return emotion_df_valid.to_dict(orient="records")

    def get_model_name(self):
        return self.config["model"]

    def get_personas(self):
        return persona

    def get_prompt_version(self):
        return self.config["prompt_version"]

    def return_data_point(self, total=-1):
        valid_data_points = self.__create_valid_data_points()

        for i, data_point in enumerate(valid_data_points):
            yield data_point
            if i == total - 1:
                break

    def save_generated_data(self, content, persona, index, filepath=None):
        if filepath is None:
            filename = (
                f"{persona}_{sanitize_model_name(self.config['model'])}_response.txt"
            )
            folder_path = os.path.join(self.config["storage_folder_path"], str(index))
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filepath = os.path.join(folder_path, filename)
        else:
            filepath = os.path.join(self.config["storage_folder_path"], filepath)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
                logger.info(f"Content saved to file: {filepath}\n")
        except Exception as e:
            logger.error(f"Error occurred while writing to file: {e}\n")
            pass  # Skip the operation if an error occurs


if __name__ == "__main__":
    data_handler = DataHandler("config.yaml")

    print(data_handler.get_model_name())
    datapoints = data_handler.return_data_point(1)
    for data in datapoints:
        print(data)
