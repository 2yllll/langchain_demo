# Quivr

+ 运行环境 Docker / Linux
+ frontend/ 先不管
    - 职责: 资源服务器
    - 框架: node / Next.js
    - 端口: 3000
+ backend/
    - 职责: 逻辑服务器，负责 API逻辑功能
    - 框架: python
    - 端口: 5050

下面 全是 backend/ 代码流程分析

# 1. 入口 main.py

用 `FastAPI` 框架 处理 Web 路由，最重要的路由：

+ `/upload`: 上传单个文件
+ `/crawl/`: 抓取url对应的html内容
    - 如果这个url是 github 地址，则会获取所有的源代码内容
+ `/chat`: 聊天

# 2. /upload 上传单个文件

入口: backend/main.py

``` python
message = await filter_file(file, enable_summarization, commons['supabase'], user)
```

方法 filter_file 在 utils/processors.py 实现:

+ 根据文件后缀，调用不同的 处理函数 取文件内容
+ 每种格式一个py文件，在 parsers/ 目录中
+ 大多数格式都是 对 langchain.document_loaders 的再次封装

## 2.1. 视频 / 音频

处理视频，实际上是处理视频里面的音频

处理音频：用 `OpenAI` 的 `whisper` API 提取 音频中的文字

``` python
with open(tmp_file.name, "rb") as audio_file:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

print(transcript.text)
```

## 2.2. 已处理格式（截至 2023.06.10）

|后缀|说明|
|--|--|
|.txt|纯文本文件|
|.csv|以逗号分隔的值（Comma-Separated Values）|
|.md|Markdown文档|
|.markdown|Markdown文档|
|.m4a|音频|
|.mp3|音频|
|.webm|视频（VP8/V9）和 音频（Vorbis/Opus）|
|.mp4|视频（MPEG-4/H.264）和 音频（AAC）|
|.mpga|MPG或MPEG音频|
|.wav|未压缩的PCM音频|
|.mpeg|视频|
|.pdf|pdf文件|
|.html|html文件|
|.pptx|Microsoft PowerPoint演示文稿|
|.docx|Microsoft Word文档|
|.odt|OpenDocument文档（由开源Office套件如LibreOffice，OpenOffice等使用）|
|.epub|电子书文件格式|
|.ipynb|Jupyter 笔记本，常用于Python代码的交互式开发和数据分析|

## 3. /upload & /crawl 的 处理终点

``` python

chunk_size = 500 # 500 字节为一个 块
chunk_overlap = 0 # 块与块重叠字节数为0；也即是 不重叠

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=chunk_size, 
    chunk_overlap=chunk_overlap
)

# 将文件 分成很多 块
texts = text_splitter.split_text(transcript)

docs_with_metadata = []
for text in texts:
    metadata = {
        "file_sha1": file_sha, 
        "file_size": file_size, 
        "file_name": file_meta_name, 
        "chunk_size": chunk_size, 
        "chunk_overlap": chunk_overlap, 
        "date": dateshort
    }
    
    doc = Document(page_content=text, metadata)

    docs_with_metadata.push(doc)

documents_vector_store.add_documents(docs_with_metadata)
```

## 3.1. documents_vector_store 向量存储

utils/vectors.py 封装了存储

|模块公有变量|构造|作用|
|--|--|--|
|embeddings|from langchain.embeddings.openai import OpenAIEmbeddings|生成 嵌入式 向量|
|supabase_client|from supabase import Client|supabase客户端|
|documents_vector_store|from langchain.vectorstores import SupabaseVectorStore|文件内容对应的 向量存储|
|embeddisummaries_vector_storengs|from langchain.vectorstores import SupabaseVectorStore|文件摘要 对应的 向量存储|

# 4. /chat 流程

入口: backend/main.py

API 参数 use_summarization 要不要用 摘要，默认不开启

``` python

# Web浏览器 通过 Post 传递过来
chat_message = {
    "temperature"=0.0,
    "max_tokens"=500,
    "use_summarization"=False,
    "model"='gpt-3.5-turbo',
    "question"='hello',
    "history"=[
        ('user', '你好'), 
        ('assistant', '你好！有什么我可以帮助你解决的问题吗？'),
    ]
}

qa = get_qa_llm(chat_message, user.email)

# 注意：历史信息没有传递过去
model_response = qa({
    "question": chat_message.question
})

history = chat_message.history
history.append(("user", chat_message.question))
history.append(("assistant", model_response["answer"]))

return {
    "history": history
}
```

## 4.1. get_qa_llm

``` python

def get_qa_llm(chat_message: ChatMessage, user_id: str):
    
    # 取 在 utils/vector.py 的 supabase_client, embeddings
    supabase_client, embeddings = ...

    # 取 Supabase 的 vectors 表的 user_id 对应的内容 
    vector_store = CustomSupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors", user_id=user_id)
    
    # 会话 记忆
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    
    ConversationalRetrievalChain.prompts = LANGUAGE_PROMPT
   
    llm = ChatOpenAI(
        model_name=chat_message.model, 
        openai_api_key=openai_api_key, 
        temperature=chat_message.temperature, 
        max_tokens=chat_message.max_tokens
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm, 
        vector_store.as_retriever(), 
        memory=memory, 
        verbose=True, 
        max_tokens_limit=1024
    )    
    
    return qa
```

## 4.2. 提示

在 backend/llm/LANGUAGE_PROMPT.py

用到 langchain 的 提示模板

``` python

from langchain.prompts.prompt import PromptTemplate

# 见 翻译1
_template = """Given the following conversation and a follow up question, answer the follow up question in the initial language of the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

# 见 翻译2
prompt_template = """Use the following pieces of context to answer the question in the language of the question. If you don't know the answer, just say that you don't know, don't try to make up an answer. 

{context}

Question: {question}
Helpful Answer:"""

QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )
```


+ 翻译 1: 给定以下对话和后续问题，用问题的初始语言回答后续问题。如果你不知道答案，就说你不知道，不要试图编造答案。
+ 翻译 2: 使用以下上下文片段以问题的语言回答问题。如果你不知道答案，就说你不知道，不要试图编造答案。
