## -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.http import HttpResponse,HttpResponseForbidden
# from fields import RelatedForeignKey
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

class GROUP(models.Model):
    id   = models.AutoField('id',primary_key=True)
    username  = models.CharField('用户名称', blank=True, max_length=30, editable=False)
    user_school = models.CharField('用户学院', blank=True, max_length=60, editable=False)
    """docstring for User"""
    def __unicode__(self):
        return u"%s" %(self.username)
    class Meta:
        db_table = 'my_user_group'
        verbose_name = '用户权限表'

class STU_INFO(models.Model):
    """docstring for STU_INFO"""
    id   = models.AutoField('id',primary_key=True)
    STU_ID = models.CharField('学号', blank=True, max_length=30, editable=False)
    STU_TYPE = models.CharField('学生类型', blank=True, max_length=30, editable=False)
    STU_SEX = models.CharField('学生类型', blank=True, max_length=30, editable=False)
    INST_CH = models.CharField('所属院系', blank=True, max_length=40, editable=False)
    STU_GRA = models.CharField('所属年级', blank=True, max_length=40, editable=False)
    score = models.CharField('学生得分', blank=True, max_length=30, editable=False)
    def __unicode__(self):
        return self.STU_NAME 
    class Meta:
        db_table= 'stu_info'
        verbose_name = '学生基本信息表'

class LEND_INFO(models.Model):
    """docstring for LEND_INFO"""
    id   = models.AutoField('id',primary_key=True)
    STU_ID = models.CharField('学号', blank=True, max_length=30, editable=False)
    DATA_DT = models.CharField('数据更新日期', blank=True, max_length=30, editable=False)
    LEND_DATE = models.CharField('借书日期', blank=True, max_length=30, editable=False)
    RET_DATE = models.CharField('还书日期', blank=True, max_length=30, editable=False)
    M_TITLE = models.CharField('图书标题', blank=True, max_length=100, editable=False)
    M_CLASS = models.CharField('图书类型', blank=True, max_length=20, editable=False)
    def __unicode__(self):
        return self.M_TITLE 
    class Meta:
        db_table= 'lend_info'
        verbose_name = '学生借书信息表'
