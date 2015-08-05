# HTML提取
从银行征信html中提取有价值的信息（姓名、身份证号、电话和城市）

## ToDoList

* 自动生成xls表格文件(已完成，使用pyExcelerator模块)
* 代码重构
* 提取doc、pdf等多种格式文件中的信息
* 自动锁单


## ChangeLog

* version5:
  * 自动生成xls表格文件

* version1~version4:
  * 完成基本功能；
  * 增加将信息提取出文件的功能；
  * 增加提取目录里所有文件夹所有文件的功能；
  * 增加删除空白目录的功能；
  * 增加将所有文件放到一个文件夹的功能
  * 增加命令行模式
  
## How to Use

* 安装有Python
  * 将html.py文件复制到html文件的根目录里，运行即可
* 编译成exe
  * 在当前目录，命令行运行 `python setup.py py2exe`。需要安装py2exe模块
  
##Result

运行结束后会产生一系列文件夹和文件，分别是：
* `分类结果`文件夹：里面包含分类成功后文件，默认按照地级市分离，如果有命令行指令则按照命令行指令分离
* `未提取`文件夹：包含所有不在分类结果里的文件
* `集合`文件夹：将所有文件夹里的html文件移动到一起
* `result.txt`文件：以逗号分隔，可以当成`.csv`文件导入，也可以直接导入，选择分隔符为`,`并设置每一列都是文本即可
* `result.xls`文件：使用`pyExcelerator`自动生成的电子表格。

## Note

* 软件将会忽视所有路径带有`分类结果` `未提取` `集合` 的文件。
* 只应用于`html`和`htm`文件
* 多次运行`result.txt`和`result.xls`是会被覆盖的，注意做好备份
* `集合`内的文件是移动过去的，其他文件夹里的文件是复制过去的。
* `html`文件应该是`名字[-*]18位身份证号.htm[l]`这种格式的

## Reference
* [pdf2txt](http://www.unixuser.org/~euske/python/pdfminer/index.html#pdf2txt)
* [Write logFile](http://www.cnblogs.com/rrxc/p/4670331.html)
* [pdf库](http://www.open-open.com/lib/list/17)
* [使用C#或者EXCEL](http://blog.csdn.net/lufy_legend/article/details/25191765)
* [使用pucurl进行web提交](http://blog.csdn.net/nwpulei/article/details/8581453) 以及 [aifeidai.js](./aifeidai.js)