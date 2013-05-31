# -*- coding: utf-8 -*-

import hashlib
import datetime
from django.db import models
from app.functions import id_number_validator

year_choices = [(y, y) for y in range(datetime.datetime.now().year, 1903, -1) ]
month_choices = [(m, m) for m in range(1, 13)]

class PasswordField(models.CharField):
    def get_prep_value(self, value):
        m = hashlib.md5(value)
        return m.hexdigest()

class Job(models.Model):
    u'''招聘岗位'''
    job_type = models.CharField(
        max_length=20, choices=((u'教师', )*2, (u'教辅', )*2, (u'管理人员', )*2))
    department = models.CharField(max_length=100)
    major = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    degree_limit = models.CharField(max_length=255, choices=((u'硕士',)*2, (u'博士',)*2))
    degree_des = models.TextField()

    def __unicode__(self):
        return '%s - %s' % (self.major, self.job_type)


class People(models.Model):
    gender_choices = ((u'男',)*2, (u'女',)*2)
    nation_choices = (
        (u'汉族',)*2, (u'蒙古族',)*2, (u'回族',)*2, (u'藏族',)*2, (u'维吾尔族',)*2, 
        (u'苗族',)*2, (u'彝族',)*2, (u'壮族',)*2, (u'布依族',)*2, (u'朝鲜族',)*2, 
        (u'满族',)*2, (u'侗族',)*2, (u'瑶族',)*2, (u'白族',)*2, (u'土家族',)*2, 
        (u'哈尼族',)*2, (u'哈萨克族',)*2, (u'傣族',)*2, (u'黎族',)*2, (u'僳僳族',)*2, 
        (u'佤族',)*2, (u'畲族',)*2, (u'高山族',)*2, (u'拉祜族',)*2, (u'水族',)*2, 
        (u'东乡族',)*2, (u'纳西族',)*2, (u'景颇族',)*2, (u'柯尔克孜族',)*2, 
        (u'土族',)*2, (u'达斡尔族',)*2, (u'仫佬族',)*2, (u'羌族',)*2, (u'布朗族',)*2, 
        (u'撒拉族',)*2, (u'毛难族',)*2, (u'仡佬族',)*2, (u'锡伯族',)*2, 
        (u'阿昌族',)*2, (u'普米族',)*2, (u'塔吉克族',)*2, (u'怒族',)*2, 
        (u'乌孜别克族',)*2, (u'俄罗斯族',)*2, (u'鄂温克族',)*2, (u'崩龙族',)*2, 
        (u'保安族',)*2, (u'裕固族',)*2, (u'京族',)*2, (u'塔塔尔族',)*2, 
        (u'独龙族',)*2, (u'鄂伦春族',)*2, (u'赫哲族',)*2, (u'门巴族',)*2, 
        (u'珞巴族',)*2, (u'基诺族',)*2, (u'其他',)*2, (u'外国血统',)*2
    )
    political_status_choices = (
        (u'中共党员',)*2, (u'中共预备党员',)*2, (u'共青团员',)*2, (u'民革党员',)*2, 
        (u'民盟盟员',)*2, (u'民建会员',)*2, (u'民进会员',)*2, (u'农工党党员',)*2, 
        (u'致公党党员',)*2, (u'九三学社社员',)*2, (u'台盟盟员',)*2, (u'无党派人士',)*2, 
        (u'群众（现称普通公民）',)*2, (u'港澳同胞',)*2, (u'其他',)*2
    )
    marital_status_choices = ((u'已婚', )*2, (u'未婚', )*2, (u'离婚', )*2, (u'其他', )*2)
    name = models.CharField(max_length=200, verbose_name=u'姓名 *')
    gender = models.CharField(max_length=3, choices=gender_choices, verbose_name=u'性别 *')
    nation = models.CharField(max_length=50, choices=nation_choices, verbose_name=u'民族 *')
    birthday = models.DateField(verbose_name=u'出生年月 *')
    id_number = models.CharField(
        max_length=18, verbose_name=u'身份证号', validators=[id_number_validator])
    job = models.ForeignKey(Job, verbose_name=u'申请岗位 *', help_text=u'请选择岗位')
    political_status = models.CharField(max_length=50, choices=political_status_choices, 
                                        verbose_name=u'政治面貌')
    marital_status = models.CharField(max_length=10, choices=marital_status_choices, 
                                      verbose_name=u'婚姻状况')
    # 籍贯
    hometown_prov = models.CharField(max_length=50)
    hometown_city = models.CharField(max_length=100)
    # 户口
    residence_prov = models.CharField(max_length=50)
    residence_city = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20, help_text=u'手机')
    other_contact = models.CharField(max_length=30, blank=True)
    foreign_language_level = models.CharField(max_length=50)
    start_work_year = models.IntegerField(choices=[(0,u'无'),]+year_choices)
    start_work_month = models.IntegerField(choices=[(0,u'无'),]+month_choices)
    query_password = models.CharField(max_length=32)
    # 专业技术资格
    technical_qualification = models.CharField(max_length=200, blank=True)
    # 执业资格
    operation_qualification = models.CharField(max_length=200, blank=True)
    # 其他资格
    other_qualification = models.CharField(max_length=200, blank=True)
    
    # 第一学历 - 起始时间
    first_edu_start_year = models.IntegerField(choices=year_choices)
    first_edu_start_month = models.IntegerField(choices=month_choices)
    # 第一学历 - 结束时间
    first_edu_end_year = models.IntegerField(choices=year_choices)
    first_edu_end_month = models.IntegerField(choices=month_choices)
    # 第一学历 - 学位
    first_edu_degree = models.CharField(
        max_length=100, choices=((u'学士',)*2, (u'无',)*2))
    # 第一学历 - 学历
    first_edu_bkgrd = models.CharField(
        max_length=100, choices=((u'专科',)*2, (u'本科',)*2, (u'无',)*2))
    # 第一学历 - 毕业院校
    first_edu_university = models.CharField(max_length=200)
    # 第一学历 - 所学专业
    first_edu_major = models.CharField(max_length=200)
    
    # 最高学历 - 起始时间
    high_edu_start_year = models.IntegerField(choices=year_choices)
    high_edu_start_month = models.IntegerField(choices=month_choices)
    # 最高学历 - 结束时间
    high_edu_edu_year = models.IntegerField(choices=year_choices)
    high_edu_edu_month = models.IntegerField(choices=month_choices)
    # 最高学历 - 学位
    high_edu_degree = models.CharField(
        max_length=100, choices=((u'学士',)*2, (u'硕士',)*2, (u'博士',)*2))
    # 最高学历 - 学历
    high_edu_bkgrd = models.CharField(
        max_length=100, choices=((u'本科',)*2, (u'硕士研究生',)*2, (u'博士研究生',)*2))
    # 最高学历 - 毕业院校
    high_edu_university = models.CharField(max_length=200)
    # 最高学历 - 所学专业
    high_edu_major = models.CharField(max_length=200)
    
    # 计算机等级
    compute_level = models.CharField(max_length=200)
    # 是否蒙汉兼通
    is_han_mongolia_both = models.CharField(
        max_length=1, choices=((u'是',)*2, (u'否',)*2), blank=True)
    # 是否服务基层项目人员
    is_basic_attendant =  models.CharField(
        max_length=1, choices=((u'是',)*2, (u'否',)*2), blank=True)
    # 个人特长及奖惩情况
    special_skill = models.TextField(blank=True, help_text=u'个人特长及奖惩情况')
    # 照片路径
    avatar = models.CharField(max_length=255, help_text=u'照片路径')
    # 审核进度
    audit_step = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True, help_text=u'0:未审核 1:通过初审 7:未过初审 8:不合格')
    
    test_paper_language = models.CharField(
        max_length=10, choices=((u'汉文',)*2, (u'蒙文',)*2), 
        help_text=u'初试选择何种文字作答')
    
    # 其他学习经历 - 起始时间
    other_edu_start_year = models.IntegerField(blank=True, null=True, choices=year_choices)
    other_edu_start_month = models.IntegerField(blank=True, null=True, choices=month_choices)
    # 其他学习经历 - 结束时间
    other_edu_edu_year = models.IntegerField(blank=True, null=True, choices=year_choices)
    other_edu_edu_month = models.IntegerField(blank=True, null=True, choices=month_choices)
    # 其他学习经历 - 学习单位
    other_edu_unit = models.CharField(max_length=100, blank=True)
    # 其他学习经历 - 所学专业
    other_edu_major = models.CharField(max_length=100, blank=True)
    # 其他学习经历 - 学历
    other_edu_bkgrd = models.CharField(
        max_length=200, blank=True, 
        choices=((u'专科',)*2, (u'本科',)*2, (u'硕士研究生',)*2, 
                 (u'博士研究生',)*2, (u'无',)*2))
    # 其他学习经历 - 学位
    other_edu_degree = models.CharField(
        max_length=200, blank=True, 
        choices=((u'学士',)*2, (u'硕士',)*2, (u'博士',)*2))
    # 其他学习经历 - 学习形式
    other_edu_type = models.CharField(
        max_length=100, blank=True, 
        choices=((u'全日制教育',)*2, (u'在职教育',)*2, 
                 (u'博士后',)*2, (u'其他',)*2))

    # 其他学习经历 - 起始时间
    other_edu_start_year_2 = models.IntegerField(blank=True, null=True, choices=year_choices)
    other_edu_start_month_2 = models.IntegerField(blank=True, null=True, choices=month_choices)
    # 其他学习经历 - 结束时间
    other_edu_edu_year_2 = models.IntegerField(blank=True, null=True, choices=year_choices)
    other_edu_edu_month_2 = models.IntegerField(blank=True, null=True, choices=month_choices)
    # 其他学习经历 - 学习单位
    other_edu_unit_2 = models.CharField(max_length=100, blank=True)
    # 其他学习经历 - 所学专业
    other_edu_major_2 = models.CharField(max_length=100, blank=True)
    # 其他学习经历 - 学历
    other_edu_bkgrd_2 = models.CharField(
        max_length=200, blank=True, 
        choices=((u'专科',)*2, (u'本科',)*2, (u'硕士研究生',)*2, 
                 (u'博士研究生',)*2, (u'无',)*2))
    # 其他学习经历 - 学位
    other_edu_degree_2 = models.CharField(
        max_length=200, blank=True, 
        choices=((u'学士',)*2, (u'硕士',)*2, (u'博士',)*2))
    # 其他学习经历 - 学习形式
    other_edu_type_2 = models.CharField(
        max_length=100, blank=True, 
        choices=((u'全日制教育',)*2, (u'在职教育',)*2, 
                 (u'博士后',)*2, (u'其他',)*2))

    create_at = models.DateTimeField(auto_now_add = True)
    last_edit_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.name


class PeopleExtra(models.Model):
    people = models.OneToOneField(People)
    audit_step = models.PositiveSmallIntegerField(
        default=0, blank=True, null=True,  
        help_text=u'0:未审核 1:通过初审 7:未过初审 8:不合格')
    reason = models.TextField(blank=True)
    ticket_number = models.CharField(max_length=8)
    exam_room = models.CharField(max_length=2)
    seat = models.CharField(max_length=2)
    create_at = models.DateTimeField(auto_now_add = True)
    last_edit_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return self.people.name

