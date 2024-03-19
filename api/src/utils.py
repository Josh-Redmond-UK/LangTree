import transformers
from transformers import AutoModel, AutoTokenizer
import torch



def get_model(name):
    return transformers.AutoModel.from_pretrained(name)