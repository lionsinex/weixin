from django.db import models

# Create your models here.

from django.db import models

# Create your models here.



class PublicNum(models.Model):
    """
    公众号
    """
   # 公众号表的id,主键索引
    id = models.AutoField(primary_key=True, verbose_name="公众号id")
    image_url = models.CharField(max_length=200, default='', null=True, blank=True,
                                         verbose_name='公众号图片')
    weixin_num = models.CharField(default=" ", max_length=50, verbose_name="微信号")
    name = models.CharField(default=" ", max_length=50, verbose_name="公众号名称")
    _biz = models.CharField(default=" ", max_length=255, verbose_name="_biz")
    introduction = models.CharField(default=' ', max_length=255, verbose_name="功能简介")
    # 反关联文章表
    # default_article= models.ForeignKey('Article', related_name='articles', null=True, blank=True,
    #                                     on_delete=models.SET_NULL, verbose_name='默认文章表')

   # 返回对象的字符串表示
    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_pc_nums"
        verbose_name = '公众号'
        verbose_name_plural = verbose_name
        ordering = ["id"]

class Article(models.Model):
    """
    公众号文章表
    """

    id = models.AutoField(primary_key=True, verbose_name="文章编号")
    publish_time = models.DateTimeField(verbose_name="文章发布时间")
    collect_time = models.DateTimeField(verbose_name="数据采集时间")
    title = models.CharField(default=" ", max_length=50, verbose_name="文章标题")
    author = models.CharField(default=" ", max_length=50, verbose_name="文章作者")
    html_text = models.TextField(default=" ", verbose_name="html内容")
    like_numbers = models.IntegerField(default=1, verbose_name="点赞数")
    content = models.CharField(default=" ", max_length=255, verbose_name="文章内容")
    read_numbers = models.IntegerField(default=1, verbose_name="阅读数")
    # 使用外键关联
    public_num = models.ForeignKey(PublicNum, on_delete=models.PROTECT, verbose_name="所属公众号")

    # 返回对象的字符串表示
    def __str__(self):
        return self.title

    class Meta:
        db_table = "tb_articles"
        verbose_name = '文章'
        verbose_name_plural = verbose_name

class CollectTask(models.Model):
    """
    采集任务表
    """

    # 在代码中进行判断时作为条件
    TASK_STATUS_ENUM = {
        # ""
        "UNCATCH": 1,
        "CATCHING": 2,
        "CATCHED": 3,

    }
    TASK_STATUS_CHOICES ={

        # (保存在数据库中值,在运营站点下字段值的显示名称[verbose_name])
        (1, "未抓取"),
        (2, "抓取中"),
        (3, "抓取完成"),

    }
    id = models.AutoField(primary_key=True, verbose_name="id")
    name = models.CharField(default=" ", max_length=50, verbose_name="任务名称")
    task_status = models.SmallIntegerField(choices=TASK_STATUS_CHOICES, default=1, verbose_name="任务状态")
    article_total_count = models.IntegerField(default=0, verbose_name="文章数量")
    _biz = models.CharField(default=" ", max_length=50, verbose_name="_biz")
    task_time = models.DateField(auto_now_add=True, verbose_name="任务创建时间")
    cl_date_start = models.DateField(verbose_name="公众号开始时间", null=True, blank=True)
    cl_date_end = models.DateField(verbose_name="公众号结束时间", null=True, blank=True)
    public = models.ForeignKey(PublicNum, on_delete=models.PROTECT, verbose_name="公众号")
    # user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="用户")
    rl_count = models.BooleanField(default=False, verbose_name="读赞数")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "tb_tasks"
        verbose_name = '任务'
        verbose_name_plural = verbose_name




