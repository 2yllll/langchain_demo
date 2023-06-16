# [QrantClient 客户端](https://github.com/qdrant/qdrant-client)

官方 客户端 实现：

+ [Python](https://github.com/qdrant/qdrant-client)
+ `Rust`
+ `Go`
+ `JS/TS`

## 概念

1. **集合 Collection**

这类函数主要用于创建、查询、更新、删除和管理集合。

集合代表了一个向量数据的集合，类似 关系数据库 的 数据表，可以为每个集合定义特定的参数。

每个集合内部的向量的大小和距离函数都是统一的，不同集合则可以不同。

| 函数名                    | 描述                       | 主要参数         |
| ------------------------- | -------------------------- | ---------------- |
| get_collections           | 获取 所有集合              | 无               |
| get_collection            | 获取 指定集合              | Name             |
| update_collection         | 更新 指定集合              | Name，更新配置   |
| delete_collection         | 删除 指定集合              | Name             |
| create_collection         | 创建 新的集合              | Name，向量配置   |
| recreate_collection       | 删除并创建 指定集合        | Name，向量配置   |
| update_collection_aliases | 更新 集合别名              | 别名 --> Name    |
| get_collection_aliases    | 获取 集合别名              | 无               |
| upload_collection         | 上传 向量/负载 到 指定集合 | Name，向量，负载 |

2. **向量 Vector**

| 函数名         | 描述                     | 主要参数               |
| -------------- | ------------------------ | ---------------------- |
| update_vectors | 更新 指定向量            | Name，向量ID，向量数据 |
| delete_vectors | 删除 指定向量            | Name，向量ID           |
| count          | 获取 指定集合中的 向量数 | Name                   |
| upsert         | 插入/更新 向量           | Name，向量ID，向量数据 |
| retrieve       | 获取 指定向量            | Name，向量ID           |
| delete         | 删除 指定向量            | Name，向量ID           |
| upload_records | 上传记录                 | Name，向量，负载       |

3. **负载 Payload & 索引 Index**

| 函数名               | 描述                      | 主要参数               |
| -------------------- | ------------------------- | ---------------------- |
| set_payload          | 设置 指定向量 的 负载     | Name，向量ID，负载     |
| overwrite_payload    | 覆盖 指定向量 的 负载     | Name，向量ID，负载     |
| delete_payload       | 删除 指定向量 的 负载     | Name，向量ID，字段名   |
| clear_payload        | 清除 指定向量 的 所有负载 | Name，向量ID           |
| create_payload_index | 创建 负载字段 的 索引     | Name，字段名，字段模式 |
| delete_payload_index | 删除 负载字段 的 索引     | Name，字段名           |

4. **快照 Snapshot**

这类函数主要用于创建、删除和恢复快照。

快照是数据的一个版本，用于备份和恢复。

| 函数名               | 描述                      | 主要参数               |
| -------------------- | ------------------------- | ---------------------- |
| list_snapshots       | 列出 指定集合 的 所有快照 | Name                   |
| create_snapshot      | 创建 指定集合 的 快照     | Name                   |
| delete_snapshot      | 删除 指定集合 的 快照     | Name，快照名称         |
| list_full_snapshots  | 列出 所有快照             | 无                     |
| create_full_snapshot | 创建 所有快照             | 无                     |
| delete_full_snapshot | 删除 所有快照             | 快照名称               |
| recover_snapshot     | 从 快照 恢复 集合         | Name，快照位置，优先级 |

5. **搜索 Search & 推荐 Recommend**

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

6. **杂项**

这类函数主要包括各种杂项操作，如获取别名，上传记录，获取锁状态，锁定和解锁存储等。

| 函数名         | 描述               | 主要参数 |
| -------------- | ------------------ | -------- |
| http           | 执行HTTP操作       | HTTP请求 |
| scroll         | 分页 获取 查询结果 | 分页参数 |
| get_aliases    | 获取 别名          | 无       |
| get_locks      | 获取 当前锁状态    | 无       |
| lock_storage   | 锁定 存储          | 锁定原因 |
| unlock_storage | 解锁 存储          | 无       |

7. 不用管 **API**

| 函数名                 | 描述              | 主要参数 |
| ---------------------- | ----------------- | -------- |
| rest                   | RestFull 接口     |          |
| grpc_collections       | gRPC 接口，集合   |          |
| grpc_points            | gRPC 接口，向量点 |          |
| async_grpc_points      | gRPC 异步         |          |
| async_grpc_collections | gRPC 异步         |          |

