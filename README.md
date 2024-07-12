# 简单多线程目录扫描
### 1. 简介
支持自定义字典及线程数量（默认字典用的御剑的）

### 2. 环境
使用的python3.6（python版本不能低于3.4，因为使用了fullmatch）  
需要安装requests、fake_useragent库

### 3. 食用指南
在dirScan.py同级目录下打开cmd（字典也放在一起）  
> 可以有以下调用方法：
> 
> - a. `python dirScan.py 测试网址`
> - b. `python dirScan.py 测试网址 线程数量`
> - c. `python dirScan.py 测试网址 你的字典文件`
> - d. `python dirScan.py 测试网址 你的字典文件 线程数量`
> 
默认的字典是御剑滴，默认10个线程(你的python应该装了环境变量了吧，应该装了吧)  
#### 示例  
>只指定测试网址
```bash
python dirScan.py http://example.com
```
>指定测试网址和线程数量
```bash
python dirScan.py http://example.com 10
```
>指定测试网址和自定义字典文件
```bash
python dirScan.py http://example.com custom_dict.txt
```
>指定测试网址、自定义字典文件和线程数量
```bash
python dirScan.py http://example.com custom_dict.txt 8
```
### 4. 一些补充
如果响应返回这些状态码，会记下网址，存在dirScan.py的同级目录  
code = [200, 300, 301, 302, 303, 304, 305, 307, 403]  
如果所有响应没有返回以上状态码，会创建一个文件，并在程序结束时删除  
### 5. 一张图片  
