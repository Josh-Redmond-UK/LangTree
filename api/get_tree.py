from transformers import pipeline, GPT2Tokenizer, GPT2Model, GPT2LMHeadModel
import inseq
import torch


tokenizer = GPT2Tokenizer.from_pretrained("openai-community/gpt2")
model = GPT2LMHeadModel.from_pretrained("openai-community/gpt2")


input_text = 'In computer '
inputs = tokenizer(input_text, return_tensors="pt")
#outputs = model(**inputs)
#model_path = 'openai-community/gpt2'
#generator = pipeline("text-generation", model=model_path)


tokenizer.pad_token_id = tokenizer.eos_token_id

outputs = model.generate(
   **inputs,
   num_beams=5,
   num_return_sequences=5,
   top_k=5,
   max_new_tokens=1,
   #num_beam_groups=5,
   do_sample=True,
   #diversity_penalty=0.5,

)
#for i, beam_output in enumerate(outputs):
#    print("{}: {}".format(i, tokenizer.decode(beam_output, skip_special_tokens=True)))
print("model outputs", outputs)
outputs2 = model(**inputs)
print("model outputs2", outputs2)
temperature= 1000.0
print("model logits", outputs2.logits)
print(outputs2.logits.shape)

next_token = outputs2.logits[:, -1]
next_token_logits = next_token / temperature
    

next_token_probs = torch.nn.functional.softmax(next_token_logits, dim=-1)

print("next token", next_token_probs.argmax())
print("next token", tokenizer.decode(next_token_probs.argmax()))


top_k_tokens = torch.topk(next_token, 5)
print("top k tokens", top_k_tokens[1][0])
print("number of k", len(top_k_tokens[1][0]))

for k in top_k_tokens[1][0]:
    print("token", tokenizer.decode(k))


def get_next_topk_greedy(text, model, tokenizer, temperature=1.0, k=5):
    tokenizer.pad_token_id = tokenizer.eos_token_id
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs)
    next_token_logits = outputs.logits[:, -1]
    # scale using temperature
    next_token_logits = next_token_logits / temperature
    

    next_token_probs = torch.nn.functional.softmax(next_token_logits, dim=-1)
    top_k_tokens = torch.topk(next_token_probs, k)
    new_texts = []

    for idx, t in enumerate(top_k_tokens[1][0]):
        new_texts.append(text + tokenizer.decode(t))

    return new_texts


def get_next_topk_beams(text, model, tokenizer, next_tokens = 1, k=5):
    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(**inputs, num_beams=k, 
                   num_return_sequences=k, max_new_tokens=next_tokens)

    return [tokenizer.decode(x) for x in outputs]
    #inputs = tokenizer(input_text, return_tensors="pt")
    #outputs = model(**inputs)
    next_token_logits = outputs.logits[:, -1]
    next_token_probs = torch.nn.functional.softmax(next_token_logits, dim=-1)
    top_k_tokens = torch.topk(next_token_probs, k)
    new_texts = []

    for idx, t in enumerate(top_k_tokens[1][0]):
        new_texts.append(text + tokenizer.decode(t))

    return new_texts




class treeNode:
    def __init__(self, text, depth=0):
        self.depth = depth
        self.text = text
        self.children = []
    def add_child(self, obj):
        self.children.append(obj)
    

def tree_dfs(root, model, tokenizer, k=5, max_depth=20):
    if root.depth > max_depth:
        print("depth", root.depth, root.text)
        return
    new_texts = get_next_topk_beams(root.text, model, tokenizer, 2, k)
    for t in new_texts:
        child = treeNode(t, root.depth+1)
        root.add_child(child)
        tree_dfs(child, model, tokenizer, k, max_depth)


def tree_bfs(root, model, tokenizer, k=2, max_depth=3):
    queue = [root]
    while queue:
        node = queue.pop(0)
        print("depth", node.depth, node.text)
        if node.depth < max_depth:
            new_texts = get_next_topk_beams(node.text, model, tokenizer, 2, k)
            for t in new_texts:
                child = treeNode(t, node.depth+1)
                node.add_child(child)
                queue.append(child)

rootnode = treeNode(input_text)



tree_dfs(rootnode, model, tokenizer, k=2, max_depth=10)