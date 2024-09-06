from fastapi import FastAPI
from router import blog_get
from router import blog_post

app = FastAPI()

# blog_get
app.include_router(blog_get.router)

# blog_post
app.include_router(blog_post.router)

@app.get("/")
def index():
    return {"Hello": "FastAPI"}

# Test:http://192.168.50.16:8000/docs
# run:uvicorn API_Test_main:app --host 192.168.50.16 --port 8000 --reload
# get:http://192.168.50.16:8000/blog/soil-moisture/1
# pi_ip:16->23
#(ngrok:run):uvicorn API_Test_main:app --host 127.0.0.1 --port 8080 --reload