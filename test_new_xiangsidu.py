product_center=['云端业务工作室','云端营销','企业驾驶舱','供应链金融','中小企业服务站','数据淘金','企业大脑'
            ,'云端应用工作室','企业上云服务站','供应商指南','云端应标群','云网物流']
question = '用户怎么登录'
if (i in question for i in product_center):
    entity_name = '产品介绍'
    print('yes')