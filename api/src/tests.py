import unittest
import inseq
from utils import *
import json
from transformers import  GPT2Tokenizer, GPT2Model, GPT2LMHeadModel

class MyTestCase(unittest.TestCase):

    def test_tree(self):
        test_node = treeNode("Hello, world!")
        test_node.add_child(treeNode("Hello, world, 2!"))
        assert len(test_node.children) == 1
    
    def test_get_next_topk_beams(self):
        tokenizer_string = 'openai-community/gpt2'
        model_string = 'openai-community/gpt2'
        tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
        model = GPT2LMHeadModel.from_pretrained(model_string)

        root = treeNode("Hello, ")
        outputs = get_next_topk_beams(root.text, model, tokenizer, 2, 5)

        assert len(outputs) == 5
    
    def test_dfs(self):
        tokenizer_string = 'openai-community/gpt2'
        model_string = 'openai-community/gpt2'
        tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
        model = GPT2LMHeadModel.from_pretrained(model_string)
        root = treeNode("Hello, ")
        tree_dfs(root, model, tokenizer, 2, 5)
        assert len(root.children) == 2

    def test_bfs(self):
        tokenizer_string = 'openai-community/gpt2'
        model_string = 'openai-community/gpt2'
        tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_string)
        model = GPT2LMHeadModel.from_pretrained(model_string)
        root = treeNode("Hello, ")
        tree_bfs(root, model, tokenizer, 2, 5)
        assert len(root.children) == 2
    
    def test_tree_to_dict(self):
        test_node = treeNode("Hello, world!")
        test_node.add_child(treeNode("Hello, world, 2!"))
        test_dict = tree_to_dict(test_node)
        assert test_dict['text'] == "Hello, world!"
        assert len(test_dict['children']) == 1

    def test_serialize_tree(self):
        test_node = treeNode("Hello, world!")
        test_node.add_child(treeNode("Hello, world, 2!"))
        test_dict = tree_to_dict(test_node)
        serialized = serialize_tree(test_node)
        assert json.loads(serialized) == test_dict

    def test_attribute_model(self):
        model_string = 'openai-community/gpt2'
        model = GPT2LMHeadModel.from_pretrained(model_string)
        attribution_model = inseq.load_model(model, "saliency")

        attribution = attribute_node("Hello", "Hello, world!", attribution_model)
        res = json.loads(attribution)
        

if __name__ == '__main__':
    unittest.main()