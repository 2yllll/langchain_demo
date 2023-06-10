# Python 库依赖

# 1. AI 相关

| 库名                                              | 作用                                                                                                     |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `OpenAI`                                          | 访问OpenAI的API                                                                                          |
| `Anthropic`                                       | Claude 模型的 API                                                                                        |
| `Langchain`                                       | LLM 应用框架                                                                                             |
| [Guidance](https://github.com/microsoft/guidance) | 比 Prompt 或 CoT，更有效的控制LLM；将生成、提示和逻辑控制交错到单个连续流中，以匹配LLM实际处理文本的方式 |
| `Tiktoken`                                        | OpenAI库，用于计算字符串在LLM中使用的tokens数                                                            |
| `Google_cloud_aiplatform`                         | 为Google Cloud AI Platform提供了Python客户端                                                             |

# 2. Web开发框架 & 实用库

| 库名               | 作用                                                      |
| ------------------ | --------------------------------------------------------- |
| `FastAPI`          | 通过依赖注入 和 async-await 的 Web 开发框架                                    |
| `Supabase`         | 开源 的`Firebase`替代品，可快速构建Web应用                |
| `Uvicorn`          | 基于`uvloop`和`httptools`的`ASGI`服务器，提供异步网络服务 |
| `Streamlit`        | 用于创建数据应用，进行数据可视化 和 模型部署              |
| `Python-multipart` | 解析multipart/form-data，常用于文件上传。                 |
|[Unstructured](https://github.com/Unstructured-IO/unstructured)|
用于预处理文本文档的开源组件 例如 PDF、HTML 和 Word 文档。这些组件被包装成砖块unstructured 🧱，提供 用户构建针对他们关心的文档的管道所需的构建块 |
| `StrEnum`          | 提供字符串枚举类                                          |

# 3. 文档处理

| 库名          | 作用                                                   |
| ------------- | ------------------------------------------------------ |
| `Markdown`    | 解析 Markdown 语法，转成 html                          |
| `PyMuPDF`     | PDF 解析库                                             |
| `PyPDF`       | PDF 解析库：读取、拆分、合并、加密和解密               |
| `Pdf2Imagev`  | pdf --> 图像                                           |
| `PyPandoc`    | 调用Pandoc，将文件从一种标记格式转换到另一种格式的工具 |
| `Docx2txt`    | .docx 提取内容                                         |
| `Python-jose` | 处理 `JOSE` Javascript Object Signing and Encryption   |

