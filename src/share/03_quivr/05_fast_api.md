# `FastAPI`

通过依赖注入 和 async-await 的 高性能 Python Web 框架

FastAPI 基于 Starlette（异步 web 框架）进行构建，性能好则归功于 `Starlette`（用于 web 部分）和 `Pydantic`（用于数据部分）。

+ 初始化: app = FastAPI()
+ 依赖注入 定义路由 @app.get("/user", dependencies=[Depends(JWTBearer())])
    - 依赖 负责处理 `JWT` (JSON Web Token) 认证
+ 定义路由处理函数
+ 在处理函数中 处理Web请求
+ 返回响应: 返回dict，会被FastAPI转换为 JSON 格式，并将其作为 HTTP 响应返回

|主要类|作用|
|--|--|
|`Request`|代表 HTTP 请求。这个对象包含了请求的所有信息，如方法（GET, POST等）、头部、路径参数等。|
|`Response`|代表 HTTP 响应。这个对象包含了响应的所有信息，如状态码、头部、Cookies、内容等。|
|`File`|在路由中指定文件参数。|
|`UploadFile`|用于处理上传的文件。这个对象提供了一些方法和属性来获取和处理文件的数据。|
|`Depends`|在路由中指定 依赖项|
|`Form`|在路由中指定 表单参数。|
|`Body`|在路由中指定 请求体参数。|
|`Query`|在路由中指定 查询参数。|
|`Path`|在路由中指定 路径参数。|
|`Cookie`|在路由中指定 cookie 参数。|
|`Header`|在路由中指定 头部参数。|
|`BaseModel`|`Pydantic` 的基础模型类。你可以从这个类继承来创建自定义的数据模型。|

``` python
@app.on_event("startup")

@app.get("/")

# 文件一次 upload
@app.post("/upload", dependencies=[Depends(JWTBearer())])

@app.post("/chat/", dependencies=[Depends(JWTBearer())])

@app.post("/crawl/", dependencies=[Depends(JWTBearer())])

@app.get("/explore", dependencies=[Depends(JWTBearer())])

@app.delete("/explore/{file_name}", dependencies=[Depends(JWTBearer())])

@app.get("/explore/{file_name}", dependencies=[Depends(JWTBearer())])

@app.get("/user", dependencies=[Depends(JWTBearer())])
```

## 依赖

fastapi 有个 `Depends` 类，实际是个注册

在 utils/vectors.py 中，往框架注入 某个依赖：

def common_dependencies():
    return {
        "supabase": supabase_client,
        "embeddings": embeddings,
        "documents_vector_store": documents_vector_store,
        "summaries_vector_store": summaries_vector_store
    }

CommonsDep = Annotated[dict, Depends(common_dependencies)]

使用：

``` python
@app.post("/chat/", dependencies=[Depends(JWTBearer())])
async def chat_endpoint(commons: CommonsDep, chat_message: ChatMessage, credentials: dict = Depends(JWTBearer()))
    pass
```

## 例子 /chat

### 参数 credentials JWT 信息

可以看作是服务器 session 的一种凭证信息。

从 JWT (JSON Web Tokens) 中解码出来的载荷（payload）部分。

这个 JWT 是在客户端登录或者认证后，服务器发给客户端的，客户端在之后的请求中会将这个 JWT 发送回服务器，服务器解码 JWT，验证其有效性，并获取其中的信息。

``` python
{
    'aud': 'authenticated',  # （Audience）：接收 JWT 的一方，通常是你的服务器的标识符。
    'exp': DDDDDDDDDD,       #  JWT 的过期时间，一般是 Unix 时间戳。
    'sub': 'XXXX-YYYY-ZZZZ-WWWW-TTTT',  # JWT 的主题，通常是标识用户的唯一标识符。
    'email': 邮箱地址,        # 用户的电子邮件地址
    'phone': '',             
    'app_metadata': {
        'provider': 'email', 
        'providers': ['email']
    }, 
    'user_metadata': {}, 
    'role': 'authenticated',   # 用户的角色，例如这里的 "authenticated" 表示这是已经认证的用户。
    'aal': 'aal1',    # （Authentication Assurance Level）：表示认证的等级，用来表明用户验证其身份的可靠程度。
    'amr': [{         # （Authentication Methods References）：这个字段记录了用户进行认证的具体方法和时间戳。
        'method': 'password', 
        'timestamp': 过期时间戳
    }], 
    'session_id': 'XXXXXXX'
}
```

### 参数 commons: CommonsDep

一开始，就在 utils/vector.py 中，初始化 全局变量 `commons`

``` python
{
    "supabase": supabase 客户端 对象
    "embeddings": OpenAI Embedding 对象
    "documents_vector_store": documents_vector_store,
    "summaries_vector_store": summaries_vector_store
}
```

使用时候的参数打印：

``` python 

{
    'supabase': <supabase.client.Client object at 0x7ffb0dc5d790>, 
    'embeddings': OpenAIEmbeddings(
        client=<class 'openai.api_resources.embedding.Embedding'>, 
        model='text-embedding-ada-002', 
        deployment='text-embedding-ada-002', 
        openai_api_version=None, 
        openai_api_base=None, 
        openai_api_type=None, 
        openai_proxy=None, 
        embedding_ctx_length=8191, 
        openai_api_key='XXXXXXXXXXXX', 
        openai_organization=None, 
        allowed_special=set(), 
        disallowed_special='all', 
        chunk_size=1000, 
        max_retries=6, 
        request_timeout=None, 
        headers=None
    ), 
    'documents_vector_store': <langchain.vectorstores.supabase.SupabaseVectorStore object at 0x7ffb0d8c3290>, 
    'summaries_vector_store': <langchain.vectorstores.supabase.SupabaseVectorStore object at 0x7ffb0d8cc250>}
```

### 参数 chat_message: ChatMessage(Pydantic::BaseModel)

简单来说，继承自 BaseModel 的类，就是 post的 body 字段反序列化的内容；

history = [从旧到新的对话记录]

``` python
{
    "temperature"=0.0,
    "max_tokens"=500,
    "use_summarization"=False,
    "model"='gpt-3.5-turbo',
    "question"='hello',
    "history"=[
        ('user', '你好'), 
        ('assistant', '你好！有什么我可以帮助你解决的问题吗？'), 
        ('user', '请问 quivr 的安装步骤是什么？'), 
        ('assistant', '以下是 Quivr 的安装步骤：\n\n1. 启动 WSL-2 Ubuntu 22.04，并安装并启动 Docker Desktop。\n2. 在命令行中输入 `python3.11`，如果有反应则说明已经安装了 Python 3.11，否则需要执行以下命令安装 Python 3.11：\n\n```\nsudo apt update\nsudo apt upgrade\nsudo add-apt-repository ppa:deadsnakes/ppa -y\nsudo apt update\nsudo apt install python3.11\npython3.11 --version\n```\n\n3. 申请 Supabase 账号，并获取 API 密钥和项目 URL。\n4. 克隆 Quivr 的 Github 仓库：`git clone https://github.com/StanGirard/quivr.git`。\n5. 进入 Quivr 目录：`cd quivr`。\n6. 复制 `.XXX_env` 文件：`cp .backend_env.example backend/.env` 和 `cp .frontend_env.example frontend/.env`。\n7. 更新 `backend/.env` 文件中的以下内容：\n\n```\nSUPABASE_URL=Supabase项目URL\nSUPABASE_SERVICE_KEY=Supabase项目API密钥\nOPENAI_API_KEY="sk-XXXXXX"\n```\n\n8. 更新 `frontend/.env` 文件中的以下内容：\n\n```\nNEXT_PUBLIC_SUPABASE_URL=Supabase项目URL\nNEXT_PUBLIC_SUPABASE_ANON_KEY=Supabase项目API密钥\n```\n\n9. 到 Supabase 的 SqlEditor 输入以下 4 个 SQL 代码，创建 4 张表：\n\n- https://github.com/StanGirard/quivr/blob/main/scripts/supabase_new_store_documents.sql\n- https://github.com/StanGirard/quivr/blob/main/scripts/supabase_usage_table.sql\n- https://github.com/StanGirard/quivr/blob/main/scripts/supabase_vector_store_summary.sql\n- https://github.com/StanGirard/quivr/blob/main/scripts/supabase_users_table.sql\n\n10. 安装并启动 Docker 服务器，每次修改完 `.env` 文件的内容都需要重新构建：\n\n```\ndocker compose'), 
        ('user', '目前 有哪些 unity 代码？'), 
        ('assistant', "I'm sorry, I cannot answer this question as there is no context provided to determine which Unity code you are referring to. Can you please provide more information or context?")
    ],
}
```