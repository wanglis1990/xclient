# 描述
> 通用的调用第三方HTTP服务的HTTPClient工具模板


# 安装
``` 
pip install git+https://x/xclient.git
``` 


# 编码修改
* 重命名，将X替换为实际需求的服务命名

```
XClient -> ScrmClient
XClient -> UnionPayClient

XClientException -> ScrmClientException

XStatusCode -> ScrmStatusCode

setup.py 相应配置修改
```
* 新增模块

``` 
直接在xclient目录下新增模块，比如member.py coupon.py, 参考order.py

在xclient.__init__.py注册方法
member_register = member.MemberRegister()
coupon_query = coupon.CouponQuery()

``` 

# 示例
```
from xclient.client import XClient

x_client = XClient("用户名", "密码")

# 订单创建
x_client.order_create("H100006", "2018-07-13", "2018-07-14", "18800000000", "王力宏", remark="测试")

# 订单删除
x_client.order_delete("O123456", remark="测试")
```
