### 链眼社区，项目网址：http://chaineye.info/

#### 1.项目介绍

整个项目是 Python 的 Django 框架编写，项目包含 PC 网页端，H5端和操作后台，目前开源代码为 PC 端，后续会陆续开源移动端和操作后台，项目整体设计美观大气，用到的技术也是比较简单，适合个人博客使用，也适合改造成大型平台。和目前开源的博客或者内容平台差距比较大。

#### 2.为什么选择开源

首先介绍一下我和我的团队，我是郭世江，多年的技术开发经验，我们团队叫问我社区，我和我的团队一起做了一个社区，叫做问我社区（http://www.wenwoha.com ）,我们这个团队都是一群技术爱好者，做社区的目的不是为了赚钱，而是想帮助那些想学习 IT 技术的朋友提供一个小小的选择，而链眼这个项目是我们社区规划里面的一个小模块，专攻区块链相关的内容。由于大家平时都比较忙，去做这个社区的时间也比较少，所以我们想把这个代码开源出来呼吁社区一起做这个事儿，如果您喜欢，您可以复制我们代码去建设一个平台，当然，我们还是希望您可以加入我们一起做。

- 如果你只是想复制我们代码，那么你只要在网站下方加上我们的代码链接和问我社区和链眼的友链就可以使用我们的的代码
- 如果你想加入我们，问我社区（http://www.wenwoha.com ）上面有联系方式。

#### 3.代码部署

在部署代码前，你需要安装 python 3.8 以上版本，Mysql 数据库和 Redis

第一步，克隆代码：
```buildoutcfg
git clone git@github.com:guoshijiang/chaineye.git
```

第二步，搭建一个 virtualenv：
```buildoutcfg
cd chaineye
virtualenv .env
source .env/bin/activate
```

第三步，安装依赖：
```buildoutcfg
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

第四步，数据库migrate：
```buildoutcfg
 python3 manage.py migrate
```
如果你改变数据库结构，请先运行 `python3 manage.py makemigrations`, 然后再运行 `python3 manage.py migrate`

第五步，运行服务：
```buildoutcfg
 python3 manage.py runserver
```

如果你在线上部署，建议使用，supervisor 管理进程，Ng 转发，把静态文件使用 `python3 manage.py collectstatic` 收集到相应的目录。


注意：以后 PC 端的代码，我们开发新功能的时候也基于这个代码开发，欢迎大家加入一起搞

