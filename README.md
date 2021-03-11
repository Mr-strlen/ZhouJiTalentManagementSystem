#  ZhouJiTalentManagementSystem
<img src="https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/logo.png" width="120">
“欲济无舟楫”？舟楫人才系统，为您的职业发展，保驾护航。

## 设计的开发过程
1. 第一部分 登录注册，档案简历，档案查询，查看离职情况
2. 第二部分 COO登录注册，查看别的公司信息，调档申请，接受申请
3. 第三部分 hr写评价，离职，COO对hr增删改，Hr修改员工
4. 第四部分 带有NLP的评价系统（词频分析+词云生成）
5. 第五部分 推荐系统（选做）
6. 第六级 帖子系统（选做）

## 技术记录
### 页面跳转
1. a标签

### 页面参数传递
1. 从app.py传到html *jinja*
2. 从html传到app.py *get/post ajax*
3. url路径参数传参

1. 按钮跳转到网页--里面写跳转的网页，  如果是传递传数用表单
2. app到html用jinjia模板，页面使用{{}}进行解析
3. html到app.py可ajax可以使用json格式传递，app接收用request.args.get()
4. html到html传递数据可以使用会话形式，页面的跳转必须通过app.py的路由再到方法，方法中使用request
5. js是操作前端html的标签，它可以传递数据到后台，也可以接收数据从后台，通过Json的格式，这个最好使用Jquery
6. ajax应对单个页面的不同请求，实现局部刷新

### cookies+session部分
1. 介绍和案例 https://blog.csdn.net/kongsuhongbaby/article/details/101391022
### Flask+SQLAlchemy(ORM)
1. SQLAlchemy属性常用数据类型 https://blog.csdn.net/dremcl/article/details/105873842
2. 增删改查 https://blog.csdn.net/weixin_44251004/article/details/89388538
### 网页开发
1. 查询展示实现分页（使用Jinja模板） https://w.cnblogs.com/whycai/p/12283701.html