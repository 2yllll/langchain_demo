import uuid
import numpy as np

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import Distance, VectorParams, PointStruct

# 创建 Qdrant 客户端 对象
# 优先 使用 gRPC
client = QdrantClient(host="localhost", port=6333, grpc_port=6334, prefer_grpc=True)

# 集合名
collection_name = "my_collection"

# 向量大小 和 查询用的距离函数
vector_size = 100
distance = Distance.COSINE

# 重新创建集合（有则删除，然后创建）
client.recreate_collection(collection_name, vectors_config=VectorParams(size=vector_size, distance=distance))

# 插入数据，这里随机模拟 600个长度为vector_size的向量，当成 payload 的 嵌入向量
vectors = np.random.rand(600, vector_size)

client.upsert(
    collection_name=collection_name,
    points=[
        PointStruct(
            id=idx,
            vector=vector.tolist(),
            payload={
                "city": "London", 
                "rand_number": idx % 10
            }
        )
        for idx, vector in enumerate(vectors)
    ]
)

# 模拟 查询的 嵌入向量
query_vector = np.random.rand(vector_size)

# 每个 Segment 独立 执行
# 如果 Segment Point 数量 低于阈值，则 首选 完整扫描
# 在选择策略之前 估计 过滤结果 的 基数
# 如果 基数 低于 阈值，则使用 有效负载索引 检索 Point
# 如果 基数 高于 阈值，则使用 可过滤 向量索引
r = client.search(
    collection_name=collection_name,
    query_filter=models.Filter( # 过滤，仅在满足过滤条件的Point中进行搜索
        must=[
            models.FieldCondition(
                key="city",
                match=models.MatchValue(
                    value="London",
                ),
            )
        ]
    ),
    search_params=models.SearchParams(
        hnsw_ef=128, # 指定efHNSW 算法参数的值。
        exact=False  # 不使用近似搜索（ANN）的选项。如果设置为 true，则搜索可能会运行很长时间，因为它会执行完整扫描以检索准确的结果。
    ),
    query_vector=query_vector,
    limit=3, # 最相似 的 数量
     with_vectors=False,
    with_payload=False,
)

# r = list(ScoredPoint)
# ScoredPoint {id=440, version=0, score=0.8316, payload, vector,}
print(r)