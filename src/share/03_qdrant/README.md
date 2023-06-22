# [Qdrant](https://qdrant.tech/documentation/quick-start/) 向量数据库 

Qdrant 是`Rust`语言实现的`向量数据库`。有很多存储方式：

已经集成到：

+ `LangChain`
+ Microsoft `Semantic Kernel`
+ ChatGPT retrieval Plugin

## 导航

+ [01. 入门](01_qdrant.ipynb)
+ [02. 概念](02_qdrant_concept.md)
+ [03. 客户端](03_qdrant_client.py)

## 客户端

可以存储在：

+ 内存：关掉程序会丢失
+ 本地磁盘：Sqlite实现
+ 服务器：通过`Docker` 或 Rust-源码构建 部署
+ 官方云端 Qdrant Clound, 通过 API-KEY 访问

支持的 API 类型：

+ [Rest](https://qdrant.github.io/qdrant/redoc/index.html) 端口 6333, 支持 OpenAI 3.0 API
+ [gRPC](https://github.com/qdrant/qdrant/blob/master/docs/grpc/docs.md#qdrant-CreateAlias) 端口 6334，二进制，性能高，数据小

## 数据库特性

+ `Filter` and `Payload`
    - 根据 json-payload 进行过滤；
    - 提供 灵活的组合：should, must, and must_not
+ 不同数据类型 对应 不同的过滤条件
    - 字符串 匹配
    - 数值范围
    - 地理位置 
+ `Query Planning` and `Payload Index`
    - 根据 查询目标，优化 索引
+ `SIMD` 加速
+ Write-Ahead 日志
+ 分布式部署：集群，Raft协议
+ Stand-alone 单机运行
     - 不依赖 服务器，比如 内存存储，本地文件存储（基于 Sqlite）
