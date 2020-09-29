#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -y 参数可以是一个yaml文件或者目录，如果是目录会遍历分别执行

'''
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
'''

import os,sys,subprocess,json,socket,argparse,yaml

os.chdir(os.path.split(os.path.realpath(__file__))[0])
localhost = socket.gethostname()

def run_shell(shell):
	cmd = subprocess.Popen(
		shell,
		stdin=subprocess.PIPE,
		stderr=sys.stderr,
		close_fds=True,
		stdout=sys.stdout,
		universal_newlines=True,
		shell=True,
		bufsize=1
	)
	cmd.communicate()
	return cmd.returncode

def distribute_file(files, host):
	if files is not None and len(files) != 0 and host != localhost: # 文件不分发给本机
		for file in files:
			print(run_shell('./xcp {} {}'.format(host, file)))

def distribute_bash(bashs, host):
	if bashs is not None and len(bashs) != 0:
		for bash in bashs:
			print(run_shell('./xcall {} "{}"'.format(host, bash)))

def distribute(yamlfile, once=False):
	with open(yamlfile, 'r') as f:
		meta = yaml.load(f.read(), Loader=yaml.FullLoader)
		if len(meta['host']) != 0:
			for host in meta['host']:
				if once == True:
					distribute_file(meta['once']['file'], host)
					distribute_bash(meta['once']['bash'], host)
				distribute_file(meta['file'], host)
				distribute_bash(meta['bash'], host)

parser = argparse.ArgumentParser(
    description="Distribute, cluster file or bash distribute",
	add_help=False
)
parser.add_argument(
    "-y", "--yaml", default=None, help="yaml config file or directory describe how to distribute"
)
parser.add_argument(
    "-f", "--file", default=None, help="a file want to distribute"
)
parser.add_argument(
    "-b", "--bash", default=None, help="a bash want to distribute"
)
parser.add_argument(
    "-h", "--hosts", default=None, help="distribute to which hosts, use ',' split"
)
parser.add_argument(
    "-once", "--once", action="store_true", help="don't skil once area"
)
parser.set_defaults(once=False)

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

hosts = args.hosts
with open('hosts.yaml', 'r') as f:
	temp = yaml.load(f.read(), Loader=yaml.FullLoader)
	if hosts in temp.keys():
		hosts = temp['hosts']

if args.yaml is not None:
	if os.path.isdir(args.yaml):
		if args.once is False:
			for y in os.listdir(args.yaml):
				distribute(args.yaml + '/' + y)
		else:
			print('yaml dir not support once')
	else:
		distribute(args.yaml, args.once)
elif args.file is not None and args.hosts is not None:
	hosts = hosts.split(',')
	for host in hosts:
		if host != localhost:
			print(run_shell('./xcp {} {}'.format(host, args.file)))
elif args.bash is not None and args.hosts is not None:
	hosts = hosts.split(',')
	for host in hosts:
		print(run_shell('./xcall {} "{}"'.format(host, args.bash)))
else:
	print('params is invalid')
