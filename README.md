<!--
parent:
  order: false
-->

<div align="center">
  <h1> Chaineye Repo </h1>
</div>

<div align="center">
  <a href="https://github.com/SavourDao/hailstone/releases/latest">
    <img alt="Version" src="https://img.shields.io/github/tag/SavourDao/savour-core.svg" />
  </a>
  <a href="https://github.com/SavourDao/hailstone/blob/main/LICENSE">
    <img alt="License: Apache-2.0" src="https://img.shields.io/github/license/SavourDao/savour-core.svg" />
  </a>
   <a href="https://www.python.org/downloads/">
    <img alt="License: Apache-2.0" src="http://img.shields.io/badge/Python3.*-ff3366.svg"/>
  </a>
  
 
</div>


#### 1.Introduction

The whole project is written in Python's Django framework. The project includes PC web terminal, H5 terminal and operation background. The overall design of the project is beautiful and atmospheric, and the technologies used are also relatively Simple, suitable for personal blog use, but also suitable for a large platform. There is a big gap with the current open source blog or content platform.

#### 2.Deployment

Before deploying, you need to install python 3.8 or above, Mysql and Redis

1. clone：
```buildoutcfg
git clone git@github.com:guoshijiang/chaineye.git
```

2. set up a virtualenv：
```buildoutcfg
cd chaineye
virtualenv .env
source .env/bin/activate
```

3. install

```buildoutcfg
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

4. migrate database
```buildoutcfg
 python3 manage.py migrate
```
If you change the database structure, please run `python3 manage.py makemigrations` first, then run `python3 manage.py migrate`

5. run：
```buildoutcfg
 python3 manage.py runserver
```

If you deploy online, it is recommended to use supervisor to manage the process, Ng forwarding, and use `python3 manage.py collectstatic` to collect static files to the corresponding directory.



