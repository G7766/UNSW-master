#!/usr/bin/perl

#在执行该脚本前要先确保文件有可执行权限，我们可以先将文件权限修改为 0755 ：
#$ chmod 0755 hello.pl
#$ ./hello.pl 
print "Hello world\n";
print("Hello, world\n");
print 'Hello, world\n';    # 单引号
print "\n";
=pod 注释
这是一个多行注释
这是一个多行注释
这是一个多行注释
这是一个多行注释
=cut
$a = 10;
print "a = $a\n";
print 'a = $a\n';
$a = 10;
$var = <<"EOF";
这是一个 Here 文档实例，使用双引号。
可以在这输如字符串和变量。
例如：a = $a
EOF
print "$var\n";
 
$var = <<'EOF';
这是一个 Here 文档实例，使用单引号。
例如：a = $a
EOF
print "$var\n";


$result = "菜鸟教程 \"runoob\"";
print "$result\n";
print "\$result\n";


#数组变量以字符 @ 开头，索引从 0 开始，如：@arr=(1,2,3)
@arr=(1,2,3);
#哈希是一个无序的 key/value 对集合。可以使用键作为下标获取值。哈希变量以字符 % 开头
#%h=('a'=>1,'b'=>2);



$z = time();
print "$z\n";
@months = qw( 一月 二月 三月 四月 五月 六月 七月 八月 九月 十月 十一月 十二月 );
@days = qw(星期天 星期一 星期二 星期三 星期四 星期五 星期六);
 
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
print "$mday $months[$mon] $days[$wday]\n";

$datestring = localtime();
print "时间日期为：$datestring\n";


$gmt_datestring = gmtime();
print "GMT 时间日期为：$gmt_datestring\n";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
 
printf("格式化时间：HH:MM:SS\n");
printf("%02d:%02d:%02d\n", $hour, $min, $sec);



# 函数定义
sub Hello{
	print "Hello, World!\n";
}
 
# 函数调用
Hello();