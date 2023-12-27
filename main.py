from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
app = FastAPI(title="SecondDictionary")

@app.get('/')
def get_root_page():
        return {"status": 200, "msg": "ok"}
