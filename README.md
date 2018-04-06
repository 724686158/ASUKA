地址：山东科技大学

指导老师：倪维健

Project Onwer：孟子成

# ASUKA
面向kubernetes集群的配置管理系统

#主要功能模块

## alchimest
存储各组件Resource（包含Version， Environment Var， if DaemonSet， if Host, PV&PVC, Secret）。
存储应用（组件的集合）与组件的一对多关系。

## furion
存储Region Data。
存储应用对Region Data的依赖。

## coil
从中心实例组发送数据副本给私有区内的衍生实例。
验证衍生实例内数据副本的版本，是否受到污染。

## phoenix
面向kubernetes API的yaml渲染。
