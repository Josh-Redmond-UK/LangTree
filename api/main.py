from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.websockets import WebSocketDisconnect
import asyncio
from src.utils import *
from transformers import  GPT2Tokenizer, GPT2LMHeadModel
import inseq
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi.middleware import Middleware
from fastapi.staticfiles import StaticFiles


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
valid_params = {'models':['openai-community/gpt2'], 'tokenizers':['openai-community/gpt2']}




middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Or specify your frontend origin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )]



app = FastAPI(middleware=middleware)
app.mount("/static", StaticFiles(directory="static"), name="static")

print("app loaded!")



@app.get("/")
async def root():
    return {"message": "LangTree API is running!"}

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
def update_params(tokenizer_string, model_string):
    if tokenizer_string in valid_params['tokenizers'] and model_string in valid_params['models']:
        tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
        model = GPT2LMHeadModel.from_pretrained(model_string)
        attribution_model = inseq.load_model(model, "saliency")
        return {"tokenizer": tokenizer_string, "model": model_string}
    else:
        raise HTTPException(status_code=422, detail="Invalid parameters")


@app.websocket("/ws/tree")
async def websocket_endpoint(websocket: WebSocket, text: str, k: int, max_depth: int):
    print(f"WebSocket connection attempt from {websocket.client}")
    try:
        await websocket.accept()
        print("web socket accepted")
        while True:
            data = await websocket.receive_text()
            print(data)
            root_node = treeNode(text, new_tokens=text)
            await websocket.send_json({"type": "node", "data": tree_to_dict(root_node)})
            print("sent first node")
            async for node in tree_dfs_async(root_node, model, tokenizer, k=int(k), max_depth=int(max_depth)):
                await websocket.send_json({"type": "node", "data": tree_to_dict(node)})
                print(node)
                await asyncio.sleep(0.01)
                print(f'sent node at {time.time()}')

            await websocket.send_json({"type": "complete"})
    except Exception as e:
        print(f"Error accepting WebSocket connection: {e}")
        raise e 
