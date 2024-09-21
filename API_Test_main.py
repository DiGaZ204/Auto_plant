from fastapi import FastAPI
from router import blog_get, blog_post

app = FastAPI()

# 包含 GET 路由
app.include_router(blog_get.router)

# 包含 POST 路由
app.include_router(blog_post.router)

@app.get("/")
def index():
    return {"Hello": "FastAPI"}

"""
測試：http://192.168.50.16:8000/docs
運行：uvicorn main:app --host 192.168.50.16 --port 8000 --reload
樹莓派 IP：16->23
(ngrok 運行)：uvicorn API_Test_main:app --host 127.0.0.1 --port 8000 --reload
"""