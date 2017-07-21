1. zss module used to calculate edit distance:
https://github.com/timtadh/zhang-shasha

2. results/：以前做的聚类结果，100棵子树，未调阈值
groupTrees.py：以前做的聚类过程，输入是计算好的100棵子树的距离矩阵treematrix.csv
这几个都不要管！

3. trees/和treePics/：原始数据，20个网页切出来的2293棵子树

4. labels/：归到15个类里的600棵子树的截图
calDistance.py：算labels/里若干个类的距离矩阵，带去重，未并行，现在树结构较简单，速度还可以
