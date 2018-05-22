项目名称：ASUKA

地址：山东科技大学

指导老师：倪维健

Project Onwer：孟子成



## 概述
面向容器化微服务框架的配置管理系统


## 主要功能模块

### alchimest
镜像（IMAGE），组件（COMPONENT），软件包（PACKAGE）的配置管理。

### furion
集群（REGION），服务（SERVICE），环境（ENVIRONMENT）的配置管理。

### coil
记录alchimest和furion的地址，将软件包和环境相连（Link，或称“发版”），记录发版行为，并提供结果的下载。

### phoenix
根据发版的结果，导出kubernetes的yaml。（尚未完成）


## 参考开源项目

### 树状图绘制：https://github.com/panhc/d3js-tree-example