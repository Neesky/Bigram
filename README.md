基于人民日报标注语料（data.txt），训练一个Bigram语言模型，并预测任意给定语句的语言概率。

训练参数：

```python
--origin_data_file    file where to load data
--modified_data_file  file where to put modified_data
--sentence            sentence to be predicted
--type                use what to smooth {katz,add}
```



参考资料：

katz: https://zhuanlan.zhihu.com/p/100256789

hanlp: https://zhuanlan.zhihu.com/p/187560424

hanlp: https://blog.csdn.net/Changxing_J/article/details/105990294

bigram: https://blog.csdn.net/Yellow_python/article/details/89088854?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_title~default-0.no_search_link&spm=1001.2101.3001.4242

都写了参考资料了，要不再写写致谢。

感谢助教，感谢自己，感谢一个一直帮助我的人。