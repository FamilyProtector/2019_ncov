#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
	问:为什么红十字会接受了社会捐赠大量物资，而医院还是缺物资？
	答:一个重要原因就是消耗量大于供应。
	   二捐赠物资和急需物资，品种、型号、标准不是很好地对应。
	   三还有周转不够快，调拨不及时等，这些都是我们需要在工作中不断加以改进的。

	个人理解的是第三有部分也是因二导致的。
	
	ref:
		[0][python爬取《我和我的祖国》豆瓣短评并做词云展示](https://zhuanlan.zhihu.com/p/85051008)
		[1][jieba库及wordcloud库的使用](https://www.cnblogs.com/wyb666/p/9119538.html)
		[2][基于jieba动态加载字典和调整词频的电子病历分词-git专业词库](https://www.cnblogs.com/Luv-GEM/p/10534713.html)
'''

__author__	= 'FamilyProtector'
__version__	= 'v0.0.1'
__date__	= '2020.02.02'



import logging
logging.basicConfig(
        level = logging.INFO,      #不需要输出时改为INFO/DEBUG                   
        format = '%(asctime)s %(filename)s[line:%(lineno)d] %(message)s'
        )

import random,os,re,sys,codecs
import time
import requests
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np
#np.set_option('max_colwidth',500)

import jieba
import jieba.analyse
from wordcloud import WordCloud
from imageio import imread
import base64

#添加个修饰类,Func开始、结束。
self_font_path	= 'C:/Windows/Fonts/msyh.ttc'
word_cloud_path	= ''.join(('mpr_',time.strftime('%Y-%m-%d-%a-%H%M%S',time.localtime(time.time())),'.png'))
self_pic_path	= 'ChinaMap.jpg'


def word_seg(src_path='MRP_Analysis_2.txt', self_dict_path='self_dict.txt'):
	
	#以只读模式打开需求文档
	txt = ''
	with open(src_path,'r',encoding='utf-8') as f:		
		txt = f.read()
		f.close()
	logging.debug('---------File read done---------!')
	logging.debug(txt)
	
	#结巴分词
	wordstr=''
	try:
	
		try:
			jieba.load_userdict(self_dict_path)
		except FileNotFoundError:
			pass
		except Exception as e:
			raise e
		
		jieba.add_word('拜欧海多汀', freq = 20000, tag = None)
		jieba.suggest_freq(('护', '将'), tune = True)						
	
		#cut返回的是生成器，lcut返回的是列表.选择精准模式，关闭HMM模式，返回一个list.
		words = jieba.lcut(txt, cut_all=False, HMM=False)
		logging.debug(words)
		wordstr = ''.join(words)												
		logging.debug(wordstr)
		
	except Exception as e:
		raise e
	
	return wordstr

def word_count():
	
	pass

	
def word_cloud(wordstr):
	
	try:	
		mask = None
		try:
			mask =imread(self_pic_path)
		except FileNotFoundError:
			pass
		except Exception as e:
			raise e
		
		
		excludes = {'你好','另外','\n','\t'}								#排除词列表，剔除无效词语 #省疾控中心
		#对词云图参数进行设置,以 wordstr 文本生成词云
		wordcloud = WordCloud(background_color="white",						
							  width=800,									
							  height=600,									
							  font_path=self_font_path,						#指定微软雅黑的路径，不设置会中文显示异常
							  max_words=1000,								#词云中最大词数
							  max_font_size=150,							#词云中最大的字体号数
							  random_state=200,								#设置有多少种配色方案
							  mask=mask,									#指定词云背景图
							  stopwords = excludes,							#被排除的词
							  ).generate(wordstr)
		wordcloud.to_file(word_cloud_path)
		
		
		plt.imshow(wordcloud)
		plt.axis("off")
		plt.show()
		
	except Exception as e :
		raise e

def png2base64str(png_path):
	imgdata =''
	with open(png_path,'rb') as f:
		imgdata=base64.b64encode(f.read()) 
		f.close()
	print(imgdata)
	return imgdata

def base642png(png_path):
	bs='iVBORw0KGgoAAAANSUhEUg....' 
	imgdata=base64.b64decode(bs)
	with open(png_path,'wb') as f:
		f.write(imgdata)
		f.close()

		
def main():
	logging.info('Begining...')
	try:
		word_cloud(word_seg(sys.argv[1]))
	except IndexError:
		logging.info('请输入你的源文件路径~')
	except Exception as e:
		raise
	logging.info('欢迎更新')


if __name__ == '__main__':
	
	main()
	
	
	
	