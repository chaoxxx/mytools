# coding=utf-8
import datetime

a=r"\n\n\n\n\t\t\t\t\t\t\t\t被告张德有于判决生效后15日内偿还原告孙冰借款本金90,000.00元；并从2016年2月22日起至实际给付之日止以本金40,000.00元按月利率1.5分计息；从2016年3月15日起至实际给付之日止以本金50,000.00元按月利率1.125分计息。 如果未按本判决指定的期间履行给付金钱义务，应当依照《中华人民共和国民事诉讼法》第二百五十三条之规定，加倍支付迟延履行期间的债务利息。 案件受理费2,682.00元，公告费700.00元由被告张德有负担。\n                             \n\n\n\n"

a = a.replace(r"\t","").replace(r"\n","")




print(a)



time_now = datetime.datetime.now().strftime('%H:%M:%S.%f')
print(time_now)

