from .base import BaseClient


class OrderCreate(BaseClient):
    """订单创建"""

    path = "/x/order/create"

    def __call__(self, hotel_id, checkin, checkout, mobile, guest_name, *, remark):
        """订单创建

        param::
            hotel_id: 酒店ID
            checkin: 入住日期
            checkout: 离店日期
            mobile: 联系人手机号
            guest_name: 入住人姓名
            remark: 备注
        """

        params = {
            "hotelId": hotel_id,
            "checkIn": checkin,
            "checkOut": checkout,
            "mobile": mobile,
            "guestName": guest_name,
            "remark": remark,
        }
        return self._post(self.path, json=params)


class OrderDelete(BaseClient):
    """订单删除"""

    path = "/x/order/delete"

    def __call__(self, order_id, *, remark):
        """订单删除

        param::
            order_id: 订单ID
            remark: 备注
        """

        params = {
            "orderId": order_id,
            "remark": remark,
        }
        return self._post(self.path, json=params)
