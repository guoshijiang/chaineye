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

The whole project is written in Python's Django framework. The project includes PC web terminal, H5 terminal and operation background. Currently, the open source code is the PC terminal, and the mobile terminal and operation background will be open sourced in the future. The overall design of the project is beautiful and atmospheric, and the technologies used are also relatively Simple, suitable for personal blog use, but also suitable for transforming into a large platform. There is a big gap with the current open source blog or content platform.

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

### Notice

In the future, the code on the PC side will be developed based on this code when we develop new functions. Welcome everyone to join us.

If you use this code and have any questions during the construction process, you can ask my college (www.wenwoha.com) to find the contact information above, or you can directly add my WeChat: LGZAXE


