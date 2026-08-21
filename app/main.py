from fastapi import FastAPI

app = FastAPI(title="Supervity P7")


@app.get("/")
def root():
    return {"message": "Supervity P7 is running"}