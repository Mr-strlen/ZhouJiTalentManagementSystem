#  舟楫-跨公司人才管理系统 ZhouJiTalentManagementSystem
<img src="https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/logo.png" width="120">
  
欲济无舟楫，端居耻圣明？   
舟楫人才系统，为您的职业发展，保驾护航。

## CAU镇星团队
- 李丰
- 王思诺
- 钱鹏昊
- 马红飞
- 谢林浪
- 陈翰雲

## 项目日期
2020.3.1-2020.3.18

## 效果演示
- [COO审批申请](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/A.COO%E5%AE%A1%E6%89%B9%E7%94%B3%E8%AF%B7.mp4)

- [提交调档信息申请](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/A.%E6%8F%90%E4%BA%A4%E8%B0%83%E6%A1%A3%E4%BF%A1%E6%81%AF%E7%94%B3%E8%AF%B7.mp4)

- [COO审批申请](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/A.COO%E5%AE%A1%E6%89%B9%E7%94%B3%E8%AF%B7.mp4)

- [查看员工评价+高级评价系统](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/B.%E6%9F%A5%E7%9C%8B%E5%91%98%E5%B7%A5%E8%AF%84%E4%BB%B7%2B%E9%AB%98%E7%BA%A7%E8%AF%84%E4%BB%B7%E7%B3%BB%E7%BB%9F.mp4)

- [添加员工评价](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/B.%E6%B7%BB%E5%8A%A0%E5%91%98%E5%B7%A5%E8%AF%84%E4%BB%B7.mp4)

- [提交调档信息申请](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/A.%E6%8F%90%E4%BA%A4%E8%B0%83%E6%A1%A3%E4%BF%A1%E6%81%AF%E7%94%B3%E8%AF%B7.mp4)

- [HR论坛](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/C.HR%E8%AE%BA%E5%9D%9B.mp4)

- [员工离职](https://github.com/Mr-strlen/ZhouJiTalentManagementSystem/blob/main/%E6%BC%94%E7%A4%BA%E8%A7%86%E9%A2%91/D.%E5%91%98%E5%B7%A5%E7%A6%BB%E8%81%8C.mp4)

## 数据
由于员工档案数据、调档申请和帖子系统并没有公开的数据集，这里使用随机生成的方式产生  
**数据注入代码和NLP测试代码均在ExtraCode/Addfiles内**
### HR评价数据
- 获取方式 https://class.acagrid.com/pc/comment
- 使用期末评语生成，将“老师”换成“领导”，“同学”换成“同事”，“学生”换成“员工”
- **问题：** 因为生成评语本身就是基于固定语句随机生成的，所以之后分词的结果毕竟雷同，影响了词云的多样性，进而无法根据评价实现特色推荐

## 技术架构

- 基于Flask框架
- 前端：HTML+CSS+JS 
- 数据库：SQLAlchemy+MySQL(orm封装)
- 用户信息：Cookies+Session
- 版本控制：Git
- 可视化图表：Echarts, Layui, x-admin模板

## 功能

### 员工管理

- HR用户的登陆注册
- COO用户更高权限的登陆注册
- 对本公司员工档案的建立，修改，删除
- 基于姓名、职务、学历、毕业院校等关键词，实现对员工的精确查找
- 对本公司员工进行离职办理


### 员工评价

- 给本公司员工进行多条文字性评价
- 从领导力、创新性、交际能力、勤奋度、工作效率五个维度为员工打分，每次打分会覆盖上一次打分记录
- 基于员工的所有评价，进行分词生成个人词云，显示最大关键词
- 计算打分均数和评价的热词评分，得出该员工在五个维度的综合分数，生成个人评价雷达图
- 根据需求排序，快速得到不同视角下的员工工作情况

### 招聘查询

- 查看系统内未就业员工的个人信息，包括基本信息、历史公司和历史评价
- 基于历史评价，生成个人词云，显示最大关键词，协助HR快速把握员工性格特征
- 根据历史评价热词评分和过去五维度打分，生成个人能力雷达图
- 根据需求排序，帮助HR得到心仪的员工

### 跨公司信息查询

- 本公司HR可以向联盟内其他公司发出信息查看申请，了解同行员工信息
- 其他公司COO审批申请，给予信息查询权限

### HR交流社区

- 开放的论坛讨论社区，包括看帖，发帖，回帖等功能
- HR和COO没有权限区分，人人平等，交流工作生活，促进联盟内企业间合作

### 额外功能
- 严格的权限管理制度，在没有审批的情况下无法访问其他公司数据

