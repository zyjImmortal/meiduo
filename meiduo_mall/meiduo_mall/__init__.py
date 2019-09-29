import pymysql

# 注释掉/site-packages/django/db/backends/mysql/base.py关于版本的判断
# 修改site-packages/django/db/backends/mysql/operations.py，query = query.encode(errors='replace')	# 这里把 decode 改为 encode
pymysql.install_as_MySQLdb()
