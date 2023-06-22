- [Qrant 概念](#qrant-概念)
  - [1. 集合 `Collection`](#1-集合-collection)
  - [2. 向量 `Vector`](#2-向量-vector)
  - [3. 负载 `Payload` \& 索引 `Index`](#3-负载-payload--索引-index)
  - [4. 快照 `Snapshot`](#4-快照-snapshot)
  - [5. 搜索 `Search` \& 推荐 `Recommend`](#5-搜索-search--推荐-recommend)
  - [6. 杂项](#6-杂项)
  - [7. API](#7-api)

# [Qrant 概念](https://qdrant.tech/documentation/concepts/collections/)

| 概念                   | 意思                      | 说明 |
| ---------------------- | ------------------------- | ---- |
| `Collection` & `Alias` | `Point`的集合             |      |
| `Payload`              | 负载                      |      |
| `Point`                | 点: 带`Payload`的`Vector` |      |
| `Search`               | 搜索                      |      |
| `Filter`               | 过滤                      |      |
| `Optimizer`            | 优化                      |      |
| `Storage`              | 存储                      |      |
| `Index`                | 索引                      |      |
| `Snapshot`             | 快照                      |      |

## 1. 集合 `Collection`

`Collection` 是 一组 `Point` 的集合

同一个`Collection`的`Vector`，维度必须相同，比较距离算法相同

比较距离：

+ 欧式距离
+ 余弦相似度：此时，上传向量时，会做归一化
+ 点积

| 函数名                    | 描述                       | 主要参数         |
| ------------------------- | -------------------------- | ---------------- |
| create_collection         | 创建 新的集合              | Name，向量配置   |
| recreate_collection       | 删除并创建 指定集合        | Name，向量配置   |
| delete_collection         | 删除 指定集合              | Name             |
| update_collection         | 更新 指定集合 参数         | Name，更新配置   |
| get_collection            | 获取 指定集合 的 详细信息  | Name             |
| update_collection_aliases | 创建 集合别名              | 别名 --> Name    |
| get_collection_aliases    | 获取 集合别名              | 无               |
| upload_collection         | 上传 向量/负载 到 指定集合 | Name，向量，负载 |
| get_aliases               | 获取 所有别名              | 无               |
| get_collections           | 获取 所有集合              | 无               |

创建 集合 的 参数：

|                     |                                                                                                       |                              |
| ------------------- | ----------------------------------------------------------------------------------------------------- | ---------------------------- |
| hnsw_config         | `Index` 相关                                                                                          |                              |
| wal_config          | `Storage` 相关                                                                                        | Write-Ahead-Log （预写日志） |
| optimizers_config   | `Optimizer` 相关                                                                                      |                              |
| quantization_config | [量化](https://qdrant.tech/documentation/guides/quantization/#setting-up-quantization-in-qdrant) 相关 |                              |
| shard_number        | [分布式部署](https://qdrant.tech/documentation/guides/distributed_deployment) 相关                    |                              |
| on_disk_payload     |                                                                                                       |

更新集合：例子 上传Payload时，禁用 索引生成；结束后，打开索引生成

``` python
# 为 为存储的矢量 超过 10000 kB 的 Segments 建立索引。
optimizer_config=models.OptimizersConfigDiff(
    indexing_threshold=10000
)
```

Collection Aliases 功能就是用来在旧的和新的向量集之间无缝切换的，切换是原子操作；

Collection Aliases的功能确实类似于3D渲染时的buffer switching（双缓冲）机制或者叫做页面切换（Page Flipping）。

## 2. 向量 `Vector`

| 函数名         | 描述                     | 主要参数               |
| -------------- | ------------------------ | ---------------------- |
| update_vectors | 更新 指定向量            | Name，向量ID，向量数据 |
| delete_vectors | 删除 指定向量            | Name，向量ID           |
| count          | 获取 指定集合中的 向量数 | Name                   |
| upsert         | 插入/更新 向量           | Name，向量ID，向量数据 |
| retrieve       | 获取 指定向量            | Name，向量ID           |
| delete         | 删除 指定向量            | Name，向量ID           |
| upload_records | 上传记录                 | Name，向量，负载       |

## 3. 负载 `Payload` & 索引 `Index`

+ `Payload` 指 向量对应的原始内容；
+ `Index` 用于优化查询性能；

| 函数名               | 描述                      | 主要参数               |
| -------------------- | ------------------------- | ---------------------- |
| set_payload          | 设置 指定向量 的 负载     | Name，向量ID，负载     |
| overwrite_payload    | 覆盖 指定向量 的 负载     | Name，向量ID，负载     |
| delete_payload       | 删除 指定向量 的 负载     | Name，向量ID，字段名   |
| clear_payload        | 清除 指定向量 的 所有负载 | Name，向量ID           |
| create_payload_index | 创建 负载字段 的 索引     | Name，字段名，字段模式 |
| delete_payload_index | 删除 负载字段 的 索引     | Name，字段名           |

## 4. 快照 `Snapshot`

`Snapshot` 数据的一个版本，用于备份和恢复。

| 函数名               | 描述                      | 主要参数               |
| -------------------- | ------------------------- | ---------------------- |
| list_snapshots       | 列出 指定集合 的 所有快照 | Name                   |
| create_snapshot      | 创建 指定集合 的 快照     | Name                   |
| delete_snapshot      | 删除 指定集合 的 快照     | Name，快照名称         |
| list_full_snapshots  | 列出 所有快照             | 无                     |
| create_full_snapshot | 创建 所有快照             | 无                     |
| delete_full_snapshot | 删除 所有快照             | 快照名称               |
| recover_snapshot     | 从 快照 恢复 集合         | Name，快照位置，优先级 |

## 5. 搜索 `Search` & 推荐 `Recommend`

这类函数主要用于 搜索 和 推荐 向量。

+ `Search`: 给定一个向量，到数据库查最相似的；
+ `Recommend`: 给一个向量，和一组候选向量，返回候选中最相似的；

| 函数名           | 描述               | 主要参数                   |
| ---------------- | ------------------ | -------------------------- |
| search           | 指定集合 搜索 向量 | Name，查询向量，参数       |
| search_batch     | 批量 搜索 向量     | Name，查询向量列表，参数   |
| search_groups    | 按组 搜索 向量     | Name，查询向量，组数，参数 |
| recommend        | 推荐 相似向量      | Name，向量ID，参数         |
| recommend_batch  | 批量 推荐 相似向量 | Name，向量ID列表，参数     |
| recommend_groups | 按组 推荐 相似向量 | Name，向量ID，组数，参数   |

## 6. 杂项

| 函数名         | 描述               | 主要参数 |
| -------------- | ------------------ | -------- |
| get_locks      | 获取 当前锁状态    | 无       |
| lock_storage   | 锁定 存储          | 锁定原因 |
| unlock_storage | 解锁 存储          | 无       |
| http           | 执行HTTP操作       | HTTP请求 |
| scroll         | 分页 获取 查询结果 | 分页参数 |

## 7. API

+ [Rest](https://qdrant.github.io/qdrant/redoc/index.html) 端口 6333, 支持 OpenAI 3.0 API
+ [gRPC](https://github.com/qdrant/qdrant/blob/master/docs/grpc/docs.md#qdrant-CreateAlias) 端口 6334，二进制，性能高，数据小

| 函数名                 | 描述              | 主要参数 |
| ---------------------- | ----------------- | -------- |
| rest                   | RestFull 接口     |          |
| grpc_collections       | gRPC 接口，集合   |          |
| grpc_points            | gRPC 接口，向量点 |          |
| async_grpc_points      | gRPC 异步         |          |
| async_grpc_collections | gRPC 异步         |          |

