# wisdom-class
大二课程设计 - 智慧班级管理系统 后台

## 数据库配置

- 手动创建mysql查询、创建数据库：`CREATE DATABASE WisdomClass;`

注意，要确保你的数据库配置是这样的（否则运行后端程序之前需要更改settings.py文件中的配置）：

```python
{
        'USER':'root',
        'PASSWORD':'123456',
        'HOST':'127.0.0.1',
        'PORT':'3306',
}
```

## 后端应用启动

- 确保安装python，pip包管理工具。安装django框架、xlsxwriter等依赖后，执行下面步骤：
  1. `python manage.py makemigrations`
  1. `python manage.py migrate `
  1. `python manage.py runserver`
