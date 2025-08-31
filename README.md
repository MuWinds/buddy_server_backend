# buddy_server_backend

给 Expense-Buddy 用的后端，基于 PostgreSQL 和 FastAPI

配置方法：

1.在 PostgreSQL 里新建一个名为 buddy 的模式

2.输入指令

```bash
alembic upgrade head
```

将数据库表结构导入 PostgreSQL 中

3.复制项目根目录下的.env.example 并更名为.env，修改配置文件

4.输入下面的指令启动项目

```bash
uvicorn app.main:app --reload
```
