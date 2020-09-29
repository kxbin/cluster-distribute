# cluster-distribute
distribute cluster bash or file，集群bash命令或文件分发

# how to use
1. ``git clone https://github.com/kxbin/cluster-distribute.git``


2. ``cd cluster-distribute``


3. ``chmode 755 ./*``


4. ``./link``


5. ``distb``


# example
前提：指定的这些hosts能够相互之间免密ssh登录


``distb -b 'echo a' -h 'host1,host2'``


``distb -f '/root/a.txt' -h 'host1,host2'``


``distb -y example.yaml``
