# LangTree

LangTree is a tool designed to help with research into mechanistic interpretability of large language models. It allows for the conditional generation of strings in a tree format, which displays the top-k paths that the model could have taken at each token's generation. 

LangTree is a single page web app and API, with the front end using D3.js and DaisyUI, and the back end using FastAPI. The back end is essentially a wrapper for the huggingface transformers library which also uses InSeq to attribute token generation. Users can select different parameters in the app's GUI. 

## How To Use

1. Create a conda or venv environment with python 3.10
2. Install all the dependencies as listed in api/requirements.txt
3. In terminal, navigate to the api folder and run 'uvicorn main:app --reload'
4. Open app/index.html in your browser of choice (ideally run it from a local webserver)