# `Quiver` 中的 [Supabase](https://supabase.com)

开源 的`Firebase`替代品，可快速构建Web应用

+ 好处：方便，不用运维？
+ 坏处：隐私 & 安全

具体作用：

+ 用户权限管理
+ 第三方授权管理：邮箱验证，手机验证，Github验证
+ 内置 数据库

# 1. summaries 索引向量

文档内容 摘要 对应的向量

| 字段名      | 类型   | 说明 | 其他                                                         |
| ----------- | ------ | ---- | ------------------------------------------------------------ |
| id          | bigint |      |                                                              |
| document_id | bigint |      | document id                                                  |
| content     | text   |      | document 内容对应的 摘要内容                                 |
| metadata    | jsonb  |      | 由 quivr 自定义 其 字段，见 例子                             |
| embedding   | vector |      | 来自 OpenAI 的，基本是 1536个 [-1.0, 1.0] 浮点数 组成的 数组 |

# 2. vectors 内容向量

| 字段名    | 类型   | 说明 | 其他                                                         |
| --------- | ------ | ---- | ------------------------------------------------------------ |
| id        | bigint |      |                                                              |
| user_id   | text   |      | 邮箱地址 等 唯一标志                                         |
| content   | text   |      |                                                              |
| metadata  | jsonb  |      | 由 quivr 自定义 其 字段，见 例子                             |
| embedding | vector |      | 来自 OpenAI 的，基本是 1536个 [-1.0, 1.0] 浮点数 组成的 数组 |

例子：

``` json
{
    "embedding": "来自 OpenAI 的，基本是 1536个 [-1.0, 1.0] 浮点数 组成的 数组",
    "metadata": {
        "date": "20230608",
        "file_name": "Quivr.md",
        "file_sha1": "495044d3245919188af824368864e1ec60d52c29",
        "file_size": 2638,
        "chunk_size": 500,
        "chunk_overlap": 0,
        "summarization": "false"
    }
}
```

# 3. users 用户信息

| 字段名         | 类型    | 说明                 | 其他 |
| -------------- | ------- | -------------------- | ---- |
| date           | text    |                      |      |
| user_id        | text    | 邮箱地址 等 唯一标志 |      |
| requests_count | integer |                      |      |

# 4. stats 状态？

| 字段名    | 类型      | 说明 | 其他 |
| --------- | --------- | ---- | ---- |
| time      | timestamp |      |      |
| chat      | boolean   |      |      |
| embedding | boolean   |      |      |
| details   | text      |      |      |
| metadata  | jsonb     |      |      |
| id        | integer   |      |      |

