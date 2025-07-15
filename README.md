# Next Diary

一个简单的日记互换网站

## 技术栈

前端使用Vue3+TS+Element-Plus

后端使用FastAPI+SQLModel

## 安装部署

首先需要安装uv作为python环境管理工具

一键启动后端

```bash
cd ./next-diary-server
uv run main.py
```

前端需要使用pnpm作为包管理工具

```bash
cd ./next-diary-client
pnpm install
```
启动
```bash
pnpm dev
```
打包构建
```bash
pnpm build
```