# [Quivr：部署到本地](https://github.com/StanGirard/quivr)

[Github 备份地址](https://github.com/moyy/langchain_demo/blob/main/src/share/03_quivr/02_local.md)

# 00. Quivr 简介

[Quivr](https://github.com/StanGirard/quivr) 简单来说：利用 Supabase 做向量数据库，加上 Langchain / LLM 来做一个 基于各种文档 为主题的 聊天工具 / 知识库

功能：

+ 围绕某个主题 upload 各种文档
+ 围绕某个主题 的 对话
+ 支持 私有 LLM，目前主要是 [GPT4All](https://gpt4all.io/index.html)

框架：

+ 前端 node / next.js
+ 后端：python / supabase + Langchain

支持的 文件 格式：
   
+ txt
+ Markdown
+ PDF
+ Powerpoint
+ Excel
+ Word
+ Audio / Video 里面的音频流 变 文档

# 01. 准备

+ Windows 11
+ git
+ 可用的 OPenAI API Key
+ 安装 / 启动 Docker Desktop

**注：** 开始之前，先到 Docker 删除 `quivr` 的 Container（镜像 可以 保留）

# 02. Docker 部署 Supabase

见 [这篇文章](../07_supabase/01_local_deploy.md)

# 03. **如果你不想踩坑，一定要** 确定版本

``` bash
# Get the code
git clone https://github.com/StanGirard/quivr.git

# Go to
cd quivr

# 这里对应的是 0.0.28 tag 的 下一个提交版本
# 为什么一定是这个，因为 我试过 0.0.15-0.0.20 全部因为作者的bug而构建失败。
# 所以第一次为了保险，最好和我的版本一致！
git checkout 3e68000983dc69200cbc0b15ed0126e5dd16633d

copy .backend_env.example backend/.env
copy .frontend_env.example frontend/.env

```

# 04. 替换 backend/.env 的参数

+ SUPABASE_URL=http://localhost:8000 # 一定是 8000，那个是 supabase 的 kong 网关对应的端口，不是3000，也不是3001
+ SUPABASE_SERVICE_KEY=这里替换成上面 `SERVICE_ROLE_KEY` 对应的 值 
+ OPENAI_API_KEY=GPT-API-密钥
+ JWT_SECRET_KEY=这里替换成上面 `JWT_SECRET` 对应的 值

# 05. 替换 frontend/.env 的参数

+ NEXT_PUBLIC_BACKEND_URL=http://localhost:5050
+ NEXT_PUBLIC_SUPABASE_URL=http://localhost:8000
+ NEXT_PUBLIC_SUPABASE_ANON_KEY=这里替换成上面 `ANON_KEY` 对应的 值

# 06. 到 本地 supabase 新建 数据库

+ 浏览器打开 Supabase 管理端 http://localhost:3001 点击 项目（**注：** 本地部署的supabase不能新建项目，只有一个默认项目）
+ 跟官网一样，到 sql editor，将 本地 quivr 目录 的 scripts/tables.sql 的sql代码拷贝过去执行；
  - **注1：** sql 不能到 github 拷贝，因为每个代码版本的sql可能不一样，如果你不想浪费时间，就一个版本对应一个数据库！
  - **注2：** 因为 quivr 自己都不稳定，所以升级代码后，发现更新sql后崩溃，请忍痛删掉已有数据，或者 找个数据库高手，请教下怎么才能兼容性升级！

# 07. **Windows 需要：** Linux 请忽略

docker-compose.yml 文件，有个 ~/，第二次之后，因为windows的目录权限严格到郁闷，会直接失败。

所以要将 ~/ 改成 ./


``` yml
# 找到这行修改如下 - ~/.config/gcloud:/root/.config/gcloud

  - ./.config/gcloud:/root/.config/gcloud

```

# 08. **国内：** 快速安装 pip

**注：** 不加这个，是2小时；加了这个，是 10-15分钟；

backend/Dockerfile 的 pip install 加上 国内镜像

``` Dockerfile

# 找到这里，替换成下面的 RUN pip install --no-cache-dir -r /code/requirements.txt --timeout 100

RUN pip install --no-cache-dir -r /code/requirements.txt --timeout 100 -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

```

frontend/Dockerfile 的 pip install 加上 国内镜像

``` Dockerfile

# 找到这里，替换成下面的 RUN pip3 install --no-cache --upgrade pip setuptools

RUN pip3 install --no-cache --upgrade pip setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn

```

# 09. 构建

**国内：** 运行前，因为你前面加了国内镜像，要关闭 clash 这些代理工具（至少要关闭全局功能），否则你会发现要等几小时。

``` bash

docker compose -f docker-compose.yml up --build

```

**国内：** 15分钟后，你会发现安装成功，启动崩溃！所以还有最后一步！

# 10. **国内：** 访问 宿主代理

等上面安装成功，初始化崩溃之后，就可以 打开 clash 这些代理工具了；

假设你买的是本地代理服务，比如 你本地 可以通过 localhost:7890 代理 http / https

那么，如果想在 Docker 程序 也是用代理，需要改 docker-compose.yml 文件

找到 container_name: backend，在其下一行加入三句，其中 host.docker.internal 对应Docker的宿主主机（也就是你本地电脑）

``` yml

container_name: backend
environment:
  http_proxy: http://host.docker.internal:7890
  https_proxy: http://host.docker.internal:7890
```

命令行再次运行：

``` bash

docker compose -f docker-compose.yml up --build

```

成功后，浏览器访问 http://localhost:3000 