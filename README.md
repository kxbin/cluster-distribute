# cluster-distribute
distribute cluster bash or file，集群 bash 命令或文件分发

# how to use
1. ``git clone https://github.com/kxbin/cluster-distribute.git``


2. ``cd cluster-distribute``


3. ``chmode 755 ./*``


4. ``./link``


5. ``distb``


# example
前提：python3 环境， link 只用执行一次，并且指定的这些 hosts 能够相互之间免密 ssh 登录

yaml 中以及 -f 指定的分发文件路径必须是绝对路径


```
# 分发 echo a 命令到 host1 和 host2 
distb -b 'echo a' -h 'host1,host2'
```


```
# 分发 /root/a.txt 文件到 host1 和 host2 
distb -f '/root/a.txt' -h 'host1,host2'
```


```
# 根据 yaml 配置文件决定如何分发
distb -y example.yaml
```

# yaml
```
$符号必须加\\转义 
host: 分发的主机名 file: 分发的文件或目录 bash: 分发的 shell 命令 once: 只执行一次的代码块 需要 -once 参数开启
yaml 格式如下，distb 会先执行 bash 再执行 file:

host:
    - "m01"
    - "m02"
bash:
    - "echo a"
file:
    - "/root/a.txt"
once:
    bash:
        - "echo b"
    file:
        - "/root/b.txt"
```
