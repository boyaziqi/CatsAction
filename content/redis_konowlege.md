title:  Redis知识整理
date: 2017-02-11
category: redis
tags: redis, geo

## 前述

本篇讲述Celery的原理和基本使用

## 基本原理

Celery基于Broker传递执行任务，当tasks被调用时，先序列化，然后传递到Broker，worker取出来执行。


## 序列化

**命令**

**实现机制**