## ip管理系统

此系统是一个IP管理的web系统，主要使用django5和bootstrap5实现，功能比较简单，主要用于记录与查看不同网段的ip使用情况

主要功能：

- 支持添加子网和ip
- 支持查看子网ip的可视面板，方便知道子网ip的使用情况
- 支持用户登录

### 运行系统

**1.安装python**

建议版本3.10以上版本

```
conda create --name python310 python=3.10
conda activate python310
```

2.**安装依赖**

```
python -m pip install -r requirements.txt
```

**3.迁移数据库**

默认是sqlite数据库，想使用其他数据库请参考[django数据库配置文档](https://docs.djangoproject.com/en/5.1/ref/settings/#databases)

```
python manage.py makemigrations
python manage.py migrate
```

**4.创建用户**

```
 python manage.py createsuperuser
```

**5.运行系统**

```
python manage.py runserver 0.0.0.0:8080
```

访问系统：http://127.0.0.1:8080

## 命令行工具

### ip扫描

功能：扫描子网的存活ip，并写入数据库

使用

```
python3 tools/scan_network.py 192.168.15.0/24
```

注意：如果子网包含的ip过多，扫描会有些慢，请耐心等待
