# coding:utf-8
import wx_pay_util

# 统一下单
url_unified_order = 'pay/unifiedorder'

# 查询订单
url_order_query = 'pay/orderquery'

# 关闭订单
url_close_order = 'pay/closeorder'

# 申请退款
url_refund = 'secapi/pay/refund'

# 查询退款
url_refund_query = 'pay/refundquery'

# 下载对账单
url_download_bill = 'pay/downloadbill'

# 下载资金账单
url_download_fundflow = 'pay/downloadfundflow'


def get_response():
    data = {
        'appid': "wxdace645e0bc2c424",
        # 'bill_date': 20180601,
        # 'bill_type': 'ALL',
        'mch_id': '1900008951',
        'nonce_str': 'ibuaiVcKdpRxkhJA',
        'sub_mch_id': '218224494',
        'out_trade_no': '2018060515533101817182221344',
    }
    secret = '3AC991426F056322E053645AA8C0CC12'
    wechat = wx_pay_util.WechatDroid(url_order_query, data, secret)
    wechat.save()


if __name__ == '__main__':
    get_response()
