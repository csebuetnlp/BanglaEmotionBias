from data_handler import *
from prompt_creator import *
from models import *

# from Llama3 import *
from datetime import datetime
from tqdm import tqdm

logger = logging.getLogger(__name__)
#  export $(cat .env | xargs) && env


def generate_inference_data(
    data_handler: DataHandlerBase,
    prompt_creator: PromptCreator,
    model: Model,
    total: int = -1,
    calcualate_cost: bool = False,
):
    datapoints = data_handler.return_data_point(total)
    personas = data_handler.get_personas()
    total_input_tokens = 0
    total_output_tokens = 0
    prompt_version = data_handler.get_prompt_version()
    for data_point in tqdm(datapoints):
        current_index = data_point["ID"]
        logger.info(f"Current index: {current_index}")
        for persona in personas:
            logger.info(f"Current persona: {persona}")
            prompt = prompt_creator.create_prompt(
                prompt=data_point["text"],
                persona=persona,
                domain=data_point["Domain"],
                version=prompt_version,
            )
            try:
                model_response = model.create_response(prompt)
            except Exception as e:
                logger.error(
                    f"Error in creating response for index {current_index} and persona {persona}"
                )
                logger.error(e)
                continue
            # model_response = model.create_response(prompt)
            response = model_response["content"]

            data_handler.save_generated_data(
                response, persona=persona, index=current_index
            )

            if calcualate_cost:
                total_input_tokens += model_response["input_tokens"]
                total_output_tokens += model_response["output_tokens"]
                cost = model.calculate_cost(
                    model_response["input_tokens"], model_response["output_tokens"]
                )
                cost_till_now = model.calculate_cost(
                    total_input_tokens, total_output_tokens
                )
                logger.info(
                    f"Cost for index {current_index}: {cost}, Total cost: {cost_till_now}"
                )


def sanitize_log_name(filename):
    return filename.replace(" ", "_").replace(":", "_").replace("-", "_")


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--total", type=int, default=-1)
    parser.add_argument("--calculate_cost", type=bool, default=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    logging.basicConfig(
        filename=sanitize_log_name(f"./logs/data_generation_{datetime.now()}.log"),
        level=logging.INFO,
    )
    with open("hf_token.txt", "r") as f:
        token = f.read().strip("\n")

    data_handler = DataHandler(args.config)

    if "gpt" in data_handler.get_model_name():
        with open(".env", "w") as f:
            api_key = f.read().strip()
    else:
        api_key = ""
    message_creator = ChatGptMessageCreator()
    logger.info(f"Model name: {data_handler.get_model_name()}")
    model = ChatgptModel(
        model_name=data_handler.get_model_name(),
        key=api_key,
    )
    # model.activate_model()
    logger.info("Data generation started")
    generate_inference_data(
        data_handler=data_handler,
        prompt_creator=message_creator,
        model=model,
        total=args.total,
        calcualate_cost=args.calculate_cost,
    )

    logger.info("Data generation finished")
