# [Qdrant](https://qdrant.tech/documentation/quick-start/) 向量数据库 

Qdrant 是`Rust`语言实现的`向量数据库`。有很多存储方式：

+ 内存数据库：纯内存，程序关掉就丢失；
+ 磁盘数据库：用 `Sqlite` 实现，部署方便，适用于小规模数据集；
+ 标准 C/S 存储服务
    - 私有部署 服务器：用 `Docker` 搭建
    - 官方 [Qdrant 云](https://cloud.qdrant.io/)，需要登录，创建 `API_KEY`

## 导航

+ [入门](./01_qdrant.ipynb)