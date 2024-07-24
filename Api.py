from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def funcion():
return "message" "Hello World"