## 吉林大学作业解析工具

**这个公司开发的考试系统居然在考试期间回传答案数据....于是做了这么一个阴间工具，从 HTTP 包中直接获取试卷/作业答案，并且以简洁易懂的方式展现给有需要的同学，仅供学习交流使用。**

> 现已使用现学现用的 ReactJS 重写了前端，优化一些前端的体验。

![screenshot](https://raw.githubusercontent.com/FantWings/jlu-exam_react/master/public/demo.png)
适用范围：吉林大学弘成科技发展有限公司开发的学生作业系统

## 使用方法

**在线使用：https://jlu.htips.cn**

### 操作步骤

- 在操作之前，请先点击开始考试，进入考试界面
- 按下 F12 键，打开浏览器调试工具（**如果你用的是苹果电脑自带的 Safari 浏览器请看下面，其他浏览器请跳过**）
  - Safari 默认关闭了开发者模式，请先[启用开发模式](https://jingyan.baidu.com/article/9113f81bfa87586b3214c7d4.html)，才可调出 F12 界面
  - 开发者模式启用后，在页面按下键盘 Option+Command+A 组合键，继续下一步。
- 选择"网络（Network）"，在筛选器上筛选“XHR”
- 在题目上随便选一个答案，点击“保存”
- 这时可以在网络工具下看到出现一个“SubmitAnserPaper”
- 选中“SubmitAnserPaper”，点“响应（Response）”
- 按下键盘 `Ctrl+A`（苹果电脑 `Command+A`）全选，并按下`Ctrl+C`（苹果电脑 `Command+C`）复制全部内容。
- 将复制的数据`Ctrl+V`（苹果电脑 `Command+V`）粘贴至解析工具，输入执行密钥，点击提交，即可解析答案。

## 下载源码试一试

如果你对源码感兴趣或者你也想试试改进这个工具，下面将指引你如何去做：

**环境需求：3.X 或以上的 Python && 1.1.X 以上的 Flask 库版本**

### 下载源码

- 使用命令将代码 clone 至本地：
  `git clone https://github.com/FantWings/jlu-exam_python.git`

### 运行后端（下列二选其一）

1. **直接运行**

- 请确保系统内安装了 3.X 或以上的 Python 版本，使用`python -v`查看 Python 版本。
- 在根目录执行`pip install Server/requirements.txt`安装 flask 所需要的扩展
  - 注意 mysqlclient 需要依赖 mysql-config，如果你是 Ubuntu/Debian 系统，请注意安装 libmysqlclient-dev
- 使用拷贝下列命令，配置环境变量，设置服务端链接数据库的方式（注意该方法为临时方法，终端关闭后会失效，如有需要，请写入到 bashrc 等位置使其永久生效）：

```bash
export SQL_HOST="<数据库IP地址>" \
export SQL_USER="<数据库用户名>" \
export SQL_PASS="<数据库密码>" \
export SQL_BASE="<数据库名称>" \
export SQL_PORT="<数据库端口号，默认3306>"
```

- 运行 `flask run`启动开发后端。
  - 默认监听 127.0.0.1:5000，如果需要任意网络访问请使用参数-h 0.0.0.0（安全角度非常不建议）
- 运行`uwsgi --socket 0.0.0.0:5000 --protocol=http -p 3 -w wsgi:app` 启动生产环境后端。
  - 建议配合 NGINX 来启动后端更为安全。

2. **Docker**

- 请先安装 Docker 运行时
- 复制下列命令，替换文本，在终端粘贴直接运行：

```bash
sudo docker run -d --name jlu_helper \
       -e SQL_HOST=<数据库IP地址> \
       -e SQL_BASE=<数据库名称> \
       -e SQL_USER=<数据库用户名> \
       -e SQL_PASS=<数据库密码> \
       -e SQL_PORT=<数据库端口号，默认3306> \
       -p 9000:9090 \
       fantwings/jlu-helper:latest
```
