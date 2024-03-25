from fastapi import FastAPI, HTTPException
from src.utils import *
from transformers import  GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
import inseq
from fastapi.middleware.cors import CORSMiddleware

#default globals
global tokenizer_string
global model_string
global tokenizer
global model
tokenizer_string = 'openai-community/gpt2'
model_string = 'openai-community/gpt2'
tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
model = GPT2LMHeadModel.from_pretrained(model_string)
attribution_model = inseq.load_model(model, "saliency")

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 

valid_params = {'models':['openai-community/gpt2'], 'tokenizers':['openai-community/gpt2']}


@app.get("/api/tree/")
def get_tree(text, k, max_depth):
    root_node = treeNode(text, new_tokens=text)
    print("k", k, "max_depth", max_depth)
    tree_dfs(root_node, model, tokenizer, k=int(k), max_depth=int(max_depth))
    return serialize_tree(root_node)

@app.get("/api/attribute_text/")
def attribute_text(input_text, node_text):
    print(input_text)
    print(node_text)
    return attribute_node(input_text, node_text, attribution_model)
    

@app.get("/api/get_valid_params")
def get_valid_params():
    return valid_params

@app.post("api/update_params")
def update_paarams(tokenizer_string, model_string):
    if tokenizer_string in valid_params['tokenizers'] and model_string in valid_params['models']:
        tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
        model = GPT2LMHeadModel.from_pretrained(model_string)
        attribution_model = inseq.load_model(model, "saliency")
        return {"tokenizer": tokenizer_string, "model": model_string}
    else:
        raise HTTPException(status_code=422, detail="Invalid parameters")


