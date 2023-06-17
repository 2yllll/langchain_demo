# [Quivr](https://github.com/StanGirard/quivr)

## 1. 准备

+ Windows 11 + Docker Desktop
+ 安装并启动 Docker Desktop
+ 命令行输入 python3.11 有反应
    - windows 端，安装完 python 3.11 版本后，记得加环境变量，同时复制一份exe，改名为 python3.exe 和 python3.11.exe
+ [申请 Supabase 账号](https://supabase.com/dashboard/projects)

## 2. 开始

+ git clone https://github.com/StanGirard/quivr.git
+ git checkout v0.0.15
    - 将git版本回滚到 v0.0.15 的 tag 版本；
    - **注**：别的版本可能有新问题和不同之处，请参考官网的README
+ cd quivr
+ 复制文件 .XXX_env 文件
    - cp .backend_env.example backend/.env
    - cp .frontend_env.example frontend/.env
+ 更新 backend/.env 
    - SUPABASE_URL=Supabase项目URL
    - SUPABASE_SERVICE_KEY=Supabase项目API 密钥
    - OPENAI_API_KEY="sk-XXXXXX"
    - JWT_SECRET_KEY="pwXXXXX"
+ 更新 front/.env
    - NEXT_PUBLIC_SUPABASE_URL=Supabase项目URL
    - NEXT_PUBLIC_SUPABASE_ANON_KEY=Supabase项目API 密钥

![](../../../images/20230617121944.png)

## 3. 到 [Supabase](https://supabase.com/dashboard/projects) 的 SqlEditor，拷贝 [这里](https://github.com/StanGirard/quivr/blob/main/scripts/tables.sql) 的sql代码，创建sql表格

顺利的话，15分钟内重头构建成功；

注：如果原来的版本已经有数据表，最好先全部删除，再运行sql脚本

![](../../../images/20230617120444.png)

![](../../../images/20230617120233.png)

## 4. docker 安装 / 启动 服务器

注1：每次修改完 .env的内容，都要重新 --build

注2：**国内**，阿里云镜像，在 backend/Dockerfile

``` bash
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt --timeout 100  -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

注3：**国内**，遇到 SSL 错误，记得 代理

Docker 的环境变量是隔离的，不会使用 Ubuntu 的 环境变量；所以 http_proxy 得 单独设置

docker-compose.yml 为 backend 添加 environment 配置；

修改如下：

``` yml
backend:
    env_file:
      - ./backend/.env
    build:
      context: backend
      dockerfile: Dockerfile
    environment:
      http_proxy: http://192.168.XX.YY:ZZZZ
      https_proxy: http://192.168.XX.YY:ZZZZ
      no_proxy: localhost,127.0.0.1,.example.com
```

运行：

``` bash
docker compose -f docker-compose.yml up --build
```

## 5. 访问页面 

https://localhost:3000

## 6. 每次 启动运行

``` bash
docker compose -f docker-compose.yml up
```