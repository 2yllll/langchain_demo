# GPT & Langchain 例子

## 1. [准备工作](./src/share/00_setup.md)

+ 要 代理，搭梯子
+ 要 OpenAI 账号
+ 要 信用卡绑定 API（注：此处不需要 Plus账号，信用卡是为了根据token扣api费用的）
+ 申请一个 API Key：
    - 将 OpenAI 的 API-KEY 填到 环境变量 `OPENAI_API_KEY` 里

## 2. 运行环境

+ 安装: 3.7版本及其以上的 `python` 
+ 编辑器：`vscode`
    - 含扩展：`python`插件，`jupyter` 笔记本插件

## 3. 导航: 从`GPT`到`LangChain`

+ [01. GPT 例子](./src/share/01_chagpt.ipynb)
+ [02. Quivr](./src/share/02_quivr/README.md)
+ [03. 向量数据库：Qdrant with Langchain](./src/share/03_qdrant/README.md)

## 4. 导航: [LangChain](https://python.langchain.com/en/latest/)

+ [2.1. model: 模型](./src/components/01_model.ipynb)
+ [2.2. prompt: 提示](./src/components/02_prompt.ipynb)
+ [2.3. chain: 链](./src/components/03_chain.ipynb)
+ [2.4. memory: 记忆](./src/components/04_memory.ipynb)
+ [2.5. index: 存储 & 索引](./src/components/05_indexes.ipynb)
+ [2.6. agent: 智能体 & 插件](./src/components/06_agent.ipynb)
+ [2.7. callback: 回调](./src/components/07_callback.ipynb)