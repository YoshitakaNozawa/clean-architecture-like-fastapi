from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from config.openapi_conf import swagger_title, tags_metadata
from drivers.router import user_router
from drivers.router import hoge_router

app = FastAPI(title=swagger_title, openapi_tags=tags_metadata)
handler = Mangum(app)

# CORSを回避するために設定
origins = ["*"]
headers = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=headers,
)

""" routerを起動する """
app.include_router(user_router.router, tags=["ユーザー系"])
app.include_router(hoge_router.router, tags=["〇〇系"])
