print('Python环境测试')
import sys
print('Python版本:', sys.version)
print('Python路径:', sys.executable)

try:
    import flask
    print('Flask版本:', flask.__version__)
    print('Flask路径:', flask.__file__)
except ImportError as e:
    print('Flask导入错误:', e)

print('测试完成')