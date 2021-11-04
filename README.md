# r_nlu
An intergrated NLU serivice, in associate bert_nlu model

### 项目结构
项目使用了rpc服务框架，which is not necessary，逻辑主入口在`d_match.py`，可以独立运行

`dmap.txt`:domain mapping配置文件，从slot/domain/intent到输出domain的映射关系  
`smap.txt`:slot mapping配置文件，slot在不同场景下的细粒度映射关系  
`rmap.txt`:导航场景正则映射配置文件  
`ocslots.txt`:slot/intent名-slot/intent文本映射配置文件（前缀树用）  
`pmodel.py`:bert_nlu服务的调用解析逻辑  
`pregex.py`:正则匹配的解析逻辑  
`ptrie.py`:前缀树构造检索类  

