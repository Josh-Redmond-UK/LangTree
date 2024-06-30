from transformers import AutoModel, AutoTokenizer
import pandas as pd
import numpy as np 
import json 


def get_next_topk_beams(text, model, tokenizer, next_tokens = 1, k=5):
    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(**inputs, num_beams=k, pad_token_id=tokenizer.eos_token_id,
                   num_return_sequences=k, max_new_tokens=next_tokens)

    return [tokenizer.decode(x) for x in outputs]



class treeNode:
    def __init__(self, text, depth=0, new_tokens=""):
        self.depth = depth
        self.text = text
        self.children = []
        self.new_tokens = new_tokens
    def add_child(self, obj):
        self.children.append(obj)
    

def tree_dfs(root, model, tokenizer, k=5, max_depth=20):
    if root.depth > max_depth:
        #print("depth", root.depth, root.text)
        return
    new_texts = get_next_topk_beams(root.text, model, tokenizer, 2, k)
    for t in new_texts:
        child = treeNode(t, root.depth+1, new_tokens=t[len(root.text):])
        root.add_child(child)
        tree_dfs(child, model, tokenizer, k, max_depth)


def tree_bfs(root, model, tokenizer, k=2, max_depth=3):
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node.depth < max_depth:
            new_texts = get_next_topk_beams(node.text, model, tokenizer, 2, k)
            for t in new_texts:
                child = treeNode(t, node.depth+1)
                node.add_child(child)
                queue.append(child)



def tree_to_dict(root_node):

    node_dict = {'text': root_node.text, 
                 'disp_text': root_node.new_tokens,
                 'depth': root_node.depth,
                 'children': [tree_to_dict(x) for x in root_node.children]}
    return node_dict


def serialize_tree(root_node):
    return json.dumps(tree_to_dict(root_node))


def attribute_node(input_text, node_text, model):
    att = model.attribute(input_text, node_text)
    df = pd.DataFrame(att.get_scores_dicts()[0]['target_attributions'])

    column_names = [x[1].replace('Ġ', ' ') for x in df.columns.values]
    row_names = [x[1].replace('Ġ', ' ') for x in df.index.values]

    vals = np.array(df.values)
    vals = np.ascontiguousarray(np.nan_to_num(vals)).squeeze().tolist()


    attribution_payload = {"col_names": column_names, "row_names": row_names,"data": vals}

    return json.dumps(attribution_payload)

async def tree_dfs_async(root, model, tokenizer, k=5, max_depth=20):
    if root.depth >= max_depth:
        return

    new_texts = get_next_topk_beams(root.text, model, tokenizer, 2, k)
    for t in new_texts:
        child = treeNode(t, root.depth+1, new_tokens=t[len(root.text):])
        root.add_child(child)
        yield child
        
        async for descendant in tree_dfs_async(child, model, tokenizer, k, max_depth):
            yield descendant
