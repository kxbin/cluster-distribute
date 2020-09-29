# cluster-distribute
distribute cluster bash or file，集群bash命令或文件分发

# how to use
1. ``git clone https://github.com/kxbin/cluster-distribute.git``


2. ``cd cluster-distribute``


3. ``chmode 755 ./*``


4. ``./link``


5. ``distb``


# example
前提：python3环境， pip3 install pyyaml，yum install rsync，并且指定的这些hosts能够相互之间免密ssh登录

yaml中以及-f指定的分发文件路径必须是绝对路径


``distb -b 'echo a' -h 'host1,host2'``


``distb -f '/root/a.txt' -h 'host1,host2'``


``distb -y example.yaml``

# yaml
```
$符号必须加\\转义 
host:分发的主机名 file:分发的文件或目录 bash:分发的shell命令 once:只执行一次的代码块 需要-once参数开启
yaml格式如下:

host:
    - "m01"
    - "m02"
file:
    - "/root/a.txt"
bash:
    - "echo a"
once:
    file:
        - "/root/b.txt"
    bash:
        - "echo b"
```
