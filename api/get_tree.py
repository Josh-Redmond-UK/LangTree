from transformers import pipeline, GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
import inseq
import torch
import json
import pandas as pd
import numpy as np
from src.utils import *
import base64

tokenizer_string = 'openai-community/gpt2'
model_string = 'openai-community/gpt2'
input_text = 'Once upon a time '


tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
model = GPT2LMHeadModel.from_pretrained(model_string)
attribution_model = inseq.load_model(model, "saliency")
inputs = tokenizer(input_text, return_tensors="pt")


tokenizer.pad_token_id = tokenizer.eos_token_id


rootnode = treeNode(input_text)

tree_dfs(rootnode, model, tokenizer, k=2, max_depth=2)
print(serialize_tree(rootnode))
print(attribution_model.attribute(input_text, input_text+" there was a cat in a castle").show())
print(attribute_node(input_text, input_text+" there was a cat in a castle", attribution_model))
