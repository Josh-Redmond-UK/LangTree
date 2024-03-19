import fastapi

app = fastapi.FastAPI()

@app.get("/api/tree")
def get_tree():
    return {"tree": "🌲"}