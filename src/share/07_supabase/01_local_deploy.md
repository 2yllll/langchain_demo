- [通过`Docker`本地部署`Supabase`](#通过docker本地部署supabase)
  - [1. 准备](#1-准备)
  - [2. 开始](#2-开始)
  - [3. 更新 密钥](#3-更新-密钥)
  - [4. 关于 邮箱 SMTP\_ 服务](#4-关于-邮箱-smtp_-服务)
  - [5. 再次配置密码：`可能不需要，没试过`](#5-再次配置密码可能不需要没试过)
  - [6. 启动](#6-启动)
  - [7. `注意事项`：修改配置后如何生效](#7-注意事项修改配置后如何生效)

# [通过`Docker`本地部署`Supabase`](https://supabase.com/docs/guides/self-hosting/docker)

[Github 备份地址]()

## 1. 准备

+ Windows 11
+ git
+ 安装 / 启动 Docker Desktop

## 2. 开始

到你想要的目录，进入 cmd 控制台：

``` bash
# Get the code
git clone https://github.com/supabase/supabase

# Go to the docker folder
cd supabase/docker

# Copy the fake env vars
copy .env.example .env

```

## 3. 更新 密钥

用 [这里](https://supabase.com/docs/guides/self-hosting/docker#generate-api-keys) 更新 .env:

+ `STUDIO_PORT`=3001    # 这里改成3001，为了和 quivr 起冲突
+ `SITE_URL`=http://localhost:3001
+ `POSTGRES_PASSWORD`=123456      # 数据库密码，按自己意愿设置
+ `JWT_SECRET`=拷贝 `JWT Secret` 的值
+ `ANON_KEY`=将 `Preconfigured Payload` 切成 `ANON_KEY`，点击 `Generate JWT`, 拷贝 `Generated Token`
+ `SERVICE_ROLE_KEY`=将 `Preconfigured Payload` 切成 `SERVICE_KEY`，点击 `Generate JWT`, 拷贝 `Generated Token`

## 4. 关于 邮箱 SMTP_ 服务

作用：因为需要邮箱认证，所以必须要链接一个 SMTP 服务器，才能供其他账号登录和中转，为了方便，以QQ邮箱为例子。

**注意：** 实际当中，一定要申请 **企业邮箱**，以 Outlook 邮箱为主

QQ邮箱-设置，账户，开启 SMTP服务，获取授权码

![](../../../images/20230630160225.png)

![](../../../images/20230630160430.png)

![](../../../images/20230630160545.png)

![](../../../images/20230630160832.png)


修改 .env 配置

``` yml
## Email auth
SMTP_ADMIN_EMAIL=XXXX@qq.com # 你的邮箱
SMTP_HOST=smtp.qq.com # 固定ip
SMTP_PORT=587         # 固定端口
SMTP_USER=XXXX@qq.com # 你的邮箱
SMTP_PASS=xxxxx # 获取的授权码
SMTP_SENDER_NAME=XXXX # 发信人
```

## 5. 再次配置密码：`可能不需要，没试过`

到这里配置网关密码 supabase\docker\volumes\api\kong.yml

``` yml
###
### Consumers / Users
###
consumers:
  - username: anon
    keyauth_credentials:
      - key: 这里替换成上面 `ANON_KEY` 对应的 值
  - username: service_role
    keyauth_credentials:
      - key: 这里替换成上面 `SERVICE_ROLE_KEY` 对应的 值

```

## 6. 启动

``` bash
docker compose up
```

成功后，就用浏览器打开: http://localhost:3001

## 7. `注意事项`：修改配置后如何生效

个人实际情况：修改了 `docker-compose.yml` 或者 `.env` 有关数据库的配置，都要 清理掉数据库的数据。

+ rmdir /S /Q volumes\db\data
+ docker compose up --build
