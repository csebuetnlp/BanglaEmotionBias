# Gender Bias In Bangla Emotion Attribution

In this repository we provide the data and code for the work `An Empirical Study of Gendered Stereotypes in Emotional Attributes for Bangla in Multilingual Large Language Models`. 

The two major sections in this work include `DataGeneration` and `GraphGeneration` directories that contain the code for emotion related LLM response generation and data visualization code for presenting results.

## Data Generation

The configurations required for data generation are to be mentioned in `config.yaml`. The data preprocessing is done in `data_handler.py` file. Prompting examples can be found in `prompt_creator.py`. The process to generate data is to place all the required data folders inside a directory named `Data` and then place the useable data in `config.yaml` file. Then the responses to be generated have to be modified inside `executor.py` file. We can also find the data generation logs inside `DataGeneration/logs` directory. Before starting the generation process, one needs to run `DataGeneration/installation.sh` or install `requirements.txt`.

```python
python executor.py
```
## GraphGeneration

The necessary codes for producing graph data are given inside `GraphGeneration` folder.
