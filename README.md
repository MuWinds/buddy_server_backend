# buddy_server_backend

给 Expense-Buddy 用的后端，基于 PostgreSQL 和 FastAPI

配置方法：

1.在 PostgreSQL 里新建一个名为 buddy 的模式

2.运行项目根目录下的 agent_character.sql，将数据库表结构导入 PostgreSQL 中

3.复制项目根目录下的.env.example 并更名为.env，修改配置文件

4.配置 Python 环境，输入下面的指令安装依赖

```bash
pip install requirements.txt
```

5.输入下面的指令启动项目

```bash
uvicorn app.main:app --reload
```

注意：正式的生产环节需要去掉最后的`--reload`部分，以关闭 debug 模式
