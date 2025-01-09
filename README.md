# KML-HBVWGS

HBV病毒全基因组分析，在 kr1stoff/KML-VirusWGS 基础上进行开发，制定好分型数据库、分型对应收录号、分型参考基因组和注释数据库

## 命令行

```bash
poetry -C /data/mengxf/GitHub/KML-HBVWGS run python /data/mengxf/GitHub/KML-HBVWGS/main.py -s input.tsv -w result/241218
```

## 设计思路

1. 使用 `bwa` 比对获得分型
2. 使用分型作为参考基因组获取一致性序列
3. 根据 `genbank` 位置信息提取分型基因组(先准备好数据库)和样本一致性序列8个基因的核酸序列
4. 按照位置一一对应, 返回不一致的氨基酸突变
