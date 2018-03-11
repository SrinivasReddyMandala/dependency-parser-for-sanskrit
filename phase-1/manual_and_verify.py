
# -------------------------------------- libraries --------------------------------------------
# !/usr/local/bin/python
# coding: utf-8
from os import walk
import random
import pickle
import copy as cpy
import operator
# import csv
import networkx as nx
# import numpy as np
# from scipy.sparse import *
# from scipy import *
# import matplotlib.pyplot as plt
import sys,codecs,re
sys.path.append('../')
reload(sys);
sys.setdefaultencoding("utf8")
import sys,codecs,re
sys.path.append('../')
# import pandas
# import numpy as np

# This Python file uses the following encoding: utf-8

# --------------------------------------- paths -----------------------------------------------

save_path="stats/"
sent_path="test/1/"
new_sent_path="other/"
under_path='under_sent/'

# -------------------------------- class definitions ------------------------------------------
class gold_sent(object):
	"""docstring for gold_sent"""
	def __init__(self, sent_id,string_form, content_list):
		super(gold_sent, self).__init__()
		self.sent_id = sent_id
		self.string_form = string_form
		self.content_list = content_list  
		# list of gold words
		pass
	def print_gold(self):
		print "Sentence ID : " + str(self.sent_id)
		print "String : " + str(self.string_form)
		for cur_word in self.content_list:
			cur_word.print_gold()
			pass
		pass
	pass

class gold_word(object):
	"""docstring for gold_word"""
	def __init__(self, name, POS, dep_tag, from_tag, to_tag):
		super(gold_word, self).__init__()
		self.name = name
		self.POS = POS
		self.dep_tag = dep_tag
		self.from_tag = from_tag
		self.to_tag = to_tag
		pass
	def print_gold(self):
		# global possible_dep_tag
		# if (self.dep_tag in possible_dep_tag) or (self.dep_tag==None):
		# 	return
		# 	pass
		print "Word : " + str(self.name)
		print "POS : " + str(self.POS)
		print "dep_tag : "+str(self.dep_tag)
		print "from_tag : " + str(self.from_tag)
		print "to_tag : " + str(self.to_tag)
		pass
	pass

class sentences:
	def __init__(self,sent_id,sentence):
		self.sent_id=sent_id
		self.sentence=sentence
		self.chunk=[]
		pass
	def print_sents(self):
		print "sent_id :" + str(self.sent_id)
		print "sentence :" + str(self.sentence)
		print "Chunks : "
		print "N_of chunks :" + str(len(self.chunk))
		for cur_chunk in self.chunk:
			cur_chunk.print_chunk()
			pass
		pass
	pass

class words:
	def __init__(self,main_word,word_length,offset,starting_posn,max_line):
		self.main_word=main_word
		self.word_length=word_length
		self.offset=offset
		self.starting_posn=starting_posn
		self.max_line=max_line
		pass
	def print_word(self):
		print "main word :" + str(self.main_word)
		print "word length :" + str(self.word_length)
		print "offset :" + str(self.offset)
		print "starting_posn :" + str(self.starting_posn)
		print "max_line :" + str(self.max_line)
		pass

class segments:
	def __init__(self,uper_word,colspan,line_num,own_word,offset,prob,own_seg,lemma,links):
		self.uper_word=uper_word
		self.colspan=colspan
		self.line_num=line_num
		self.own_word=own_word
		self.offset=offset 
		self.prob=prob
		self.own_seg=own_seg
		self.lemma=lemma
		self.links=links
		pass

class word_new:
	def __init__(self,names,lemmas,urls,forms):
		self.names=names
		self.lemmas=lemmas
		self.urls=urls
		self.forms=forms
		pass
	def print_word_new(self):
		print "word starts >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
		print "names :" + str(self.names)
		print "lemmas :" + str(self.lemmas)
		print "urls :" + str(self.urls)
		print "forms :" + str(self.forms)
		print "word complete >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
		pass

class chunks:
	def __init__(self,chunk_name):
		self.chunk_name=chunk_name
		self.chunk_words={}
		pass
	def print_chunk(self):
		print "chunk_name :" + str(self.chunk_name.encode('utf-8'))
		# print utf_to_ascii(self.chunk_name)
		# print "chunk keys :" + str(self.chunk_words.keys())
		sorted_keys=self.chunk_words.keys()
		sorted_keys.sort()
		print sorted_keys
		print "chunk starts $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		for cur_key in sorted_keys :
			print "word_list starts @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
			print "key is " + str(cur_key)
			for cur_word in self.chunk_words[cur_key] :
				# print cur_word.__class__.__name__
				print str(cur_word.print_word_new())
			print "word_list ends @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
		print "chunk ends $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
		pass

class word_definite:
	def __init__(self,derived, lemma, cng, pos, chunk_id):
		self.lemma = lemma
		self.derived = derived
		self.cng = str(cng)
		self.tup = "{}_{}".format(self.lemma, self.cng)
		self.pos = pos
		self.chunk_id = chunk_id        
		# Fields Required for heap
		self.dist = np.inf
		self.src = -1
		self.id = -1
		self.isConflicted = False
	def __str__(self):
		return 'WD_Node[C: %d, P: %d, %s @(%s) => %s]' %(self.chunk_id, self.pos, self.lemma, self.cng, self.derived)
	def __repr__(self):
		return str(self)
# -------------------------------- global variables -------------------------------------------
# sandhi_dict=pickle.load(open( "sandhi_dict.p" , 'rb'))
# word_null_dict=pickle.load(open( "word_null_dict.p" , 'rb'))
gold_sentence_list=pickle.load( open( "support/gold_sentence_list.p", "rb" ) )
dcs_lemmas_count_dict=pickle.load( open( "support/dcs_lemmas_count_dict.p", "rb" ) )
dcs_words_count_dict=pickle.load( open( "support/dcs_words_count_dict.p", "rb" ) )
slp_under_list=[]
word_lemma_error_list=[]
# -------------------------------- load required pickles --------------------------------------

# -------------------------------- previous functions -----------------------------------------


def is_verb(cur_form):
	sec_v_list = [ "ou" , "pp." , "ppa." , "pfp." , "inf." , "abs."]
	main_v_list = ["pr. ps." , "imp. ps." , "impft. ps." , "aor. ps." , "opt. ps." , "fut. ac." , "fut. ps." , "cond. ac." , "cond.ps." , "per. fut. ac." , "per. fut. ps." , "aor. [1] ac." , "aor. [1] ps." , "aor. [2] ac." , "aor. [2] ps." , "aor. [3] ac." , "aor. [3] ps." , "aor. [4] ac." , "aor. [4] ps." , "aor. [5] ac." , "aor. [5] ps." , "aor. [7] ac." , "aor. [7] ps." , "pft. ac." , "per. pft."]+["pr." , "opt." , "imp." , "impft."]
	dummy_v_list=['ppr','pfu','int','des','inj','opt','pft','ppr','pr','impft','imp','fut','cond','per','aor','ben','ca' ,'pp','pfp','inf','abs']
	# n_sec
	for cur_sec in sec_v_list+dummy_v_list:
		if cur_sec in str(cur_form) :
			return True
			pass
		pass
	# n_main
	for cur_main in main_v_list:
		if cur_main in str(cur_form):
			return True
			pass
	return False
	pass

def splitTillPeriod(config,listInput): #see that config is not empty and is of type string
	#returns config sans first part and firstpart is appended to listInput
	
	configList=list(config)
	out=''
	periodIndex=0
	val=''
	for i,val in enumerate(configList):
	   a=2
	   periodIndex=i
	   if val=='.':
		break
	   if val!=" ": 
		   out=out+val; 
	if val!=".":
		config1=" ".join(config.split())
		listInput.append(config1)
		return ""
	else:	
		config1="".join(configList[(periodIndex+1):])
		listInput.append(out)
		return config1
		pass
	pass

def wordTypeCheck(config):
	#if it is noun Im assuming it has 3 parts
	#form is noun or verb or...
	form=None
	# print(form, config)
	
	nounMapping={28:	'xt?',  29:	'Nom. sg. masc.',  30:	'Nom. sg. fem.',  31:	'Nom. sg. neutr.',  32:	'Nom. sg. adj.',  33:	'xt?',  34:	'Nom. du. masc.',  35:	'Nom. du. fem.',  36:	'Nom. du. neutr.',  37:	'Nom. du. adj.',  38:	'xt?',  39:	'Nom. pl. masc.',  40:	'Nom. pl. fem.',  41:	'Nom. pl. neutr.',  42:	'Nom. pl. adj.',  48:	'xt?',  49:	'Voc. sg. masc.',  50:	'Voc. sg. fem.',  51:	'Voc. sg. neutr.',  54:	'Voc. du. masc.',  55:	'Voc. du. fem.',  56:	'Voc. du. neutr.',  58:	'xt?',  59:	'Voc. pl. masc.',  60:	'Voc. pl. fem.',  61:	'Voc. pl. neutr.',  68:	'xt?',  69:	'Acc. sg. masc.',  70:	'Acc. sg. fem.',  71:	'Acc. sg. neutr.',  72:	'Acc. sg. adj.',  73:	'xt?',  74:	'Acc. du. masc.',  75:	'Acc. du. fem.',  76:	'Acc. du. neutr.',  77:	'Acc. du. adj.',  78:	'xt?',  79:	'Acc. pl. masc.',  80:	'Acc. pl. fem.',  81:	'Acc. pl. neutr.',  82:	'Acc. pl. adj.',  88:	'xt?',  89:	'Instr. sg. masc.',  90:	'Instr. sg. fem.',  91:	'Instr. sg. neutr.',  92:	'Instr. sg. adj.',  93:	'xt?',  94:	'Instr. du. masc.',  95:	'Instr. du. fem.',  96:	'Instr. du. neutr.',  97:	'Instr. du. adj.',  98:	'xt?',  99:	'Instr. pl. masc.',  100:	'Instr. pl. fem.',  101:	'Instr. pl. neutr.',  102:	'Instr. pl. adj.',  108:	'xt?',  109:	'Dat. sg. masc.',  110:	'Dat. sg. fem.',  111:	'Dat. sg. neutr.',  112:	'Dat. sg. adj.',  114:	'Dat. du. masc.',  115:	'Dat. du. fem.',  116:	'Dat. du. neutr.',  117:	'Dat. du. adj.',  118:	'xt?',  119:	'Dat. pl. masc.',  120:	'Dat. pl. fem.',  121:	'Dat. pl. neutr.',  122:	'Dat. pl. adj.',  128:	'xt?',  129:	'Abl. sg. masc.',  130:	'Abl. sg. fem.',  131:	'Abl. sg. neutr.',  132:	'Abl. sg. adj.',  134:	'Abl. du. masc.',  135:	'Abl. du. fem.',  136:	'Abl. du. neutr.',  137:	'Abl. du. adj.',  138:	'xt?',  139:	'Abl. pl. masc.',  140:	'Abl. pl. fem.',  141:	'Abl. pl. neutr.',  142:	'Abl. pl. adj.',  148:	'xt?',  149:	'Gen. sg. masc.',  150:	'Gen. sg. fem.',  151:	'Gen. sg. neutr.',  152:	'Gen. sg. adj.',  153:	'xt?',  154:	'Gen. du. masc.',  155:	'Gen. du. fem.',  156:	'Gen. du. neutr.',  157:	'Gen. du. adj.',  158:	'xt?',  159:	'Gen. pl. masc.',  160:	'Gen. pl. fem.',  161:	'Gen. pl. neutr.',  162:	'Gen. pl. adj.',  168:	'xt?',  169:	'Loc. sg. masc.',  170:	'Loc. sg. fem.',  171:	'Loc. sg. neutr.',  172:	'Loc. sg. adj.',  173:	'xt?',  174:	'Loc. du. masc.',  175:	'Loc. du. fem.',  176:	'Loc. du. neutr.',  177:	'Loc. du. adj.',  178:	'xt?',  179:	'Loc. pl. masc.',  180:	'Loc. pl. fem.',  181:	'Loc. pl. neutr.',  182:	'Loc. pl. adj.',  }
	verbMapping1={1: 'pr. [*] ac.', 2: 'opt. [*] ac.', 3: 'imp. [*] ac', 4: 'impft. [*] ac.', 5: 'fut. ac/ps.', 6: 'cond. ac/ps.', 7: 'per. fut. ac/ps.', 8: 'aor. [1] ac/ps.', 9: 'aor. [2] ac/ps.', 10: 'aor. [3] ac/ps.', 11: 'aor. [4] ac/ps.', 12: 'aor. [5] ac/ps.', 13: 'aor. [7] ac/ps.', 14: 'ben. ac/ps.', 15: 'pft. ac.', 16: 'per. pft.', 19: 'pp.', 20: 'ppa.', 21: 'pfp.', 22: 'inf.', 23: 'abs.', 24: 'pr. ps.', 26: 'imp. ps.', 27: 'impft. ps.', 28: 'aor. ps.', 29: 'opt. ps.', 30: 'ou', }
	verbMapping2={1: 'sg. 1', 2: 'sg. 2', 3: 'sg. 3', 4: 'du. 1', 5: 'du. 2', 6: 'du. 3', 7: 'pl. 1', 8: 'pl. 2', 9: 'pl. 3', }

	indeclinable_list=['part.' , 'conj.' , 'abs.' , 'prep.' , 'ind.' , 'ca. abs.' ]
	if form == None :
		for cur_ind in indeclinable_list:
			if cur_ind in config:
				form='indeclinable'
				pass
			pass
		pass
	if form == None:
		if ('iic.' in config) or ('iiv.' in config):
			form = 'compound'
		pass
	if form == None:
		if ('adv' in str(config)) or ('adv.' in config) or ('und.' in config) or ('tasil' in config) :
			form ="undetermined"
			pass
		pass
	if form == None:
		if is_verb(config):
			form='verb'
			pass
		pass
	noun_start=['g' , 'i', 'nom' , 'voc' , 'acc' , 'inst' , 'dat' , 'abl' , 'gen' , 'loc']
	if config.split(".")[0].strip() in noun_start :
		form ='noun'
		pass
	if form=='indeclinable':
		if config=='part.':
			return 2
		elif config=='conj.':
			return 2
		elif config=='abs.':
			return -230
		elif config=='prep.':
			return 2
		elif config=='ind.':
			return 2
		elif config=='ca. abs.':
			return -230
		else:
			return 'config is invalid'
		
	elif form=='compound':
		if config=='iic.':
			return 3
		elif config=='iiv.':
			return 3
		else:
			return 'config is invalid'
		
	elif form=='undetermined':
		if config=='adv.':
			return 2
		elif config=='und.':
			return 1
		elif config=='tasil':
			return 1
		else:
			return 'config is invalid'
	
	elif form=='noun':
		# print("entered noun")
		config1=config
		x=[]
		config1=splitTillPeriod(config1,x)
		one=x[0]
		x=[]
		config1=splitTillPeriod(config1,x)
		two=x[0]
		x=[]
		config1=splitTillPeriod(config1,x)
		three=x[0]
		
		isAdj=0
		if three=='*':
			three='n'
			isAdj=1
			
		for i in nounMapping.keys():
			if one!='i'and one!='g':
				if one[len(one)-2:] in nounMapping[i]:
					if two in nounMapping[i]:
					
						if three in nounMapping[i]:
							if(isAdj==0):
							  return i  
							else:
								return i+1
									  
			   
			elif one=='i':
				 if 'Instr' in nounMapping[i]:
					if two in nounMapping[i]:
									   
					  if three=='n':
						if 'neutr' in nounMapping[i]:
							 if(isAdj==0):
							  return i  
							 else:
								return i+1
					
					  elif three in nounMapping[i]:
						   return i 
			elif one=='g':
				if 'Gen' in nounMapping[i]:
				   if two in nounMapping[i]:
									   
					  if three=='n':
						if 'neutr' in nounMapping[i]:
							 if(isAdj==0):
							  return i  
							 else:
								return i+1
					
					  elif three in nounMapping[i]:
								return i 
		
	elif form=='verb':
		unit=0
		ten=0
		#to remove ca des int
		x=[]
		configActual=config
		config=splitTillPeriod(config,x)
		if(x[0]=='ca' or x[0]=='des' or x[0]=='int'):
			y=2 #do nothing
		else:
			config=configActual
		#if [vn.] is present
		if 'vn.' in config:
			config=config.replace('vn.','')	   
		
		x=[]
		config=splitTillPeriod(config,x)
		
		one=x[0]
		two=''
		three=''
		ONE=''
		TWO=''
		
		if config!='':
			x=[]
			config=splitTillPeriod(config,x)
			temp=x[0]
			if temp!='sg'and temp!='pl' and temp!='du':
				two=temp
			else:
				ONE=temp
		 
		if config!='':
			x=[]
			config=splitTillPeriod(config,x)
			temp=x[0]
			print
			if temp!='sg'and temp!='pl' and temp!='du':
				if ONE=='':
					three=temp
			elif ONE!='':
				TWO=temp
			else:
				ONE=temp
		if config!='':
			x=[]
			config=splitTillPeriod(config,x)
			temp=x[0]
			if temp=='sg'or temp=='pl' or temp=='du':
				ONE=temp
			elif temp=='1'or temp=='2' or temp=='3':
				TWO=temp
		
		if config!='':
			x=[]
			config=splitTillPeriod(config,x)
			temp=x[0]	   
			if temp=='1'or temp=='2' or temp=='3':
				TWO=temp  
		
		for i in verbMapping2.keys():
			if ONE!='':
				if ONE in verbMapping2[i] and TWO in verbMapping2[i]:
				   unit=i
				   break
				
		if one=='pp':
			ten=19
		if one=='ppa':
			ten=20
		if one=='pfp':
			ten=21 
		if one=='inf':
			ten=22
		if one=='abs':
			ten=23
		if one=='inj':
			ten=30
			
		if one=='pr' or one=='ppr':
			if two=='ps':
				ten=24
			else :
				ten=24
		if one=='imp':
			if two=='ps':
				ten=26
		if one=='impft':
			if two=='ps':
				ten=27
		if one=='aor':
			if two=='ps':
				ten=28
		if one=='opt':
			if two=='ps':
				ten=29  
				
		if one=='pr'or one=='ppr':
			if 'ac' in two or 'md' in two:
				ten=1
		if one=='opt':
			if 'ac' in two or 'md' in two:
				ten=2		
		if one=='imp':
			if 'ac' in two or 'md' in two:
				ten=3
		if one=='impft':
			if 'ac' in two or 'md' in two:
				ten=4
		if one=='pft' or one=='ppf':
			if 'ac' in two or 'md' in two:
				ten=15
			else :
				ten=15
			 
		if one=='per':
			if two=='pft':
				ten=16
				
		
		if one=='fut' or one=='pfu':
			if 'ac' in two or 'ps' in two or 'md' in two:
				ten=5
		if one=='cond':
			if 'ac' in two or 'ps' in two or 'md' in two:
				ten=6
		if one=='ben':
			if 'ac' in two or 'ps' in two or 'md' in two:
				ten=14		
		
		if one=='aor':
			if 'ac' in two or 'ps' in two or 'md' in two:
				if '1' in two:
					ten=8
				if '2' in two:
					ten=9
				if '3' in two:
					ten=10 
				if '4' in two:
					ten=11
				if '5' in two or '6' in two:
					ten=12
				if '7' in two:
					ten=13	
		
		if one=='per':
			if two=='fut':
				if (('ac' in three) or ('ps' in three) or 'md' in three):
					ten=7
					
		if ten!=0:
			output=-1*(ten*10+unit)
			return output
		else:
			x=3
		
	else:
		return None
		pass
	pass

def is_int(s):
    try: 
        int(s)
        return True
    except :
        return False

def utf_to_ascii(a):
    # coding: utf-8 
    double_dict={}
    f=open('roman/rom2.txt','r')
    for lines in f.readlines():
            words=lines.split(',')
            words[1]=words[1].replace('\n','')
            double_dict[words[0]]=words[1]
    f.close()
    single_dict={}
    q=open('roman/rom.txt','r')
    for lines in q.readlines():
            words=lines.split(',')
            words[1]=words[1].replace('\n','')
            single_dict[words[0]]=words[1]
    q.close()
    
    for elem in double_dict:
        if elem in a:
            a=a.replace(elem,double_dict[elem])
    for elem in single_dict:
        if elem in a:
            a=a.replace(elem,single_dict[elem])
    return(a)
    pass

def is_lemma_in_slp(cur_lemma):
	for cur_char in cur_lemma:
		if not cur_char.isalpha():
			return False
			pass
		pass
	return True
	pass

def get_done_file_list(sent_path):
	f = []
	done_list=[]
	for (useless1, useless2, filenames) in walk(sent_path):
		f.extend(filenames)
		break
	for cur_file in f:
		cur_file_index=int(cur_file.split('.')[0])
		done_list.append(cur_file_index)
		pass
	done_list.sort()
	# print done_list
	# exit(0)
	return done_list
	pass

def get_gold_sent(cur_sent_id):
	global gold_sentence_list
	for cur_sent in gold_sentence_list:
		if cur_sent.sent_id == cur_sent_id:
			return cur_sent
			pass
		pass
	pass

def get_underscore():
	# cur_text_file = open('uniquesentences.txt','r')
	# un_jumble=pickle.load(open( "un_jumble.p" , 'rb'))
	# sentence_list=cur_text_file.readlines()
	file_list=get_done_file_list()
	# error_list={}
	# underscore_dict=pickle.load( open( "underscore_dict.p", "rb" ) )
	# file_list=range(1,1000)
	under_list=[]
	for cur_file_index in file_list:
		# sentence_string= sentence_list[cur_file_index-1]
		cur_file=pickle.load( open( "new/" + str(cur_file_index) + ".p", "rb" ) )
		# cur_chunk_list=[]
		# local_temp=[]
		for cur_index in range(len(cur_file.chunk)):
			cur_chunk=cur_file.chunk[cur_index]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if ('_' in slp_chunk_name):
				slp_chunk_name=slp_chunk_name.strip()
				temp_list=slp_chunk_name.split("_")
				under_list+=temp_list
				pass
			pass
		pass
	under_list=list(set(under_list))
	print under_list
	pass

def set_underscore():
	# cur_text_file = open('uniquesentences.txt','r')
	# un_jumble=pickle.load(open( "un_jumble.p" , 'rb'))
	# sentence_list=cur_text_file.readlines()
	file_list=get_done_file_list()
	error_list={}
	underscore_dict=pickle.load( open( "underscore_dict.p", "rb" ) )
	null_underscore_dict=pickle.load( open( "null_underscore_dict.p", "rb" ) )
	# file_list=range(1,1000)
	for cur_file_index in file_list:
		# sentence_string= sentence_list[cur_file_index-1]
		cur_file=pickle.load( open( "new/" + str(cur_file_index) + ".p", "rb" ) )
		# cur_un_jumble=un_jumble[cur_file_index]
		# print cur_un_jumble
		cur_chunk_list=[]
		local_temp=[]
		for cur_index in range(len(cur_file.chunk)):
			cur_chunk=cur_file.chunk[cur_index]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if ('_' in slp_chunk_name):
				# print slp_chunk_name
				under_data=slp_chunk_name.strip().split("_")
				temp_list=[]
				for cur_word in under_data:
					if cur_word in underscore_dict.keys():
						local_chunk=underscore_dict[cur_word]
						temp_list.append(local_chunk)
						pass
					elif cur_word in null_underscore_dict.keys():
						local_chunk=null_underscore_dict[cur_word]
						temp_list.append(local_chunk)
						pass
					pass
				# new ch_list -> new[:]+[]+new[:]
				if len(temp_list)!=len(under_data):
					local_temp.append(slp_chunk_name)
					my_chunk=copy.deepcopy(cur_file.chunk)
					cur_chunk_list.append(my_chunk)				
					pass
				else :
					cur_chunk_list+=temp_list
					pass
				pass
			else :
				my_chunk=copy.deepcopy(cur_file.chunk)
				cur_chunk_list.append(my_chunk)
				pass
			pass
		cur_chunk=cur_chunk_list
		if local_temp!=[]:
			error_list[cur_file_index]=local_temp
			pass
		pickle.dump( cur_file, open(new_sent_path + str(cur_file_index)+'.p', "wb" ))
		pass
	print error_list
	pass

def my_tester():
	cur_file_index=1
	cur_file=pickle.load( open( "new/" + str(cur_file_index) + ".p", "rb" ) )
	cur_file.print_sents()
	exit()
	pass

def get_null_words():
	file_list=get_done_file_list()
	error_list={}
	# file_list=[1,2,3,4]
	for cur_file_index in file_list:
		cur_file=pickle.load( open( "new/" + str(cur_file_index) + ".p", "rb" ) )
		local_temp=[]
		for cur_chunk in cur_file.chunk:
			sorted_keys=cur_chunk.chunk_words.keys()
			sorted_keys.sort()
			cur_word=cur_chunk.chunk_words[sorted_keys[0]]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if '_' in slp_chunk_name:
				continue
				pass
			if cur_word[0].lemmas==[]:
				local_temp.append(slp_chunk_name)
				continue
				pass
			pass
		if local_temp!=[]:
			error_list[cur_file_index]=local_temp
			pass
		pass
	print error_list
	pass

def get_underscore_dict():
	file_list=range(1,1437)
	error_list=[]
	# underscore_dict={}
	underscore_dict=pickle.load( open( "underscore_dict.p", "rb" ) )
	null_underscore_dict={}
	# file_list=[1,2,3,4]
	for cur_file_index in file_list:
		cur_file=pickle.load( open( "words/" + str(cur_file_index) + ".p", "rb" ) )
		for cur_chunk in cur_file.chunk:
			sorted_keys=cur_chunk.chunk_words.keys()
			sorted_keys.sort()
			cur_word=cur_chunk.chunk_words[sorted_keys[0]]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if cur_word[0].lemmas==[]:
				error_list.append(slp_chunk_name)
				null_underscore_dict[slp_chunk_name]=copy.deepcopy(cur_chunk)
				continue
				pass
			underscore_dict[slp_chunk_name]=copy.deepcopy(cur_chunk)
			pass
		pass
	pickle.dump(underscore_dict,open('underscore_dict.p' , 'w'))
	pickle.dump(null_underscore_dict,open('null_underscore_dict.p' , 'w'))	
	print error_list
	pass

def get_null_compounds():
	file_list=get_done_file_list()
	error_list=[]
	# file_list=[1,2,3,4]
	for cur_file_index in file_list:
		cur_file=pickle.load( open( "new/" + str(cur_file_index) + ".p", "rb" ) )
		local_temp=[]
		for cur_chunk in cur_file.chunk:
			sorted_keys=cur_chunk.chunk_words.keys()
			sorted_keys.sort()
			cur_word=cur_chunk.chunk_words[sorted_keys[0]]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if (cur_word[0].lemmas==[]) and ('-' in slp_chunk_name):
				local_temp.append(slp_chunk_name)
				continue
				pass
			pass
		if local_temp!=[]:
			error_list+=local_temp
			pass
		pass
	print error_list
	pass

def get_compound_dict():
	file_list=range(1,57)
	error_list=[]
	compound_dict={}
	null_compound_dict={}
	# file_list=[1,2,3,4]
	for cur_file_index in file_list:
		cur_file=pickle.load( open( "compounds/" + str(cur_file_index) + ".p", "rb" ) )
		for cur_chunk in cur_file.chunk:
			sorted_keys=cur_chunk.chunk_words.keys()
			sorted_keys.sort()
			cur_word=cur_chunk.chunk_words[sorted_keys[0]]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if cur_word[0].lemmas==[]:
				error_list.append(slp_chunk_name)
				null_compound_dict[slp_chunk_name]=copy.deepcopy(cur_chunk)
				continue
				pass
			compound_dict[slp_chunk_name]=copy.deepcopy(cur_chunk)
			pass
		pass
	pickle.dump(compound_dict,open('compound_dict.p' , 'w'))
	pickle.dump(null_compound_dict,open('null_compound_dict.p' , 'w'))	
	print error_list
	pass

def get_compound_dict_2():
	# file_list=range(1,28)
	file_list=range(1,4)
	error_list=[]
	compound_dict={}
	null_compound_dict={}
	f = open('compounds.txt', 'r')
  	content=f.readlines()
	for cur_file_index in file_list:
		cur_file=pickle.load( open( "compounds/" + str(cur_file_index) + ".p", "rb" ) )
		for cur_chunk in cur_file.chunk:
			sorted_keys=cur_chunk.chunk_words.keys()
			sorted_keys.sort()
			cur_word=cur_chunk.chunk_words[sorted_keys[0]]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			cur_line=content[file_list.index(cur_file_index)].strip()
			if cur_word[0].lemmas==[]:
				error_list.append(cur_line)
				null_compound_dict[cur_line]=copy.deepcopy(cur_chunk)
				continue
				pass
			compound_dict[cur_line]=copy.deepcopy(cur_chunk)
			pass
		pass
	pickle.dump(compound_dict,open('compound_dict.p' , 'w'))
	pickle.dump(null_compound_dict,open('null_compound_dict.p' , 'w'))	
	print error_list
	pass

def set_compounds():
	# cur_text_file = open('uniquesentences.txt','r')
	# un_jumble=pickle.load(open( "un_jumble.p" , 'rb'))
	# sentence_list=cur_text_file.readlines()
	file_list=get_done_file_list()
	error_list={}
	compound_dict=pickle.load( open( "compound_dict.p", "rb" ) )
	null_compound_dict=pickle.load( open( "null_compound_dict.p", "rb" ) )
	underscore_dict=pickle.load( open( "under_1/underscore_dict.p", "rb" ) )
	null_underscore_dict=pickle.load( open( "under_1/null_underscore_dict.p", "rb" ) )
	# file_list=range(1,1000)
	for cur_file_index in file_list:
		# sentence_string= sentence_list[cur_file_index-1]
		cur_file=pickle.load( open( "new/" + str(cur_file_index) + ".p", "rb" ) )
		# cur_un_jumble=un_jumble[cur_file_index]
		# print cur_un_jumble
		cur_chunk_list=[]
		local_temp=[]
		for cur_index in range(len(cur_file.chunk)):
			cur_chunk=cur_file.chunk[cur_index]
			slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
			if ('-' in slp_chunk_name):
				if ('_' in slp_chunk_name):
					# print slp_chunk_name
					under_data=slp_chunk_name.strip().split("_")
					temp_list=[]
					for cur_word in under_data:
						if cur_word in underscore_dict.keys():
							local_chunk=underscore_dict[cur_word]
							temp_list.append(local_chunk)
							pass
						elif cur_word in null_underscore_dict.keys():
							local_chunk=null_underscore_dict[cur_word]
							temp_list.append(local_chunk)
							pass
						elif cur_word in compound_dict.keys():
							local_chunk=compound_dict[cur_word]
							temp_list.append(local_chunk)
							pass
						elif cur_word in null_compound_dict.keys():
							local_chunk=null_compound_dict[cur_word]
							temp_list.append(local_chunk)
							pass
						pass
					# new ch_list -> new[:]+[]+new[:]
					if len(temp_list)!=len(under_data):
						local_temp.append(slp_chunk_name)
						my_chunk=copy.deepcopy(cur_file.chunk)
						cur_chunk_list.append(my_chunk)				
						pass
					else :
						cur_chunk_list+=temp_list
						pass
					pass
				else :
					if slp_chunk_name in compound_dict.keys():
						local_chunk=compound_dict[slp_chunk_name]
						my_chunk=copy.deepcopy(local_chunk)
						cur_chunk_list.append(my_chunk)
						pass
					elif slp_chunk_name in null_compound_dict.keys():
						local_chunk=null_compound_dict[slp_chunk_name]
						my_chunk=copy.deepcopy(local_chunk)
						cur_chunk_list.append(my_chunk)
						pass
					pass
				pass
			pass
		cur_chunk=cur_chunk_list
		if local_temp!=[]:
			error_list[cur_file_index]=local_temp
			pass
		pickle.dump( cur_file, open(new_sent_path + str(cur_file_index)+'.p', "wb" ))
		pass
	print error_list
	pass

def pickle_tester():
	cur_file=pickle.load( open( "test/" + str(1) + ".p", "rb" ) )
	cur_file.print_sents()
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
	cur_file=pickle.load( open( "test/" + str(2) + ".p", "rb" ) )
	cur_file.print_sents()
	pass

# sandhi_dict=pickle.load(open( "support/sandhi_dict.p" , 'rb'))

def get_first_length(wd1, wd2):
	global sandhi_dict
	for rule_num in sandhi_dict.keys():
		rule_first_end,rule_second_start,result_str=sandhi_dict[rule_num]
		first_end=wd1[:-len(rule_first_end)]
		second_start=wd2[:len(rule_second_start)]
		if (rule_first_end==first_end) and (rule_second_start==second_start):
			# ret_str=wd1[:len(wd1)-len(rule_first_end)]+result_str+wd2[len(rule_second_start):]
			return len(wd1)-len(rule_first_end)
			pass
		pass
	return len(wd1)
	pass

def round_1(cur_file_index):
	cur_file=pickle.load( open( "test/" + str(cur_file_index) + ".p", "rb" ) )
	for cur_index in range(len(cur_file.chunk)):
		cur_chunk=cur_file.chunk[cur_index]
		# for each of 11 chunks
		slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
		sorted_keys=cur_chunk.chunk_words.keys()
		sorted_keys.sort()
		# take the largest if single.
		cur_key=sorted_keys[0]
		cur_word=cur_chunk.chunk_words[cur_key][0]
		# name, lemma_list, pos_list
		slp_cur_word=utf_to_ascii((cur_word.names).encode("raw_unicode_escape"))
		if slp_chunk_name == slp_cur_word :
			print slp_chunk_name
			print slp_cur_word
			temp_dict={}
			temp_dict[cur_key]=[cur_word]
			cur_chunk.chunk_words=temp_dict
			cur_file.chunk[cur_index]=cur_chunk
			pass
		pass
	# cur_file.print_sents()
	pass

def are_compatible(wd1,wd2):
	return False
	pass

def round_2(cur_file_index):
	cur_file=pickle.load( open( "test/" + str(cur_file_index) + ".p", "rb" ) )
	for cur_index in range(len(cur_file.chunk)):
		cur_chunk=cur_file.chunk[cur_index]
		# for each of 11 chunks
		slp_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
		sorted_keys=cur_chunk.chunk_words.keys()
		sorted_keys.sort()
		# make the position.
		position_dict={}
		min_word_dict={}
		for cur_key in sorted_keys:
			min_word=utf_to_ascii((cur_chunk.chunk_words[cur_key][0].names).encode("raw_unicode_escape"))
			min_val=len(min_word)
			for cur_word in cur_chunk.chunk_words[cur_key] :
				slp_word=utf_to_ascii((cur_word.names).encode("raw_unicode_escape"))
				if len(slp_word)<min_val:
					min_val=len(slp_word)
					min_word=slp_word
					pass
				pass
			min_word_dict[cur_key]=[min_val,min_word]
			pass
		# position incorrect
		position_dict[sorted_keys[0]]=0
		for index_1 in range(len(sorted_keys)-1):
			cur_key=sorted_keys[index_1]
			w1=min_word_dict[cur_key][1]
			w2=min_word_dict[sorted_keys[index_1+1]][1]
			position_dict[sorted_keys[index_1+1]]=position_dict[cur_key]+get_first_length(w1,w2)
			pass
		# get start pos.
		two_d_list=[]
		cur_word_list=cur_chunk.chunk_words[sorted_keys[0]]
		for cur_word in cur_word_list:
			flag=False
			pos_list=[]
			for cur_form in cur_word.forms:
				form_keys=cur_form.keys()
				for sub_key in form_keys:
					temp_string=str(cur_form[sub_key])
					if "http:sanskrit.inria" in temp_string:
						continue
						pass
					if 'iic.' in cur_form[sub_key]:
						flag=True
						pass
					pos_list.append(cur_form[sub_key])
					pass
				pass
			if flag:
				two_d_list.append([[sorted_keys[0], cur_word]])
				pass
			pass
		# check all compatibles.
		for cur_key in sorted_keys[1:]:
			cur_word_list=cur_chunk.chunk_words[cur_key]
			for cur_word in cur_word_list:
				for index_1 in range(len(two_d_list)):
					cur_path=two_d_list[index_1]
					last_word=cur_path[-1][1]
					# append to two_d_list
					if are_compatible(last_word,cur_word):
						two_d_list[index_1].append([cur_key,cur_word])
						pass
					pass
				pass
			pass
		# either pos_1+w1len+1=pos_2 or pos_2<=pos_1 and compatible
		# from start goto end.
		# not got atleast one path, no change.
		pass
	# cur_file.print_sents()
	pass

def preliminary_processor():
	# take the largest if single.
	round_1(1)
	# take the combos where all but last are 'iic.'
	round_2(1)
	# then for all sentences with multiple tuples left use the rules.
	round_3(1)
	pass

file_list_1140=[1, 2, 3, 4, 6, 9, 11, 13, 14, 15, 16, 18, 29, 34, 42, 43, 47, 48, 50, 51, 52, 53, 54, 56, 58, 67, 71, 74, 76, 84, 90, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 107, 108, 115, 116, 117, 119, 121, 122, 124, 125, 126, 127, 128, 130, 138, 142, 143, 144, 145, 146, 147, 148, 149, 150, 152, 153, 155, 156, 157, 165, 167, 168, 170, 171, 172, 174, 175, 176, 184, 186, 188, 192, 195, 196, 198, 200, 201, 203, 205, 208, 211, 213, 214, 215, 217, 219, 222, 223, 228, 229, 230, 232, 233, 235, 236, 237, 238, 239, 241, 244, 246, 247, 248, 249, 250, 251, 252, 253, 260, 261, 262, 264, 265, 269, 270, 274, 275, 276, 282, 283, 285, 286, 287, 288, 289, 291, 292, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 311, 317, 320, 321, 326, 328, 331, 332, 334, 336, 352, 353, 355, 366, 368, 393, 394, 397, 423, 429, 434, 437, 441, 445, 446, 451, 458, 484, 508, 514, 518, 522, 523, 526, 528, 530, 532, 539, 541, 560, 564, 572, 573, 576, 577, 580, 581, 582, 591, 595, 596, 597, 598, 600, 601, 602, 604, 605, 606, 607, 610, 614, 615, 616, 619, 620, 623, 625, 628, 630, 632, 634, 636, 638, 639, 641, 642, 644, 646, 649, 652, 653, 654, 655, 656, 657, 658, 659, 660, 662, 663, 664, 665, 666, 667, 669, 670, 671, 672, 673, 674, 675, 676, 677, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 692, 693, 694, 696, 698, 699, 700, 701, 702, 703, 704, 707, 709, 710, 711, 712, 713, 714, 715, 717, 719, 720, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 741, 742, 743, 744, 746, 747, 748, 749, 751, 752, 753, 754, 755, 756, 757, 759, 760, 761, 762, 764, 765, 766, 767, 768, 769, 772, 773, 774, 775, 776, 777, 779, 780, 781, 782, 783, 784, 785, 787, 788, 789, 790, 791, 792, 793, 794, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 817, 818, 821, 823, 824, 825, 826, 827, 828, 831, 832, 833, 834, 836, 837, 838, 839, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 854, 857, 859, 861, 862, 863, 864, 865, 867, 868, 874, 875, 877, 878, 879, 880, 882, 885, 886, 887, 888, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 906, 907, 908, 909, 910, 911, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 937, 938, 939, 940, 941, 942, 943, 945, 946, 947, 948, 949, 950, 951, 953, 955, 956, 958, 959, 960, 961, 962, 963, 964, 965, 968, 969, 970, 971, 972, 973, 974, 975, 977, 978, 979, 981, 982, 983, 985, 987, 988, 989, 990, 991, 992, 993, 994, 995, 997, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1012, 1013, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1032, 1035, 1037, 1038, 1040, 1045, 1046, 1051, 1052, 1054, 1055, 1061, 1067, 1070, 1072, 1073, 1075, 1076, 1087, 1094, 1097, 1100, 1103, 1123, 1124, 1134, 1137, 1145, 1147, 1150, 1151, 1152, 1153, 1159, 1171, 1179, 1180, 1182, 1183, 1187, 1189, 1190, 1192, 1194, 1200, 1201, 1208, 1209, 1216, 1218, 1220, 1221, 1224, 1225, 1239, 1241, 1242, 1248, 1254, 1259, 1261, 1267, 1268, 1270, 1293, 1295, 1301, 1303, 1305, 1306, 1317, 1318, 1321, 1323, 1324, 1327, 1331, 1332, 1334, 1335, 1336, 1339, 1340, 1341, 1343, 1348, 1351, 1358, 1359, 1361, 1365, 1372, 1375, 1377, 1379, 1390, 1391, 1393, 1397, 1405, 1407, 1416, 1422, 1425, 1426, 1428, 1432, 1435, 1437, 1439, 1443, 1459, 1468, 1469, 1470, 1477, 1478, 1479, 1482, 1484, 1486, 1494, 1495, 1503, 1508, 1522, 1524, 1528, 1536, 1537, 1539, 1541, 1549, 1551, 1553, 1555, 1558, 1559, 1563, 1564, 1565, 1569, 1574, 1585, 1586, 1598, 1600, 1601, 1614, 1625, 1626, 1627, 1633, 1634, 1636, 1638, 1639, 1643, 1646, 1650, 1654, 1656, 1657, 1658, 1662, 1672, 1673, 1679, 1680, 1691, 1693, 1697, 1702, 1712, 1717, 1720, 1721, 1726, 1729, 1744, 1746, 1761, 1767, 1769, 1774, 1775, 1780, 1781, 1787, 1790, 1791, 1793, 1795, 1803, 1805, 1808, 1809, 1810, 1816, 1828, 1853, 1856, 1859, 1873, 1876, 1878, 1879, 1881, 1883, 1887, 1896, 1897, 1898, 1902, 1913, 1925, 1953, 1957, 1958, 1959, 1960, 1961, 1965, 1967, 1970, 1980, 1983, 1986, 1987, 1992, 2008, 2009, 2022, 2027, 2028, 2030, 2032, 2039, 2043, 2055, 2056, 2058, 2061, 2063, 2074, 2080, 2086, 2089, 2093, 2100, 2108, 2110, 2130, 2141, 2151, 2158, 2162, 2174, 2185, 2194, 2197, 2198, 2200, 2204, 2206, 2210, 2214, 2216, 2218, 2224, 2239, 2243, 2249, 2253, 2255, 2257, 2276, 2281, 2292, 2293, 2305, 2307, 2308, 2309, 2310, 2312, 2313, 2315, 2316, 2317, 2318, 2327, 2328, 2329, 2331, 2334, 2338, 2341, 2345, 2350, 2352, 2353, 2354, 2356, 2358, 2360, 2363, 2372, 2397, 2398, 2411, 2414, 2419, 2427, 2432, 2449, 2460, 2465, 2466, 2468, 2469, 2477, 2481, 2484, 2489, 2492, 2493, 2498, 2507, 2514, 2522, 2525, 2526, 2528, 2529, 2536, 2537, 2538, 2541, 2543, 2544, 2554, 2558, 2563, 2564, 2565, 2566, 2567, 2568, 2586, 2595, 2601, 2617, 2621, 2625, 2626, 2627, 2635, 2645, 2646, 2660, 2679, 2688, 2693, 2699, 2700, 2705, 2713, 2718, 2719, 2728, 2732, 2736, 2737, 2741, 2743, 2746, 2753, 2767, 2769, 2778, 2786, 2790, 2805, 2806, 2810, 2815, 2819, 2825, 2827, 2828, 2829, 2830, 2831, 2835, 2840, 2845, 2849, 2852, 2854, 2861, 2868, 2871, 2873, 2876, 2877, 2881, 2882, 2883, 2888, 2890, 2896, 2898, 2914, 2917, 2930, 2932, 2948, 2955, 2962, 2992, 3022, 3023, 3026, 3028, 3031, 3035, 3040, 3050, 3052, 3055, 3058, 3060, 3068, 3075, 3077, 3088, 3092, 3099, 3102, 3107, 3109, 3111, 3115, 3123, 3126, 3127, 3134, 3147, 3153, 3165, 3185, 3187, 3189, 3191, 3198, 3199, 3200, 3201, 3205, 3207, 3209, 3210, 3215, 3218, 3226, 3234, 3239, 3244, 3245, 3247, 3257, 3261, 3262, 3273, 3275, 3281, 3283, 3286, 3289, 3291, 3310, 3312, 3313, 3323, 3330, 3332, 3343, 3345, 3347, 3348, 3349, 3350, 3351, 3352, 3353, 3354, 3355, 3357, 3359, 3360, 3361, 3362, 3368, 3370, 3371, 3373, 3376, 3389, 3391, 3397, 3399, 3400, 3426, 3431, 3433, 3435, 3437, 3438, 3443, 3455, 3456, 3459, 3463, 3464, 3467, 3468, 3469, 3470, 3471, 3474, 3475, 3477, 3480, 3485, 3495, 3497, 3499, 3518, 3519, 3520, 3525, 3531, 3535, 3536, 3538, 3540, 3543, 3547, 3552, 3553, 3557, 3565, 3581, 3593, 3594, 3595, 3605, 3632, 3634, 3635, 3641, 3651, 3659, 3674, 3677, 3679, 3680, 3682, 3692, 3693, 3696, 3697, 3704, 3710, 3711, 3713, 3715, 3719, 3734, 3738, 3741, 3742, 3753, 3787, 3788, 3794, 3801, 3804, 3823, 3824, 3828, 3830, 3831, 3833, 3834, 3838, 3842, 3889, 3937]
file_list_549=[2, 3, 4, 6, 14, 29, 42, 50, 51, 52, 54, 56, 84, 90, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 107, 115, 117, 119, 121, 124, 125, 126, 127, 128, 130, 138, 144, 146, 153, 156, 157, 170, 172, 175, 176, 184, 192, 195, 196, 201, 203, 211, 213, 217, 219, 222, 228, 229, 230, 232, 233, 236, 237, 238, 241, 244, 246, 247, 248, 249, 250, 251, 252, 253, 261, 265, 269, 274, 275, 276, 283, 285, 286, 287, 288, 289, 294, 295, 300, 301, 302, 303, 304, 305, 311, 317, 320, 331, 336, 353, 355, 368, 393, 423, 445, 446, 451, 484, 514, 518, 528, 532, 539, 573, 576, 577, 597, 600, 601, 604, 606, 607, 610, 614, 615, 625, 630, 638, 639, 641, 644, 654, 655, 656, 658, 659, 664, 665, 674, 675, 676, 680, 681, 682, 684, 686, 687, 688, 689, 692, 694, 696, 698, 700, 701, 704, 707, 712, 713, 714, 717, 719, 720, 722, 723, 729, 731, 734, 737, 738, 742, 743, 746, 747, 748, 749, 751, 752, 753, 756, 759, 761, 764, 765, 766, 767, 768, 769, 772, 773, 774, 777, 779, 780, 784, 785, 787, 791, 792, 793, 817, 818, 821, 823, 825, 826, 827, 828, 832, 833, 834, 836, 839, 842, 843, 846, 849, 850, 851, 862, 863, 867, 868, 874, 875, 877, 879, 880, 882, 885, 886, 887, 888, 909, 915, 916, 917, 918, 920, 922, 926, 927, 930, 937, 938, 939, 940, 945, 946, 947, 950, 961, 964, 965, 969, 970, 971, 973, 977, 978, 981, 985, 987, 988, 989, 990, 991, 992, 999, 1002, 1004, 1009, 1010, 1012, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1032, 1035, 1038, 1046, 1052, 1055, 1061, 1072, 1075, 1087, 1097, 1100, 1103, 1123, 1137, 1151, 1152, 1171, 1179, 1180, 1187, 1189, 1194, 1201, 1218, 1220, 1225, 1239, 1248, 1254, 1259, 1267, 1268, 1293, 1295, 1305, 1306, 1317, 1318, 1321, 1324, 1334, 1335, 1336, 1339, 1351, 1358, 1361, 1365, 1372, 1375, 1377, 1390, 1393, 1397, 1407, 1416, 1426, 1428, 1443, 1470, 1478, 1479, 1482, 1484, 1494, 1495, 1508, 1522, 1528, 1536, 1537, 1539, 1551, 1555, 1558, 1559, 1564, 1565, 1569, 1600, 1601, 1627, 1633, 1636, 1657, 1672, 1673, 1679, 1680, 1693, 1702, 1712, 1721, 1746, 1761, 1767, 1769, 1774, 1775, 1781, 1791, 1808, 1809, 1853, 1856, 1859, 1873, 1876, 1881, 1883, 1887, 1913, 1953, 1957, 1958, 1960, 1961, 1965, 1970, 1992, 2008, 2027, 2028, 2032, 2055, 2063, 2141, 2158, 2174, 2214, 2218, 2224, 2239, 2249, 2257, 2276, 2293, 2307, 2309, 2334, 2338, 2341, 2345, 2350, 2354, 2356, 2358, 2363, 2372, 2397, 2398, 2427, 2468, 2484, 2492, 2498, 2507, 2514, 2529, 2536, 2537, 2538, 2544, 2558, 2566, 2567, 2625, 2635, 2646, 2688, 2693, 2699, 2700, 2705, 2728, 2736, 2746, 2769, 2810, 2815, 2819, 2825, 2827, 2829, 2840, 2849, 2861, 2868, 2871, 2873, 2876, 2881, 2955, 2962, 3031, 3040, 3060, 3088, 3102, 3107, 3111, 3127, 3153, 3165, 3185, 3187, 3189, 3200, 3205, 3207, 3215, 3239, 3257, 3323, 3347, 3354, 3357, 3361, 3362, 3376, 3399, 3433, 3435, 3443, 3459, 3463, 3464, 3467, 3469, 3470, 3475, 3477, 3497, 3499, 3518, 3520, 3552, 3553, 3565, 3594, 3605, 3632, 3674, 3692, 3693, 3696, 3704, 3710, 3713, 3719, 3734, 3738, 3742, 3788, 3823, 3824, 3830, 3833, 3834, 3842, 3889]
file_list_590=[1, 9, 11, 13, 15, 16, 18, 34, 43, 47, 48, 53, 58, 67, 71, 74, 76, 108, 116, 122, 142, 143, 145, 147, 148, 149, 150, 152, 155, 165, 167, 168, 171, 174, 186, 188, 198, 200, 205, 208, 214, 215, 223, 235, 239, 260, 262, 264, 270, 282, 291, 292, 296, 297, 298, 299, 306, 307, 321, 326, 328, 332, 334, 352, 366, 394, 397, 429, 434, 437, 441, 458, 508, 522, 523, 526, 530, 541, 560, 564, 572, 580, 581, 582, 591, 595, 596, 598, 602, 605, 616, 619, 620, 623, 628, 632, 634, 636, 642, 646, 649, 652, 653, 657, 660, 662, 663, 666, 667, 669, 670, 671, 672, 673, 677, 683, 685, 693, 699, 702, 703, 709, 710, 711, 715, 724, 725, 726, 727, 728, 730, 732, 733, 735, 736, 739, 741, 744, 754, 755, 757, 760, 762, 775, 776, 781, 782, 783, 788, 789, 790, 794, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 824, 831, 837, 838, 844, 845, 847, 848, 852, 854, 857, 859, 861, 864, 865, 878, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 906, 907, 908, 910, 911, 913, 914, 919, 921, 923, 924, 925, 928, 929, 931, 932, 933, 934, 935, 941, 942, 943, 948, 949, 951, 953, 955, 956, 958, 959, 960, 962, 963, 968, 972, 974, 975, 979, 982, 983, 993, 994, 995, 997, 1000, 1001, 1003, 1005, 1006, 1007, 1008, 1013, 1015, 1037, 1040, 1045, 1051, 1054, 1067, 1070, 1073, 1076, 1094, 1124, 1134, 1145, 1147, 1150, 1153, 1159, 1182, 1183, 1190, 1192, 1200, 1208, 1209, 1216, 1221, 1224, 1241, 1242, 1261, 1270, 1301, 1303, 1323, 1327, 1331, 1332, 1340, 1341, 1343, 1348, 1359, 1379, 1391, 1405, 1422, 1425, 1432, 1435, 1437, 1439, 1459, 1468, 1469, 1477, 1486, 1503, 1524, 1541, 1549, 1553, 1563, 1574, 1585, 1586, 1598, 1614, 1625, 1626, 1634, 1638, 1639, 1643, 1646, 1650, 1654, 1656, 1658, 1662, 1691, 1697, 1717, 1720, 1726, 1729, 1744, 1780, 1787, 1790, 1793, 1795, 1803, 1805, 1810, 1816, 1828, 1878, 1879, 1896, 1897, 1898, 1902, 1925, 1959, 1967, 1980, 1983, 1986, 1987, 2009, 2022, 2030, 2039, 2043, 2056, 2058, 2061, 2074, 2080, 2086, 2089, 2093, 2100, 2108, 2110, 2130, 2151, 2162, 2185, 2194, 2197, 2198, 2200, 2204, 2206, 2210, 2216, 2243, 2253, 2255, 2281, 2292, 2305, 2308, 2310, 2312, 2313, 2315, 2316, 2317, 2318, 2327, 2328, 2329, 2331, 2352, 2353, 2360, 2411, 2414, 2419, 2432, 2449, 2460, 2465, 2466, 2469, 2477, 2481, 2489, 2493, 2522, 2525, 2526, 2528, 2541, 2543, 2554, 2563, 2564, 2565, 2568, 2586, 2595, 2601, 2617, 2621, 2626, 2627, 2645, 2660, 2679, 2713, 2718, 2719, 2732, 2737, 2741, 2743, 2753, 2767, 2778, 2786, 2790, 2805, 2806, 2828, 2830, 2831, 2835, 2845, 2852, 2854, 2877, 2882, 2883, 2888, 2890, 2896, 2898, 2914, 2917, 2930, 2932, 2948, 2992, 3022, 3023, 3026, 3028, 3035, 3050, 3052, 3055, 3058, 3068, 3075, 3077, 3092, 3099, 3109, 3115, 3123, 3126, 3134, 3147, 3191, 3198, 3199, 3201, 3209, 3210, 3218, 3226, 3234, 3244, 3245, 3247, 3261, 3262, 3273, 3275, 3281, 3283, 3286, 3289, 3291, 3310, 3312, 3313, 3330, 3332, 3343, 3345, 3348, 3349, 3350, 3351, 3352, 3353, 3355, 3359, 3360, 3368, 3370, 3371, 3373, 3389, 3391, 3397, 3400, 3426, 3431, 3437, 3438, 3455, 3456, 3468, 3471, 3474, 3480, 3485, 3495, 3519, 3525, 3531, 3535, 3536, 3538, 3540, 3543, 3547, 3557, 3581, 3593, 3595, 3634, 3635, 3641, 3651, 3659, 3677, 3679, 3680, 3682, 3697, 3711, 3715, 3741, 3753, 3787, 3794, 3801, 3804, 3828, 3831, 3838, 3937]
remaining_list=[5, 7, 8, 10, 12, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 49, 55, 57, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 72, 73, 75, 77, 78, 79, 80, 81, 82, 83, 85, 86, 87, 88, 89, 91, 92, 93, 94, 99, 106, 109, 110, 111, 112, 113, 114, 118, 120, 123, 129, 131, 132, 133, 134, 135, 136, 137, 139, 140, 141, 151, 154, 158, 159, 160, 161, 162, 163, 164, 166, 169, 173, 177, 178, 179, 180, 181, 182, 183, 185, 187, 189, 190, 191, 193, 194, 197, 199, 202, 204, 206, 207, 209, 210, 212, 216, 218, 220, 221, 224, 225, 226, 227, 231, 234, 240, 242, 243, 245, 254, 255, 256, 257, 258, 259, 263, 266, 267, 268, 271, 272, 273, 277, 278, 279, 280, 281, 284, 290, 293, 308, 309, 310, 312, 313, 314, 315, 316, 318, 319, 322, 323, 324, 325, 327, 329, 330, 333, 335, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 354, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 367, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 395, 396, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 424, 425, 426, 427, 428, 430, 431, 432, 433, 435, 436, 438, 439, 440, 442, 443, 444, 447, 448, 449, 450, 452, 453, 454, 455, 456, 457, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 509, 510, 511, 512, 513, 515, 516, 517, 519, 520, 521, 524, 525, 527, 529, 531, 533, 534, 535, 536, 537, 538, 540, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 561, 562, 563, 565, 566, 567, 568, 569, 570, 571, 574, 575, 578, 579, 583, 584, 585, 586, 587, 588, 589, 590, 592, 593, 594, 599, 603, 608, 609, 611, 612, 613, 617, 618, 621, 622, 624, 626, 627, 629, 631, 633, 635, 637, 640, 643, 645, 647, 648, 650, 651, 661, 668, 678, 679, 690, 691, 695, 697, 705, 706, 708, 716, 718, 721, 740, 745, 750, 758, 763, 770, 771, 778, 786, 795, 815, 816, 819, 820, 822, 829, 830, 835, 840, 841, 853, 855, 856, 858, 860, 866, 869, 870, 871, 872, 873, 876, 881, 883, 884, 889, 890, 891, 905, 912, 936, 944, 952, 954, 957, 966, 967, 976, 980, 984, 986, 996, 998, 1011, 1014, 1027, 1031, 1033, 1034, 1036, 1039, 1041, 1042, 1043, 1044, 1047, 1048, 1049, 1050, 1053, 1056, 1057, 1058, 1059, 1060, 1062, 1063, 1064, 1065, 1066, 1068, 1069, 1071, 1074, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1088, 1089, 1090, 1091, 1092, 1093, 1095, 1096, 1098, 1099, 1101, 1102, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1135, 1136, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1146, 1148, 1149, 1154, 1155, 1156, 1157, 1158, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1181, 1184, 1185, 1186, 1188, 1191, 1193, 1195, 1196, 1197, 1198, 1199, 1202, 1203, 1204, 1205, 1206, 1207, 1210, 1211, 1212, 1213, 1214, 1215, 1217, 1219, 1222, 1223, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1240, 1243, 1244, 1245, 1246, 1247, 1249, 1250, 1251, 1252, 1253, 1255, 1256, 1257, 1258, 1260, 1262, 1263, 1264, 1265, 1266, 1269, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1294, 1296, 1297, 1298, 1299, 1300, 1302, 1304, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1319, 1320, 1322, 1325, 1326, 1328, 1329, 1330, 1333, 1337, 1338, 1342, 1344, 1345, 1346, 1347, 1349, 1350, 1352, 1353, 1354, 1355, 1356, 1357, 1360, 1362, 1363, 1364, 1366, 1367, 1368, 1369, 1370, 1371, 1373, 1374, 1376, 1378, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1392, 1394, 1395, 1396, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1406, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1417, 1418, 1419, 1420, 1421, 1423, 1424, 1427, 1429, 1430, 1431, 1433, 1434, 1436, 1438, 1440, 1441, 1442, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1471, 1472, 1473, 1474, 1475, 1476, 1480, 1481, 1483, 1485, 1487, 1488, 1489, 1490, 1491, 1492, 1493, 1496, 1497, 1498, 1499, 1500, 1501, 1502, 1504, 1505, 1506, 1507, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1523, 1525, 1526, 1527, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1538, 1540, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1550, 1552, 1554, 1556, 1557, 1560, 1561, 1562, 1566, 1567, 1568, 1570, 1571, 1572, 1573, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1599, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1628, 1629, 1630, 1631, 1632, 1635, 1637, 1640, 1641, 1642, 1644, 1645, 1647, 1648, 1649, 1651, 1652, 1653, 1655, 1659, 1660, 1661, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1674, 1675, 1676, 1677, 1678, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688, 1689, 1690, 1692, 1694, 1695, 1696, 1698, 1699, 1700, 1701, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1713, 1714, 1715, 1716, 1718, 1719, 1722, 1723, 1724, 1725, 1727, 1728, 1730, 1731, 1732, 1733, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1745, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1762, 1763, 1764, 1765, 1766, 1768, 1770, 1771, 1772, 1773, 1776, 1777, 1778, 1779, 1782, 1783, 1784, 1785, 1786, 1788, 1789, 1792, 1794, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1804, 1806, 1807, 1811, 1812, 1813, 1814, 1815, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1854, 1855, 1857, 1858, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1874, 1875, 1877, 1880, 1882, 1884, 1885, 1886, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1899, 1900, 1901, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1954, 1955, 1956, 1962, 1963, 1964, 1966, 1968, 1969, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1981, 1982, 1984, 1985, 1988, 1989, 1990, 1991, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023, 2024, 2025, 2026, 2029, 2031, 2033, 2034, 2035, 2036, 2037, 2038, 2040, 2041, 2042, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2057, 2059, 2060, 2062, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2075, 2076, 2077, 2078, 2079, 2081, 2082, 2083, 2084, 2085, 2087, 2088, 2090, 2091, 2092, 2094, 2095, 2096, 2097, 2098, 2099, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2109, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138, 2139, 2140, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2152, 2153, 2154, 2155, 2156, 2157, 2159, 2160, 2161, 2163, 2164, 2165, 2166, 2167, 2168, 2169, 2170, 2171, 2172, 2173, 2175, 2176, 2177, 2178, 2179, 2180, 2181, 2182, 2183, 2184, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2195, 2196, 2199, 2201, 2202, 2203, 2205, 2207, 2208, 2209, 2211, 2212, 2213, 2215, 2217, 2219, 2220, 2221, 2222, 2223, 2225, 2226, 2227, 2228, 2229, 2230, 2231, 2232, 2233, 2234, 2235, 2236, 2237, 2238, 2240, 2241, 2242, 2244, 2245, 2246, 2247, 2248, 2250, 2251, 2252, 2254, 2256, 2258, 2259, 2260, 2261, 2262, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2277, 2278, 2279, 2280, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2306, 2311, 2314, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2330, 2332, 2333, 2335, 2336, 2337, 2339, 2340, 2342, 2343, 2344, 2346, 2347, 2348, 2349, 2351, 2355, 2357, 2359, 2361, 2362, 2364, 2365, 2366, 2367, 2368, 2369, 2370, 2371, 2373, 2374, 2375, 2376, 2377, 2378, 2379, 2380, 2381, 2382, 2383, 2384, 2385, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2396, 2399, 2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409, 2410, 2412, 2413, 2415, 2416, 2417, 2418, 2420, 2421, 2422, 2423, 2424, 2425, 2426, 2428, 2429, 2430, 2431, 2433, 2434, 2435, 2436, 2437, 2438, 2439, 2440, 2441, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2461, 2462, 2463, 2464, 2467, 2470, 2471, 2472, 2473, 2474, 2475, 2476, 2478, 2479, 2480, 2482, 2483, 2485, 2486, 2487, 2488, 2490, 2491, 2494, 2495, 2496, 2497, 2499, 2500, 2501, 2502, 2503, 2504, 2505, 2506, 2508, 2509, 2510, 2511, 2512, 2513, 2515, 2516, 2517, 2518, 2519, 2520, 2521, 2523, 2524, 2527, 2530, 2531, 2532, 2533, 2534, 2535, 2539, 2540, 2542, 2545, 2546, 2547, 2548, 2549, 2550, 2551, 2552, 2553, 2555, 2556, 2557, 2559, 2560, 2561, 2562, 2569, 2570, 2571, 2572, 2573, 2574, 2575, 2576, 2577, 2578, 2579, 2580, 2581, 2582, 2583, 2584, 2585, 2587, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2596, 2597, 2598, 2599, 2600, 2602, 2603, 2604, 2605, 2606, 2607, 2608, 2609, 2610, 2611, 2612, 2613, 2614, 2615, 2616, 2618, 2619, 2620, 2622, 2623, 2624, 2628, 2629, 2630, 2631, 2632, 2633, 2634, 2636, 2637, 2638, 2639, 2640, 2641, 2642, 2643, 2644, 2647, 2648, 2649, 2650, 2651, 2652, 2653, 2654, 2655, 2656, 2657, 2658, 2659, 2661, 2662, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2674, 2675, 2676, 2677, 2678, 2680, 2681, 2682, 2683, 2684, 2685, 2686, 2687, 2689, 2690, 2691, 2692, 2694, 2695, 2696, 2697, 2698, 2701, 2702, 2703, 2704, 2706, 2707, 2708, 2709, 2710, 2711, 2712, 2714, 2715, 2716, 2717, 2720, 2721, 2722, 2723, 2724, 2725, 2726, 2727, 2729, 2730, 2731, 2733, 2734, 2735, 2738, 2739, 2740, 2742, 2744, 2745, 2747, 2748, 2749, 2750, 2751, 2752, 2754, 2755, 2756, 2757, 2758, 2759, 2760, 2761, 2762, 2763, 2764, 2765, 2766, 2768, 2770, 2771, 2772, 2773, 2774, 2775, 2776, 2777, 2779, 2780, 2781, 2782, 2783, 2784, 2785, 2787, 2788, 2789, 2791, 2792, 2793, 2794, 2795, 2796, 2797, 2798, 2799, 2800, 2801, 2802, 2803, 2804, 2807, 2808, 2809, 2811, 2812, 2813, 2814, 2816, 2817, 2818, 2820, 2821, 2822, 2823, 2824, 2826, 2832, 2833, 2834, 2836, 2837, 2838, 2839, 2841, 2842, 2843, 2844, 2846, 2847, 2848, 2850, 2851, 2853, 2855, 2856, 2857, 2858, 2859, 2860, 2862, 2863, 2864, 2865, 2866, 2867, 2869, 2870, 2872, 2874, 2875, 2878, 2879, 2880, 2884, 2885, 2886, 2887, 2889, 2891, 2892, 2893, 2894, 2895, 2897, 2899, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2907, 2908, 2909, 2910, 2911, 2912, 2913, 2915, 2916, 2918, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2926, 2927, 2928, 2929, 2931, 2933, 2934, 2935, 2936, 2937, 2938, 2939, 2940, 2941, 2942, 2943, 2944, 2945, 2946, 2947, 2949, 2950, 2951, 2952, 2953, 2954, 2956, 2957, 2958, 2959, 2960, 2961, 2963, 2964, 2965, 2966, 2967, 2968, 2969, 2970, 2971, 2972, 2973, 2974, 2975, 2976, 2977, 2978, 2979, 2980, 2981, 2982, 2983, 2984, 2985, 2986, 2987, 2988, 2989, 2990, 2991, 2993, 2994, 2995, 2996, 2997, 2998, 2999, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3018, 3019, 3020, 3021, 3024, 3025, 3027, 3029, 3030, 3032, 3033, 3034, 3036, 3037, 3038, 3039, 3041, 3042, 3043, 3044, 3045, 3046, 3047, 3048, 3049, 3051, 3053, 3054, 3056, 3057, 3059, 3061, 3062, 3063, 3064, 3065, 3066, 3067, 3069, 3070, 3071, 3072, 3073, 3074, 3076, 3078, 3079, 3080, 3081, 3082, 3083, 3084, 3085, 3086, 3087, 3089, 3090, 3091, 3093, 3094, 3095, 3096, 3097, 3098, 3100, 3101, 3103, 3104, 3105, 3106, 3108, 3110, 3112, 3113, 3114, 3116, 3117, 3118, 3119, 3120, 3121, 3122, 3124, 3125, 3128, 3129, 3130, 3131, 3132, 3133, 3135, 3136, 3137, 3138, 3139, 3140, 3141, 3142, 3143, 3144, 3145, 3146, 3148, 3149, 3150, 3151, 3152, 3154, 3155, 3156, 3157, 3158, 3159, 3160, 3161, 3162, 3163, 3164, 3166, 3167, 3168, 3169, 3170, 3171, 3172, 3173, 3174, 3175, 3176, 3177, 3178, 3179, 3180, 3181, 3182, 3183, 3184, 3186, 3188, 3190, 3192, 3193, 3194, 3195, 3196, 3197, 3202, 3203, 3204, 3206, 3208, 3211, 3212, 3213, 3214, 3216, 3217, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3227, 3228, 3229, 3230, 3231, 3232, 3233, 3235, 3236, 3237, 3238, 3240, 3241, 3242, 3243, 3246, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3255, 3256, 3258, 3259, 3260, 3263, 3264, 3265, 3266, 3267, 3268, 3269, 3270, 3271, 3272, 3274, 3276, 3277, 3278, 3279, 3280, 3282, 3284, 3285, 3287, 3288, 3290, 3292, 3293, 3294, 3295, 3296, 3297, 3298, 3299, 3300, 3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309, 3311, 3314, 3315, 3316, 3317, 3318, 3319, 3320, 3321, 3322, 3324, 3325, 3326, 3327, 3328, 3329, 3331, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3344, 3346, 3356, 3358, 3363, 3364, 3365, 3366, 3367, 3369, 3372, 3374, 3375, 3377, 3378, 3379, 3380, 3381, 3382, 3383, 3384, 3385, 3386, 3387, 3388, 3390, 3392, 3393, 3394, 3395, 3396, 3398, 3401, 3402, 3403, 3404, 3405, 3406, 3407, 3408, 3409, 3410, 3411, 3412, 3413, 3414, 3415, 3416, 3417, 3418, 3419, 3420, 3421, 3422, 3423, 3424, 3425, 3427, 3428, 3429, 3430, 3432, 3434, 3436, 3439, 3440, 3441, 3442, 3444, 3445, 3446, 3447, 3448, 3449, 3450, 3451, 3452, 3453, 3454, 3457, 3458, 3460, 3461, 3462, 3465, 3466, 3472, 3473, 3476, 3478, 3479, 3481, 3482, 3483, 3484, 3486, 3487, 3488, 3489, 3490, 3491, 3492, 3493, 3494, 3496, 3498, 3500, 3501, 3502, 3503, 3504, 3505, 3506, 3507, 3508, 3509, 3510, 3511, 3512, 3513, 3514, 3515, 3516, 3517, 3521, 3522, 3523, 3524, 3526, 3527, 3528, 3529, 3530, 3532, 3533, 3534, 3537, 3539, 3541, 3542, 3544, 3545, 3546, 3548, 3549, 3550, 3551, 3554, 3555, 3556, 3558, 3559, 3560, 3561, 3562, 3563, 3564, 3566, 3567, 3568, 3569, 3570, 3571, 3572, 3573, 3574, 3575, 3576, 3577, 3578, 3579, 3580, 3582, 3583, 3584, 3585, 3586, 3587, 3588, 3589, 3590, 3591, 3592, 3596, 3597, 3598, 3599, 3600, 3601, 3602, 3603, 3604, 3606, 3607, 3608, 3609, 3610, 3611, 3612, 3613, 3614, 3615, 3616, 3617, 3618, 3619, 3620, 3621, 3622, 3623, 3624, 3625, 3626, 3627, 3628, 3629, 3630, 3631, 3633, 3636, 3637, 3638, 3639, 3640, 3642, 3643, 3644, 3645, 3646, 3647, 3648, 3649, 3650, 3652, 3653, 3654, 3655, 3656, 3657, 3658, 3660, 3661, 3662, 3663, 3664, 3665, 3666, 3667, 3668, 3669, 3670, 3671, 3672, 3673, 3675, 3676, 3678, 3681, 3683, 3684, 3685, 3686, 3687, 3688, 3689, 3690, 3691, 3694, 3695, 3698, 3699, 3700, 3701, 3702, 3703, 3705, 3706, 3707, 3708, 3709, 3712, 3714, 3716, 3717, 3718, 3720, 3721, 3722, 3723, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3731, 3732, 3733, 3735, 3736, 3737, 3739, 3740, 3743, 3744, 3745, 3746, 3747, 3748, 3749, 3750, 3751, 3752, 3754, 3755, 3756, 3757, 3758, 3759, 3760, 3761, 3762, 3763, 3764, 3765, 3766, 3767, 3768, 3769, 3770, 3771, 3772, 3773, 3774, 3775, 3776, 3777, 3778, 3779, 3780, 3781, 3782, 3783, 3784, 3785, 3786, 3789, 3790, 3791, 3792, 3793, 3795, 3796, 3797, 3798, 3799, 3800, 3802, 3803, 3805, 3806, 3807, 3808, 3809, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3819, 3820, 3821, 3822, 3825, 3826, 3827, 3829, 3832, 3835, 3836, 3837, 3839, 3840, 3841, 3843, 3844, 3845, 3846, 3847, 3848, 3849, 3850, 3851, 3852, 3853, 3854, 3855, 3856, 3857, 3858, 3859, 3860, 3861, 3862, 3863, 3864, 3865, 3866, 3867, 3868, 3869, 3870, 3871, 3872, 3873, 3874, 3875, 3876, 3877, 3878, 3879, 3880, 3881, 3882, 3883, 3884, 3885, 3886, 3887, 3888, 3890, 3891, 3892, 3893, 3894, 3895, 3896, 3897, 3898, 3899, 3900, 3901, 3902, 3903, 3904, 3905, 3906, 3907, 3908, 3909, 3910, 3911, 3912, 3913, 3914, 3915, 3916, 3917, 3918, 3919, 3920, 3921, 3922, 3923, 3924, 3925, 3926, 3927, 3928, 3929, 3930, 3931, 3932, 3933, 3934, 3935, 3936, 3938, 3939, 3940, 3941, 3942, 3943, 3944, 3945, 3946, 3947, 3948, 3949, 3950, 3951, 3952]
error_list=[5, 26, 28, 36, 38, 55, 69, 70, 72, 75, 80, 83, 86, 91, 141, 158, 178, 245, 259, 273, 322, 327, 330, 335, 337, 338, 339, 340, 342, 343, 344, 370, 389, 398, 405, 406, 409, 411, 414, 421, 432, 433, 448, 452, 463, 472, 481, 485, 489, 496, 501, 509, 519, 531, 533, 535, 536, 550, 552, 554, 562, 566, 567, 571, 585, 590, 599, 606, 608, 613, 617, 637, 640, 691, 695, 706, 708, 830, 841, 871, 883, 890, 912, 957, 976, 996, 998, 1039, 1048, 1058, 1062, 1066, 1068, 1078, 1089, 1109, 1111, 1122, 1126, 1129, 1132, 1140, 1166, 1170, 1172, 1173, 1175, 1178, 1183, 1196, 1197, 1219, 1228, 1230, 1244, 1245, 1246, 1247, 1250, 1252, 1253, 1258, 1263, 1287, 1304, 1308, 1309, 1310, 1312, 1316, 1320, 1322, 1326, 1329, 1330, 1336, 1353, 1355, 1362, 1363, 1367, 1368, 1380, 1394, 1402, 1410, 1415, 1458, 1460, 1464, 1471, 1473, 1474, 1492, 1518, 1519, 1543, 1547, 1550, 1554, 1556, 1557, 1576, 1577, 1580, 1592, 1604, 1607, 1616, 1619, 1640, 1643, 1652, 1653, 1683, 1684, 1690, 1702, 1704, 1710, 1722, 1730, 1733, 1739, 1748, 1752, 1753, 1754, 1755, 1763, 1779, 1784, 1796, 1799, 1811, 1814, 1831, 1833, 1835, 1836, 1837, 1843, 1850, 1851, 1852, 1862, 1863, 1868, 1874, 1875, 1877, 1882, 1888, 1890, 1891, 1893, 1894, 1901, 1906, 1908, 1912, 1916, 1926, 1936, 1937, 1939, 1944, 1947, 1950, 1951, 1956, 1963, 1964, 1968, 1977, 1981, 1985, 1989, 1995, 1996, 1997, 2002, 2006, 2034, 2041, 2052, 2060, 2072, 2076, 2077, 2081, 2083, 2088, 2093, 2094, 2096, 2097, 2098, 2099, 2104, 2106, 2107, 2116, 2117, 2118, 2121, 2122, 2127, 2131, 2133, 2136, 2142, 2143, 2152, 2153, 2154, 2155, 2156, 2159, 2165, 2182, 2184, 2205, 2207, 2213, 2217, 2219, 2220, 2222, 2225, 2226, 2227, 2230, 2244, 2245, 2248, 2259, 2261, 2267, 2268, 2271, 2272, 2273, 2274, 2277, 2278, 2279, 2282, 2283, 2288, 2289, 2291, 2294, 2300, 2302, 2304, 2322, 2325, 2339, 2368, 2370, 2373, 2380, 2384, 2385, 2399, 2403, 2404, 2405, 2420, 2422, 2425, 2429, 2430, 2434, 2435, 2439, 2440, 2442, 2445, 2446, 2447, 2482, 2496, 2497, 2509, 2524, 2549, 2550, 2551, 2573, 2579, 2584, 2596, 2597, 2604, 2606, 2607, 2619, 2634, 2640, 2641, 2643, 2647, 2648, 2657, 2658, 2662, 2672, 2684, 2687, 2694, 2706, 2707, 2709, 2711, 2716, 2723, 2742, 2745, 2747, 2749, 2750, 2756, 2757, 2758, 2761, 2766, 2768, 2772, 2773, 2774, 2775, 2788, 2789, 2793, 2798, 2808, 2816, 2817, 2822, 2834, 2837, 2844, 2848, 2850, 2851, 2862, 2864, 2869, 2870, 2893, 2894, 2897, 2907, 2909, 2913, 2918, 2926, 2933, 2943, 2946, 2959, 2960, 2961, 2968, 2969, 2973, 2977, 2985, 2986, 2989, 2995, 3001, 3006, 3007, 3009, 3014, 3017, 3041, 3046, 3052, 3053, 3084, 3113, 3120, 3124, 3141, 3145, 3148, 3150, 3151, 3152, 3162, 3167, 3170, 3171, 3172, 3173, 3175, 3184, 3191, 3194, 3204, 3213, 3214, 3216, 3227, 3229, 3233, 3235, 3242, 3246, 3251, 3252, 3253, 3259, 3260, 3262, 3269, 3287, 3290, 3295, 3297, 3305, 3309, 3317, 3318, 3321, 3327, 3331, 3333, 3335, 3356, 3364, 3384, 3386, 3388, 3390, 3392, 3398, 3404, 3411, 3412, 3413, 3414, 3415, 3424, 3430, 3434, 3439, 3440, 3441, 3442, 3444, 3450, 3457, 3461, 3462, 3494, 3498, 3502, 3506, 3507, 3509, 3510, 3515, 3524, 3539, 3546, 3558, 3559, 3561, 3564, 3566, 3568, 3571, 3576, 3583, 3589, 3592, 3599, 3609, 3619, 3620, 3622, 3623, 3625, 3631, 3640, 3642, 3645, 3648, 3650, 3653, 3663, 3667, 3670, 3683, 3685, 3690, 3691, 3695, 3698, 3701, 3707, 3712, 3714, 3717, 3722, 3723, 3731, 3739, 3740, 3742, 3743, 3749, 3751, 3758, 3761, 3767, 3772, 3773, 3774, 3777, 3789, 3793, 3795, 3797, 3800, 3809, 3820, 3844, 3850, 3858, 3861, 3873, 3875, 3876, 3877, 3880, 3887, 3890, 3899, 3905, 3911, 3912, 3913, 3914, 3916, 3917, 3918, 3922, 3925, 3927, 3928, 3933, 3944, 3950, 3951, 3952]


def get_input_sentences():
	# cur_file_list=[14, 29, 52, 84, 90, 300, 304, 393, 446, 451, 484, 518, 577, 606, 607, 610, 659, 698, 700, 774, 1017, 1052, 1055, 1201, 1365, 1375, 1407, 1470, 1495, 1679, 1702, 1721, 1853, 1957, 1961, 1965, 1970, 1992, 2063, 2214, 2249, 2350, 2363, 2398, 2498, 2507, 2514, 2625, 2746, 2861, 2955, 2962, 3107, 3134, 3185, 3189, 3215, 3239, 3435, 3443, 3459, 3470, 3594, 3692, 3742]
	# cur_file_list=[1, 9, 11, 13, 15, 16, 18, 34, 43, 47, 48, 53, 58, 67, 71, 74, 76, 108, 116, 122, 142, 143, 145, 147, 148, 149, 150, 152, 155, 165, 167, 168, 171, 174, 186, 188, 198, 200, 205, 208, 214, 215, 223, 235, 239, 260, 262, 264, 270, 282, 291, 292, 296, 297, 298, 299, 306, 307, 321, 326, 328, 332, 334, 352, 366, 394, 397, 429, 434, 437, 441, 458, 508, 522, 523, 526, 530, 541, 560, 564, 572, 580, 581, 582, 591, 595, 596, 598, 602, 605, 616, 619, 620, 623, 628, 632, 634, 636, 642, 646, 649, 652, 653, 657, 660, 662, 663, 666, 667, 669, 670, 671, 672, 673, 677, 683, 685, 693, 699, 702, 703, 709, 710, 711, 715, 724, 725, 726, 727, 728, 730, 732, 733, 735, 736, 739, 741, 744, 754, 755, 757, 760, 762, 775, 776, 781, 782, 783, 788, 789, 790, 794, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 824, 831, 837, 838, 844, 845, 847, 848, 852, 854, 857, 859, 861, 864, 865, 878, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 906, 907, 908, 910, 911, 913, 914, 919, 921, 923, 924, 925, 928, 929, 931, 932, 933, 934, 935, 941, 942, 943, 948, 949, 951, 953, 955, 956, 958, 959, 960, 962, 963, 968, 972, 974, 975, 979, 982, 983, 993, 994, 995, 997, 1000, 1001, 1003, 1005, 1006, 1007, 1008, 1013, 1015, 1037, 1040, 1045, 1051, 1054, 1067, 1070, 1073, 1076, 1094, 1124, 1134, 1145, 1147, 1150, 1153, 1159, 1182, 1183, 1190, 1192, 1200, 1208, 1209, 1216, 1221, 1224, 1241, 1242, 1261, 1270, 1301, 1303, 1323, 1327, 1331, 1332, 1340, 1341, 1343, 1348, 1359, 1379, 1391, 1405, 1422, 1425, 1432, 1435, 1437, 1439, 1459, 1468, 1469, 1477, 1486, 1503, 1524, 1541, 1549, 1553, 1563, 1574, 1585, 1586, 1598, 1614, 1625, 1626, 1634, 1638, 1639, 1643, 1646, 1650, 1654, 1656, 1658, 1662, 1691, 1697, 1717, 1720, 1726, 1729, 1744, 1780, 1787, 1790, 1793, 1795, 1803, 1805, 1810, 1816, 1828, 1878, 1879, 1896, 1897, 1898, 1902, 1925, 1959, 1967, 1980, 1983, 1986, 1987, 2009, 2022, 2030, 2039, 2043, 2056, 2058, 2061, 2074, 2080, 2086, 2089, 2093, 2100, 2108, 2110, 2130, 2151, 2162, 2185, 2194, 2197, 2198, 2200, 2204, 2206, 2210, 2216, 2243, 2253, 2255, 2281, 2292, 2305, 2308, 2310, 2312, 2313, 2315, 2316, 2317, 2318, 2327, 2328, 2329, 2331, 2352, 2353, 2360, 2411, 2414, 2419, 2432, 2449, 2460, 2465, 2466, 2469, 2477, 2481, 2489, 2493, 2522, 2525, 2526, 2528, 2541, 2543, 2554, 2563, 2564, 2565, 2568, 2586, 2595, 2601, 2617, 2621, 2626, 2627, 2645, 2660, 2679, 2713, 2718, 2719, 2732, 2737, 2741, 2743, 2753, 2767, 2778, 2786, 2790, 2805, 2806, 2828, 2830, 2831, 2835, 2845, 2852, 2854, 2877, 2882, 2883, 2888, 2890, 2896, 2898, 2914, 2917, 2930, 2932, 2948, 2992, 3022, 3023, 3026, 3028, 3035, 3050, 3052, 3055, 3058, 3068, 3075, 3077, 3092, 3099, 3109, 3115, 3123, 3126, 3134, 3147, 3191, 3198, 3199, 3201, 3209, 3210, 3218, 3226, 3234, 3244, 3245, 3247, 3261, 3262, 3273, 3275, 3281, 3283, 3286, 3289, 3291, 3310, 3312, 3313, 3330, 3332, 3343, 3345, 3348, 3349, 3350, 3351, 3352, 3353, 3355, 3359, 3360, 3368, 3370, 3371, 3373, 3389, 3391, 3397, 3400, 3426, 3431, 3437, 3438, 3455, 3456, 3468, 3471, 3474, 3480, 3485, 3495, 3519, 3525, 3531, 3535, 3536, 3538, 3540, 3543, 3547, 3557, 3581, 3593, 3595, 3634, 3635, 3641, 3651, 3659, 3677, 3679, 3680, 3682, 3697, 3711, 3715, 3741, 3753, 3787, 3794, 3801, 3804, 3828, 3831, 3838, 3937]
	# _
	pp=[3587,3589,3604,2070,2071,3608,2587,1053,542,3617,3108,2597,3110,3625,554,2311,558,559,2611,2314,3135,2912,1604,354,3155,3668,2647,3162,3163,1629,2654,3260,1648,2173,2176,534,1162,1165,2704,1682,2709,2201,2842,3269,2720,1700,678,3757,3613,3762,3256,3871,2236,2244,2245,1736,3280,1747,3620,3450,2277,2282,2285,2798,1777,2295,3841,1799,1802,268,2323,1815,2841,1818,3119,1821,2335,2848,1313,3886,2867,3381,3382,2361,3903,1864,1868,2383,3411,1880,1885,1374,1253,2400,1889,2402,1892,3944,2410,2927,2416,2417,378,379,3460,3461,3465,2444,400,2963,409,418,1445,422,425,426,3501,3059,440,3002,3010,456,3916,2506,1271,3534,466,3029,1501,1505,3046,2023,3560,493,3054,2035,2041,3066]
	pp+=[2311,267,2361,387,400,459,464,469,471,473,477,478,549,565,579,586,2735,2755,3881,3900,3901,3949,1417,1419,1421,1438,1441,1444,1457,1472,1475,1500,3549,1507,1510,1540,1579,1594,1595,1602,1615,1620,1642,1647,2375,3843,3851,3874,3882,3894,3915,3943,3945]
	pp+=[5, 26, 28, 36, 38, 55, 69, 70, 72, 75, 80, 83, 86, 91, 141, 158, 178, 245, 259, 273, 322, 327, 330, 335, 337, 338, 339, 340, 342, 343, 344, 370, 389, 398, 405, 406, 409, 411, 414, 421, 432, 433, 448, 452, 463, 472, 481, 485, 489, 496, 501, 509, 519, 531, 533, 535, 536, 550, 552, 554, 562, 566, 567, 571, 585, 590, 599, 606, 608, 613, 617, 637, 640, 691, 695, 706, 708, 830, 841, 871, 883, 890, 912, 957, 976, 996, 998, 1039, 1048, 1058, 1062, 1066, 1068, 1078, 1089, 1109, 1111, 1122, 1126, 1129, 1132, 1140, 1166, 1170, 1172, 1173, 1175, 1178, 1183, 1196, 1197, 1219, 1228, 1230, 1244, 1245, 1246, 1247, 1250, 1252, 1253, 1258, 1263, 1287, 1304, 1308, 1309, 1310, 1312, 1316, 1320, 1322, 1326, 1329, 1330, 1336, 1353, 1355, 1362, 1363, 1367, 1368, 1380, 1394, 1402, 1410, 1415, 1458, 1460, 1464, 1471, 1473, 1474, 1492, 1518, 1519, 1543, 1547, 1550, 1554, 1556, 1557, 1576, 1577, 1580, 1592, 1604, 1607, 1616, 1619, 1640, 1643, 1652, 1653, 1683, 1684, 1690, 1702, 1704, 1710, 1722, 1730, 1733, 1739, 1748, 1752, 1753, 1754, 1755, 1763, 1779, 1784, 1796, 1799, 1811, 1814, 1831, 1833, 1835, 1836, 1837, 1843, 1850, 1851, 1852, 1862, 1863, 1868, 1874, 1875, 1877, 1882, 1888, 1890, 1891, 1893, 1894, 1901, 1906, 1908, 1912, 1916, 1926, 1936, 1937, 1939, 1944, 1947, 1950, 1951, 1956, 1963, 1964, 1968, 1977, 1981, 1985, 1989, 1995, 1996, 1997, 2002, 2006, 2034, 2041, 2052, 2060, 2072, 2076, 2077, 2081, 2083, 2088, 2093, 2094, 2096, 2097, 2098, 2099, 2104, 2106, 2107, 2116, 2117, 2118, 2121, 2122, 2127, 2131, 2133, 2136, 2142, 2143, 2152, 2153, 2154, 2155, 2156, 2159, 2165, 2182, 2184, 2205, 2207, 2213, 2217, 2219, 2220, 2222, 2225, 2226, 2227, 2230, 2244, 2245, 2248, 2259, 2261, 2267, 2268, 2271, 2272, 2273, 2274, 2277, 2278, 2279, 2282, 2283, 2288, 2289, 2291, 2294, 2300, 2302, 2304, 2322, 2325, 2339, 2368, 2370, 2373, 2380, 2384, 2385, 2399, 2403, 2404, 2405, 2420, 2422, 2425, 2429, 2430, 2434, 2435, 2439, 2440, 2442, 2445, 2446, 2447, 2482, 2496, 2497, 2509, 2524, 2549, 2550, 2551, 2573, 2579, 2584, 2596, 2597, 2604, 2606, 2607, 2619, 2634, 2640, 2641, 2643, 2647, 2648, 2657, 2658, 2662, 2672, 2684, 2687, 2694, 2706, 2707, 2709, 2711, 2716, 2723, 2742, 2745, 2747, 2749, 2750, 2756, 2757, 2758, 2761, 2766, 2768, 2772, 2773, 2774, 2775, 2788, 2789, 2793, 2798, 2808, 2816, 2817, 2822, 2834, 2837, 2844, 2848, 2850, 2851, 2862, 2864, 2869, 2870, 2893, 2894, 2897, 2907, 2909, 2913, 2918, 2926, 2933, 2943, 2946, 2959, 2960, 2961, 2968, 2969, 2973, 2977, 2985, 2986, 2989, 2995, 3001, 3006, 3007, 3009, 3014, 3017, 3041, 3046, 3052, 3053, 3084, 3113, 3120, 3124, 3141, 3145, 3148, 3150, 3151, 3152, 3162, 3167, 3170, 3171, 3172, 3173, 3175, 3184, 3191, 3194, 3204, 3213, 3214, 3216, 3227, 3229, 3233, 3235, 3242, 3246, 3251, 3252, 3253, 3259, 3260, 3262, 3269, 3287, 3290, 3295, 3297, 3305, 3309, 3317, 3318, 3321, 3327, 3331, 3333, 3335, 3356, 3364, 3384, 3386, 3388, 3390, 3392, 3398, 3404, 3411, 3412, 3413, 3414, 3415, 3424, 3430, 3434, 3439, 3440, 3441, 3442, 3444, 3450, 3457, 3461, 3462, 3494, 3498, 3502, 3506, 3507, 3509, 3510, 3515, 3524, 3539, 3546, 3558, 3559, 3561, 3564, 3566, 3568, 3571, 3576, 3583, 3589, 3592, 3599, 3609, 3619, 3620, 3622, 3623, 3625, 3631, 3640, 3642, 3645, 3648, 3650, 3653, 3663, 3667, 3670, 3683, 3685, 3690, 3691, 3695, 3698, 3701, 3707, 3712, 3714, 3717, 3722, 3723, 3731, 3739, 3740, 3742, 3743, 3749, 3751, 3758, 3761, 3767, 3772, 3773, 3774, 3777, 3789, 3793, 3795, 3797, 3800, 3809, 3820, 3844, 3850, 3858, 3861, 3873, 3875, 3876, 3877, 3880, 3887, 3890, 3899, 3905, 3911, 3912, 3913, 3914, 3916, 3917, 3918, 3922, 3925, 3927, 3928, 3933, 3944, 3950, 3951, 3952]
	remaining_list=[5, 7, 8, 10, 12, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 49, 55, 57, 59, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 72, 73, 75, 77, 78, 79, 80, 81, 82, 83, 85, 86, 87, 88, 89, 91, 92, 93, 94, 99, 106, 109, 110, 111, 112, 113, 114, 118, 120, 123, 129, 131, 132, 133, 134, 135, 136, 137, 139, 140, 141, 151, 154, 158, 159, 160, 161, 162, 163, 164, 166, 169, 173, 177, 178, 179, 180, 181, 182, 183, 185, 187, 189, 190, 191, 193, 194, 197, 199, 202, 204, 206, 207, 209, 210, 212, 216, 218, 220, 221, 224, 225, 226, 227, 231, 234, 240, 242, 243, 245, 254, 255, 256, 257, 258, 259, 263, 266, 267, 268, 271, 272, 273, 277, 278, 279, 280, 281, 284, 290, 293, 308, 309, 310, 312, 313, 314, 315, 316, 318, 319, 322, 323, 324, 325, 327, 329, 330, 333, 335, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 354, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 367, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 395, 396, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 424, 425, 426, 427, 428, 430, 431, 432, 433, 435, 436, 438, 439, 440, 442, 443, 444, 447, 448, 449, 450, 452, 453, 454, 455, 456, 457, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 509, 510, 511, 512, 513, 515, 516, 517, 519, 520, 521, 524, 525, 527, 529, 531, 533, 534, 535, 536, 537, 538, 540, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 561, 562, 563, 565, 566, 567, 568, 569, 570, 571, 574, 575, 578, 579, 583, 584, 585, 586, 587, 588, 589, 590, 592, 593, 594, 599, 603, 608, 609, 611, 612, 613, 617, 618, 621, 622, 624, 626, 627, 629, 631, 633, 635, 637, 640, 643, 645, 647, 648, 650, 651, 661, 668, 678, 679, 690, 691, 695, 697, 705, 706, 708, 716, 718, 721, 740, 745, 750, 758, 763, 770, 771, 778, 786, 795, 815, 816, 819, 820, 822, 829, 830, 835, 840, 841, 853, 855, 856, 858, 860, 866, 869, 870, 871, 872, 873, 876, 881, 883, 884, 889, 890, 891, 905, 912, 936, 944, 952, 954, 957, 966, 967, 976, 980, 984, 986, 996, 998, 1011, 1014, 1027, 1031, 1033, 1034, 1036, 1039, 1041, 1042, 1043, 1044, 1047, 1048, 1049, 1050, 1053, 1056, 1057, 1058, 1059, 1060, 1062, 1063, 1064, 1065, 1066, 1068, 1069, 1071, 1074, 1077, 1078, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1088, 1089, 1090, 1091, 1092, 1093, 1095, 1096, 1098, 1099, 1101, 1102, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1122, 1125, 1126, 1127, 1128, 1129, 1130, 1131, 1132, 1133, 1135, 1136, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1146, 1148, 1149, 1154, 1155, 1156, 1157, 1158, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1181, 1184, 1185, 1186, 1188, 1191, 1193, 1195, 1196, 1197, 1198, 1199, 1202, 1203, 1204, 1205, 1206, 1207, 1210, 1211, 1212, 1213, 1214, 1215, 1217, 1219, 1222, 1223, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1240, 1243, 1244, 1245, 1246, 1247, 1249, 1250, 1251, 1252, 1253, 1255, 1256, 1257, 1258, 1260, 1262, 1263, 1264, 1265, 1266, 1269, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1294, 1296, 1297, 1298, 1299, 1300, 1302, 1304, 1307, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1319, 1320, 1322, 1325, 1326, 1328, 1329, 1330, 1333, 1337, 1338, 1342, 1344, 1345, 1346, 1347, 1349, 1350, 1352, 1353, 1354, 1355, 1356, 1357, 1360, 1362, 1363, 1364, 1366, 1367, 1368, 1369, 1370, 1371, 1373, 1374, 1376, 1378, 1380, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1392, 1394, 1395, 1396, 1398, 1399, 1400, 1401, 1402, 1403, 1404, 1406, 1408, 1409, 1410, 1411, 1412, 1413, 1414, 1415, 1417, 1418, 1419, 1420, 1421, 1423, 1424, 1427, 1429, 1430, 1431, 1433, 1434, 1436, 1438, 1440, 1441, 1442, 1444, 1445, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1457, 1458, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1471, 1472, 1473, 1474, 1475, 1476, 1480, 1481, 1483, 1485, 1487, 1488, 1489, 1490, 1491, 1492, 1493, 1496, 1497, 1498, 1499, 1500, 1501, 1502, 1504, 1505, 1506, 1507, 1509, 1510, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1518, 1519, 1520, 1521, 1523, 1525, 1526, 1527, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1538, 1540, 1542, 1543, 1544, 1545, 1546, 1547, 1548, 1550, 1552, 1554, 1556, 1557, 1560, 1561, 1562, 1566, 1567, 1568, 1570, 1571, 1572, 1573, 1575, 1576, 1577, 1578, 1579, 1580, 1581, 1582, 1583, 1584, 1587, 1588, 1589, 1590, 1591, 1592, 1593, 1594, 1595, 1596, 1597, 1599, 1602, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610, 1611, 1612, 1613, 1615, 1616, 1617, 1618, 1619, 1620, 1621, 1622, 1623, 1624, 1628, 1629, 1630, 1631, 1632, 1635, 1637, 1640, 1641, 1642, 1644, 1645, 1647, 1648, 1649, 1651, 1652, 1653, 1655, 1659, 1660, 1661, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1674, 1675, 1676, 1677, 1678, 1681, 1682, 1683, 1684, 1685, 1686, 1687, 1688, 1689, 1690, 1692, 1694, 1695, 1696, 1698, 1699, 1700, 1701, 1703, 1704, 1705, 1706, 1707, 1708, 1709, 1710, 1711, 1713, 1714, 1715, 1716, 1718, 1719, 1722, 1723, 1724, 1725, 1727, 1728, 1730, 1731, 1732, 1733, 1734, 1735, 1736, 1737, 1738, 1739, 1740, 1741, 1742, 1743, 1745, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1762, 1763, 1764, 1765, 1766, 1768, 1770, 1771, 1772, 1773, 1776, 1777, 1778, 1779, 1782, 1783, 1784, 1785, 1786, 1788, 1789, 1792, 1794, 1796, 1797, 1798, 1799, 1800, 1801, 1802, 1804, 1806, 1807, 1811, 1812, 1813, 1814, 1815, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1851, 1852, 1854, 1855, 1857, 1858, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1874, 1875, 1877, 1880, 1882, 1884, 1885, 1886, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1899, 1900, 1901, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1914, 1915, 1916, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1954, 1955, 1956, 1962, 1963, 1964, 1966, 1968, 1969, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1981, 1982, 1984, 1985, 1988, 1989, 1990, 1991, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2023, 2024, 2025, 2026, 2029, 2031, 2033, 2034, 2035, 2036, 2037, 2038, 2040, 2041, 2042, 2044, 2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2057, 2059, 2060, 2062, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2075, 2076, 2077, 2078, 2079, 2081, 2082, 2083, 2084, 2085, 2087, 2088, 2090, 2091, 2092, 2094, 2095, 2096, 2097, 2098, 2099, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2109, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138, 2139, 2140, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2152, 2153, 2154, 2155, 2156, 2157, 2159, 2160, 2161, 2163, 2164, 2165, 2166, 2167, 2168, 2169, 2170, 2171, 2172, 2173, 2175, 2176, 2177, 2178, 2179, 2180, 2181, 2182, 2183, 2184, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2195, 2196, 2199, 2201, 2202, 2203, 2205, 2207, 2208, 2209, 2211, 2212, 2213, 2215, 2217, 2219, 2220, 2221, 2222, 2223, 2225, 2226, 2227, 2228, 2229, 2230, 2231, 2232, 2233, 2234, 2235, 2236, 2237, 2238, 2240, 2241, 2242, 2244, 2245, 2246, 2247, 2248, 2250, 2251, 2252, 2254, 2256, 2258, 2259, 2260, 2261, 2262, 2263, 2264, 2265, 2266, 2267, 2268, 2269, 2270, 2271, 2272, 2273, 2274, 2275, 2277, 2278, 2279, 2280, 2282, 2283, 2284, 2285, 2286, 2287, 2288, 2289, 2290, 2291, 2294, 2295, 2296, 2297, 2298, 2299, 2300, 2301, 2302, 2303, 2304, 2306, 2311, 2314, 2319, 2320, 2321, 2322, 2323, 2324, 2325, 2326, 2330, 2332, 2333, 2335, 2336, 2337, 2339, 2340, 2342, 2343, 2344, 2346, 2347, 2348, 2349, 2351, 2355, 2357, 2359, 2361, 2362, 2364, 2365, 2366, 2367, 2368, 2369, 2370, 2371, 2373, 2374, 2375, 2376, 2377, 2378, 2379, 2380, 2381, 2382, 2383, 2384, 2385, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2396, 2399, 2400, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2409, 2410, 2412, 2413, 2415, 2416, 2417, 2418, 2420, 2421, 2422, 2423, 2424, 2425, 2426, 2428, 2429, 2430, 2431, 2433, 2434, 2435, 2436, 2437, 2438, 2439, 2440, 2441, 2442, 2443, 2444, 2445, 2446, 2447, 2448, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2461, 2462, 2463, 2464, 2467, 2470, 2471, 2472, 2473, 2474, 2475, 2476, 2478, 2479, 2480, 2482, 2483, 2485, 2486, 2487, 2488, 2490, 2491, 2494, 2495, 2496, 2497, 2499, 2500, 2501, 2502, 2503, 2504, 2505, 2506, 2508, 2509, 2510, 2511, 2512, 2513, 2515, 2516, 2517, 2518, 2519, 2520, 2521, 2523, 2524, 2527, 2530, 2531, 2532, 2533, 2534, 2535, 2539, 2540, 2542, 2545, 2546, 2547, 2548, 2549, 2550, 2551, 2552, 2553, 2555, 2556, 2557, 2559, 2560, 2561, 2562, 2569, 2570, 2571, 2572, 2573, 2574, 2575, 2576, 2577, 2578, 2579, 2580, 2581, 2582, 2583, 2584, 2585, 2587, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2596, 2597, 2598, 2599, 2600, 2602, 2603, 2604, 2605, 2606, 2607, 2608, 2609, 2610, 2611, 2612, 2613, 2614, 2615, 2616, 2618, 2619, 2620, 2622, 2623, 2624, 2628, 2629, 2630, 2631, 2632, 2633, 2634, 2636, 2637, 2638, 2639, 2640, 2641, 2642, 2643, 2644, 2647, 2648, 2649, 2650, 2651, 2652, 2653, 2654, 2655, 2656, 2657, 2658, 2659, 2661, 2662, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2672, 2673, 2674, 2675, 2676, 2677, 2678, 2680, 2681, 2682, 2683, 2684, 2685, 2686, 2687, 2689, 2690, 2691, 2692, 2694, 2695, 2696, 2697, 2698, 2701, 2702, 2703, 2704, 2706, 2707, 2708, 2709, 2710, 2711, 2712, 2714, 2715, 2716, 2717, 2720, 2721, 2722, 2723, 2724, 2725, 2726, 2727, 2729, 2730, 2731, 2733, 2734, 2735, 2738, 2739, 2740, 2742, 2744, 2745, 2747, 2748, 2749, 2750, 2751, 2752, 2754, 2755, 2756, 2757, 2758, 2759, 2760, 2761, 2762, 2763, 2764, 2765, 2766, 2768, 2770, 2771, 2772, 2773, 2774, 2775, 2776, 2777, 2779, 2780, 2781, 2782, 2783, 2784, 2785, 2787, 2788, 2789, 2791, 2792, 2793, 2794, 2795, 2796, 2797, 2798, 2799, 2800, 2801, 2802, 2803, 2804, 2807, 2808, 2809, 2811, 2812, 2813, 2814, 2816, 2817, 2818, 2820, 2821, 2822, 2823, 2824, 2826, 2832, 2833, 2834, 2836, 2837, 2838, 2839, 2841, 2842, 2843, 2844, 2846, 2847, 2848, 2850, 2851, 2853, 2855, 2856, 2857, 2858, 2859, 2860, 2862, 2863, 2864, 2865, 2866, 2867, 2869, 2870, 2872, 2874, 2875, 2878, 2879, 2880, 2884, 2885, 2886, 2887, 2889, 2891, 2892, 2893, 2894, 2895, 2897, 2899, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2907, 2908, 2909, 2910, 2911, 2912, 2913, 2915, 2916, 2918, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2926, 2927, 2928, 2929, 2931, 2933, 2934, 2935, 2936, 2937, 2938, 2939, 2940, 2941, 2942, 2943, 2944, 2945, 2946, 2947, 2949, 2950, 2951, 2952, 2953, 2954, 2956, 2957, 2958, 2959, 2960, 2961, 2963, 2964, 2965, 2966, 2967, 2968, 2969, 2970, 2971, 2972, 2973, 2974, 2975, 2976, 2977, 2978, 2979, 2980, 2981, 2982, 2983, 2984, 2985, 2986, 2987, 2988, 2989, 2990, 2991, 2993, 2994, 2995, 2996, 2997, 2998, 2999, 3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011, 3012, 3013, 3014, 3015, 3016, 3017, 3018, 3019, 3020, 3021, 3024, 3025, 3027, 3029, 3030, 3032, 3033, 3034, 3036, 3037, 3038, 3039, 3041, 3042, 3043, 3044, 3045, 3046, 3047, 3048, 3049, 3051, 3053, 3054, 3056, 3057, 3059, 3061, 3062, 3063, 3064, 3065, 3066, 3067, 3069, 3070, 3071, 3072, 3073, 3074, 3076, 3078, 3079, 3080, 3081, 3082, 3083, 3084, 3085, 3086, 3087, 3089, 3090, 3091, 3093, 3094, 3095, 3096, 3097, 3098, 3100, 3101, 3103, 3104, 3105, 3106, 3108, 3110, 3112, 3113, 3114, 3116, 3117, 3118, 3119, 3120, 3121, 3122, 3124, 3125, 3128, 3129, 3130, 3131, 3132, 3133, 3135, 3136, 3137, 3138, 3139, 3140, 3141, 3142, 3143, 3144, 3145, 3146, 3148, 3149, 3150, 3151, 3152, 3154, 3155, 3156, 3157, 3158, 3159, 3160, 3161, 3162, 3163, 3164, 3166, 3167, 3168, 3169, 3170, 3171, 3172, 3173, 3174, 3175, 3176, 3177, 3178, 3179, 3180, 3181, 3182, 3183, 3184, 3186, 3188, 3190, 3192, 3193, 3194, 3195, 3196, 3197, 3202, 3203, 3204, 3206, 3208, 3211, 3212, 3213, 3214, 3216, 3217, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3227, 3228, 3229, 3230, 3231, 3232, 3233, 3235, 3236, 3237, 3238, 3240, 3241, 3242, 3243, 3246, 3248, 3249, 3250, 3251, 3252, 3253, 3254, 3255, 3256, 3258, 3259, 3260, 3263, 3264, 3265, 3266, 3267, 3268, 3269, 3270, 3271, 3272, 3274, 3276, 3277, 3278, 3279, 3280, 3282, 3284, 3285, 3287, 3288, 3290, 3292, 3293, 3294, 3295, 3296, 3297, 3298, 3299, 3300, 3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308, 3309, 3311, 3314, 3315, 3316, 3317, 3318, 3319, 3320, 3321, 3322, 3324, 3325, 3326, 3327, 3328, 3329, 3331, 3333, 3334, 3335, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3344, 3346, 3356, 3358, 3363, 3364, 3365, 3366, 3367, 3369, 3372, 3374, 3375, 3377, 3378, 3379, 3380, 3381, 3382, 3383, 3384, 3385, 3386, 3387, 3388, 3390, 3392, 3393, 3394, 3395, 3396, 3398, 3401, 3402, 3403, 3404, 3405, 3406, 3407, 3408, 3409, 3410, 3411, 3412, 3413, 3414, 3415, 3416, 3417, 3418, 3419, 3420, 3421, 3422, 3423, 3424, 3425, 3427, 3428, 3429, 3430, 3432, 3434, 3436, 3439, 3440, 3441, 3442, 3444, 3445, 3446, 3447, 3448, 3449, 3450, 3451, 3452, 3453, 3454, 3457, 3458, 3460, 3461, 3462, 3465, 3466, 3472, 3473, 3476, 3478, 3479, 3481, 3482, 3483, 3484, 3486, 3487, 3488, 3489, 3490, 3491, 3492, 3493, 3494, 3496, 3498, 3500, 3501, 3502, 3503, 3504, 3505, 3506, 3507, 3508, 3509, 3510, 3511, 3512, 3513, 3514, 3515, 3516, 3517, 3521, 3522, 3523, 3524, 3526, 3527, 3528, 3529, 3530, 3532, 3533, 3534, 3537, 3539, 3541, 3542, 3544, 3545, 3546, 3548, 3549, 3550, 3551, 3554, 3555, 3556, 3558, 3559, 3560, 3561, 3562, 3563, 3564, 3566, 3567, 3568, 3569, 3570, 3571, 3572, 3573, 3574, 3575, 3576, 3577, 3578, 3579, 3580, 3582, 3583, 3584, 3585, 3586, 3587, 3588, 3589, 3590, 3591, 3592, 3596, 3597, 3598, 3599, 3600, 3601, 3602, 3603, 3604, 3606, 3607, 3608, 3609, 3610, 3611, 3612, 3613, 3614, 3615, 3616, 3617, 3618, 3619, 3620, 3621, 3622, 3623, 3624, 3625, 3626, 3627, 3628, 3629, 3630, 3631, 3633, 3636, 3637, 3638, 3639, 3640, 3642, 3643, 3644, 3645, 3646, 3647, 3648, 3649, 3650, 3652, 3653, 3654, 3655, 3656, 3657, 3658, 3660, 3661, 3662, 3663, 3664, 3665, 3666, 3667, 3668, 3669, 3670, 3671, 3672, 3673, 3675, 3676, 3678, 3681, 3683, 3684, 3685, 3686, 3687, 3688, 3689, 3690, 3691, 3694, 3695, 3698, 3699, 3700, 3701, 3702, 3703, 3705, 3706, 3707, 3708, 3709, 3712, 3714, 3716, 3717, 3718, 3720, 3721, 3722, 3723, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3731, 3732, 3733, 3735, 3736, 3737, 3739, 3740, 3743, 3744, 3745, 3746, 3747, 3748, 3749, 3750, 3751, 3752, 3754, 3755, 3756, 3757, 3758, 3759, 3760, 3761, 3762, 3763, 3764, 3765, 3766, 3767, 3768, 3769, 3770, 3771, 3772, 3773, 3774, 3775, 3776, 3777, 3778, 3779, 3780, 3781, 3782, 3783, 3784, 3785, 3786, 3789, 3790, 3791, 3792, 3793, 3795, 3796, 3797, 3798, 3799, 3800, 3802, 3803, 3805, 3806, 3807, 3808, 3809, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3819, 3820, 3821, 3822, 3825, 3826, 3827, 3829, 3832, 3835, 3836, 3837, 3839, 3840, 3841, 3843, 3844, 3845, 3846, 3847, 3848, 3849, 3850, 3851, 3852, 3853, 3854, 3855, 3856, 3857, 3858, 3859, 3860, 3861, 3862, 3863, 3864, 3865, 3866, 3867, 3868, 3869, 3870, 3871, 3872, 3873, 3874, 3875, 3876, 3877, 3878, 3879, 3880, 3881, 3882, 3883, 3884, 3885, 3886, 3887, 3888, 3890, 3891, 3892, 3893, 3894, 3895, 3896, 3897, 3898, 3899, 3900, 3901, 3902, 3903, 3904, 3905, 3906, 3907, 3908, 3909, 3910, 3911, 3912, 3913, 3914, 3915, 3916, 3917, 3918, 3919, 3920, 3921, 3922, 3923, 3924, 3925, 3926, 3927, 3928, 3929, 3930, 3931, 3932, 3933, 3934, 3935, 3936, 3938, 3939, 3940, 3941, 3942, 3943, 3944, 3945, 3946, 3947, 3948, 3949, 3950, 3951, 3952]
	cur_file_list=[x for x in remaining_list if x not in pp]
	cur_file_list=new_from_svg=[245, 273, 335, 338, 339, 340, 342, 343, 354, 617, 640, 691, 695, 706, 830, 871, 890, 957, 976, 996, 998, 1166, 1173, 1219, 1438, 1441, 1556, 1989, 2094, 2131, 2165, 2173, 2225, 2274, 2314, 2370, 2380, 2946, 2968, 2985, 2986, 2995, 3173, 3214, 3233, 3333, 3381, 3386, 3461, 3691, 3717, 3731, 3740, 3841, 3951]
	cur_file_list.sort()
	cur_file=open('uniquesentences.txt','r')
	uniquesentences=cur_file.readlines()
	for cur_file_index in cur_file_list:
		cur_sent= uniquesentences[cur_file_index-1]
		cur_sent=cur_sent.strip()
		if len(cur_sent.split(" ")) > 2:
			print str(cur_file_index)+"$$"+cur_sent+"$$"
			pass
		pass
	pass

def get_lemma_pos_list(cur_word):
	# name, lemma_list, pos_list
	ret_list=[]
	pos_list=[]
	for cur_form in cur_word.forms:
		form_keys=cur_form.keys()
		for cur_key in form_keys:
			temp_string=str(cur_form[cur_key])
			if "http:sanskrit.inria" in temp_string:
				continue
				pass
			pos_list.append(cur_form[cur_key])
			pass
		pass
	lemma_list= cur_word.lemmas
	if '' in lemma_list :
		lemma_list.remove('')
		pass
	lemma_list=list(set(lemma_list))
	for cur_index in range(len(lemma_list)):
		if is_lemma_in_slp(lemma_list[cur_index]):
			continue
			pass
		lemma_list[cur_index]=utf_to_ascii((lemma_list[cur_index]).encode("raw_unicode_escape"))
		pass
	for cur_lemma in lemma_list:
		if '_' in cur_lemma:
			cur_lemma=cur_lemma.split('_')[0]
			pass
		for cur_morph_list in pos_list:
			if cur_morph_list.__class__.__name__ =='list':
				for cur_morph in cur_morph_list :
					if cur_morph.__class__.__name__ =='list':
						ret_list.append([ utf_to_ascii((cur_word.names).encode("raw_unicode_escape")), str(cur_lemma) , str(cur_morph[0])])
					else :
						ret_list.append([ utf_to_ascii((cur_word.names).encode("raw_unicode_escape")), str(cur_lemma) , str(cur_morph)])
					pass
				pass
			else :
				ret_list.append([ utf_to_ascii((cur_word.names).encode("raw_unicode_escape")), str(cur_lemma) , str(cur_morph_list)])
				pass
			pass
		pass
	return ret_list
	pass

def get_dcs_coverage(cur_tuple):
	cur_word=cur_tuple[0]
	cur_lemma=cur_tuple[1]
	cur_pos=cur_tuple[2]
	# word,lemma counts, garbage.
	ret_list=[0,0,0]
	if (cur_word in dcs_words_count_dict.keys()):
		ret_list[0]=dcs_words_count_dict[cur_word]
		pass
	if (cur_lemma in dcs_lemmas_count_dict.keys()):
		ret_list[1]=dcs_lemmas_count_dict[cur_lemma]
		pass	
	# if ret_list[1]==0:
	# 	cur_temp_str=cur_tuple[0]+"$$"+cur_tuple[1]
	# 	if cur_temp_str not in word_lemma_error_list:
	# 		word_lemma_error_list.append(cur_temp_str)
	# 		pass
	# 	pass
	return ret_list
	pass

def make_4k_pickle(cur_file_index):
	cur_file=pickle.load( open( "test/new/" + str(cur_file_index) + ".p", "rb" ) )
	cur_node_index=0
	node_dict={}
	for cur_index in range(len(cur_file.chunk)):
		cur_chunk=cur_file.chunk[cur_index]
		# for each of 11 chunks
		sorted_keys=cur_chunk.chunk_words.keys()
		sorted_keys.sort()
		if len(sorted_keys)==1:
			# anything goes
			# 0: ['tApasAnAm', 'tApasa', u'g. pl. m.', 0, [0, 250, 25]]
			cur_key=sorted_keys[0]
			for cur_word in cur_chunk.chunk_words[cur_key] :
				word_lemma_pos_list=get_lemma_pos_list(cur_word)
				if word_lemma_pos_list ==[]:
					node_dict[cur_node_index]=[utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape")) , None ,None ,cur_index,[0,0,0,]]
					cur_node_index+=1
					continue
					pass
				for cur_tuple in word_lemma_pos_list:
					node_dict[cur_node_index]=cur_tuple+[cur_index,get_dcs_coverage(cur_tuple)]
					cur_node_index+=1
					pass
				pass
			pass
		else:
			# all possible ones that are not compounds.
			for cur_key in sorted_keys:
				for cur_word in cur_chunk.chunk_words[cur_key] :
					word_lemma_pos_list=get_lemma_pos_list(cur_word)
					if word_lemma_pos_list ==[]:
						node_dict[cur_node_index]=[utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape")) , None ,None ,cur_index,[0,0,0,]]
						cur_node_index+=1
						continue
						pass
					if word_lemma_pos_list[0][2]=='iic.':
						continue
						pass
					for cur_tuple in word_lemma_pos_list:
						cur_tuple[0]=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
						node_dict[cur_node_index]=cur_tuple+[cur_index,get_dcs_coverage(cur_tuple)]
						cur_node_index+=1
						pass
					pass
				pass
			pass
		pass
	cur_sent=get_gold_sent(cur_file_index)
	temp_list=[]
	for x in cur_sent.content_list :
		# name, POS, dep_tag, from_tag, to_tag
		temp_list.append([convert_to_word_index(x.from_tag)  , convert_to_word_index(x.to_tag)  , x.dep_tag])
		pass

	print "sentence:" + str(cur_file_index)
	print "--------------"
	key_list=node_dict.keys()
	key_list.sort()
	for cur_key in key_list  : 
		cur_node=node_dict[cur_key]
		print str(cur_key) + ":" + str(cur_node)
		pass
	print "++++++++++++++"
	print temp_list
	print "=============="
	return node_dict
	pass

def refiner():
	cur_file=open('refine_manual.txt','r')
	# svg_list=[9, 15, 47, 53, 59, 65, 71, 73, 74, 76, 81, 88, 92, 94, 99, 106, 108, 109, 110, 111, 112, 113, 122, 123, 129, 142, 143, 145, 147, 150, 152, 154, 155, 160, 165, 167, 169, 174, 177, 179, 180, 183, 185, 188, 197, 198, 200, 208, 212, 215, 216, 223, 225, 226, 227, 234, 235, 239, 240, 243, 245, 254, 255, 256, 257, 258, 262, 263, 264, 266, 270, 271, 272, 273, 277, 279, 280, 281, 282, 284, 290, 291, 292, 293, 296, 297, 298, 299, 306, 307, 308, 309, 310, 312, 313, 314, 316, 324, 326, 332, 333, 334, 335, 338, 339, 340, 341, 342, 343, 346, 347, 348, 350, 351, 354, 359, 404, 430, 474, 487, 488, 499, 522, 523, 526, 530, 541, 574, 575, 581, 589, 591, 592, 596, 602, 609, 617, 618, 619, 620, 622, 624, 626, 629, 631, 634, 635, 640, 642, 643, 645, 647, 648, 649, 651, 652, 661, 668, 669, 677, 679, 683, 685, 690, 691, 693, 695, 697, 702, 703, 705, 706, 709, 715, 716, 730, 740, 741, 745, 771, 775, 776, 781, 782, 783, 786, 815, 816, 819, 822, 824, 830, 835, 840, 847, 852, 853, 855, 856, 859, 860, 861, 865, 866, 869, 871, 872, 873, 881, 884, 890, 891, 919, 936, 941, 943, 944, 952, 953, 954, 957, 959, 963, 966, 968, 972, 976, 980, 984, 986, 993, 996, 997, 998, 1000, 1001, 1003, 1005, 1007, 1008, 1011, 1013, 1014, 1015, 1027, 1031, 1034, 1036, 1037, 1040, 1041, 1042, 1043, 1044, 1050, 1054, 1064, 1081, 1088, 1093, 1094, 1096, 1102, 1108, 1117, 1118, 1133, 1134, 1154, 1158, 1166, 1173, 1174, 1177, 1190, 1192, 1216, 1219, 1227, 1283, 1338, 1340, 1347, 1348, 1350, 1364, 1369, 1376, 1378, 1405, 1409, 1420, 1423, 1425, 1436, 1438, 1441, 1447, 1448, 1459, 1463, 1468, 1483, 1490, 1491, 1503, 1521, 1524, 1526, 1530, 1531, 1538, 1549, 1556, 1568, 1572, 1585, 1605, 1614, 1625, 1634, 1635, 1644, 1645, 1646, 1649, 1656, 1659, 1669, 1717, 1731, 1745, 1765, 1770, 1773, 1776, 1790, 1794, 1823, 1832, 1896, 1915, 1921, 1946, 1954, 1969, 1976, 1984, 1989, 1999, 2009, 2016, 2022, 2026, 2029, 2033, 2039, 2043, 2045, 2058, 2061, 2069, 2086, 2089, 2094, 2100, 2103, 2108, 2109, 2126, 2130, 2131, 2165, 2173, 2194, 2198, 2200, 2215, 2223, 2225, 2240, 2242, 2243, 2255, 2274, 2314, 2316, 2318, 2344, 2353, 2357, 2359, 2360, 2370, 2379, 2380, 2396, 2449, 2452, 2454, 2456, 2474, 2477, 2481, 2542, 2546, 2556, 2557, 2559, 2583, 2586, 2595, 2636, 2649, 2669, 2732, 2733, 2753, 2778, 2791, 2799, 2805, 2814, 2821, 2826, 2828, 2831, 2835, 2843, 2852, 2855, 2872, 2877, 2884, 2886, 2888, 2891, 2896, 2901, 2911, 2930, 2936, 2946, 2948, 2957, 2968, 2978, 2985, 2986, 2988, 2992, 2995, 2997, 3003, 3015, 3018, 3026, 3027, 3036, 3039, 3055, 3058, 3097, 3101, 3103, 3160, 3173, 3195, 3208, 3214, 3219, 3231, 3233, 3244, 3248, 3275, 3283, 3311, 3313, 3319, 3333, 3344, 3346, 3348, 3349, 3350, 3352, 3368, 3381, 3386, 3391, 3395, 3405, 3418, 3423, 3461, 3468, 3479, 3526, 3533, 3537, 3545, 3554, 3563, 3582, 3634, 3658, 3673, 3691, 3697, 3703, 3708, 3711, 3717, 3731, 3735, 3740, 3741, 3763, 3764, 3779, 3782, 3790, 3791, 3798, 3821, 3840, 3841, 3869, 3888, 3896, 3908, 3920, 3935, 3951]
	line_data=cur_file.readlines()
	cur_file_index=None
	cur_node_index=None
	node_dict={}
	edge_list=[]
	refined_dict={}
	for cur_line in line_data:
		if ("sentence:" in cur_line):
			# new sentence
			cur_file_index=int(cur_line.split(":")[1])
			cur_node_index=0
			node_dict={}
			edge_list=[]
			pass
		elif (":[" in cur_line):
			# new word
			print line_data.index(cur_line)
			print cur_line
			node_data=eval(cur_line.split(":")[1])
			node_dict[cur_node_index]=node_data
			cur_node_index+=1
			pass
		elif ("[[" in cur_line):
			# edge_list
			print line_data.index(cur_line)
			print cur_line
			edge_list=eval(cur_line)
			if cur_file_index in svg_list:
				refined_dict[cur_file_index]=[node_dict, edge_list, edge_list]
				pass
			if len(node_dict.keys())!=(cur_node_index):
				print "fatal error "
				exit()
				pass
			cur_node_index=None
			pass
		pass
	for cur_key in refined_dict.keys():
		print "sentence : "+str(cur_key)
	# 	print "----------------------"
	# 	print str(refined_dict[cur_key][0])
	# 	print "++++++++++++++++++++++"
	# 	print str(refined_dict[cur_key][1])
	# 	print "======================"
		pass
	print len(refined_dict.keys())
	pickle.dump(refined_dict,open('manual_refined_dict.p' , 'w'))
	pass

def convert_to_word_index(a_string):
	if is_int(a_string):
		return int(a_string) -1
		pass
	else :
		return None
		pass
	pass

def get_remaining():
	cur_file=open('uniquesentences.txt','r')
	uniquesentences=cur_file.readlines()
	file_list_1140=[1, 2, 3, 4, 6, 9, 11, 13, 14, 15, 16, 18, 29, 34, 42, 43, 47, 48, 50, 51, 52, 53, 54, 56, 58, 67, 71, 74, 76, 84, 90, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 107, 108, 115, 116, 117, 119, 121, 122, 124, 125, 126, 127, 128, 130, 138, 142, 143, 144, 145, 146, 147, 148, 149, 150, 152, 153, 155, 156, 157, 165, 167, 168, 170, 171, 172, 174, 175, 176, 184, 186, 188, 192, 195, 196, 198, 200, 201, 203, 205, 208, 211, 213, 214, 215, 217, 219, 222, 223, 228, 229, 230, 232, 233, 235, 236, 237, 238, 239, 241, 244, 246, 247, 248, 249, 250, 251, 252, 253, 260, 261, 262, 264, 265, 269, 270, 274, 275, 276, 282, 283, 285, 286, 287, 288, 289, 291, 292, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 311, 317, 320, 321, 326, 328, 331, 332, 334, 336, 352, 353, 355, 366, 368, 393, 394, 397, 423, 429, 434, 437, 441, 445, 446, 451, 458, 484, 508, 514, 518, 522, 523, 526, 528, 530, 532, 539, 541, 560, 564, 572, 573, 576, 577, 580, 581, 582, 591, 595, 596, 597, 598, 600, 601, 602, 604, 605, 606, 607, 610, 614, 615, 616, 619, 620, 623, 625, 628, 630, 632, 634, 636, 638, 639, 641, 642, 644, 646, 649, 652, 653, 654, 655, 656, 657, 658, 659, 660, 662, 663, 664, 665, 666, 667, 669, 670, 671, 672, 673, 674, 675, 676, 677, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 692, 693, 694, 696, 698, 699, 700, 701, 702, 703, 704, 707, 709, 710, 711, 712, 713, 714, 715, 717, 719, 720, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 741, 742, 743, 744, 746, 747, 748, 749, 751, 752, 753, 754, 755, 756, 757, 759, 760, 761, 762, 764, 765, 766, 767, 768, 769, 772, 773, 774, 775, 776, 777, 779, 780, 781, 782, 783, 784, 785, 787, 788, 789, 790, 791, 792, 793, 794, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 817, 818, 821, 823, 824, 825, 826, 827, 828, 831, 832, 833, 834, 836, 837, 838, 839, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 854, 857, 859, 861, 862, 863, 864, 865, 867, 868, 874, 875, 877, 878, 879, 880, 882, 885, 886, 887, 888, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 906, 907, 908, 909, 910, 911, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 937, 938, 939, 940, 941, 942, 943, 945, 946, 947, 948, 949, 950, 951, 953, 955, 956, 958, 959, 960, 961, 962, 963, 964, 965, 968, 969, 970, 971, 972, 973, 974, 975, 977, 978, 979, 981, 982, 983, 985, 987, 988, 989, 990, 991, 992, 993, 994, 995, 997, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1012, 1013, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1032, 1035, 1037, 1038, 1040, 1045, 1046, 1051, 1052, 1054, 1055, 1061, 1067, 1070, 1072, 1073, 1075, 1076, 1087, 1094, 1097, 1100, 1103, 1123, 1124, 1134, 1137, 1145, 1147, 1150, 1151, 1152, 1153, 1159, 1171, 1179, 1180, 1182, 1183, 1187, 1189, 1190, 1192, 1194, 1200, 1201, 1208, 1209, 1216, 1218, 1220, 1221, 1224, 1225, 1239, 1241, 1242, 1248, 1254, 1259, 1261, 1267, 1268, 1270, 1293, 1295, 1301, 1303, 1305, 1306, 1317, 1318, 1321, 1323, 1324, 1327, 1331, 1332, 1334, 1335, 1336, 1339, 1340, 1341, 1343, 1348, 1351, 1358, 1359, 1361, 1365, 1372, 1375, 1377, 1379, 1390, 1391, 1393, 1397, 1405, 1407, 1416, 1422, 1425, 1426, 1428, 1432, 1435, 1437, 1439, 1443, 1459, 1468, 1469, 1470, 1477, 1478, 1479, 1482, 1484, 1486, 1494, 1495, 1503, 1508, 1522, 1524, 1528, 1536, 1537, 1539, 1541, 1549, 1551, 1553, 1555, 1558, 1559, 1563, 1564, 1565, 1569, 1574, 1585, 1586, 1598, 1600, 1601, 1614, 1625, 1626, 1627, 1633, 1634, 1636, 1638, 1639, 1643, 1646, 1650, 1654, 1656, 1657, 1658, 1662, 1672, 1673, 1679, 1680, 1691, 1693, 1697, 1702, 1712, 1717, 1720, 1721, 1726, 1729, 1744, 1746, 1761, 1767, 1769, 1774, 1775, 1780, 1781, 1787, 1790, 1791, 1793, 1795, 1803, 1805, 1808, 1809, 1810, 1816, 1828, 1853, 1856, 1859, 1873, 1876, 1878, 1879, 1881, 1883, 1887, 1896, 1897, 1898, 1902, 1913, 1925, 1953, 1957, 1958, 1959, 1960, 1961, 1965, 1967, 1970, 1980, 1983, 1986, 1987, 1992, 2008, 2009, 2022, 2027, 2028, 2030, 2032, 2039, 2043, 2055, 2056, 2058, 2061, 2063, 2074, 2080, 2086, 2089, 2093, 2100, 2108, 2110, 2130, 2141, 2151, 2158, 2162, 2174, 2185, 2194, 2197, 2198, 2200, 2204, 2206, 2210, 2214, 2216, 2218, 2224, 2239, 2243, 2249, 2253, 2255, 2257, 2276, 2281, 2292, 2293, 2305, 2307, 2308, 2309, 2310, 2312, 2313, 2315, 2316, 2317, 2318, 2327, 2328, 2329, 2331, 2334, 2338, 2341, 2345, 2350, 2352, 2353, 2354, 2356, 2358, 2360, 2363, 2372, 2397, 2398, 2411, 2414, 2419, 2427, 2432, 2449, 2460, 2465, 2466, 2468, 2469, 2477, 2481, 2484, 2489, 2492, 2493, 2498, 2507, 2514, 2522, 2525, 2526, 2528, 2529, 2536, 2537, 2538, 2541, 2543, 2544, 2554, 2558, 2563, 2564, 2565, 2566, 2567, 2568, 2586, 2595, 2601, 2617, 2621, 2625, 2626, 2627, 2635, 2645, 2646, 2660, 2679, 2688, 2693, 2699, 2700, 2705, 2713, 2718, 2719, 2728, 2732, 2736, 2737, 2741, 2743, 2746, 2753, 2767, 2769, 2778, 2786, 2790, 2805, 2806, 2810, 2815, 2819, 2825, 2827, 2828, 2829, 2830, 2831, 2835, 2840, 2845, 2849, 2852, 2854, 2861, 2868, 2871, 2873, 2876, 2877, 2881, 2882, 2883, 2888, 2890, 2896, 2898, 2914, 2917, 2930, 2932, 2948, 2955, 2962, 2992, 3022, 3023, 3026, 3028, 3031, 3035, 3040, 3050, 3052, 3055, 3058, 3060, 3068, 3075, 3077, 3088, 3092, 3099, 3102, 3107, 3109, 3111, 3115, 3123, 3126, 3127, 3134, 3147, 3153, 3165, 3185, 3187, 3189, 3191, 3198, 3199, 3200, 3201, 3205, 3207, 3209, 3210, 3215, 3218, 3226, 3234, 3239, 3244, 3245, 3247, 3257, 3261, 3262, 3273, 3275, 3281, 3283, 3286, 3289, 3291, 3310, 3312, 3313, 3323, 3330, 3332, 3343, 3345, 3347, 3348, 3349, 3350, 3351, 3352, 3353, 3354, 3355, 3357, 3359, 3360, 3361, 3362, 3368, 3370, 3371, 3373, 3376, 3389, 3391, 3397, 3399, 3400, 3426, 3431, 3433, 3435, 3437, 3438, 3443, 3455, 3456, 3459, 3463, 3464, 3467, 3468, 3469, 3470, 3471, 3474, 3475, 3477, 3480, 3485, 3495, 3497, 3499, 3518, 3519, 3520, 3525, 3531, 3535, 3536, 3538, 3540, 3543, 3547, 3552, 3553, 3557, 3565, 3581, 3593, 3594, 3595, 3605, 3632, 3634, 3635, 3641, 3651, 3659, 3674, 3677, 3679, 3680, 3682, 3692, 3693, 3696, 3697, 3704, 3710, 3711, 3713, 3715, 3719, 3734, 3738, 3741, 3742, 3753, 3787, 3788, 3794, 3801, 3804, 3823, 3824, 3828, 3830, 3831, 3833, 3834, 3838, 3842, 3889, 3937]
	remaining_list=[]
	for cur_file_index in range(1,len(uniquesentences)+1):
		if cur_file_index in file_list_1140:
			continue
			pass
		cur_sent= uniquesentences[cur_file_index-1]
		cur_sent=cur_sent.strip()
		remaining_list.append(cur_file_index)
		if len(cur_sent.split(" ")) > 2:
			print str(cur_file_index)+"$$"+cur_sent+"$$"
			pass
		pass
	print remaining_list
	pass

def old():
	# get_input_sentences()
	# get_remaining()
	# cur_file=pickle.load( open( "test/" + str(606) + ".p", "rb" ) )
	# cur_file.print_sents()
	file_list_1998=[60,1143,1144,1202,1660,7,8,10,12,17,19,20,21,22,23,24,25,27,30,31,32,33,35,37,39,40,41,44,45,46,49,57,59,61,62,63,64,65,66,68,73,77,78,79,81,82,85,87,88,89,92,93,94,99,106,109,110,111,112,113,114,120,123,129,131,132,133,134,135,136,137,139,140,151,154,159,160,161,162,163,164,166,169,173,177,179,180,181,182,183,185,187,189,190,191,193,194,197,199,202,204,206,207,209,210,212,216,218,220,221,224,225,226,227,231,234,240,242,243,254,255,256,257,258,263,266,271,272,277,278,279,280,281,284,290,293,308,309,310,312,313,314,315,316,318,319,323,324,325,329,333,341,345,346,347,348,349,350,351,356,357,358,359,360,361,362,363,364,365,367,369,371,372,373,374,375,376,377,380,381,382,383,384,385,386,388,390,391,392,395,396,399,401,402,403,404,407,408,410,412,413,415,416,417,419,420,424,427,428,430,431,435,436,438,439,442,443,444,447,449,450,453,454,455,457,460,461,462,465,467,468,470,474,475,476,479,480,482,483,486,487,488,490,491,492,494,495,497,498,499,500,502,503,504,505,506,507,510,511,512,513,516,517,520,521,524,525,527,529,537,538,540,543,544,545,546,547,548,551,553,555,556,557,561,563,568,569,570,574,575,578,583,584,587,588,589,592,593,594,603,609,611,612,618,621,622,624,626,627,629,631,633,635,643,645,647,648,650,651,661,668,679,690,697,705,716,718,721,740,745,750,763,770,771,778,786,795,815,816,819,820,822,829,835,840,853,855,856,858,860,866,869,870,872,873,876,881,884,889,891,936,944,952,954,966,967,980,984,986,1011,1014,1027,1031,1033,1034,1036,1041,1042,1043,1044,1047,1049,1050,1056,1057,1059,1060,1063,1064,1065,1069,1071,1074,1077,1079,1080,1081,1082,1083,1084,1085,1086,1088,1090,1091,1092,1093,1095,1096,1098,1099,1101,1102,1104,1105,1106,1107,1108,1110,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1125,1127,1128,1130,1131,1133,1135,1136,1138,1139,1141,1142,1144,1146,1148,1149,1154,1155,1156,1157,1158,1160,1161,1163,1164,1167,1168,1169,1174,1176,1177,1181,1184,1185,1186,1188,1191,1193,1195,1198,1199,1202,1203,1204,1205,1206,1207,1210,1211,1212,1213,1214,1215,1217,1222,1223,1226,1227,1229,1231,1232,1233,1234,1235,1236,1237,1238,1240,1243,1249,1251,1255,1256,1257,1260,1262,1264,1265,1266,1269,1272,1273,1274,1275,1276,1277,1278,1279,1280,1281,1282,1283,1284,1285,1286,1288,1289,1290,1291,1292,1294,1296,1297,1298,1299,1300,1302,1307,1311,1314,1315,1319,1325,1328,1333,1337,1338,1342,1344,1345,1346,1347,1349,1350,1352,1354,1356,1357,1360,1364,1366,1369,1370,1371,1373,1376,1378,1381,1382,1383,1384,1385,1386,1387,1388,1389,1392,1395,1396,1398,1399,1400,1401,1403,1404,1406,1408,1409,1411,1412,1413,1414,1418,1420,1423,1424,1427,1429,1430,1431,1433,1434,1436,1440,1442,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1461,1462,1463,1465,1466,1467,1476,1480,1481,1483,1485,1488,1489,1490,1491,1493,1496,1497,1498,1499,1502,1504,1506,1509,1511,1512,1513,1514,1515,1516,1517,1520,1521,1523,1525,1526,1527,1529,1530,1531,1532,1533,1534,1535,1538,1542,1544,1545,1546,1548,1552,1560,1561,1562,1566,1567,1568,1570,1571,1572,1573,1575,1578,1581,1582,1583,1584,1587,1588,1589,1590,1591,1593,1596,1597,1599,1603,1605,1606,1608,1609,1610,1611,1612,1613,1617,1618,1621,1622,1623,1624,1628,1630,1631,1632,1635,1637,1641,1644,1645,1649,1651,1655,1659,1660,1661,1663,1664,1665,1666,1667,1668,1669,1670,1671,1674,1675,1676,1677,1678,1681,1685,1686,1687,1688,1689,1692,1694,1695,1696,1698,1699,1701,1703,1705,1706,1707,1708,1709,1711,1713,1714,1715,1716,1718,1719,1723,1724,1725,1727,1728,1731,1732,1734,1735,1737,1738,1740,1741,1742,1743,1745,1749,1750,1751,1756,1757,1758,1759,1760,1762,1764,1765,1766,1768,1770,1771,1772,1773,1776,1778,1782,1783,1785,1786,1788,1789,1792,1794,1797,1798,1800,1801,1804,1806,1807,1812,1813,1817,1819,1820,1822,1823,1824,1825,1826,1827,1829,1830,1832,1834,1838,1839,1840,1841,1842,1844,1846,1847,1848,1849,1854,1855,1857,1858,1860,1861,1865,1866,1867,1869,1870,1871,1872,1884,1886,1895,1899,1900,1903,1904,1907,1909,1911,1915,1917,1918,1919,1920,1921,1922,1923,1924,1927,1928,1929,1930,1931,1932,1933,1934,1935,1938,1940,1941,1942,1943,1945,1946,1948,1949,1952,1954,1955,1962,1966,1969,1971,1972,1973,1974,1975,1976,1979,1982,1984,1988,1990,1991,1993,1994,1999,2000,2001,2003,2004,2005,2007,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2024,2025,2026,2029,2031,2033,2036,2037,2038,2040,2042,2044,2045,2046,2047,2048,2050,2051,2053,2054,2057,2059,2062,2064,2065,2066,2067,2068,2069,2073,2075,2078,2079,2082,2084,2085,2087,2090,2091,2092,2095,2101,2102,2103,2105,2109,2111,2112,2113,2114,2115,2119,2120,2123,2124,2125,2126,2128,2129,2132,2134,2135,2137,2138,2139,2140,2144,2145,2146,2147,2148,2149,2150,2157,2160,2161,2163,2167,2168,2169,2170,2171,2172,2177,2178,2179,2180,2181,2183,2186,2187,2188,2189,2190,2191,2192,2193,2195,2196,2199,2202,2203,2208,2209,2211,2212,2215,2221,2223,2228,2229,2231,2232,2233,2234,2235,2237,2238,2240,2241,2242,2246,2247,2250,2251,2252,2254,2256,2258,2260,2262,2263,2264,2265,2266,2269,2270,2275,2280,2284,2286,2287,2290,2296,2297,2298,2299,2301,2303,2306,2319,2320,2321,2324,2330,2332,2333,2336,2337,2340,2342,2343,2344,2346,2347,2348,2349,2351,2355,2357,2359,2362,2364,2365,2366,2367,2369,2371,2374,2376,2377,2378,2379,2381,2382,2386,2387,2388,2389,2390,2391,2392,2393,2394,2395,2396,2401,2406,2407,2408,2409,2412,2413,2415,2418,2421,2423,2424,2426,2428,2431,2433,2436,2437,2438,2441,2443,2448,2450,2451,2452,2453,2454,2455,2456,2457,2458,2459,2461,2462,2463,2464,2467,2470,2471,2472,2473,2474,2475,2476,2478,2479,2480,2483,2485,2486,2487,2488,2490,2491,2494,2495,2499,2500,2501,2502,2503,2504,2505,2508,2510,2511,2512,2513,2515,2516,2517,2518,2519,2520,2521,2523,2527,2530,2531,2532,2533,2534,2535,2539,2540,2542,2545,2546,2548,2553,2555,2556,2557,2559,2560,2561,2562,2569,2570,2571,2572,2574,2575,2576,2577,2578,2580,2581,2582,2583,2585,2588,2589,2590,2591,2592,2593,2594,2598,2599,2600,2602,2603,2605,2608,2609,2610,2612,2613,2615,2616,2620,2622,2623,2624,2628,2629,2631,2632,2633,2636,2637,2638,2639,2642,2644,2649,2650,2651,2652,2653,2655,2656,2659,2661,2663,2664,2665,2666,2667,2668,2669,2670,2671,2673,2674,2675,2677,2678,2680,2681,2682,2683,2685,2686,2689,2690,2691,2692,2695,2696,2697,2698,2701,2702,2703,2708,2710,2714,2717,2721,2722,2724,2725,2726,2727,2729,2730,2731,2733,2734,2738,2739,2740,2744,2748,2751,2752,2754,2759,2760,2762,2763,2764,2765,2770,2771,2776,2777,2779,2780,2781,2782,2783,2784,2785,2787,2791,2792,2794,2795,2796,2797,2799,2800,2801,2802,2803,2804,2807,2809,2811,2812,2813,2814,2820,2821,2823,2824,2826,2832,2833,2836,2838,2839,2843,2846,2847,2853,2855,2856,2857,2858,2859,2860,2863,2865,2866,2872,2874,2875,2878,2880,2884,2885,2886,2887,2889,2891,2892,2895,2900,2901,2902,2903,2904,2905,2906,2908,2910,2911,2915,2916,2919,2920,2921,2922,2923,2924,2925,2928,2929,2931,2934,2935,2936,2937,2938,2939,2940,2941,2942,2944,2945,2947,2949,2950,2951,2952,2953,2954,2956,2957,2958,2964,2965,2966,2967,2970,2971,2972,2974,2975,2976,2978,2979,2980,2981,2982,2983,2984,2987,2988,2990,2991,2993,2996,2997,2998,2999,3000,3003,3004,3005,3008,3011,3012,3013,3015,3016,3018,3019,3020,3021,3024,3025,3027,3030,3032,3033,3034,3036,3037,3038,3039,3042,3043,3044,3045,3047,3048,3049,3051,3056,3057,3061,3062,3063,3064,3065,3067,3069,3070,3071,3072,3073,3074,3076,3078,3079,3080,3081,3082,3083,3085,3086,3087,3089,3090,3091,3093,3094,3095,3096,3097,3098,3100,3101,3103,3104,3105,3106,3112,3114,3116,3117,3118,3121,3122,3125,3128,3129,3130,3131,3132,3133,3136,3137,3138,3139,3140,3142,3143,3144,3146,3149,3154,3156,3157,3158,3159,3160,3161,3164,3166,3168,3169,3174,3176,3177,3178,3179,3180,3181,3182,3183,3186,3188,3190,3192,3193,3195,3196,3202,3206,3208,3211,3217,3219,3220,3221,3222,3223,3224,3225,3228,3230,3231,3232,3236,3237,3238,3240,3241,3243,3248,3249,3250,3254,3255,3258,3263,3264,3265,3266,3267,3270,3271,3272,3274,3276,3277,3278,3279,3282,3284,3285,3288,3292,3293,3294,3296,3298,3299,3300,3301,3302,3303,3304,3306,3307,3308,3311,3314,3316,3319,3320,3322,3324,3325,3326,3328,3329,3334,3336,3337,3338,3339,3340,3341,3342,3344,3346,3358,3363,3365,3366,3367,3369,3372,3374,3375,3377,3378,3379,3380,3383,3385,3387,3393,3394,3395,3396,3401,3402,3403,3405,3406,3408,3409,3410,3416,3417,3418,3419,3421,3423,3425,3427,3428,3429,3432,3436,3445,3446,3447,3448,3449,3451,3452,3453,3454,3466,3472,3473,3476,3478,3479,3481,3482,3483,3484,3486,3487,3488,3489,3490,3491,3492,3493,3496,3500,3503,3504,3505,3508,3511,3512,3513,3514,3516,3517,3521,3522,3523,3526,3527,3528,3529,3530,3532,3533,3537,3541,3542,3544,3545,3548,3550,3551,3554,3555,3556,3562,3563,3567,3569,3570,3573,3574,3575,3577,3578,3579,3580,3582,3584,3585,3586,3588,3590,3591,3596,3597,3598,3600,3601,3602,3603,3606,3607,3610,3611,3612,3614,3615,3616,3618,3621,3624,3626,3627,3628,3629,3630,3633,3636,3637,3638,3639,3643,3644,3646,3647,3649,3652,3654,3655,3656,3657,3658,3660,3661,3662,3664,3665,3666,3669,3671,3672,3673,3675,3676,3678,3681,3684,3687,3688,3689,3694,3699,3700,3702,3703,3705,3706,3708,3709,3716,3718,3720,3721,3724,3725,3726,3727,3728,3729,3730,3733,3735,3736,3737,3744,3745,3746,3747,3748,3750,3752,3754,3755,3756,3759,3760,3763,3764,3765,3766,3768,3769,3770,3771,3775,3776,3778,3779,3780,3781,3782,3783,3784,3785,3786,3790,3791,3792,3796,3798,3799,3802,3803,3805,3806,3807,3808,3810,3811,3812,3813,3814,3815,3816,3817,3818,3819,3821,3822,3825,3826,3827,3829,3832,3835,3836,3837,3839,3840,3845,3846,3847,3848,3849,3852,3853,3854,3855,3856,3857,3859,3860,3862,3863,3864,3865,3866,3867,3868,3869,3870,3872,3879,3883,3884,3885,3888,3891,3892,3893,3895,3896,3897,3898,3902,3904,3906,3907,3908,3909,3910,3919,3920,3921,3923,3924,3926,3929,3930,3931,3932,3934,3935,3936,3938,3939,3940,3941,3942,3946,3947,3948]
	file_list=file_list_1998
	error_list=[60, 1143, 1144, 1202, 1660, 1144, 1202, 1660, 1686, 1711, 2053, 2181, 2738, 3030, 3177, 3511]
	file_list=[61, 62, 63, 64, 66, 68, 77, 78, 79, 82, 85, 87, 89, 93, 114, 120, 131, 132, 133, 134, 135, 136, 137, 139, 140, 151, 159, 161, 162, 163, 164, 166, 173, 181, 182, 187, 189, 190, 191, 193, 194, 199, 202, 204, 206, 207, 209, 210, 218, 220, 221, 224, 231, 242, 278, 315, 318, 319, 323, 325, 329, 345, 349, 356, 357, 358, 360, 361, 362, 363, 365, 367, 369, 371, 372, 373, 374, 375, 376, 377, 380, 381, 382, 383, 384, 385, 386, 388, 390, 392, 395, 396, 399, 402, 403, 407, 408, 410, 412, 413, 415, 416, 417, 419, 420, 424, 427, 428, 431, 435, 436, 438, 439, 442, 443, 444, 447, 449, 450, 453, 454, 455, 457, 460, 461, 462, 465, 467, 468, 470, 475, 476, 479, 480, 482, 483, 486, 490, 491, 492, 494, 495, 498, 500, 502, 503, 504, 505, 506, 507, 510, 511, 512, 513, 516, 517, 520, 521, 524, 525, 527, 529, 537, 538, 540, 543, 544, 545, 546, 547, 548, 551, 553, 555, 556, 557, 561, 563, 568, 569, 570, 578, 583, 584, 587, 588, 593, 594, 603, 611, 612, 621, 627, 633, 650, 718, 721, 750, 763, 770, 778, 795, 820, 829, 858, 870, 876, 889, 967, 1033, 1047, 1049, 1056, 1057, 1059, 1060, 1063, 1065, 1069, 1071, 1074, 1077, 1079, 1080, 1082, 1083, 1084, 1085, 1086, 1090, 1091, 1092, 1095, 1098, 1099, 1104, 1105, 1106, 1107, 1110, 1112, 1113, 1114, 1115, 1116, 1119, 1120, 1121, 1125, 1127, 1128, 1130, 1131, 1135, 1136, 1138, 1142, 1146, 1148, 1149, 1155, 1156, 1157, 1160, 1161, 1163, 1164, 1167, 1168, 1169, 1176, 1181, 1184, 1185, 1186, 1188, 1191, 1193, 1195, 1198, 1199, 1203, 1204, 1205, 1206, 1207, 1210, 1211, 1212, 1213, 1214, 1215, 1217, 1222, 1223, 1226, 1229, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1240, 1243, 1249, 1251, 1255, 1256, 1257, 1260, 1262, 1264, 1265, 1266, 1269, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1284, 1285, 1286, 1289, 1290, 1291, 1292, 1294, 1296, 1297, 1298, 1299, 1300, 1302, 1307, 1311, 1314, 1315, 1319, 1325, 1333, 1337, 1342, 1344, 1345, 1346, 1349, 1352, 1354, 1356, 1357, 1360, 1366, 1370, 1371, 1373, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1392, 1395, 1396, 1398, 1399, 1400, 1401, 1403, 1404, 1406, 1408, 1411, 1412, 1413, 1414, 1418, 1424, 1427, 1429, 1430, 1431, 1433, 1434, 1440, 1442, 1446, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1461, 1462, 1465, 1466, 1467, 1476, 1480, 1481, 1485, 1488, 1489, 1493, 1496, 1497, 1498, 1499, 1502, 1504, 1506, 1509, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1520, 1523, 1525, 1527, 1529, 1532, 1533, 1534, 1535, 1542, 1544, 1545, 1546, 1548, 1552, 1560, 1561, 1562, 1566, 1567, 1570, 1571, 1573, 1575, 1578, 1581, 1582, 1583, 1584, 1587, 1588, 1589, 1590, 1591, 1593, 1596, 1597, 1599, 1603, 1606, 1608, 1609, 1610, 1611, 1612, 1613, 1617, 1618, 1621, 1622, 1623, 1624, 1628, 1630, 1631, 1632, 1637, 1641, 1651, 1655, 1661, 1663, 1664, 1665, 1666, 1667, 1668, 1670, 1671, 1675, 1676, 1677, 1681, 1685, 1687, 1688, 1689, 1692, 1694, 1695, 1696, 1698, 1699, 1701, 1703, 1705, 1706, 1707, 1708, 1709, 1713, 1714, 1715, 1718, 1719, 1723, 1724, 1725, 1727, 1728, 1732, 1734, 1735, 1737, 1738, 1740, 1741, 1742, 1743, 1749, 1750, 1751, 1756, 1757, 1758, 1759, 1760, 1762, 1764, 1766, 1768, 1771, 1772, 1778, 1782, 1783, 1785, 1786, 1788, 1789, 1792, 1797, 1798, 1800, 1801, 1804, 1806, 1807, 1812, 1813, 1817, 1819, 1820, 1822, 1824, 1825, 1826, 1827, 1829, 1830, 1834, 1838, 1839, 1840, 1841, 1842, 1844, 1846, 1847, 1848, 1849, 1854, 1855, 1857, 1858, 1860, 1861, 1865, 1866, 1867, 1869, 1870, 1871, 1872, 1884, 1886, 1895, 1899, 1900, 1903, 1904, 1907, 1909, 1911, 1917, 1918, 1919, 1920, 1922, 1923, 1924, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1938, 1940, 1941, 1942, 1943, 1945, 1948, 1949, 1952, 1955, 1962, 1966, 1971, 1972, 1973, 1974, 1975, 1979, 1982, 1988, 1990, 1991, 1993, 1994, 2000, 2001, 2003, 2004, 2005, 2007, 2010, 2011, 2012, 2013, 2015, 2017, 2018, 2019, 2020, 2021, 2024, 2025, 2031, 2036, 2037, 2038, 2040, 2042, 2044, 2046, 2047, 2048, 2050, 2051, 2054, 2057, 2059, 2062, 2064, 2065, 2066, 2067, 2068, 2073, 2075, 2078, 2079, 2082, 2084, 2085, 2087, 2090, 2091, 2092, 2095, 2101, 2102, 2105, 2111, 2112, 2113, 2114, 2115, 2119, 2120, 2123, 2124, 2125, 2128, 2129, 2132, 2134, 2135, 2137, 2138, 2139, 2140, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2157, 2160, 2161, 2163, 2167, 2168, 2169, 2170, 2171, 2172, 2177, 2179, 2180, 2183, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2195, 2196, 2199, 2202, 2203, 2208, 2209, 2211, 2212, 2221, 2228, 2229, 2231, 2232, 2233, 2234, 2235, 2237, 2238, 2241, 2246, 2247, 2250, 2251, 2252, 2256, 2258, 2260, 2262, 2263, 2264, 2265, 2266, 2269, 2270, 2275, 2280, 2284, 2286, 2287, 2290, 2296, 2297, 2298, 2299, 2301, 2303, 2306, 2319, 2320, 2324, 2330, 2332, 2333, 2336, 2340, 2342, 2343, 2346, 2347, 2348, 2349, 2351, 2355, 2362, 2364, 2365, 2366, 2367, 2369, 2371, 2374, 2376, 2377, 2378, 2381, 2382, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2401, 2406, 2407, 2408, 2409, 2412, 2413, 2415, 2418, 2421, 2423, 2424, 2426, 2428, 2431, 2433, 2436, 2437, 2438, 2441, 2443, 2448, 2450, 2451, 2453, 2455, 2457, 2458, 2459, 2461, 2462, 2463, 2464, 2467, 2470, 2472, 2473, 2475, 2476, 2478, 2479, 2480, 2483, 2485, 2486, 2487, 2488, 2490, 2491, 2494, 2495, 2499, 2500, 2501, 2502, 2503, 2505, 2508, 2510, 2511, 2512, 2513, 2516, 2517, 2518, 2519, 2520, 2521, 2523, 2527, 2530, 2531, 2532, 2533, 2534, 2535, 2539, 2545, 2548, 2553, 2555, 2560, 2561, 2562, 2569, 2570, 2571, 2572, 2574, 2575, 2576, 2577, 2578, 2580, 2581, 2582, 2585, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2598, 2599, 2600, 2602, 2603, 2605, 2608, 2609, 2610, 2612, 2613, 2615, 2616, 2620, 2622, 2623, 2624, 2628, 2629, 2631, 2632, 2633, 2637, 2638, 2639, 2642, 2644, 2650, 2651, 2652, 2653, 2655, 2656, 2659, 2661, 2663, 2664, 2665, 2666, 2667, 2668, 2670, 2671, 2673, 2674, 2675, 2677, 2678, 2680, 2681, 2682, 2683, 2685, 2686, 2689, 2690, 2691, 2692, 2695, 2696, 2697, 2698, 2701, 2702, 2703, 2708, 2710, 2714, 2717, 2721, 2722, 2724, 2725, 2726, 2727, 2729, 2730, 2731, 2734, 2739, 2740, 2744, 2748, 2751, 2752, 2754, 2760, 2762, 2763, 2764, 2765, 2770, 2771, 2776, 2777, 2779, 2780, 2781, 2782, 2783, 2784, 2785, 2787, 2792, 2794, 2795, 2796, 2797, 2801, 2802, 2803, 2804, 2807, 2809, 2811, 2813, 2820, 2823, 2824, 2832, 2833, 2836, 2838, 2839, 2847, 2853, 2856, 2857, 2858, 2859, 2860, 2863, 2865, 2866, 2874, 2878, 2880, 2889, 2895, 2900, 2904, 2905, 2906, 2908, 2910, 2915, 2916, 2919, 2920, 2922, 2923, 2924, 2928, 2929, 2931, 2935, 2938, 2939, 2940, 2941, 2942, 2944, 2945, 2947, 2949, 2950, 2951, 2952, 2953, 2954, 2956, 2958, 2964, 2966, 2967, 2971, 2972, 2975, 2980, 2981, 2982, 2984, 2987, 2990, 2991, 2993, 2996, 2998, 2999, 3000, 3004, 3005, 3008, 3011, 3012, 3013, 3016, 3019, 3020, 3021, 3024, 3025, 3032, 3033, 3034, 3037, 3038, 3042, 3043, 3044, 3045, 3047, 3048, 3049, 3051, 3056, 3057, 3061, 3062, 3063, 3064, 3065, 3067, 3069, 3070, 3071, 3072, 3073, 3074, 3076, 3078, 3079, 3080, 3081, 3082, 3083, 3086, 3087, 3089, 3090, 3091, 3093, 3094, 3095, 3096, 3098, 3100, 3105, 3106, 3112, 3114, 3116, 3117, 3118, 3121, 3122, 3125, 3128, 3129, 3130, 3131, 3132, 3133, 3136, 3137, 3138, 3139, 3140, 3142, 3143, 3144, 3146, 3149, 3154, 3156, 3157, 3158, 3161, 3164, 3166, 3168, 3169, 3174, 3176, 3178, 3179, 3180, 3181, 3182, 3183, 3186, 3188, 3190, 3192, 3193, 3196, 3202, 3206, 3211, 3217, 3220, 3221, 3222, 3223, 3224, 3225, 3228, 3230, 3232, 3236, 3237, 3238, 3240, 3241, 3243, 3249, 3250, 3254, 3255, 3258, 3263, 3264, 3265, 3266, 3267, 3270, 3271, 3272, 3274, 3276, 3277, 3278, 3279, 3282, 3284, 3285, 3288, 3292, 3293, 3294, 3296, 3299, 3300, 3301, 3302, 3303, 3304, 3306, 3307, 3308, 3314, 3316, 3320, 3322, 3324, 3325, 3326, 3328, 3329, 3334, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3358, 3363, 3365, 3366, 3367, 3369, 3372, 3374, 3377, 3378, 3379, 3380, 3383, 3385, 3387, 3393, 3394, 3396, 3402, 3403, 3406, 3408, 3409, 3410, 3416, 3417, 3419, 3425, 3427, 3428, 3429, 3432, 3436, 3445, 3446, 3447, 3448, 3449, 3451, 3452, 3453, 3454, 3466, 3472, 3473, 3476, 3478, 3482, 3483, 3484, 3486, 3487, 3488, 3489, 3490, 3491, 3492, 3493, 3496, 3500, 3503, 3504, 3505, 3508, 3512, 3513, 3514, 3516, 3517, 3521, 3522, 3523, 3527, 3528, 3529, 3530, 3532, 3541, 3542, 3544, 3548, 3550, 3551, 3555, 3556, 3562, 3567, 3569, 3570, 3574, 3575, 3577, 3578, 3579, 3580, 3584, 3586, 3588, 3590, 3591, 3596, 3597, 3598, 3600, 3601, 3602, 3603, 3606, 3607, 3610, 3611, 3612, 3614, 3615, 3616, 3618, 3621, 3624, 3626, 3627, 3628, 3629, 3630, 3633, 3636, 3637, 3638, 3639, 3643, 3644, 3646, 3647, 3649, 3652, 3654, 3655, 3656, 3657, 3660, 3661, 3662, 3664, 3665, 3666, 3669, 3671, 3672, 3675, 3676, 3678, 3681, 3684, 3687, 3688, 3689, 3694, 3699, 3700, 3702, 3705, 3706, 3709, 3716, 3718, 3720, 3721, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3733, 3736, 3737, 3744, 3745, 3746, 3747, 3748, 3750, 3752, 3754, 3755, 3756, 3759, 3760, 3765, 3766, 3768, 3769, 3770, 3771, 3775, 3776, 3778, 3780, 3781, 3783, 3784, 3785, 3786, 3792, 3796, 3799, 3802, 3803, 3805, 3806, 3807, 3808, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3822, 3825, 3826, 3827, 3829, 3832, 3835, 3836, 3837, 3839, 3845, 3846, 3847, 3848, 3849, 3852, 3853, 3854, 3855, 3856, 3857, 3859, 3860, 3862, 3863, 3864, 3865, 3866, 3867, 3868, 3870, 3872, 3879, 3883, 3884, 3885, 3891, 3892, 3893, 3895, 3897, 3898, 3902, 3904, 3906, 3907, 3909, 3910, 3919, 3921, 3923, 3924, 3926, 3929, 3930, 3931, 3932, 3934, 3936, 3938, 3939, 3940, 3941, 3942, 3946, 3947, 3948]
	# file_list=get_done_file_list()
	file_list=[1, 11, 13, 16, 18, 34, 43, 48, 58, 67, 148, 149, 168, 171, 186, 205, 214, 321, 328, 366, 397, 434, 437, 441, 458, 508, 564, 580, 598, 605, 623, 628, 632, 636, 646, 657, 663, 672, 699, 844, 845, 848, 854, 857, 864, 929, 975, 1006, 1045, 1051, 1067, 1070, 1124, 1145, 1147, 1150, 1153, 1159, 1182, 1183, 1200, 1208, 1209, 1224, 1241, 1242, 1261, 1270, 1301, 1303, 1327, 1331, 1332, 1341, 1343, 1359, 1379, 1391, 1435, 1437, 1439, 1469, 1477, 1486, 1541, 1553, 1574, 1586, 1598, 1626, 1638, 1639, 1643, 1650, 1654, 1658, 1662, 1691, 1697, 1720, 1726, 1729, 1780, 1793, 1803, 1805, 1810, 1828, 1878, 1897, 1898, 1925, 1959, 1967, 1986, 2030, 2056, 2074, 2080, 2093, 2110, 2162, 2185, 2197, 2204, 2206, 2210, 2216, 2253, 2292, 2305, 2310, 2313, 2315, 2317, 2327, 2328, 2329, 2352, 2411, 2414, 2419, 2432, 2460, 2465, 2466, 2489, 2493, 2522, 2525, 2526, 2528, 2541, 2563, 2568, 2601, 2621, 2626, 2645, 2660, 2679, 2713, 2719, 2737, 2741, 2743, 2767, 2786, 2830, 2845, 2854, 2883, 2890, 2914, 2917, 2932, 3022, 3023, 3028, 3035, 3050, 3052, 3068, 3092, 3099, 3109, 3115, 3123, 3126, 3134, 3147, 3191, 3198, 3209, 3218, 3234, 3245, 3247, 3261, 3262, 3281, 3310, 3312, 3332, 3343, 3345, 3355, 3359, 3360, 3371, 3400, 3438, 3455, 3480, 3495, 3525, 3536, 3547, 3557, 3581, 3593, 3635, 3641, 3651, 3659, 3679, 3682, 3715, 3753, 3787, 3794, 3804, 3828, 3831, 3838, 3937]
	for cur_file_index in file_list:
		try:
			make_4k_pickle(cur_file_index)
			pass
		except :
			error_list.append(cur_file_index)
		pass
	# print "--------------------"
	# print error_list
	# print "--------------------"
	exit()
	# file_list=[14,29,52,84,90,300,304,393,446,451,484,518,577,606,607,610,659,698,700,774,1017,1052,1055,1201,1365,1375,1407,1470,1495,1679,1702,1721,1853,1957,1961,1965,1970,1992,2063,2214,2249,2350,2363,2398,2498,2507,2514,2625,2746,2861,2955,2962,3107,3134,3185,3189,3215,3239,3435,3443,3459,3470,3594,3692,3742]
	# file_list_590=[1, 9, 11, 13, 15, 16, 18, 34, 43, 47, 48, 53, 58, 67, 71, 74, 76, 108, 116, 122, 142, 143, 145, 147, 148, 149, 150, 152, 155, 165, 167, 168, 171, 174, 186, 188, 198, 200, 205, 208, 214, 215, 223, 235, 239, 260, 262, 264, 270, 282, 291, 292, 296, 297, 298, 299, 306, 307, 321, 326, 328, 332, 334, 352, 366, 394, 397, 429, 434, 437, 441, 458, 508, 522, 523, 526, 530, 541, 560, 564, 572, 580, 581, 582, 591, 595, 596, 598, 602, 605, 616, 619, 620, 623, 628, 632, 634, 636, 642, 646, 649, 652, 653, 657, 660, 662, 663, 666, 667, 669, 670, 671, 672, 673, 677, 683, 685, 693, 699, 702, 703, 709, 710, 711, 715, 724, 725, 726, 727, 728, 730, 732, 733, 735, 736, 739, 741, 744, 754, 755, 757, 760, 762, 775, 776, 781, 782, 783, 788, 789, 790, 794, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 824, 831, 837, 838, 844, 845, 847, 848, 852, 854, 857, 859, 861, 864, 865, 878, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 906, 907, 908, 910, 911, 913, 914, 919, 921, 923, 924, 925, 928, 929, 931, 932, 933, 934, 935, 941, 942, 943, 948, 949, 951, 953, 955, 956, 958, 959, 960, 962, 963, 968, 972, 974, 975, 979, 982, 983, 993, 994, 995, 997, 1000, 1001, 1003, 1005, 1006, 1007, 1008, 1013, 1015, 1037, 1040, 1045, 1051, 1054, 1067, 1070, 1073, 1076, 1094, 1124, 1134, 1145, 1147, 1150, 1153, 1159, 1182, 1183, 1190, 1192, 1200, 1208, 1209, 1216, 1221, 1224, 1241, 1242, 1261, 1270, 1301, 1303, 1323, 1327, 1331, 1332, 1340, 1341, 1343, 1348, 1359, 1379, 1391, 1405, 1422, 1425, 1432, 1435, 1437, 1439, 1459, 1468, 1469, 1477, 1486, 1503, 1524, 1541, 1549, 1553, 1563, 1574, 1585, 1586, 1598, 1614, 1625, 1626, 1634, 1638, 1639, 1643, 1646, 1650, 1654, 1656, 1658, 1662, 1691, 1697, 1717, 1720, 1726, 1729, 1744, 1780, 1787, 1790, 1793, 1795, 1803, 1805, 1810, 1816, 1828, 1878, 1879, 1896, 1897, 1898, 1902, 1925, 1959, 1967, 1980, 1983, 1986, 1987, 2009, 2022, 2030, 2039, 2043, 2056, 2058, 2061, 2074, 2080, 2086, 2089, 2093, 2100, 2108, 2110, 2130, 2151, 2162, 2185, 2194, 2197, 2198, 2200, 2204, 2206, 2210, 2216, 2243, 2253, 2255, 2281, 2292, 2305, 2308, 2310, 2312, 2313, 2315, 2316, 2317, 2318, 2327, 2328, 2329, 2331, 2352, 2353, 2360, 2411, 2414, 2419, 2432, 2449, 2460, 2465, 2466, 2469, 2477, 2481, 2489, 2493, 2522, 2525, 2526, 2528, 2541, 2543, 2554, 2563, 2564, 2565, 2568, 2586, 2595, 2601, 2617, 2621, 2626, 2627, 2645, 2660, 2679, 2713, 2718, 2719, 2732, 2737, 2741, 2743, 2753, 2767, 2778, 2786, 2790, 2805, 2806, 2828, 2830, 2831, 2835, 2845, 2852, 2854, 2877, 2882, 2883, 2888, 2890, 2896, 2898, 2914, 2917, 2930, 2932, 2948, 2992, 3022, 3023, 3026, 3028, 3035, 3050, 3052, 3055, 3058, 3068, 3075, 3077, 3092, 3099, 3109, 3115, 3123, 3126, 3134, 3147, 3191, 3198, 3199, 3201, 3209, 3210, 3218, 3226, 3234, 3244, 3245, 3247, 3261, 3262, 3273, 3275, 3281, 3283, 3286, 3289, 3291, 3310, 3312, 3313, 3330, 3332, 3343, 3345, 3348, 3349, 3350, 3351, 3352, 3353, 3355, 3359, 3360, 3368, 3370, 3371, 3373, 3389, 3391, 3397, 3400, 3426, 3431, 3437, 3438, 3455, 3456, 3468, 3471, 3474, 3480, 3485, 3495, 3519, 3525, 3531, 3535, 3536, 3538, 3540, 3543, 3547, 3557, 3581, 3593, 3595, 3634, 3635, 3641, 3651, 3659, 3677, 3679, 3680, 3682, 3697, 3711, 3715, 3741, 3753, 3787, 3794, 3801, 3804, 3828, 3831, 3838, 3937]
	file_list_419=[1,9,11,13,15,16,18,34,43,47,48,53,58,67,71,74,76,108,122,142,143,145,147,148,149,150,152,155,165,167,168,171,174,186,188,198,200,205,208,214,215,223,235,239,260,262,264,270,282,291,292,296,297,298,299,306,307,321,326,328,332,334,366,397,434,437,441,458,508,522,523,526,530,541,564,580,581,591,596,598,602,605,619,620,623,628,632,634,636,642,646,649,652,657,663,669,672,673,677,683,685,693,699,702,703,709,715,730,741,775,776,781,782,783,824,844,845,847,848,852,854,857,859,861,864,865,919,929,941,943,953,959,963,968,972,975,993,997,1000,1001,1003,1005,1006,1007,1008,1013,1015,1037,1040,1045,1051,1054,1067,1070,1094,1124,1134,1145,1147,1150,1153,1159,1182,1183,1190,1192,1200,1208,1209,1216,1224,1241,1242,1261,1270,1301,1303,1327,1331,1332,1340,1341,1343,1348,1359,1379,1391,1405,1425,1435,1437,1439,1459,1468,1469,1477,1486,1503,1524,1541,1549,1553,1574,1585,1586,1598,1614,1625,1626,1634,1638,1639,1643,1646,1650,1654,1656,1658,1662,1691,1697,1717,1720,1726,1729,1780,1790,1793,1803,1805,1810,1828,1878,1896,1897,1898,1925,1959,1967,1986,2009,2022,2030,2039,2043,2056,2058,2061,2074,2080,2086,2089,2093,2100,2108,2110,2130,2162,2185,2194,2197,2198,2200,2204,2206,2210,2216,2243,2253,2255,2292,2305,2310,2313,2315,2316,2317,2318,2327,2328,2329,2352,2353,2360,2411,2414,2419,2432,2449,2460,2465,2466,2477,2481,2489,2493,2522,2525,2526,2528,2541,2563,2568,2586,2595,2601,2621,2626,2645,2660,2679,2713,2719,2732,2737,2741,2743,2753,2767,2778,2786,2790,2805,2828,2830,2831,2835,2845,2852,2854,2877,2883,2888,2890,2896,2914,2917,2930,2932,2948,2992,3022,3023,3026,3028,3035,3050,3052,3055,3058,3068,3092,3099,3109,3115,3123,3126,3134,3147,3191,3198,3209,3218,3234,3244,3245,3247,3261,3262,3275,3281,3283,3310,3312,3313,3332,3343,3345,3348,3349,3350,3352,3355,3359,3360,3368,3371,3391,3400,3438,3455,3468,3480,3495,3525,3536,3547,3557,3581,3593,3634,3635,3641,3651,3659,3679,3682,3697,3711,3715,3741,3753,3787,3794,3804,3828,3831,3838,3937]
	file_list=file_list_590
	ambi_morph_tuples={}
	for cur_file_index in file_list:
		ambi_morph_tuples[cur_file_index]=make_4k_pickle(cur_file_index)
		pass
	# pickle.dump(ambi_morph_tuples,open('ambi_morph_tuples_65.p' , 'w'))
	# refiner()	
	pass

def print_gold_tree(cur_sent_id):
	cur_sent=get_gold_sent(cur_sent_id)
	if cur_sent==None:
		return None
		pass
	temp_list=[]
	for x in cur_sent.content_list :
		# name, POS, dep_tag, from_tag, to_tag
		temp_list.append([convert_to_word_index(x.from_tag)  , convert_to_word_index(x.to_tag)  , x.dep_tag])
		pass
	print "sentence:" + str(cur_sent_id)
	print "++++++++++++++"
	print temp_list
	print "=============="
	return temp_list
	pass

def get_svg_trees():
	svg_to_take=[9,15,47,53,59,65,71,73,74,76,81,88,92,94,99,106,108,109,110,111,112,113,122,123,129,142,143,145,147,150,152,154,155,160,165,167,169,174,177,179,180,183,185,188,197,198,200,208,212,215,216,223,225,226,227,234,235,239,240,243,245,254,255,256,257,258,262,263,264,266,270,271,272,273,277,279,280,281,282,284,290,291,292,293,296,297,298,299,306,307,308,309,310,312,313,314,316,324,326,332,333,334,335,338,339,340,341,342,343,346,347,348,350,351,354,359,404,430,474,487,488,499,522,523,526,530,541,574,575,581,589,591,592,596,602,609,617,618,619,620,622,624,626,629,631,634,635,640,642,643,645,647,648,649,651,652,661,668,669,677,679,683,685,690,691,693,695,697,702,703,705,706,709,715,716,730,740,741,745,771,775,776,781,782,783,786,815,816,819,822,824,830,835,840,847,852,853,855,856,859,860,861,865,866,869,871,872,873,881,884,890,891,919,936,941,943,944,952,953,954,957,959,963,966,968,972,976,980,984,986,993,996,997,998,1000,1001,1003,1005,1007,1008,1011,1013,1014,1015,1027,1031,1034,1036,1037,1040,1041,1042,1043,1044,1050,1054,1064,1076,1081,1088,1093,1094,1096,1102,1108,1117,1118,1133,1134,1154,1158,1166,1173,1174,1177,1190,1192,1216,1219,1227,1283,1338,1340,1347,1348,1350,1364,1369,1376,1378,1405,1409,1420,1423,1425,1436,1438,1441,1447,1448,1459,1463,1468,1483,1490,1491,1503,1521,1524,1526,1530,1531,1538,1549,1556,1568,1572,1585,1605,1614,1625,1634,1635,1640,1644,1645,1646,1649,1656,1659,1669,1717,1731,1744,1745,1765,1770,1773,1776,1790,1794,1823,1832,1896,1902,1905,1910,1915,1921,1946,1954,1969,1976,1983,1984,1987,1989,1999,2009,2016,2022,2026,2029,2033,2039,2043,2045,2058,2061,2069,2086,2089,2094,2100,2103,2108,2109,2126,2130,2131,2151,2165,2173,2194,2198,2200,2215,2223,2225,2240,2242,2243,2255,2274,2314,2316,2318,2337,2344,2353,2357,2359,2360,2370,2379,2380,2396,2449,2452,2454,2456,2474,2477,2481,2542,2543,2546,2554,2556,2557,2559,2583,2586,2595,2636,2649,2669,2732,2733,2753,2778,2791,2799,2805,2814,2821,2826,2828,2831,2835,2843,2852,2855,2872,2877,2884,2886,2888,2891,2896,2897,2901,2907,2911,2930,2936,2946,2948,2957,2968,2978,2985,2986,2988,2992,2995,2997,3003,3015,3018,3026,3027,3036,3039,3055,3058,3097,3101,3103,3160,3173,3195,3197,3208,3214,3219,3231,3233,3244,3248,3275,3283,3311,3313,3319,3330,3333,3344,3346,3348,3349,3350,3352,3353,3368,3370,3381,3386,3389,3390,3391,3395,3405,3407,3418,3423,3426,3431,3456,3461,3468,3479,3526,3533,3535,3537,3543,3545,3554,3563,3582,3595,3634,3658,3673,3691,3697,3703,3708,3711,3717,3731,3732,3735,3740,3741,3763,3764,3779,3782,3790,3791,3798,3821,3840,3841,3869,3888,3896,3908,3920,3935,3951]
	svg_tree_dict={}
	for cur_sent_id in svg_to_take:
		temp_list=print_gold_tree(cur_sent_id)
		if temp_list != None:
			svg_tree_dict[cur_sent_id]=temp_list
			pass
		pass
	pickle.dump(svg_tree_dict,open('svg_tree_dict.p' , 'w'))
	pass

def get_manual_trees():
	manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	manual_tree_dict={}
	for cur_sent_id in manual_refined_dict.keys():
		temp_list=manual_refined_dict[cur_sent_id][1]
		manual_tree_dict[cur_sent_id]=temp_list
		print "sentence:" + str(cur_sent_id)
		print "++++++++++++++"
		print temp_list
		print "=============="
		pass
	pickle.dump(manual_tree_dict,open('manual_tree_dict.p' , 'w'))
	pass

def do_svg_g_2(svg_tree_dict):
	flag=0
	for cur_sent_id in svg_tree_dict.keys():
		edge_list=svg_tree_dict[cur_sent_id]
		if len(edge_list)<3:
			flag=1
			print "error : "+str(cur_sent_id)
			pass
		pass
	if flag==1:
		exit()
		pass
	pass

def do_svg_basic(svg_tree_dict):
	for cur_sent_id in svg_tree_dict.keys():
		edge_list=svg_tree_dict[cur_sent_id]
		for cur_edge in edge_list:
			# one none
			from_node=cur_edge[0]
			to_node=cur_edge[1]
			dep_tag=cur_edge[2]
			f_none=(from_node==None)
			t_none=(to_node==None)
			d_none=(dep_tag==None)
			if (f_none and (not (t_none or d_none))) or (t_none and (not (f_none or d_none))) or (d_none and (not (t_none or f_none))) :
				print "sentence:" + str(cur_sent_id)
				print "++++++++++++++"
				print edge_list
				print "=============="
				pass
			pass
		pass
	pass

def do_svg_none_none(svg_tree_dict):
	for cur_sent_id in svg_tree_dict.keys():
		edge_list=svg_tree_dict[cur_sent_id]
		count=0
		indices_list=[]
		nodes_list=[]
		for cur_edge in edge_list:
			from_node=cur_edge[0]
			to_node=cur_edge[1]
			dep_tag=cur_edge[2]
			nodes_list.append(from_node)
			nodes_list.append(to_node)
			if (to_node==None) and(dep_tag==None):
				indices_list.append(edge_list.index(cur_edge))
				count+=1
				pass
			pass
		if count>1:
			for cur_index in indices_list:
				cur_edge=edge_list[cur_index]
				cur_edge[1]=max(nodes_list)+1
				cur_edge[2]='samucciwam'
				edge_list[cur_index]=cur_edge
				pass
			edge_list.append([max(nodes_list)+1,None,None])
			print "sentence:" + str(cur_sent_id)
			print "++++++++++++++"
			print edge_list
			print "=============="
			pass
		pass
	return
	pass

def do_svg_self_edges(svg_tree_dict):
	for cur_sent_id in svg_tree_dict.keys():
		edge_list=svg_tree_dict[cur_sent_id]
		flag=0
		for cur_edge in edge_list:
			from_node=cur_edge[0]
			to_node=cur_edge[1]
			if from_node==to_node:
				flag=1
				edge_list[edge_list.index(cur_edge)][1]=to_node+1
				pass
		if flag==1:
			print "sentence:" + str(cur_sent_id)
			print "++++++++++++++"
			print edge_list
			print "=============="
			pass
			pass
		pass
	return
	pass

def do_svg_vipsa(svg_tree_dict):
	for cur_sent_id in svg_tree_dict.keys():
		edge_list=svg_tree_dict[cur_sent_id]
		flag=0
		for cur_edge in edge_list:
			from_node=cur_edge[0]
			to_node=cur_edge[1]
			dep_tag=cur_edge[2]
			if dep_tag=='vipsa':
				prev_index=edge_list.index(cur_edge)-1
				next_index=edge_list.index(cur_edge)+1
				if prev_index>=0:
					prev_edge=edge_list[prev_index]
					if prev_edge[0]==to_node:
						continue
						pass
					pass
				if next_index>=len(edge_list):
					flag=1
					edge_list.append([to_node,to_node+1,'sambanxah'])
					pass
				else :
					next_edge=edge_list[next_index]
					if next_edge[0]!=to_node:
						flag=1
						edge_list.insert(next_index,[to_node,to_node+1,'sambanxah'])
						pass
					pass
				pass
			pass
		if flag==1:
			print "sentence:" + str(cur_sent_id)
			print "++++++++++++++"
			print edge_list
			print "=============="
			pass
		pass
	return
	pass

def do_svg_not_tree(svg_tree_dict):
	for cur_sent_id in svg_tree_dict.keys():
		edge_list=svg_tree_dict[cur_sent_id]
		if not is_tree_local(edge_list) :
			print "sentence:" + str(cur_sent_id)
			print "++++++++++++++"
			print edge_list
			print "=============="
			pass
		pass
	pass

def is_tree_local(edge_list):
	G = nx.Graph()
	for cur_edge in edge_list:
		from_node=cur_edge[0]
		to_node=cur_edge[1]
		G.add_edge(from_node, to_node)
		pass
	return nx.is_connected(G)
	pass

def test_trees(svg_tree_dict):
	# print 'do_svg_g_2'
	do_svg_g_2(svg_tree_dict)
	# basic fixes
	# print 'do_svg_basic'
	do_svg_basic(svg_tree_dict)
	# self edges
	# print 'do_svg_self_edges'
	do_svg_self_edges(svg_tree_dict)
	# two None, None
	# print 'do_svg_none_none'
	do_svg_none_none(svg_tree_dict)
	# vipsa
	# print 'do_svg_vipsa'
	do_svg_vipsa(svg_tree_dict)
	# not a tree
	# print 'do_svg_not_tree'
	do_svg_not_tree(svg_tree_dict)
	pass

def make_rooted_tree(edge_list):
	from_nodes_list=[]
	all_nodes_list=[]
	for cur_edge in edge_list:
		from_nodes_list.append(cur_edge[0])
		all_nodes_list+=cur_edge[:2]
		pass
	from_nodes_list=list(set(from_nodes_list))
	# print from_nodes_list
	all_nodes_list=list(set(all_nodes_list))
	# print all_nodes_list
	root=[x for x in all_nodes_list if x not in from_nodes_list]
	if len(root)!=1:
		print "fatal error !!"
		pass
	for root_index in root :
		edge_list.insert(root_index,[root_index,None,None])
		pass
	return edge_list
	pass

def print_dis():
	dis_data=pickle.load(open( "disambiguated_dataset.p" , 'rb'))
	re_done=[14,29,52,84,90,300,304,393,446,451,484,518,577,606,607,610,659,698,700,774,1017,1052,1055,1201,1365,1375,1407,1470,1495,1679,1702,1721,1853,1957,1961,1965,1970,1992,2063,2214,2249,2350,2398,2498,2507,2625,2861,2955,3107,3134,3185,3215,3239,3435,3443,3459,3470,3594,3692,3742]
	dis_sent_list= dis_data.keys()
	for cur_sent_id in dis_sent_list:
		node_dict=dis_data[cur_sent_id][0]
		edge_list=dis_data[cur_sent_id][2]
		print "sentence:" + str(cur_sent_id)
		print "--------------"
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			print str(cur_key) + ":" + str(cur_node)
			pass
		print "++++++++++++++"
		print make_rooted_tree(edge_list)
		print "=============="
		pass
	pass

def update_svg_tree():
	svg_tree_dict=pickle.load(open( "sisu_tree_dict.p" , 'rb'))
	cur_file=open('update_svg.txt','r')
	line_data=cur_file.readlines()
	cur_file_index=None
	edge_list=[]
	updated_list=[]
	for cur_line in line_data:
		if ("sentence:" in cur_line):
			# new sentence
			cur_file_index=int(cur_line.split(":")[1])
			edge_list=[]
			updated_list.append(cur_file_index)
			pass
		elif ("[[" in cur_line):
			# edge_list
			print line_data.index(cur_line)
			print cur_line
			edge_list=eval(cur_line)
			svg_tree_dict[cur_file_index]=edge_list
			cur_node_index=None
			pass
		pass
	for cur_key in updated_list:
		print "sentence : "+str(cur_key)
		pass
	pickle.dump(svg_tree_dict,open('sisu_tree_dict.p' , 'w'))
	pass

def save_trees_to_refined():
	sisu_gold_dict=pickle.load(open( "svg_gold_dict.p" , 'rb'))
	sisu_tree_dict=pickle.load(open( "svg_tree_dict.p" , 'rb'))
	for cur_sent_id in sisu_tree_dict.keys():
		node_dict=sisu_gold_dict[cur_sent_id][0]
		edge_list=sisu_tree_dict[cur_sent_id]
		sisu_gold_dict[cur_sent_id]=[node_dict,edge_list,edge_list]
		pass
	print len(sisu_gold_dict.keys())
	print len(sisu_tree_dict.keys())
	pickle.dump(sisu_gold_dict,open('svg_gold_dict.p' , 'w'))
	pass

def verify_ne_1(cur_sent_id, node_dict, edge_list):
	node_error_flag=0
	key_list=node_dict.keys()
	key_list.sort()
	for cur_key in key_list  : 
		cur_node=node_dict[cur_key]
		if cur_key != cur_node[3]:
			node_error_flag= 1
			pass
		pass
	if node_error_flag==1:
		print "sentence:" + str(cur_sent_id)
		print "--------------"
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			print str(cur_key) + ":" + str(cur_node)
			pass
		print "++++++++++++++"
		print edge_list
		print "=============="
		pass
	pass

def verify_ne_2(cur_sent_id, node_dict, edge_list):
	node_error_flag=0
	key_list=node_dict.keys()
	key_list.sort()
	n_keys=len(key_list)
	if key_list != range(n_keys):
		node_error_flag=1
		pass
	if node_error_flag==1:
		print "sentence:" + str(cur_sent_id)
		print "--------------"
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			print str(cur_key) + ":" + str(cur_node)
			pass
		print "++++++++++++++"
		print edge_list
		print "=============="
		pass
	pass

def verify_ne_3(cur_sent_id, node_dict, edge_list):
	node_error_flag=0
	key_list=node_dict.keys()
	key_list.sort()
	from_nodes_list=[]
	for cur_edge in edge_list:
		from_nodes_list.append(cur_edge[0])
		pass
	from_nodes_list.sort()
	if key_list!=from_nodes_list:
		node_error_flag=1
		pass
	if node_error_flag==1:
		print "sentence:" + str(cur_sent_id)
		print "--------------"
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			print str(cur_key) + ":" + str(cur_node)
			pass
		print "++++++++++++++"
		print edge_list
		print "=============="
		pass
	pass

def verify_node_tree(svg_gold_dict):
	# chek correspondence and exactly 1 None  (root)
	# edge missing
	for cur_sent_id in svg_gold_dict.keys():
		node_dict=svg_gold_dict[cur_sent_id][0]
		edge_list=svg_gold_dict[cur_sent_id][1]
		# verify by node
		verify_ne_1(cur_sent_id, node_dict, edge_list)
		# verify node_dict
		verify_ne_2(cur_sent_id, node_dict, edge_list)
		# verify node-edges
		verify_ne_3(cur_sent_id, node_dict, edge_list)		
		pass
	pass

def update_manual():
	cur_file=open('update_svg.txt','r')
	line_data=cur_file.readlines()
	cur_file_index=None
	cur_node_index=None
	node_dict={}
	edge_list=[]
	cur_update=[]
	refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	for cur_line in line_data:
		if ("sentence:" in cur_line):
			# new sentence
			cur_file_index=int(cur_line.split(":")[1])
			cur_node_index=0
			node_dict={}
			edge_list=[]
			pass
		elif (":[" in cur_line):
			# new word
			print line_data.index(cur_line)
			print cur_line
			node_data=eval(cur_line.split(":")[1])
			node_dict[cur_node_index]=node_data
			cur_node_index+=1
			pass
		elif ("[[" in cur_line):
			# edge_list
			print line_data.index(cur_line)
			print cur_line
			edge_list=eval(cur_line)
			refined_dict[cur_file_index]=[node_dict, edge_list, edge_list]
			cur_update.append(cur_file_index)
			if len(node_dict.keys())!=(cur_node_index):
				print "fatal error "
				exit()
				pass
			cur_node_index=None
			pass
		pass
	for cur_key in cur_update:
		print "sentence : "+str(cur_key)
	# 	print "----------------------"
	# 	print str(refined_dict[cur_key][0])
	# 	print "++++++++++++++++++++++"
	# 	print str(refined_dict[cur_key][1])
	# 	print "======================"
		pass
	print len(cur_update)
	print len(refined_dict.keys())
	pickle.dump(refined_dict,open('manual_refined_dict.p' , 'w'))
	pass

def manual_full_print():
	# file_list=[245, 273, 335, 338, 339, 340, 342, 343, 354, 617, 640, 691, 695, 706, 830, 871, 890, 957, 976, 996, 998, 1166, 1173, 1219, 1438, 1441, 1556, 1989, 2094, 2131, 2165, 2173, 2225, 2274, 2314, 2370, 2380, 2946, 2968, 2985, 2986, 2995, 3173, 3214, 3233, 3333, 3381, 3386, 3461, 3691, 3717, 3731, 3740, 3841, 3951]
	file_list=[54, 157, 1336]
	manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	for cur_sent_id in file_list:
		node_dict=manual_refined_dict[cur_sent_id][0]
		edge_list=manual_refined_dict[cur_sent_id][1]
		print "sentence:" + str(cur_sent_id)
		print "--------------"
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			print str(cur_key) + ":" + str(cur_node)
			pass
		print "++++++++++++++"
		print edge_list
		print "=============="
		pass
	pass

def update_none_none_to_ca():
	# add ca-conj at end :
	update_ca_svg_list=[2086,2094,53,2109,2131,2194,2223,2242,310,523,574,2649,2799,2852,2198,2985,2988,3015,3018,3036,1050,3103,1064,1134,1177,3248,3275,3319,2274,3423,1409,1483,2318,1634,3703,1659,3735,3740,3764,3791,3798,1832,2043]
	update_ca_svg_list=list(set(update_ca_svg_list))
	update_ca_svg_list.sort()
	update_ca_manual_list=[43,48,54,148,149,157,191,193,205,220,321,323,358,373,397,441,479,494,512,547,556,563,657,1077,1082,1084,1090,1092,1105,1114,1115,1120,1124,1136,1211,1232,1274,1276,1291,1336,1343,1381,1404,1446,1566,1567,1573,1668,1709,1801,1830,1909,1966,1967,1975,2038,2078,2091,2170,2187,2327,2365,2371,2393,2487,2623,2697,3013,3020,3034,3044,3056,3076,3090,3157,3181,3190,3206,3249,3258,3278,3296,3303,3578,3580,3643,3760,3784,3802,3814,3816,3947]
	update_ca_manual_list=list(set(update_ca_manual_list))
	update_ca_manual_list.sort()
	update_ca_sisu_list=[16,26,30,40,47,49,53,54,62,63,65,66,68,71,72,82,83,87,89,100,108,110,115,124,132,137,143,144,161,170,171,173,177,184,195,199,201,202,209,210,214,216,225,227,233,235,239,243,245,246,247,251,252,254,258,259,260,264,271,277,278,296,298,319,325,331,337,338,342,344,346,350,351,352,353,357,358,359,368,381,391,397,399,404,412,415,419,426,439,441,445,447,453,458,461,474,475,478,486,494,495,497,499,500,504,507,508,510,511,512,513,515,517,518,519,520,521,522,523,524,525,527,528,529,532,533,535,536,550,552,553,555,556,558,559,563,564,565,575,576,578,579,586,589,590,599,600,602,608,609,610,611,612,613,614,615,616,621,622,623,624,625,627,628,629,630,631,633,634,636,637,644,646,648,654,655,663,664,666,667,668,678,680,681,696]
	update_ca_sisu_list=list(set(update_ca_sisu_list))
	update_ca_sisu_list.sort()

	svg_gold_dict=pickle.load(open( "svg_gold_dict.p" , 'rb'))
	count=0
	for cur_sent_id in update_ca_svg_list:
		node_dict=svg_gold_dict[cur_sent_id][0]
		edge_list=svg_gold_dict[cur_sent_id][1]
		cur_node_index=edge_list[-1][0]
		if cur_node_index != len(node_dict.keys()):
			print cur_sent_id
			print "-----------------"
			pass
		node_dict[cur_node_index]=['ca', 'ca', 'conj.', cur_node_index, [121400, 121400, 120753]]
		svg_gold_dict[cur_sent_id]=[node_dict,edge_list,edge_list]
		count+=1
		pass
	print len(svg_gold_dict.keys())
	print count
	print len(update_ca_svg_list)
	# pickle.dump(svg_gold_dict,open('svg_gold_dict.p' , 'w'))
	pass

def verify_node_lemmas(svg_gold_dict):
	# manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	# collect all lemmas together.
	not_in_dcs_lemma_dict={}
	count_not_in_dcs_lemma_dict={}
	for cur_sent_id in svg_gold_dict.keys():
		node_dict=svg_gold_dict[cur_sent_id][0]
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			cur_data=get_dcs_coverage(cur_node[:3])
			if cur_data[1]==0:
				if cur_node[1] in count_not_in_dcs_lemma_dict.keys():
					count_not_in_dcs_lemma_dict[cur_node[1]]+=1
					temp_list=not_in_dcs_lemma_dict[cur_node[1]]
					temp_list.append([cur_node[0], cur_node[2]])
					not_in_dcs_lemma_dict[cur_node[1]]=temp_list
					pass
				else :
					count_not_in_dcs_lemma_dict[cur_node[1]]=1
					temp_list=[cur_node[0], cur_node[2]]
					not_in_dcs_lemma_dict[cur_node[1]]=[temp_list]
					pass
				pass
			pass
		pass
	print len(count_not_in_dcs_lemma_dict.keys())
	ordered_tuples=sorted(count_not_in_dcs_lemma_dict.items(), key=operator.itemgetter(1))
	for cur_tuple in ordered_tuples:
		cur_lemma=cur_tuple[0]
		cur_count=cur_tuple[1]
		print 'lemma :' +  str(cur_lemma)+ '->'
		print "--------------------------------"
		cur_count=min([3,cur_count])
		for cur_index in range(cur_count):
			print not_in_dcs_lemma_dict[cur_lemma][cur_index]
			pass
		print "+++++++++++++++++++++++++++++++++++"
		pass
	# sisu_gold_dict=pickle.load(open( "sisu_gold_dict.p" , 'rb'))
	# collect heritage and manual lemmas together.
	pass

def cur_fixer():
	# file_list=[2058,2061,2069,2100,2103,2108,2126,2130,2165,2173,2753,2733,2240,2243,2255,2316,2353,2359,2370,3468,2379,2452,3821,2449,2456,2474,2477,2481,2542,2546,2556,2557,2559,2586,2636,2669,635,2732,2791,2805,2814,2821,2826,2828,2831,2835,2843,2855,2872,2877,2884,2886,2891,2896,3779,2911,2930,2936,2946,2948,2957,2200,2968,2978,2986,2888,2995,2997,3003,3026,3027,3039,3058,2901,3097,3101,2225,1096,1102,3160,3173,3195,1154,1158,3208,1166,3219,1173,1174,3231,3233,1190,1192,3244,1216,1219,3283,3311,3313,1283,3333,3344,3346,3348,3349,3350,3352,3368,3381,1338,1340,3391,1347,1348,1350,3214,1364,1369,3418,1376,1378,1405,3461,1420,1423,1425,3479,1436,1438,1447,1448,1459,1463,1468,3526,3533,3537,1490,1491,3545,1503,3554,3563,1521,1524,1526,1530,1531,3582,1538,1549,1556,3673,1568,2992,1572,1585,3634,2314,1605,3658,1614,1625,1635,3691,1644,1645,1646,1649,1656,3708,3711,3717,3731,3741,3697,3763,1717,1731,3782,3790,1745,1765,1770,1773,1776,1790,1794,1823,2357,2360,1669,3386,1896,3405,1915,1921,3395,1946,1954,1969,1976,1984,1989,2380,1999,2009,2016,2022,2026,2029,2033,1227,2039,2045]
	manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	for cur_sent_id in file_list:
		node_dict=manual_refined_dict[cur_sent_id][0]
		edge_list=manual_refined_dict[cur_sent_id][1]
		verify_ne_3(cur_sent_id,node_dict,edge_list)
		pass
	# verify n_of_nones
	pass

def update_pos_bug_fix_svg():
	svg_gold_dict=pickle.load(open( "svg_gold_dict.p" , 'rb'))
	# pos_bug_fix_dict=pickle.load(open( "pos_bug_fix_dict.p" , 'rb'))
	file_list=svg_gold_dict.keys()
	file_list.sort()
	# for cur_sent_id in file_list:
	# 	node_dict=svg_gold_dict[cur_sent_id][0]
	# 	key_list=node_dict.keys()
	# 	key_list.sort()
	# 	local_fix=pos_bug_fix_dict[cur_sent_id]
	# 	for cur_key in key_list:
	# 		cur_node=node_dict[cur_key]
	# 		# print str(cur_key) +":" + str(cur_node)
	# 		if cur_node[0]=="ca":
	# 			continue
	# 			pass
	# 		elif cur_node[0]=="munayaH":
	# 			cur_node[2]="nom. pl. m."
	# 			node_dict[cur_key]=cpy.deepcopy(cur_node)
	# 			continue
	# 			pass
	# 		cur_node[2]=local_fix[cur_key]
	# 		node_dict[cur_key]=cpy.deepcopy(cur_node)
	# 		pass
	# 	# for cur_key in key_list:
	# 	# 	cur_node=node_dict[cur_key]
	# 	# 	print str(cur_key) +":" + str(cur_node)
	# 	# 	pass
	# 	svg_gold_dict[cur_sent_id][0]=cpy.deepcopy(node_dict)
	# 	pass
	for cur_sent_id in file_list:
		node_dict=svg_gold_dict[cur_sent_id][0]
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list:
			cur_node=node_dict[cur_key]
			print str(cur_key) +":" + str(cur_node)
			pass
	# pickle.dump(svg_gold_dict,open('svg_gold_dict.p' , 'w'))
	pass

def complete_sisu_gold_lemma_update():
	sisu_lemma_update_list=get_lemma_update_list()
	sisu_gold_dict=pickle.load(open( "sisu_gold_dict.p" , 'rb'))
	# if word== and lemma== then substitute.
	for cur_sent_id in sisu_gold_dict.keys():
		node_dict=sisu_gold_dict[cur_sent_id][0]
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			cur_word=cur_node[0]
			cur_lemma=cur_node[1]
			replace_lemma=None
			for cur_search_node in sisu_lemma_update_list:
				if (cur_word==cur_search_node[0]) and (cur_lemma==cur_search_node[1]):
					replace_lemma=cur_search_node[2]
					pass
				pass
			if replace_lemma!=None:
				if (get_dcs_coverage([cur_word, replace_lemma, cur_node[2]])[1]==0):
					# alter
					cur_alter=replace_lemma[:len(replace_lemma)-1]+replace_lemma[-1].lower()
					cur_data=get_dcs_coverage([cur_word, cur_alter, cur_node[2]])
					if (cur_data[0]!=0) and ((cur_data[1]!=0)):
						replace_lemma=cur_alter
						print "un-orthodox"
						pass
					cur_alter=replace_lemma[:len(replace_lemma)-1]+replace_lemma[-1].upper()
					cur_data=get_dcs_coverage([cur_word, cur_alter, cur_node[2]])
					if (cur_data[0]!=0) and ((cur_data[1]!=0)):
						replace_lemma=cur_alter
						print "un-orthodox"
						pass
					pass
				print [cur_sent_id, cur_key]
				cur_node[1]=cpy.deepcopy(replace_lemma)
				node_dict[cur_key]=cpy.deepcopy(cur_node)
				pass
			pass
		sisu_gold_dict[cur_sent_id][0]=cpy.deepcopy(node_dict)
		pass
	# pickle.dump(sisu_gold_dict,open('sisu_gold_dict.p' , 'w'))
	pass

def get_lemma_update_list():
	cur_path='/media/mandal/1bdad34f-aa4e-4216-b820-f44f2e99cd49/Sem_9/PG_BTP/4k_remaining/archive/lemma_update_txt/'
	cur_file=open(cur_path+'lemma_update_sisu.txt','r')
	line_data=cur_file.readlines()
	lemma_update_sisu_list=[]
	for cur_index in range(len(line_data)):
		cur_line=line_data[cur_index]
		if "->" in cur_line:
			# lemma :->DanA
			# ['DanAni', '', 'acc. pl. n.']
			old_lemma=cur_line.split(":")[1].split("->")[0]
			new_lemma=cur_line.split("->")[-1].strip()
			next_line=line_data[cur_index+1]
			cur_word=eval(next_line)[0]
			lemma_update_sisu_list.append( [cur_word, old_lemma, new_lemma])
			pass
		pass
	return lemma_update_sisu_list
	pass

def  complete_gold_lemma_update():
	cur_path='/media/mandal/1bdad34f-aa4e-4216-b820-f44f2e99cd49/Sem_9/PG_BTP/4k_remaining/archive/lemma_update_txt/'
	manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	# svg_gold_dict=pickle.load(open( "svg_gold_dict.p" , 'rb'))
	cur_file=open(cur_path+'lemma_update_manual.txt','r')
	line_data=cur_file.readlines()
	lemma_update_svg_dict={}
	for cur_line in line_data:
		if "->" in cur_line:
			old_lemma=cur_line.split(":")[1].split("->")[0]
			new_lemma=cur_line.split("->")[-1].strip()
			lemma_update_svg_dict[old_lemma]=new_lemma
			pass
		pass
	print len(lemma_update_svg_dict.keys())
	for cur_sent_id in manual_refined_dict.keys():
		node_dict=manual_refined_dict[cur_sent_id][0]
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list  : 
			cur_node=node_dict[cur_key]
			cur_word=cur_node[0]
			cur_lemma=cur_node[1]
			replace_lemma=None
			if cur_lemma in lemma_update_svg_dict.keys():
				replace_lemma=lemma_update_svg_dict[cur_lemma]
				pass
			if replace_lemma!=None:
				if (get_dcs_coverage([cur_word, replace_lemma, cur_node[2]])[1]==0):
					# alter
					cur_alter=replace_lemma[:len(replace_lemma)-1]+replace_lemma[-1].lower()
					cur_data=get_dcs_coverage([cur_word, cur_alter, cur_node[2]])
					if (cur_data[0]!=0) and ((cur_data[1]!=0)):
						replace_lemma=cur_alter
						print "un-orthodox"
						pass
					cur_alter=replace_lemma[:len(replace_lemma)-1]+replace_lemma[-1].upper()
					cur_data=get_dcs_coverage([cur_word, cur_alter, cur_node[2]])
					if (cur_data[0]!=0) and ((cur_data[1]!=0)):
						replace_lemma=cur_alter
						print "un-orthodox"
						pass
					pass
				print [cur_sent_id, cur_key]
				cur_node[1]=cpy.deepcopy(replace_lemma)
				node_dict[cur_key]=cpy.deepcopy(cur_node)
				pass
			pass
		manual_refined_dict[cur_sent_id][0]=cpy.deepcopy(node_dict)
		pass
	pickle.dump(manual_refined_dict,open('manual_refined_dict.p' , 'w'))
	pass

def look_at_486():
	previous_486=[2, 3, 4, 6, 42, 50, 51, 54, 56, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 107, 115, 117, 119, 121, 124, 125, 126, 127, 128, 130, 138, 144, 146, 153, 156, 157, 170, 172, 175, 176, 184, 192, 195, 196, 201, 203, 211, 213, 217, 219, 222, 228, 229, 230, 232, 233, 236, 237, 238, 241, 244, 246, 247, 248, 249, 250, 251, 252, 253, 261, 265, 269, 274, 275, 276, 283, 285, 286, 287, 288, 289, 294, 295, 301, 302, 303, 305, 311, 317, 320, 331, 336, 353, 355, 368, 423, 445, 514, 528, 532, 539, 573, 576, 597, 600, 601, 604, 614, 615, 625, 630, 638, 639, 641, 644, 654, 655, 656, 658, 664, 665, 674, 675, 676, 680, 681, 682, 684, 686, 687, 688, 689, 692, 694, 696, 701, 704, 707, 712, 713, 714, 717, 719, 720, 722, 723, 729, 731, 734, 737, 738, 742, 743, 746, 747, 748, 749, 751, 752, 753, 756, 759, 761, 764, 765, 766, 767, 768, 769, 772, 773, 777, 779, 780, 784, 785, 787, 791, 792, 793, 817, 818, 821, 823, 825, 826, 827, 828, 832, 833, 834, 836, 839, 842, 843, 846, 849, 850, 851, 862, 863, 867, 868, 874, 875, 877, 879, 880, 882, 885, 886, 887, 888, 909, 915, 916, 917, 918, 920, 922, 926, 927, 930, 937, 938, 939, 940, 945, 946, 947, 950, 961, 964, 965, 969, 970, 971, 973, 977, 978, 981, 985, 987, 988, 989, 990, 991, 992, 999, 1002, 1004, 1009, 1010, 1012, 1016, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1032, 1035, 1038, 1046, 1061, 1072, 1075, 1087, 1097, 1100, 1103, 1123, 1137, 1151, 1152, 1171, 1179, 1180, 1187, 1189, 1194, 1218, 1220, 1225, 1239, 1248, 1254, 1259, 1267, 1268, 1293, 1295, 1305, 1306, 1317, 1318, 1321, 1324, 1334, 1335, 1336, 1339, 1351, 1358, 1361, 1372, 1377, 1390, 1393, 1397, 1416, 1426, 1428, 1443, 1478, 1479, 1482, 1484, 1494, 1508, 1522, 1528, 1536, 1537, 1539, 1551, 1555, 1558, 1559, 1564, 1565, 1569, 1600, 1601, 1627, 1633, 1636, 1657, 1672, 1673, 1680, 1693, 1712, 1746, 1761, 1767, 1769, 1774, 1775, 1781, 1791, 1808, 1809, 1856, 1859, 1873, 1876, 1881, 1883, 1887, 1913, 1953, 1958, 1960, 2008, 2027, 2028, 2032, 2055, 2141, 2158, 2174, 2218, 2224, 2239, 2257, 2276, 2293, 2307, 2309, 2334, 2338, 2341, 2345, 2354, 2356, 2358, 2372, 2397, 2427, 2468, 2484, 2492, 2529, 2536, 2537, 2538, 2544, 2558, 2566, 2567, 2635, 2646, 2688, 2693, 2699, 2700, 2705, 2728, 2736, 2769, 2810, 2815, 2819, 2825, 2827, 2829, 2840, 2849, 2868, 2871, 2873, 2876, 2881, 3031, 3040, 3060, 3088, 3102, 3111, 3127, 3153, 3165, 3187, 3200, 3205, 3207, 3257, 3323, 3347, 3354, 3357, 3361, 3362, 3376, 3399, 3433, 3463, 3464, 3467, 3469, 3475, 3477, 3497, 3499, 3518, 3520, 3552, 3553, 3565, 3605, 3632, 3674, 3693, 3696, 3704, 3710, 3713, 3719, 3734, 3738, 3788, 3823, 3824, 3830, 3833, 3834, 3842, 3889]
	# merge with manual 55
	error_list=[]
	old_dataset_486=pickle.load(open( "final_dataset.p" , 'rb'))
	manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	for cur_sent_id in previous_486:
		node_dict=old_dataset_486[cur_sent_id][0]
		print "sentence:" + str(cur_sent_id)
		print "--------------"
		key_list=node_dict.keys()
		key_list.sort()
		word_key_list=[]
		for cur_key in key_list:
			temp_list=node_dict[cur_key]
			temp_list[2]=str(temp_list[2])
			print str(cur_key)+":"+str(temp_list)
			word_key_list.append(temp_list[3])
			pass
		gold_key_list=manual_refined_dict[cur_sent_id][0].keys()
		word_key_list=list(set(word_key_list))
		if (word_key_list)!=(gold_key_list):
			error_list.append(cur_sent_id)
			pass
		print "=============="
		pass
	print error_list
	pass

def handle_chunk_underscore(cur_chunk):
	sorted_keys=cur_chunk.chunk_words.keys()
	sorted_keys.sort()
	cur_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
	print "chunk:"+cur_chunk_name
	print "---------------------"
	if (len(cur_chunk_name.split("_")))==(len(sorted_keys)):
		for cur_key in range(len(sorted_keys)):
			print [cur_key]
			pass
		pass
	else :
		for cur_key in range(len(cur_chunk_name.split("_"))):
			print sorted_keys
			pass
		pass
	print "+++++++++++++++++++++"
	for cur_key in sorted_keys:
		cur_word_str=utf_to_ascii((cur_chunk.chunk_words[cur_key][0].names).encode("raw_unicode_escape"))
		print str(cur_key) +" : "+ str(cur_word_str)
		pass
	print '======================'
	# per chunk
	# seperate list of nodes
	pass

def prepare_sentence_ambi(cur_file_index):
	cur_file=pickle.load( open( "test/old/" + str(cur_file_index) + ".p", "rb" ) )
	cur_node_index=0
	node_dict={}
	for cur_index in range(len(cur_file.chunk)):
		cur_chunk=cur_file.chunk[cur_index]
		# for each of 11 chunks
		sorted_keys=cur_chunk.chunk_words.keys()
		sorted_keys.sort()
		cur_chunk_name=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
		if "_" in cur_chunk_name:
			underscore_ret_list=handle_chunk_underscore(cur_chunk)
			# for cur_node in underscore_ret_list:
			# 	node_dict[cur_node_index]=cur_node
			# 	cur_node_index+=1
			# 	pass
			continue
			pass
		if len(sorted_keys)==1:
			# anything goes
			# 0: ['tApasAnAm', 'tApasa', u'g. pl. m.', 0, [0, 250, 25]]
			cur_key=sorted_keys[0]
			for cur_word in cur_chunk.chunk_words[cur_key] :
				word_lemma_pos_list=get_lemma_pos_list(cur_word)
				if word_lemma_pos_list ==[]:
					node_dict[cur_node_index]=[utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape")) , None ,None ,cur_index,[0,0,0,]]
					cur_node_index+=1
					continue
					pass
				for cur_tuple in word_lemma_pos_list:
					node_dict[cur_node_index]=cur_tuple+[cur_index,get_dcs_coverage(cur_tuple)]
					cur_node_index+=1
					pass
				pass
			pass
		else:
			# all possible ones that are not compounds.
			for cur_key in sorted_keys:
				for cur_word in cur_chunk.chunk_words[cur_key] :
					word_lemma_pos_list=get_lemma_pos_list(cur_word)
					if word_lemma_pos_list ==[]:
						node_dict[cur_node_index]=[utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape")) , None ,None ,cur_index,[0,0,0,]]
						cur_node_index+=1
						continue
						pass
					if word_lemma_pos_list[0][2]=='iic.':
						continue
						pass
					for cur_tuple in word_lemma_pos_list:
						cur_tuple[0]=utf_to_ascii((cur_chunk.chunk_name).encode("raw_unicode_escape"))
						node_dict[cur_node_index]=cur_tuple+[cur_index,get_dcs_coverage(cur_tuple)]
						cur_node_index+=1
						pass
					pass
				pass
			pass
		pass
	# print "sentence:" + str(cur_file_index)
	# print "--------------"
	# key_list=node_dict.keys()
	# key_list.sort()
	# for cur_key in key_list  : 
	# 	cur_node=node_dict[cur_key]
	# 	print str(cur_key) + ":" + str(cur_node)
	# 	pass
	# print "=============="
	return node_dict
	pass

def prepare_pickle_ambi():
	file_list_pickles=[1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 37, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 52, 53, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 71, 73, 74, 76, 77, 78, 79, 81, 82, 84, 85, 87, 88, 89, 90, 92, 93, 94, 99, 106, 108, 109, 110, 111, 112, 113, 114, 120, 122, 123, 129, 131, 132, 133, 134, 135, 136, 137, 139, 140, 142, 143, 145, 147, 148, 149, 150, 151, 152, 154, 155, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 171, 173, 174, 177, 179, 180, 181, 182, 183, 185, 186, 187, 188, 189, 190, 191, 193, 194, 197, 198, 199, 200, 202, 204, 205, 206, 207, 208, 209, 210, 212, 214, 215, 216, 218, 220, 221, 223, 224, 225, 226, 227, 231, 234, 235, 239, 240, 242, 243, 254, 255, 256, 257, 258, 260, 262, 263, 264, 266, 270, 271, 272, 277, 278, 279, 280, 281, 282, 284, 290, 291, 292, 293, 296, 297, 298, 299, 300, 304, 306, 307, 308, 309, 310, 312, 313, 314, 315, 316, 318, 319, 321, 323, 324, 325, 326, 328, 329, 332, 333, 334, 341, 345, 346, 347, 348, 349, 350, 351, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 369, 371, 372, 373, 374, 375, 376, 377, 380, 381, 382, 383, 384, 385, 386, 388, 390, 391, 392, 393, 395, 396, 397, 399, 401, 402, 403, 404, 407, 408, 410, 412, 413, 415, 416, 417, 419, 420, 424, 427, 428, 430, 431, 434, 435, 436, 437, 438, 439, 441, 442, 443, 444, 446, 447, 449, 450, 451, 453, 454, 455, 457, 458, 460, 461, 462, 465, 467, 468, 470, 474, 475, 476, 479, 480, 482, 483, 484, 486, 487, 488, 490, 491, 492, 494, 495, 497, 498, 499, 500, 502, 503, 504, 505, 506, 507, 508, 510, 511, 512, 513, 516, 517, 518, 520, 521, 522, 523, 524, 525, 526, 527, 529, 530, 537, 538, 540, 541, 543, 544, 545, 546, 547, 548, 551, 553, 555, 556, 557, 561, 563, 564, 568, 569, 570, 574, 575, 577, 578, 580, 581, 583, 584, 587, 588, 589, 591, 592, 593, 594, 596, 598, 602, 603, 605, 606, 607, 609, 610, 611, 612, 618, 619, 620, 621, 622, 623, 624, 626, 627, 628, 629, 631, 632, 633, 634, 635, 636, 642, 643, 645, 646, 647, 648, 649, 650, 651, 652, 657, 659, 661, 663, 668, 669, 672, 673, 677, 679, 683, 685, 690, 693, 697, 698, 699, 700, 702, 703, 705, 709, 715, 716, 718, 721, 730, 740, 741, 745, 750, 763, 770, 771, 774, 775, 776, 778, 781, 782, 783, 786, 795, 815, 816, 819, 820, 822, 824, 829, 835, 840, 844, 845, 847, 848, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 864, 865, 866, 869, 870, 872, 873, 876, 881, 884, 889, 891, 919, 929, 936, 941, 943, 944, 952, 953, 954, 959, 963, 966, 967, 968, 972, 975, 980, 984, 986, 993, 997, 1000, 1001, 1003, 1005, 1006, 1007, 1008, 1011, 1013, 1014, 1015, 1017, 1027, 1031, 1033, 1034, 1036, 1037, 1040, 1041, 1042, 1043, 1044, 1045, 1047, 1049, 1050, 1051, 1052, 1054, 1055, 1056, 1057, 1059, 1060, 1063, 1064, 1065, 1067, 1069, 1070, 1071, 1074, 1077, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1088, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1098, 1099, 1101, 1102, 1104, 1105, 1106, 1107, 1108, 1110, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1124, 1125, 1127, 1128, 1130, 1131, 1133, 1134, 1135, 1136, 1138, 1139, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1163, 1164, 1167, 1168, 1169, 1174, 1176, 1177, 1181, 1182, 1183, 1184, 1185, 1186, 1188, 1190, 1191, 1192, 1193, 1195, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1222, 1223, 1224, 1226, 1227, 1229, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1240, 1241, 1242, 1243, 1249, 1251, 1255, 1256, 1257, 1260, 1261, 1262, 1264, 1265, 1266, 1269, 1270, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1288, 1289, 1290, 1291, 1292, 1294, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1307, 1311, 1314, 1315, 1319, 1325, 1327, 1328, 1331, 1332, 1333, 1337, 1338, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1352, 1354, 1356, 1357, 1359, 1360, 1364, 1365, 1366, 1369, 1370, 1371, 1373, 1375, 1376, 1378, 1379, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1391, 1392, 1395, 1396, 1398, 1399, 1400, 1401, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1411, 1412, 1413, 1414, 1418, 1420, 1423, 1424, 1425, 1427, 1429, 1430, 1431, 1433, 1434, 1435, 1436, 1437, 1439, 1440, 1442, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1459, 1461, 1462, 1463, 1465, 1466, 1467, 1468, 1469, 1470, 1476, 1477, 1480, 1481, 1483, 1485, 1486, 1488, 1489, 1490, 1491, 1493, 1495, 1496, 1497, 1498, 1499, 1502, 1503, 1504, 1506, 1509, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1520, 1521, 1523, 1524, 1525, 1526, 1527, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1538, 1541, 1542, 1544, 1545, 1546, 1548, 1549, 1552, 1553, 1560, 1561, 1562, 1566, 1567, 1568, 1570, 1571, 1572, 1573, 1574, 1575, 1578, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1593, 1596, 1597, 1598, 1599, 1603, 1605, 1606, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1617, 1618, 1621, 1622, 1623, 1624, 1625, 1626, 1628, 1630, 1631, 1632, 1634, 1635, 1637, 1638, 1639, 1641, 1643, 1644, 1645, 1646, 1649, 1650, 1651, 1654, 1655, 1656, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1674, 1675, 1676, 1677, 1678, 1679, 1681, 1685, 1686, 1687, 1688, 1689, 1691, 1692, 1694, 1695, 1696, 1697, 1698, 1699, 1701, 1702, 1703, 1705, 1706, 1707, 1708, 1709, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1731, 1732, 1734, 1735, 1737, 1738, 1740, 1741, 1742, 1743, 1745, 1749, 1750, 1751, 1756, 1757, 1758, 1759, 1760, 1762, 1764, 1765, 1766, 1768, 1770, 1771, 1772, 1773, 1776, 1778, 1780, 1782, 1783, 1785, 1786, 1788, 1789, 1790, 1792, 1793, 1794, 1797, 1798, 1800, 1801, 1803, 1804, 1805, 1806, 1807, 1810, 1812, 1813, 1817, 1819, 1820, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1832, 1834, 1838, 1839, 1840, 1841, 1842, 1844, 1846, 1847, 1848, 1849, 1853, 1854, 1855, 1857, 1858, 1860, 1861, 1865, 1866, 1867, 1869, 1870, 1871, 1872, 1878, 1884, 1886, 1895, 1896, 1897, 1898, 1899, 1900, 1903, 1904, 1907, 1909, 1911, 1915, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1938, 1940, 1941, 1942, 1943, 1945, 1946, 1948, 1949, 1952, 1954, 1955, 1957, 1959, 1961, 1962, 1965, 1966, 1967, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1979, 1982, 1984, 1986, 1988, 1990, 1991, 1992, 1993, 1994, 1999, 2000, 2001, 2003, 2004, 2005, 2007, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2024, 2025, 2026, 2029, 2030, 2031, 2033, 2036, 2037, 2038, 2039, 2040, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2050, 2051, 2054, 2056, 2057, 2058, 2059, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2073, 2074, 2075, 2078, 2079, 2080, 2082, 2084, 2085, 2086, 2087, 2089, 2090, 2091, 2092, 2093, 2095, 2100, 2101, 2102, 2103, 2105, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2119, 2120, 2123, 2124, 2125, 2126, 2128, 2129, 2130, 2132, 2134, 2135, 2137, 2138, 2139, 2140, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2157, 2160, 2161, 2162, 2163, 2167, 2168, 2169, 2170, 2171, 2172, 2177, 2178, 2179, 2180, 2181, 2183, 2185, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2200, 2202, 2203, 2204, 2206, 2208, 2209, 2210, 2211, 2212, 2214, 2215, 2216, 2221, 2223, 2228, 2229, 2231, 2232, 2233, 2234, 2235, 2237, 2238, 2240, 2241, 2242, 2243, 2246, 2247, 2249, 2250, 2251, 2252, 2253, 2254, 2255, 2256, 2258, 2260, 2262, 2263, 2264, 2265, 2266, 2269, 2270, 2275, 2280, 2284, 2286, 2287, 2290, 2292, 2296, 2297, 2298, 2299, 2301, 2303, 2305, 2306, 2310, 2313, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2324, 2327, 2328, 2329, 2330, 2332, 2333, 2336, 2337, 2340, 2342, 2343, 2344, 2346, 2347, 2348, 2349, 2350, 2351, 2352, 2353, 2355, 2357, 2359, 2360, 2362, 2363, 2364, 2365, 2366, 2367, 2369, 2371, 2374, 2376, 2377, 2378, 2379, 2381, 2382, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2396, 2398, 2401, 2406, 2407, 2408, 2409, 2411, 2412, 2413, 2414, 2415, 2418, 2419, 2421, 2423, 2424, 2426, 2428, 2431, 2432, 2433, 2436, 2437, 2438, 2441, 2443, 2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2470, 2471, 2472, 2473, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2481, 2483, 2485, 2486, 2487, 2488, 2489, 2490, 2491, 2493, 2494, 2495, 2498, 2499, 2500, 2501, 2502, 2503, 2504, 2505, 2507, 2508, 2510, 2511, 2512, 2513, 2514, 2515, 2516, 2517, 2518, 2519, 2520, 2521, 2522, 2523, 2525, 2526, 2527, 2528, 2530, 2531, 2532, 2533, 2534, 2535, 2539, 2540, 2541, 2542, 2545, 2546, 2548, 2553, 2555, 2556, 2557, 2559, 2560, 2561, 2562, 2563, 2568, 2569, 2570, 2571, 2572, 2574, 2575, 2576, 2577, 2578, 2580, 2581, 2582, 2583, 2585, 2586, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2595, 2598, 2599, 2600, 2601, 2602, 2603, 2605, 2608, 2609, 2610, 2612, 2613, 2615, 2616, 2620, 2621, 2622, 2623, 2624, 2625, 2626, 2628, 2629, 2631, 2632, 2633, 2636, 2637, 2638, 2639, 2642, 2644, 2645, 2649, 2650, 2651, 2652, 2653, 2655, 2656, 2659, 2660, 2661, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2673, 2674, 2675, 2677, 2678, 2679, 2680, 2681, 2682, 2683, 2685, 2686, 2689, 2690, 2691, 2692, 2695, 2696, 2697, 2698, 2701, 2702, 2703, 2708, 2710, 2713, 2714, 2717, 2719, 2721, 2722, 2724, 2725, 2726, 2727, 2729, 2730, 2731, 2732, 2733, 2734, 2737, 2738, 2739, 2740, 2741, 2743, 2744, 2746, 2748, 2751, 2752, 2753, 2754, 2759, 2760, 2762, 2763, 2764, 2765, 2767, 2770, 2771, 2776, 2777, 2778, 2779, 2780, 2781, 2782, 2783, 2784, 2785, 2786, 2787, 2790, 2791, 2792, 2794, 2795, 2796, 2797, 2799, 2800, 2801, 2802, 2803, 2804, 2805, 2807, 2809, 2811, 2812, 2813, 2814, 2820, 2821, 2823, 2824, 2826, 2828, 2830, 2831, 2832, 2833, 2835, 2836, 2838, 2839, 2843, 2845, 2846, 2847, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860, 2861, 2863, 2865, 2866, 2872, 2874, 2875, 2877, 2878, 2880, 2883, 2884, 2885, 2886, 2887, 2888, 2889, 2890, 2891, 2892, 2895, 2896, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2908, 2910, 2911, 2914, 2915, 2916, 2917, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2928, 2929, 2930, 2931, 2932, 2934, 2935, 2936, 2937, 2938, 2939, 2940, 2941, 2942, 2944, 2945, 2947, 2948, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2958, 2962, 2964, 2965, 2966, 2967, 2970, 2971, 2972, 2974, 2975, 2976, 2978, 2979, 2980, 2981, 2982, 2983, 2984, 2987, 2988, 2990, 2991, 2992, 2993, 2996, 2997, 2998, 2999, 3000, 3003, 3004, 3005, 3008, 3011, 3012, 3013, 3015, 3016, 3018, 3019, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027, 3028, 3030, 3032, 3033, 3034, 3035, 3036, 3037, 3038, 3039, 3042, 3043, 3044, 3045, 3047, 3048, 3049, 3050, 3051, 3052, 3055, 3056, 3057, 3058, 3061, 3062, 3063, 3064, 3065, 3067, 3068, 3069, 3070, 3071, 3072, 3073, 3074, 3076, 3078, 3079, 3080, 3081, 3082, 3083, 3085, 3086, 3087, 3089, 3090, 3091, 3092, 3093, 3094, 3095, 3096, 3097, 3098, 3099, 3100, 3101, 3103, 3104, 3105, 3106, 3107, 3109, 3112, 3114, 3115, 3116, 3117, 3118, 3121, 3122, 3123, 3125, 3126, 3128, 3129, 3130, 3131, 3132, 3133, 3134, 3136, 3137, 3138, 3139, 3140, 3142, 3143, 3144, 3146, 3147, 3149, 3154, 3156, 3157, 3158, 3159, 3160, 3161, 3164, 3166, 3168, 3169, 3174, 3176, 3177, 3178, 3179, 3180, 3181, 3182, 3183, 3185, 3186, 3188, 3189, 3190, 3191, 3192, 3193, 3195, 3196, 3198, 3202, 3206, 3208, 3209, 3211, 3215, 3217, 3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3228, 3230, 3231, 3232, 3234, 3236, 3237, 3238, 3239, 3240, 3241, 3243, 3244, 3245, 3247, 3248, 3249, 3250, 3254, 3255, 3258, 3261, 3262, 3263, 3264, 3265, 3266, 3267, 3270, 3271, 3272, 3274, 3275, 3276, 3277, 3278, 3279, 3281, 3282, 3283, 3284, 3285, 3288, 3292, 3293, 3294, 3296, 3298, 3299, 3300, 3301, 3302, 3303, 3304, 3306, 3307, 3308, 3310, 3311, 3312, 3313, 3314, 3316, 3319, 3320, 3322, 3324, 3325, 3326, 3328, 3329, 3332, 3334, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3343, 3344, 3345, 3346, 3348, 3349, 3350, 3352, 3355, 3358, 3359, 3360, 3363, 3365, 3366, 3367, 3368, 3369, 3371, 3372, 3374, 3375, 3377, 3378, 3379, 3380, 3383, 3385, 3387, 3391, 3393, 3394, 3395, 3396, 3400, 3401, 3402, 3403, 3405, 3406, 3408, 3409, 3410, 3416, 3417, 3418, 3419, 3421, 3423, 3425, 3427, 3428, 3429, 3432, 3435, 3436, 3438, 3443, 3445, 3446, 3447, 3448, 3449, 3451, 3452, 3453, 3454, 3455, 3459, 3466, 3468, 3470, 3472, 3473, 3476, 3478, 3479, 3480, 3481, 3482, 3483, 3484, 3486, 3487, 3488, 3489, 3490, 3491, 3492, 3493, 3495, 3496, 3500, 3503, 3504, 3505, 3508, 3511, 3512, 3513, 3514, 3516, 3517, 3521, 3522, 3523, 3525, 3526, 3527, 3528, 3529, 3530, 3532, 3533, 3536, 3537, 3541, 3542, 3544, 3545, 3547, 3548, 3550, 3551, 3554, 3555, 3556, 3557, 3562, 3563, 3567, 3569, 3570, 3573, 3574, 3575, 3577, 3578, 3579, 3580, 3581, 3582, 3584, 3585, 3586, 3588, 3590, 3591, 3593, 3594, 3596, 3597, 3598, 3600, 3601, 3602, 3603, 3606, 3607, 3610, 3611, 3612, 3614, 3615, 3616, 3618, 3621, 3624, 3626, 3627, 3628, 3629, 3630, 3633, 3634, 3635, 3636, 3637, 3638, 3639, 3641, 3643, 3644, 3646, 3647, 3649, 3651, 3652, 3654, 3655, 3656, 3657, 3658, 3659, 3660, 3661, 3662, 3664, 3665, 3666, 3669, 3671, 3672, 3673, 3675, 3676, 3678, 3679, 3681, 3682, 3684, 3687, 3688, 3689, 3692, 3694, 3697, 3699, 3700, 3702, 3703, 3705, 3706, 3708, 3709, 3711, 3715, 3716, 3718, 3720, 3721, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3733, 3735, 3736, 3737, 3741, 3742, 3744, 3745, 3746, 3747, 3748, 3750, 3752, 3753, 3754, 3755, 3756, 3759, 3760, 3763, 3764, 3765, 3766, 3768, 3769, 3770, 3771, 3775, 3776, 3778, 3779, 3780, 3781, 3782, 3783, 3784, 3785, 3786, 3787, 3790, 3791, 3792, 3794, 3796, 3798, 3799, 3802, 3803, 3804, 3805, 3806, 3807, 3808, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3819, 3821, 3822, 3825, 3826, 3827, 3828, 3829, 3831, 3832, 3835, 3836, 3837, 3838, 3839, 3840, 3845, 3846, 3847, 3848, 3849, 3852, 3853, 3854, 3855, 3856, 3857, 3859, 3860, 3862, 3863, 3864, 3865, 3866, 3867, 3868, 3869, 3870, 3872, 3879, 3883, 3884, 3885, 3888, 3891, 3892, 3893, 3895, 3896, 3897, 3898, 3902, 3904, 3906, 3907, 3908, 3909, 3910, 3919, 3920, 3921, 3923, 3924, 3926, 3929, 3930, 3931, 3932, 3934, 3935, 3936, 3937, 3938, 3939, 3940, 3941, 3942, 3946, 3947, 3948]
	for cur_pickle in file_list_pickles:
		prepare_sentence_ambi(cur_pickle)
		pass
	pass

def get_underscore_rectifier():
	pass

def update_gold_dicts():
	# svg_gold_dict=pickle.load(open( "svg_gold_dict.p" , 'rb'))
	manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	# manual_refined_dict=pickle.load(open( "sisu_gold_dict.p" , 'rb'))	
	file_list=manual_refined_dict.keys()
	file_list.sort()
	not_in_dcs_stats={}
	error_list=[]
	for cur_file_index in file_list:
		node_dict=manual_refined_dict[cur_file_index][0]
		key_list=node_dict.keys()
		key_list.sort()
		not_in_dcs_node_count=0
		for cur_key in key_list:
			cur_node=node_dict[cur_key]
			cur_pos=cur_node[2]
			cur_pos=str(cur_pos)
			if "ben" in cur_pos:
				cur_pos=cur_pos.replace("ben", "dat")
				pass
			if cur_pos=="part":
				cur_pos="part."
				pass
			if cur_pos=="adv":
				cur_pos="adv."
				pass
			if cur_pos=="abs. sg. n.":
				cur_pos="abl. sg. n."
				pass
			if cur_pos=="abl. sg n":
				cur_pos="abl. sg. n."
				pass
			if cur_pos=="tasil.":
				cur_pos="ind."
				pass
			cur_node[2]=cpy.deepcopy(cur_pos)
			node_dict[cur_key]=cpy.deepcopy(cur_node)
			manual_refined_dict[cur_file_index][0]=cpy.deepcopy(node_dict)
			pass
		pass

	for cur_file_index in file_list:
		node_dict=manual_refined_dict[cur_file_index][0]
		key_list=node_dict.keys()
		key_list.sort()
		not_in_dcs_node_count=0
		for cur_key in key_list:
			cur_node=node_dict[cur_key]
			cur_cng=wordTypeCheck(cur_node[2])
			if not is_int(cur_cng):
				error_list.append(cur_node)
				pass
			pass
		pass
	for cur_node in error_list:
		print cur_node
		pass
	pickle.dump(manual_refined_dict,open('manual_refined_dict.p' , 'w'))
	pass

def get_new_input_sentences():
	all_lemmas_covered_dict=pickle.load(open( "all_lemmas_covered_dict.p" , 'rb'))
	manual_key_list=all_lemmas_covered_dict.keys()
	manual_key_list.sort()
	for cur_sent_id in manual_key_list:
		cur_temp_str=""
		node_dict=all_lemmas_covered_dict[cur_sent_id][0]
		key_list=node_dict.keys()
		key_list.sort()
		for cur_key in key_list:
			cur_node=node_dict[cur_key]
			cur_temp_str+=cur_node[0]
			cur_temp_str+=" "
			pass
		cur_temp_str=cur_temp_str.strip()
		print str(cur_sent_id)+":"+cur_temp_str
		pass
	pass

def handle_dcs_notfound():
	look_for_cng_patterns_dict=pickle.load(open( "look_for_cng_patterns_dict.p" , 'rb'))
	manual_key_list=look_for_cng_patterns_dict.keys()
	manual_key_list.sort()
	list_1=[9, 17, 20, 21, 24, 34, 39, 43, 49, 57, 61, 62, 68, 71, 78, 79, 90, 111, 120, 135, 144, 146, 147, 149, 152, 157, 160, 161, 162, 163, 164, 171, 181, 186, 194, 197, 198, 199, 205, 208, 215, 219, 221, 224, 225, 231, 233, 239, 240, 241, 245, 278, 289, 296, 304, 324, 329, 332, 335, 340, 342, 343, 345, 351, 354, 355, 358, 360, 365, 371, 373, 404, 441, 445, 474, 486, 491, 500, 502, 507, 512, 513, 516, 517, 521, 522, 524, 525, 526, 527, 537, 538, 543, 551, 553, 563, 569, 580, 589, 591, 594, 602, 605, 617, 621, 635, 636, 640, 642, 645, 646, 648, 650, 651, 663, 690, 699, 749, 775, 781, 792, 827, 829, 840, 845, 855, 857, 858, 863, 870, 915, 919, 941, 963, 964, 966, 969, 1008, 1011, 1013, 1019, 1037, 1044, 1045, 1047, 1049, 1050, 1051, 1057, 1060, 1064, 1065, 1067, 1069, 1081, 1082, 1083, 1084, 1087, 1091, 1092, 1093, 1094, 1097, 1106, 1107, 1113, 1115, 1118, 1119, 1125, 1130, 1138, 1142, 1148, 1149, 1157, 1158, 1161, 1166, 1173, 1179, 1183, 1189, 1192, 1214, 1216, 1219, 1222, 1232, 1248, 1257, 1262, 1272, 1273, 1274, 1275, 1277, 1280, 1281, 1282, 1285, 1289, 1290, 1291, 1294, 1299, 1302, 1303, 1311, 1314, 1315, 1327, 1331, 1333, 1341, 1343, 1344, 1346, 1352, 1357, 1370, 1371, 1381, 1383, 1398, 1400, 1403, 1404, 1405, 1409, 1412, 1425, 1431, 1436, 1438, 1439, 1440, 1441, 1443, 1450, 1451, 1459, 1468, 1480, 1483, 1491, 1494, 1496, 1504, 1506, 1509, 1511, 1512, 1513, 1514, 1515, 1521, 1528, 1531, 1532, 1533, 1534, 1535, 1549, 1556, 1561, 1562, 1570, 1571, 1574, 1585, 1590, 1593, 1596, 1597, 1598, 1600, 1603, 1605, 1606, 1617, 1618, 1625, 1630, 1631, 1632, 1635, 1636, 1638, 1643, 1646, 1670, 1687, 1696, 1701, 1706, 1709, 1712, 1714]

	list_2=[1718, 1721, 1724, 1728, 1735, 1737, 1740, 1741, 1742, 1743, 1746, 1759, 1772, 1774, 1776, 1778, 1782, 1791, 1801, 1803, 1806, 1808, 1812, 1817, 1823, 1825, 1842, 1846, 1848, 1854, 1855, 1857, 1858, 1861, 1865, 1870, 1897, 1899, 1900, 1904, 1911, 1918, 1921, 1925, 1933, 1934, 1948, 1949, 1962, 1966, 1969, 1970, 1975, 1979, 1988, 2001, 2005, 2017, 2019, 2024, 2027, 2036, 2038, 2043, 2044, 2046, 2050, 2057, 2061, 2064, 2065, 2075, 2080, 2084, 2085, 2086, 2091, 2092, 2093, 2094, 2100, 2103, 2109, 2111, 2114, 2119, 2120, 2123, 2125, 2128, 2134, 2137, 2139, 2144, 2145, 2147, 2148, 2150, 2157, 2160, 2167, 2168, 2171, 2173, 2183, 2186, 2187, 2188, 2197, 2198, 2204, 2206, 2209, 2211, 2212, 2214, 2218, 2221, 2232, 2235, 2237, 2240, 2242, 2250, 2252, 2256, 2266, 2299, 2303, 2314, 2318, 2319, 2320, 2324, 2327, 2328, 2333, 2336, 2340, 2342, 2346, 2347, 2348, 2364, 2367, 2369, 2370, 2374, 2376, 2377, 2386, 2387, 2389, 2390, 2393, 2414, 2418, 2421, 2423, 2436, 2437, 2438, 2450, 2454, 2455, 2456, 2458, 2459, 2462, 2475, 2483, 2485, 2486, 2488, 2493, 2498, 2501, 2502, 2503, 2505, 2508, 2510, 2511, 2513, 2519, 2520, 2527, 2528, 2530, 2539, 2541, 2542, 2556, 2561, 2571, 2574, 2575, 2577, 2578, 2582, 2583, 2586, 2590, 2591, 2602, 2610, 2612, 2620, 2622, 2623, 2624, 2625, 2629, 2638, 2639, 2644, 2663, 2664, 2667, 2669, 2671, 2675, 2680, 2681, 2689, 2690, 2702, 2708, 2710, 2722, 2725, 2728, 2730, 2743, 2744, 2748, 2751, 2752, 2754, 2764, 2767, 2770, 2776, 2781, 2783, 2786, 2796, 2797, 2801, 2802, 2821, 2826, 2835, 2839, 2852, 2859, 2860, 2865, 2868, 2871, 2874, 2876, 2891, 2905, 2917, 2930, 2931, 2936, 2939, 2946, 2947, 2950, 2951, 2957, 2964, 2972, 2980, 2985, 2993, 2998, 3000, 3003, 3008, 3013, 3015, 3018, 3025, 3026, 3034, 3036, 3038, 3039, 3043, 3045, 3047, 3048, 3052, 3056, 3064, 3067]

	list_3=[3073, 3076, 3080, 3082, 3090, 3093, 3094, 3095, 3096, 3100, 3101, 3103, 3106, 3107, 3125, 3131, 3132, 3133, 3137, 3138, 3139, 3140, 3142, 3143, 3144, 3146, 3149, 3154, 3156, 3157, 3164, 3173, 3178, 3179, 3181, 3183, 3185, 3193, 3200, 3208, 3209, 3214, 3219, 3222, 3224, 3228, 3230, 3233, 3234, 3239, 3240, 3241, 3245, 3248, 3250, 3254, 3261, 3263, 3264, 3267, 3275, 3282, 3288, 3292, 3299, 3300, 3307, 3320, 3322, 3326, 3329, 3334, 3336, 3337, 3342, 3345, 3350, 3352, 3359, 3365, 3368, 3371, 3374, 3386, 3391, 3396, 3403, 3408, 3409, 3425, 3432, 3449, 3454, 3461, 3475, 3488, 3489, 3491, 3495, 3496, 3500, 3508, 3513, 3514, 3516, 3521, 3523, 3525, 3527, 3547, 3565, 3567, 3570, 3575, 3577, 3579, 3582, 3586, 3593, 3596, 3598, 3601, 3602, 3605, 3606, 3607, 3610, 3618, 3626, 3627, 3630, 3637, 3641, 3644, 3646, 3649, 3654, 3655, 3657, 3659, 3661, 3669, 3674, 3675, 3676, 3692, 3699, 3705, 3706, 3711, 3717, 3724, 3733, 3735, 3736, 3740, 3741, 3745, 3752, 3755, 3756, 3764, 3769, 3770, 3778, 3780, 3785, 3790, 3803, 3805, 3808, 3812, 3815, 3816, 3817, 3818, 3823, 3825, 3826, 3827, 3831, 3833, 3836, 3839, 3845, 3847, 3854, 3857, 3859, 3860, 3863, 3865, 3866, 3867, 3869, 3870, 3883, 3884, 3892, 3897, 3926, 3931, 3932, 3936, 3938, 3948, 4001, 4003, 4004, 4009, 4011, 4012, 4017, 4019, 4020, 4021, 4022, 4024, 4025, 4030, 4031, 4032, 4033, 4034, 4036, 4037, 4038, 4042, 4043, 4044, 4045, 4046, 4047, 4048, 4049, 4050, 4054, 4056, 4058, 4059, 4063, 4065, 4068, 4069, 4070, 4071, 4073, 4074, 4076, 4079, 4081, 4082, 4085, 4086, 4087, 4089, 4090, 4091, 4093, 4095, 4097, 4099, 4102, 4103, 4104, 4106, 4108, 4110, 4115, 4116, 4117, 4119, 4120, 4123, 4124, 4125, 4126, 4127, 4128, 4129, 4131, 4132, 4133, 4135, 4139, 4144, 4145, 4146, 4148, 4150, 4151, 4155, 4158, 4161, 4163, 4164, 4166, 4167, 4169, 4171]

	list_4=[4172, 4173, 4174, 4175, 4176, 4178, 4179, 4181, 4184, 4185, 4186, 4187, 4189, 4190, 4193, 4194, 4196, 4197, 4198, 4199, 4201, 4202, 4203, 4208, 4209, 4211, 4213, 4216, 4217, 4218, 4220, 4222, 4224, 4227, 4228, 4229, 4230, 4233, 4234, 4235, 4236, 4238, 4239, 4242, 4245, 4246, 4248, 4255, 4260, 4263, 4264, 4268, 4269, 4270, 4271, 4273, 4277, 4279, 4280, 4282, 4283, 4284, 4285, 4287, 4289, 4290, 4291, 4292, 4294, 4295, 4296, 4298, 4301, 4304, 4305, 4307, 4308, 4309, 4311, 4313, 4315, 4316, 4317, 4318, 4321, 4322, 4323, 4324, 4327, 4329, 4330, 4332, 4333, 4334, 4335, 4337, 4338, 4339, 4340, 4342, 4344, 4345, 4346, 4348, 4349, 4351, 4352, 4353, 4355, 4356, 4357, 4360, 4361, 4362, 4363, 4365, 4368, 4370, 4372, 4375, 4379, 4380, 4381, 4384, 4385, 4386, 4387, 4388, 4389, 4391, 4392, 4394, 4395, 4396, 4399, 4400, 4401, 4403, 4405, 4406, 4407, 4412, 4413, 4414, 4416, 4417, 4418, 4419, 4421, 4422, 4423, 4424, 4425, 4428, 4429, 4431, 4432, 4433, 4436, 4437, 4439, 4441, 4444, 4445, 4446, 4447, 4450, 4451, 4452, 4453, 4455, 4456, 4458, 4459, 4460, 4461, 4465, 4469, 4471, 4472, 4475, 4478, 4479, 4480, 4481, 4482, 4484, 4486, 4487, 4490, 4491, 4492, 4494, 4496, 4498, 4499, 4500, 4501, 4503, 4504, 4505, 4507, 4508, 4510, 4512, 4514, 4516, 4517, 4518, 4522, 4524, 4526, 4527, 4529, 4530, 4535, 4536, 4537, 4538, 4541, 4542, 4544, 4546, 4547, 4548, 4549, 4551, 4552, 4553, 4554, 4555, 4556, 4557, 4558, 4560, 4561, 4563, 4565, 4566, 4568, 4574, 4579, 4580, 4581, 4582, 4583, 4584, 4585, 4588, 4591, 4593, 4594, 4595, 4596, 4602, 4607, 4608, 4615, 4616, 4618, 4620, 4622, 4623, 4624, 4626, 4628, 4630, 4631, 4632, 4635, 4636, 4637, 4638, 4646, 4647, 4648, 4651, 4652, 4653, 4654, 4658, 4659, 4663, 4665, 4666, 4667, 4670, 4672, 4678, 4679, 4680, 4682, 4683, 4685, 4688, 4691, 4692, 4695, 4697]

	manual_key_list=list_4

	print manual_key_list
	print "----------------------------------------------"
	patterns_matched_dict={}
	for cur_sent_id in manual_key_list:
		# [node_dict, edge_list, cng_set, lemma_cng_list, lemma_new_lemma_list]
		print str(len(manual_key_list)-manual_key_list.index(cur_sent_id))+"more to go."
		node_dict=look_for_cng_patterns_dict[cur_sent_id][0]
		manual_cng_set=look_for_cng_patterns_dict[cur_sent_id][2]
		lemma_cng_list=look_for_cng_patterns_dict[cur_sent_id][3]
		lemma_new_lemma_list=look_for_cng_patterns_dict[cur_sent_id][4]
		dcs_match_list=get_dcs_pattern_matches(manual_cng_set)
		patterns_matched_dict[cur_sent_id]=dcs_match_list
		pass
	pickle.dump(patterns_matched_dict,open('patterns_matched_dict_list_4.p' , 'w'))
	patterns_matched_dict_list_1=pickle.load(open( "patterns_matched_dict_list_1.p" , 'rb'))
	patterns_matched_dict_list_2=pickle.load(open( "patterns_matched_dict_list_2.p" , 'rb'))
	patterns_matched_dict_list_3=pickle.load(open( "patterns_matched_dict_list_3.p" , 'rb'))
	patterns_matched_dict_list_4=pickle.load(open( "patterns_matched_dict_list_4.p" , 'rb'))
	list_1=[9, 17, 20, 21, 24, 34, 39, 43, 49, 57, 61, 62, 68, 71, 78, 79, 90, 111, 120, 135, 144, 146, 147, 149, 152, 157, 160, 161, 162, 163, 164, 171, 181, 186, 194, 197, 198, 199, 205, 208, 215, 219, 221, 224, 225, 231, 233, 239, 240, 241, 245, 278, 289, 296, 304, 324, 329, 332, 335, 340, 342, 343, 345, 351, 354, 355, 358, 360, 365, 371, 373, 404, 441, 445, 474, 486, 491, 500, 502, 507, 512, 513, 516, 517, 521, 522, 524, 525, 526, 527, 537, 538, 543, 551, 553, 563, 569, 580, 589, 591, 594, 602, 605, 617, 621, 635, 636, 640, 642, 645, 646, 648, 650, 651, 663, 690, 699, 749, 775, 781, 792, 827, 829, 840, 845, 855, 857, 858, 863, 870, 915, 919, 941, 963, 964, 966, 969, 1008, 1011, 1013, 1019, 1037, 1044, 1045, 1047, 1049, 1050, 1051, 1057, 1060, 1064, 1065, 1067, 1069, 1081, 1082, 1083, 1084, 1087, 1091, 1092, 1093, 1094, 1097, 1106, 1107, 1113, 1115, 1118, 1119, 1125, 1130, 1138, 1142, 1148, 1149, 1157, 1158, 1161, 1166, 1173, 1179, 1183, 1189, 1192, 1214, 1216, 1219, 1222, 1232, 1248, 1257, 1262, 1272, 1273, 1274, 1275, 1277, 1280, 1281, 1282, 1285, 1289, 1290, 1291, 1294, 1299, 1302, 1303, 1311, 1314, 1315, 1327, 1331, 1333, 1341, 1343, 1344, 1346, 1352, 1357, 1370, 1371, 1381, 1383, 1398, 1400, 1403, 1404, 1405, 1409, 1412, 1425, 1431, 1436, 1438, 1439, 1440, 1441, 1443, 1450, 1451, 1459, 1468, 1480, 1483, 1491, 1494, 1496, 1504, 1506, 1509, 1511, 1512, 1513, 1514, 1515, 1521, 1528, 1531, 1532, 1533, 1534, 1535, 1549, 1556, 1561, 1562, 1570, 1571, 1574, 1585, 1590, 1593, 1596, 1597, 1598, 1600, 1603, 1605, 1606, 1617, 1618, 1625, 1630, 1631, 1632, 1635, 1636, 1638, 1643, 1646, 1670, 1687, 1696, 1701, 1706, 1709, 1712, 1714]
	list_2=[1718, 1721, 1724, 1728, 1735, 1737, 1740, 1741, 1742, 1743, 1746, 1759, 1772, 1774, 1776, 1778, 1782, 1791, 1801, 1803, 1806, 1808, 1812, 1817, 1823, 1825, 1842, 1846, 1848, 1854, 1855, 1857, 1858, 1861, 1865, 1870, 1897, 1899, 1900, 1904, 1911, 1918, 1921, 1925, 1933, 1934, 1948, 1949, 1962, 1966, 1969, 1970, 1975, 1979, 1988, 2001, 2005, 2017, 2019, 2024, 2027, 2036, 2038, 2043, 2044, 2046, 2050, 2057, 2061, 2064, 2065, 2075, 2080, 2084, 2085, 2086, 2091, 2092, 2093, 2094, 2100, 2103, 2109, 2111, 2114, 2119, 2120, 2123, 2125, 2128, 2134, 2137, 2139, 2144, 2145, 2147, 2148, 2150, 2157, 2160, 2167, 2168, 2171, 2173, 2183, 2186, 2187, 2188, 2197, 2198, 2204, 2206, 2209, 2211, 2212, 2214, 2218, 2221, 2232, 2235, 2237, 2240, 2242, 2250, 2252, 2256, 2266, 2299, 2303, 2314, 2318, 2319, 2320, 2324, 2327, 2328, 2333, 2336, 2340, 2342, 2346, 2347, 2348, 2364, 2367, 2369, 2370, 2374, 2376, 2377, 2386, 2387, 2389, 2390, 2393, 2414, 2418, 2421, 2423, 2436, 2437, 2438, 2450, 2454, 2455, 2456, 2458, 2459, 2462, 2475, 2483, 2485, 2486, 2488, 2493, 2498, 2501, 2502, 2503, 2505, 2508, 2510, 2511, 2513, 2519, 2520, 2527, 2528, 2530, 2539, 2541, 2542, 2556, 2561, 2571, 2574, 2575, 2577, 2578, 2582, 2583, 2586, 2590, 2591, 2602, 2610, 2612, 2620, 2622, 2623, 2624, 2625, 2629, 2638, 2639, 2644, 2663, 2664, 2667, 2669, 2671, 2675, 2680, 2681, 2689, 2690, 2702, 2708, 2710, 2722, 2725, 2728, 2730, 2743, 2744, 2748, 2751, 2752, 2754, 2764, 2767, 2770, 2776, 2781, 2783, 2786, 2796, 2797, 2801, 2802, 2821, 2826, 2835, 2839, 2852, 2859, 2860, 2865, 2868, 2871, 2874, 2876, 2891, 2905, 2917, 2930, 2931, 2936, 2939, 2946, 2947, 2950, 2951, 2957, 2964, 2972, 2980, 2985, 2993, 2998, 3000, 3003, 3008, 3013, 3015, 3018, 3025, 3026, 3034, 3036, 3038, 3039, 3043, 3045, 3047, 3048, 3052, 3056, 3064, 3067]
	list_3=[3073, 3076, 3080, 3082, 3090, 3093, 3094, 3095, 3096, 3100, 3101, 3103, 3106, 3107, 3125, 3131, 3132, 3133, 3137, 3138, 3139, 3140, 3142, 3143, 3144, 3146, 3149, 3154, 3156, 3157, 3164, 3173, 3178, 3179, 3181, 3183, 3185, 3193, 3200, 3208, 3209, 3214, 3219, 3222, 3224, 3228, 3230, 3233, 3234, 3239, 3240, 3241, 3245, 3248, 3250, 3254, 3261, 3263, 3264, 3267, 3275, 3282, 3288, 3292, 3299, 3300, 3307, 3320, 3322, 3326, 3329, 3334, 3336, 3337, 3342, 3345, 3350, 3352, 3359, 3365, 3368, 3371, 3374, 3386, 3391, 3396, 3403, 3408, 3409, 3425, 3432, 3449, 3454, 3461, 3475, 3488, 3489, 3491, 3495, 3496, 3500, 3508, 3513, 3514, 3516, 3521, 3523, 3525, 3527, 3547, 3565, 3567, 3570, 3575, 3577, 3579, 3582, 3586, 3593, 3596, 3598, 3601, 3602, 3605, 3606, 3607, 3610, 3618, 3626, 3627, 3630, 3637, 3641, 3644, 3646, 3649, 3654, 3655, 3657, 3659, 3661, 3669, 3674, 3675, 3676, 3692, 3699, 3705, 3706, 3711, 3717, 3724, 3733, 3735, 3736, 3740, 3741, 3745, 3752, 3755, 3756, 3764, 3769, 3770, 3778, 3780, 3785, 3790, 3803, 3805, 3808, 3812, 3815, 3816, 3817, 3818, 3823, 3825, 3826, 3827, 3831, 3833, 3836, 3839, 3845, 3847, 3854, 3857, 3859, 3860, 3863, 3865, 3866, 3867, 3869, 3870, 3883, 3884, 3892, 3897, 3926, 3931, 3932, 3936, 3938, 3948, 4001, 4003, 4004, 4009, 4011, 4012, 4017, 4019, 4020, 4021, 4022, 4024, 4025, 4030, 4031, 4032, 4033, 4034, 4036, 4037, 4038, 4042, 4043, 4044, 4045, 4046, 4047, 4048, 4049, 4050, 4054, 4056, 4058, 4059, 4063, 4065, 4068, 4069, 4070, 4071, 4073, 4074, 4076, 4079, 4081, 4082, 4085, 4086, 4087, 4089, 4090, 4091, 4093, 4095, 4097, 4099, 4102, 4103, 4104, 4106, 4108, 4110, 4115, 4116, 4117, 4119, 4120, 4123, 4124, 4125, 4126, 4127, 4128, 4129, 4131, 4132, 4133, 4135, 4139, 4144, 4145, 4146, 4148, 4150, 4151, 4155, 4158, 4161, 4163, 4164, 4166, 4167, 4169, 4171]
	list_4=[4172, 4173, 4174, 4175, 4176, 4178, 4179, 4181, 4184, 4185, 4186, 4187, 4189, 4190, 4193, 4194, 4196, 4197, 4198, 4199, 4201, 4202, 4203, 4208, 4209, 4211, 4213, 4216, 4217, 4218, 4220, 4222, 4224, 4227, 4228, 4229, 4230, 4233, 4234, 4235, 4236, 4238, 4239, 4242, 4245, 4246, 4248, 4255, 4260, 4263, 4264, 4268, 4269, 4270, 4271, 4273, 4277, 4279, 4280, 4282, 4283, 4284, 4285, 4287, 4289, 4290, 4291, 4292, 4294, 4295, 4296, 4298, 4301, 4304, 4305, 4307, 4308, 4309, 4311, 4313, 4315, 4316, 4317, 4318, 4321, 4322, 4323, 4324, 4327, 4329, 4330, 4332, 4333, 4334, 4335, 4337, 4338, 4339, 4340, 4342, 4344, 4345, 4346, 4348, 4349, 4351, 4352, 4353, 4355, 4356, 4357, 4360, 4361, 4362, 4363, 4365, 4368, 4370, 4372, 4375, 4379, 4380, 4381, 4384, 4385, 4386, 4387, 4388, 4389, 4391, 4392, 4394, 4395, 4396, 4399, 4400, 4401, 4403, 4405, 4406, 4407, 4412, 4413, 4414, 4416, 4417, 4418, 4419, 4421, 4422, 4423, 4424, 4425, 4428, 4429, 4431, 4432, 4433, 4436, 4437, 4439, 4441, 4444, 4445, 4446, 4447, 4450, 4451, 4452, 4453, 4455, 4456, 4458, 4459, 4460, 4461, 4465, 4469, 4471, 4472, 4475, 4478, 4479, 4480, 4481, 4482, 4484, 4486, 4487, 4490, 4491, 4492, 4494, 4496, 4498, 4499, 4500, 4501, 4503, 4504, 4505, 4507, 4508, 4510, 4512, 4514, 4516, 4517, 4518, 4522, 4524, 4526, 4527, 4529, 4530, 4535, 4536, 4537, 4538, 4541, 4542, 4544, 4546, 4547, 4548, 4549, 4551, 4552, 4553, 4554, 4555, 4556, 4557, 4558, 4560, 4561, 4563, 4565, 4566, 4568, 4574, 4579, 4580, 4581, 4582, 4583, 4584, 4585, 4588, 4591, 4593, 4594, 4595, 4596, 4602, 4607, 4608, 4615, 4616, 4618, 4620, 4622, 4623, 4624, 4626, 4628, 4630, 4631, 4632, 4635, 4636, 4637, 4638, 4646, 4647, 4648, 4651, 4652, 4653, 4654, 4658, 4659, 4663, 4665, 4666, 4667, 4670, 4672, 4678, 4679, 4680, 4682, 4683, 4685, 4688, 4691, 4692, 4695, 4697]
	patterns_matched_dict={}
	for cur_sent_id in list_1:
		patterns_matched_dict[cur_sent_id]=patterns_matched_dict_list_1[cur_sent_id]
		pass
	for cur_sent_id in list_2:
		patterns_matched_dict[cur_sent_id]=patterns_matched_dict_list_2[cur_sent_id]
		pass
	for cur_sent_id in list_3:
		patterns_matched_dict[cur_sent_id]=patterns_matched_dict_list_3[cur_sent_id]
		pass
	for cur_sent_id in list_4:
		patterns_matched_dict[cur_sent_id]=patterns_matched_dict_list_4[cur_sent_id]
		pass
	manual_key_list=patterns_matched_dict.keys()
	manual_key_list.sort()
	print manual_key_list==(list_1+list_2+list_3+list_4)
	pickle.dump(patterns_matched_dict,open('patterns_matched_dict.p' , 'w'))
	pass

if __name__ == '__main__':
	# get_input_sentences()
	new_from_svg=[245, 273, 335, 338, 339, 340, 342, 343, 354, 617, 640, 691, 695, 706, 830, 871, 890, 957, 976, 996, 998, 1166, 1173, 1219, 1438, 1441, 1556, 1989, 2094, 2131, 2165, 2173, 2225, 2274, 2314, 2370, 2380, 2946, 2968, 2985, 2986, 2995, 3173, 3214, 3233, 3333, 3381, 3386, 3461, 3691, 3717, 3731, 3740, 3841, 3951]
	# for cur_sent_id in new_from_svg:
	# 	make_4k_pickle(cur_sent_id)
	# 	pass
	# refiner()
	# manual_full_print()
	# complete_gold_lemma_update()
	# look_at_486()
	# prepare_pickle_ambi()
	# svg_gold_dict=pickle.load(open( "svg_gold_dict.p" , 'rb'))
	# prepare_pickle_ambi()
	get_underscore_rectifier()
	exit()
	manual_list=[1, 2, 3, 4, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 37, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52, 54, 56, 57, 58, 61, 62, 63, 64, 66, 67, 68, 77, 78, 79, 82, 84, 85, 87, 89, 90, 93, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 107, 114, 115, 117, 119, 120, 121, 124, 125, 126, 127, 128, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 144, 146, 148, 149, 151, 153, 156, 157, 159, 161, 162, 163, 164, 166, 168, 170, 171, 172, 173, 175, 176, 181, 182, 184, 186, 187, 189, 190, 191, 192, 193, 194, 195, 196, 199, 201, 202, 203, 204, 205, 206, 207, 209, 210, 211, 213, 214, 217, 218, 219, 220, 221, 222, 224, 228, 229, 230, 231, 232, 233, 236, 237, 238, 241, 242, 244, 246, 247, 248, 249, 250, 251, 252, 253, 261, 265, 269, 274, 275, 276, 278, 283, 285, 286, 287, 288, 289, 294, 295, 300, 301, 302, 303, 304, 305, 311, 315, 317, 318, 319, 320, 321, 323, 325, 328, 329, 331, 336, 345, 349, 353, 355, 356, 357, 358, 360, 361, 362, 363, 365, 366, 367, 368, 369, 371, 372, 373, 393, 397, 423, 434, 437, 441, 445, 446, 451, 458, 468, 470, 475, 476, 479, 480, 483, 484, 486, 490, 491, 492, 494, 498, 500, 502, 503, 504, 505, 506, 507, 508, 510, 512, 513, 514, 516, 517, 518, 520, 521, 524, 525, 527, 528, 529, 532, 537, 538, 539, 540, 543, 547, 548, 551, 553, 555, 556, 557, 561, 563, 564, 568, 569, 573, 576, 577, 578, 580, 583, 584, 587, 588, 593, 594, 597, 598, 600, 601, 603, 604, 605, 606, 607, 610, 611, 612, 614, 615, 621, 623, 625, 627, 628, 630, 632, 633, 636, 638, 639, 641, 644, 646, 650, 654, 655, 656, 657, 658, 659, 663, 664, 665, 672, 674, 675, 676, 680, 681, 682, 684, 686, 687, 688, 689, 692, 694, 696, 698, 699, 700, 701, 704, 707, 712, 713, 714, 717, 718, 719, 720, 721, 722, 723, 729, 731, 734, 737, 738, 742, 743, 746, 747, 748, 749, 750, 751, 752, 753, 756, 759, 761, 763, 764, 765, 766, 767, 768, 769, 770, 772, 773, 774, 777, 778, 779, 780, 784, 785, 787, 791, 792, 793, 795, 817, 818, 820, 821, 823, 825, 826, 827, 828, 829, 832, 833, 834, 836, 839, 842, 843, 844, 845, 846, 848, 849, 850, 851, 854, 857, 858, 862, 863, 864, 867, 868, 870, 874, 875, 876, 877, 879, 880, 882, 885, 886, 887, 888, 889, 909, 915, 916, 917, 918, 920, 922, 926, 927, 929, 930, 937, 938, 939, 940, 945, 946, 947, 950, 961, 964, 965, 967, 969, 970, 971, 973, 975, 977, 978, 981, 985, 987, 988, 989, 990, 991, 992, 999, 1002, 1004, 1006, 1009, 1010, 1012, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1032, 1033, 1035, 1038, 1045, 1046, 1047, 1049, 1051, 1052, 1055, 1057, 1060, 1061, 1063, 1065, 1067, 1069, 1070, 1071, 1072, 1074, 1075, 1077, 1079, 1080, 1082, 1083, 1084, 1085, 1086, 1087, 1090, 1091, 1092, 1095, 1097, 1098, 1099, 1100, 1103, 1104, 1105, 1106, 1107, 1110, 1112, 1113, 1114, 1115, 1116, 1119, 1120, 1121, 1123, 1124, 1125, 1127, 1128, 1130, 1131, 1135, 1136, 1137, 1138, 1142, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1155, 1156, 1157, 1159, 1160, 1161, 1163, 1164, 1167, 1168, 1169, 1171, 1176, 1179, 1180, 1181, 1182, 1183, 1187, 1189, 1194, 1198, 1199, 1200, 1201, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1217, 1218, 1220, 1222, 1223, 1224, 1225, 1226, 1229, 1231, 1232, 1239, 1241, 1242, 1248, 1254, 1257, 1259, 1260, 1261, 1262, 1264, 1265, 1266, 1267, 1268, 1269, 1270, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1284, 1285, 1286, 1289, 1290, 1291, 1292, 1293, 1294, 1295, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1305, 1306, 1307, 1311, 1314, 1315, 1317, 1318, 1319, 1321, 1324, 1325, 1327, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1339, 1341, 1342, 1343, 1344, 1345, 1346, 1349, 1351, 1352, 1354, 1356, 1357, 1358, 1359, 1360, 1361, 1365, 1366, 1370, 1371, 1372, 1373, 1375, 1377, 1379, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1390, 1391, 1392, 1393, 1395, 1396, 1397, 1398, 1399, 1400, 1401, 1403, 1404, 1406, 1407, 1408, 1411, 1412, 1413, 1414, 1416, 1418, 1424, 1426, 1427, 1428, 1429, 1430, 1431, 1433, 1434, 1435, 1437, 1439, 1440, 1442, 1443, 1446, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1461, 1462, 1465, 1466, 1467, 1469, 1470, 1476, 1477, 1478, 1479, 1480, 1481, 1482, 1484, 1485, 1486, 1488, 1489, 1493, 1494, 1495, 1496, 1497, 1498, 1499, 1502, 1504, 1506, 1508, 1509, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1520, 1522, 1523, 1525, 1527, 1528, 1529, 1532, 1533, 1534, 1535, 1536, 1537, 1539, 1541, 1542, 1544, 1545, 1546, 1548, 1551, 1552, 1553, 1555, 1558, 1559, 1560, 1561, 1562, 1564, 1565, 1566, 1567, 1569, 1570, 1571, 1573, 1574, 1575, 1578, 1581, 1582, 1583, 1584, 1586, 1587, 1588, 1589, 1590, 1591, 1593, 1596, 1597, 1598, 1599, 1600, 1601, 1603, 1606, 1608, 1609, 1610, 1611, 1612, 1613, 1617, 1618, 1621, 1622, 1623, 1624, 1626, 1627, 1628, 1630, 1631, 1632, 1633, 1636, 1637, 1638, 1639, 1641, 1643, 1650, 1651, 1654, 1655, 1657, 1658, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1670, 1671, 1672, 1673, 1675, 1676, 1677, 1679, 1680, 1685, 1687, 1688, 1689, 1691, 1692, 1693, 1694, 1695, 1696, 1697, 1698, 1699, 1701, 1702, 1703, 1705, 1706, 1707, 1708, 1709, 1712, 1713, 1714, 1715, 1718, 1719, 1720, 1721, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1732, 1734, 1735, 1737, 1738, 1740, 1741, 1742, 1743, 1746, 1749, 1750, 1751, 1756, 1757, 1758, 1759, 1760, 1761, 1762, 1764, 1766, 1767, 1768, 1769, 1771, 1772, 1774, 1775, 1778, 1780, 1781, 1782, 1783, 1785, 1786, 1788, 1789, 1791, 1792, 1793, 1797, 1798, 1800, 1801, 1803, 1804, 1805, 1806, 1807, 1808, 1809, 1810, 1812, 1813, 1817, 1819, 1820, 1822, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1834, 1838, 1839, 1840, 1841, 1842, 1844, 1846, 1847, 1848, 1849, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1865, 1866, 1867, 1869, 1870, 1871, 1872, 1873, 1876, 1878, 1881, 1883, 1884, 1886, 1887, 1895, 1897, 1898, 1899, 1900, 1903, 1904, 1907, 1909, 1911, 1913, 1917, 1918, 1919, 1920, 1922, 1923, 1924, 1925, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1938, 1941, 1942, 1943, 1945, 1948, 1949, 1953, 1955, 1957, 1958, 1959, 1960, 1961, 1962, 1965, 1966, 1967, 1970, 1971, 1972, 1973, 1974, 1975, 1979, 1982, 1986, 1988, 1991, 1992, 1993, 1994, 2000, 2001, 2003, 2005, 2007, 2008, 2010, 2011, 2012, 2013, 2015, 2017, 2018, 2019, 2020, 2021, 2024, 2025, 2027, 2028, 2030, 2031, 2032, 2036, 2037, 2038, 2042, 2044, 2046, 2047, 2048, 2050, 2051, 2054, 2055, 2056, 2057, 2059, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2073, 2074, 2075, 2078, 2079, 2080, 2082, 2084, 2085, 2087, 2090, 2091, 2092, 2093, 2095, 2101, 2102, 2105, 2110, 2111, 2112, 2113, 2114, 2115, 2119, 2120, 2123, 2124, 2125, 2128, 2129, 2132, 2134, 2135, 2137, 2138, 2139, 2140, 2141, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2157, 2158, 2160, 2161, 2162, 2163, 2167, 2168, 2169, 2170, 2171, 2172, 2174, 2177, 2180, 2183, 2185, 2186, 2187, 2188, 2189, 2190, 2191, 2195, 2196, 2197, 2199, 2202, 2203, 2204, 2206, 2208, 2209, 2210, 2211, 2212, 2214, 2216, 2218, 2221, 2224, 2228, 2229, 2231, 2232, 2233, 2234, 2235, 2237, 2238, 2239, 2241, 2246, 2247, 2249, 2250, 2251, 2252, 2253, 2256, 2257, 2258, 2260, 2262, 2263, 2264, 2266, 2269, 2270, 2275, 2276, 2280, 2286, 2287, 2290, 2292, 2293, 2296, 2298, 2299, 2301, 2303, 2305, 2306, 2307, 2309, 2310, 2313, 2315, 2317, 2319, 2320, 2324, 2327, 2328, 2329, 2330, 2332, 2333, 2334, 2336, 2338, 2340, 2341, 2342, 2345, 2346, 2347, 2348, 2349, 2350, 2351, 2352, 2354, 2355, 2356, 2358, 2362, 2364, 2365, 2366, 2367, 2369, 2371, 2372, 2374, 2376, 2377, 2378, 2381, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2397, 2398, 2401, 2406, 2407, 2408, 2409, 2411, 2412, 2413, 2414, 2415, 2418, 2419, 2421, 2423, 2424, 2426, 2427, 2428, 2431, 2432, 2436, 2437, 2438, 2441, 2443, 2448, 2450, 2451, 2455, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2468, 2470, 2472, 2473, 2475, 2478, 2479, 2483, 2484, 2485, 2486, 2487, 2488, 2489, 2490, 2491, 2492, 2493, 2494, 2495, 2498, 2499, 2500, 2501, 2502, 2503, 2505, 2507, 2508, 2510, 2511, 2512, 2513, 2516, 2517, 2518, 2519, 2520, 2522, 2523, 2525, 2526, 2527, 2528, 2529, 2530, 2531, 2532, 2533, 2536, 2537, 2538, 2539, 2541, 2544, 2545, 2548, 2553, 2555, 2558, 2560, 2561, 2562, 2563, 2566, 2567, 2568, 2569, 2571, 2572, 2574, 2575, 2576, 2577, 2578, 2580, 2581, 2582, 2585, 2588, 2589, 2590, 2591, 2592, 2593, 2598, 2599, 2600, 2601, 2602, 2603, 2605, 2608, 2610, 2612, 2613, 2615, 2616, 2620, 2621, 2622, 2623, 2624, 2625, 2626, 2628, 2629, 2631, 2632, 2633, 2635, 2638, 2639, 2642, 2644, 2645, 2646, 2650, 2651, 2652, 2653, 2655, 2656, 2659, 2660, 2663, 2664, 2665, 2666, 2667, 2668, 2670, 2671, 2673, 2674, 2675, 2677, 2678, 2679, 2680, 2681, 2683, 2685, 2686, 2688, 2689, 2690, 2691, 2692, 2693, 2697, 2698, 2699, 2700, 2701, 2702, 2703, 2705, 2708, 2710, 2713, 2714, 2717, 2719, 2721, 2722, 2724, 2725, 2726, 2727, 2728, 2729, 2730, 2731, 2734, 2736, 2737, 2739, 2740, 2741, 2743, 2744, 2748, 2751, 2752, 2754, 2760, 2762, 2764, 2765, 2767, 2769, 2770, 2771, 2776, 2779, 2780, 2781, 2782, 2783, 2784, 2785, 2786, 2787, 2792, 2794, 2795, 2796, 2797, 2801, 2802, 2803, 2804, 2807, 2809, 2810, 2811, 2813, 2815, 2819, 2820, 2824, 2825, 2827, 2829, 2830, 2832, 2833, 2836, 2838, 2839, 2840, 2845, 2847, 2849, 2853, 2854, 2856, 2857, 2858, 2859, 2860, 2861, 2863, 2865, 2866, 2868, 2871, 2873, 2874, 2876, 2878, 2880, 2881, 2883, 2889, 2890, 2895, 2900, 2904, 2905, 2906, 2908, 2910, 2914, 2915, 2916, 2917, 2919, 2920, 2922, 2923, 2924, 2928, 2929, 2931, 2932, 2938, 2939, 2940, 2941, 2944, 2945, 2947, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2958, 2964, 2966, 2967, 2971, 2972, 2975, 2980, 2981, 2984, 2987, 2990, 2991, 2993, 2996, 2998, 2999, 3000, 3004, 3005, 3008, 3011, 3013, 3016, 3019, 3020, 3022, 3023, 3024, 3025, 3028, 3031, 3032, 3033, 3034, 3035, 3037, 3038, 3040, 3042, 3043, 3044, 3045, 3047, 3048, 3049, 3050, 3051, 3052, 3056, 3057, 3060, 3061, 3062, 3063, 3064, 3065, 3067, 3068, 3069, 3070, 3071, 3072, 3073, 3074, 3076, 3078, 3079, 3080, 3082, 3083, 3086, 3087, 3088, 3089, 3090, 3091, 3092, 3093, 3094, 3095, 3096, 3098, 3099, 3100, 3102, 3106, 3107, 3109, 3111, 3112, 3114, 3115, 3116, 3117, 3118, 3122, 3123, 3125, 3126, 3127, 3129, 3131, 3132, 3133, 3134, 3136, 3137, 3138, 3139, 3140, 3142, 3143, 3144, 3146, 3147, 3149, 3153, 3154, 3156, 3157, 3158, 3161, 3164, 3165, 3168, 3169, 3174, 3176, 3178, 3179, 3180, 3181, 3182, 3183, 3185, 3186, 3187, 3188, 3190, 3191, 3192, 3193, 3196, 3198, 3200, 3202, 3205, 3206, 3207, 3209, 3211, 3215, 3217, 3218, 3220, 3222, 3223, 3224, 3225, 3228, 3230, 3232, 3234, 3236, 3237, 3238, 3239, 3240, 3241, 3243, 3245, 3247, 3249, 3250, 3254, 3255, 3257, 3258, 3261, 3262, 3263, 3264, 3266, 3267, 3270, 3271, 3272, 3274, 3276, 3277, 3278, 3279, 3281, 3282, 3284, 3285, 3288, 3292, 3293, 3294, 3296, 3299, 3300, 3301, 3302, 3303, 3304, 3306, 3307, 3308, 3310, 3312, 3316, 3320, 3322, 3323, 3324, 3325, 3326, 3328, 3329, 3332, 3334, 3336, 3337, 3338, 3339, 3340, 3342, 3343, 3345, 3347, 3354, 3355, 3357, 3358, 3359, 3360, 3361, 3362, 3363, 3365, 3366, 3367, 3369, 3371, 3372, 3374, 3376, 3377, 3378, 3379, 3380, 3383, 3385, 3387, 3393, 3394, 3396, 3399, 3400, 3402, 3403, 3406, 3408, 3409, 3410, 3416, 3417, 3419, 3425, 3427, 3428, 3429, 3432, 3433, 3435, 3436, 3438, 3443, 3445, 3446, 3447, 3448, 3449, 3451, 3452, 3453, 3454, 3455, 3459, 3463, 3464, 3466, 3467, 3469, 3470, 3473, 3475, 3477, 3478, 3480, 3482, 3483, 3484, 3486, 3487, 3488, 3489, 3490, 3491, 3492, 3493, 3495, 3496, 3497, 3499, 3500, 3503, 3504, 3505, 3508, 3512, 3513, 3514, 3516, 3517, 3518, 3520, 3521, 3522, 3523, 3525, 3527, 3528, 3529, 3530, 3532, 3536, 3541, 3542, 3547, 3548, 3550, 3551, 3552, 3553, 3555, 3556, 3562, 3565, 3567, 3569, 3570, 3574, 3575, 3577, 3578, 3579, 3580, 3581, 3584, 3586, 3588, 3591, 3593, 3594, 3596, 3597, 3598, 3600, 3601, 3602, 3603, 3605, 3606, 3607, 3610, 3611, 3612, 3614, 3615, 3616, 3618, 3621, 3624, 3626, 3627, 3628, 3629, 3630, 3632, 3633, 3635, 3636, 3637, 3638, 3639, 3641, 3643, 3644, 3646, 3647, 3649, 3651, 3652, 3654, 3655, 3656, 3657, 3659, 3660, 3661, 3662, 3664, 3665, 3666, 3669, 3671, 3672, 3674, 3675, 3676, 3678, 3679, 3681, 3682, 3684, 3687, 3688, 3689, 3692, 3693, 3694, 3696, 3699, 3700, 3704, 3705, 3706, 3709, 3710, 3713, 3715, 3716, 3718, 3719, 3720, 3721, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3733, 3734, 3736, 3737, 3738, 3742, 3744, 3745, 3746, 3747, 3748, 3750, 3752, 3753, 3754, 3755, 3756, 3759, 3760, 3765, 3766, 3768, 3769, 3770, 3771, 3775, 3776, 3778, 3780, 3781, 3783, 3784, 3785, 3786, 3787, 3788, 3792, 3794, 3796, 3799, 3802, 3803, 3804, 3805, 3806, 3807, 3808, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3822, 3823, 3824, 3825, 3826, 3827, 3828, 3829, 3830, 3831, 3832, 3833, 3834, 3835, 3836, 3837, 3838, 3839, 3842, 3845, 3846, 3847, 3848, 3849, 3852, 3853, 3854, 3855, 3856, 3857, 3859, 3860, 3863, 3864, 3865, 3866, 3867, 3868, 3870, 3872, 3879, 3883, 3884, 3885, 3889, 3891, 3892, 3893, 3895, 3897, 3898, 3902, 3904, 3906, 3907, 3909, 3910, 3919, 3921, 3923, 3924, 3926, 3929, 3930, 3931, 3932, 3934, 3936, 3937, 3938, 3939, 3940, 3941, 3942, 3946, 3947, 3948]
	# manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))
	# error_list=list(set(error_list))
	# error_list.sort()
	# print error_list
	# update_manual()
	update_pos_bug_fix_svg()
	exit()
	# get_manual_trees()
	# svg
	# update_none_none_to_ca()
	# update_manual()
	# manual_full_print()
	# cur_fixer()
	# exit()
	svg_list=[9, 15, 47, 53, 59, 65, 71, 73, 74, 76, 81, 88, 92, 94, 99, 106, 108, 109, 110, 111, 112, 113, 122, 123, 129, 142, 143, 145, 147, 150, 152, 154, 155, 160, 165, 167, 169, 174, 177, 179, 180, 183, 185, 188, 197, 198, 200, 208, 212, 215, 216, 223, 225, 226, 227, 234, 235, 239, 240, 243, 245, 254, 255, 256, 257, 258, 262, 263, 264, 266, 270, 271, 272, 273, 277, 279, 280, 281, 282, 284, 290, 291, 292, 293, 296, 297, 298, 299, 306, 307, 308, 309, 310, 312, 313, 314, 316, 324, 326, 332, 333, 334, 335, 338, 339, 340, 341, 342, 343, 346, 347, 348, 350, 351, 354, 359, 404, 430, 474, 487, 488, 499, 522, 523, 526, 530, 541, 574, 575, 581, 589, 591, 592, 596, 602, 609, 617, 618, 619, 620, 622, 624, 626, 629, 631, 634, 635, 640, 642, 643, 645, 647, 648, 649, 651, 652, 661, 668, 669, 677, 679, 683, 685, 690, 691, 693, 695, 697, 702, 703, 705, 706, 709, 715, 716, 730, 740, 741, 745, 771, 775, 776, 781, 782, 783, 786, 815, 816, 819, 822, 824, 830, 835, 840, 847, 852, 853, 855, 856, 859, 860, 861, 865, 866, 869, 871, 872, 873, 881, 884, 890, 891, 919, 936, 941, 943, 944, 952, 953, 954, 957, 959, 963, 966, 968, 972, 976, 980, 984, 986, 993, 996, 997, 998, 1000, 1001, 1003, 1005, 1007, 1008, 1011, 1013, 1014, 1015, 1027, 1031, 1034, 1036, 1037, 1040, 1041, 1042, 1043, 1044, 1050, 1054, 1064, 1081, 1088, 1093, 1094, 1096, 1102, 1108, 1117, 1118, 1133, 1134, 1154, 1158, 1166, 1173, 1174, 1177, 1190, 1192, 1216, 1219, 1227, 1283, 1338, 1340, 1347, 1348, 1350, 1364, 1369, 1376, 1378, 1405, 1409, 1420, 1423, 1425, 1436, 1438, 1441, 1447, 1448, 1459, 1463, 1468, 1483, 1490, 1491, 1503, 1521, 1524, 1526, 1530, 1531, 1538, 1549, 1556, 1568, 1572, 1585, 1605, 1614, 1625, 1634, 1635, 1644, 1645, 1646, 1649, 1656, 1659, 1669, 1717, 1731, 1745, 1765, 1770, 1773, 1776, 1790, 1794, 1823, 1832, 1896, 1915, 1921, 1946, 1954, 1969, 1976, 1984, 1989, 1999, 2009, 2016, 2022, 2026, 2029, 2033, 2039, 2043, 2045, 2058, 2061, 2069, 2086, 2089, 2094, 2100, 2103, 2108, 2109, 2126, 2130, 2131, 2165, 2173, 2194, 2198, 2200, 2215, 2223, 2225, 2240, 2242, 2243, 2255, 2274, 2314, 2316, 2318, 2344, 2353, 2357, 2359, 2360, 2370, 2379, 2380, 2396, 2449, 2452, 2454, 2456, 2474, 2477, 2481, 2542, 2546, 2556, 2557, 2559, 2583, 2586, 2595, 2636, 2649, 2669, 2732, 2733, 2753, 2778, 2791, 2799, 2805, 2814, 2821, 2826, 2828, 2831, 2835, 2843, 2852, 2855, 2872, 2877, 2884, 2886, 2888, 2891, 2896, 2901, 2911, 2930, 2936, 2946, 2948, 2957, 2968, 2978, 2985, 2986, 2988, 2992, 2995, 2997, 3003, 3015, 3018, 3026, 3027, 3036, 3039, 3055, 3058, 3097, 3101, 3103, 3160, 3173, 3195, 3208, 3214, 3219, 3231, 3233, 3244, 3248, 3275, 3283, 3311, 3313, 3319, 3333, 3344, 3346, 3348, 3349, 3350, 3352, 3368, 3381, 3386, 3391, 3395, 3405, 3418, 3423, 3461, 3468, 3479, 3526, 3533, 3537, 3545, 3554, 3563, 3582, 3634, 3658, 3673, 3691, 3697, 3703, 3708, 3711, 3717, 3731, 3735, 3740, 3741, 3763, 3764, 3779, 3782, 3790, 3791, 3798, 3821, 3840, 3841, 3869, 3888, 3896, 3908, 3920, 3935, 3951]
	file_list_pickles=[1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 37, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 52, 53, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 71, 73, 74, 76, 77, 78, 79, 81, 82, 84, 85, 87, 88, 89, 90, 92, 93, 94, 99, 106, 108, 109, 110, 111, 112, 113, 114, 120, 122, 123, 129, 131, 132, 133, 134, 135, 136, 137, 139, 140, 142, 143, 145, 147, 148, 149, 150, 151, 152, 154, 155, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 171, 173, 174, 177, 179, 180, 181, 182, 183, 185, 186, 187, 188, 189, 190, 191, 193, 194, 197, 198, 199, 200, 202, 204, 205, 206, 207, 208, 209, 210, 212, 214, 215, 216, 218, 220, 221, 223, 224, 225, 226, 227, 231, 234, 235, 239, 240, 242, 243, 254, 255, 256, 257, 258, 260, 262, 263, 264, 266, 270, 271, 272, 277, 278, 279, 280, 281, 282, 284, 290, 291, 292, 293, 296, 297, 298, 299, 300, 304, 306, 307, 308, 309, 310, 312, 313, 314, 315, 316, 318, 319, 321, 323, 324, 325, 326, 328, 329, 332, 333, 334, 341, 345, 346, 347, 348, 349, 350, 351, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 369, 371, 372, 373, 374, 375, 376, 377, 380, 381, 382, 383, 384, 385, 386, 388, 390, 391, 392, 393, 395, 396, 397, 399, 401, 402, 403, 404, 407, 408, 410, 412, 413, 415, 416, 417, 419, 420, 424, 427, 428, 430, 431, 434, 435, 436, 437, 438, 439, 441, 442, 443, 444, 446, 447, 449, 450, 451, 453, 454, 455, 457, 458, 460, 461, 462, 465, 467, 468, 470, 474, 475, 476, 479, 480, 482, 483, 484, 486, 487, 488, 490, 491, 492, 494, 495, 497, 498, 499, 500, 502, 503, 504, 505, 506, 507, 508, 510, 511, 512, 513, 516, 517, 518, 520, 521, 522, 523, 524, 525, 526, 527, 529, 530, 537, 538, 540, 541, 543, 544, 545, 546, 547, 548, 551, 553, 555, 556, 557, 561, 563, 564, 568, 569, 570, 574, 575, 577, 578, 580, 581, 583, 584, 587, 588, 589, 591, 592, 593, 594, 596, 598, 602, 603, 605, 606, 607, 609, 610, 611, 612, 618, 619, 620, 621, 622, 623, 624, 626, 627, 628, 629, 631, 632, 633, 634, 635, 636, 642, 643, 645, 646, 647, 648, 649, 650, 651, 652, 657, 659, 661, 663, 668, 669, 672, 673, 677, 679, 683, 685, 690, 693, 697, 698, 699, 700, 702, 703, 705, 709, 715, 716, 718, 721, 730, 740, 741, 745, 750, 763, 770, 771, 774, 775, 776, 778, 781, 782, 783, 786, 795, 815, 816, 819, 820, 822, 824, 829, 835, 840, 844, 845, 847, 848, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 864, 865, 866, 869, 870, 872, 873, 876, 881, 884, 889, 891, 919, 929, 936, 941, 943, 944, 952, 953, 954, 959, 963, 966, 967, 968, 972, 975, 980, 984, 986, 993, 997, 1000, 1001, 1003, 1005, 1006, 1007, 1008, 1011, 1013, 1014, 1015, 1017, 1027, 1031, 1033, 1034, 1036, 1037, 1040, 1041, 1042, 1043, 1044, 1045, 1047, 1049, 1050, 1051, 1052, 1054, 1055, 1056, 1057, 1059, 1060, 1063, 1064, 1065, 1067, 1069, 1070, 1071, 1074, 1077, 1079, 1080, 1081, 1082, 1083, 1084, 1085, 1086, 1088, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1098, 1099, 1101, 1102, 1104, 1105, 1106, 1107, 1108, 1110, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1119, 1120, 1121, 1124, 1125, 1127, 1128, 1130, 1131, 1133, 1134, 1135, 1136, 1138, 1139, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1163, 1164, 1167, 1168, 1169, 1174, 1176, 1177, 1181, 1182, 1183, 1184, 1185, 1186, 1188, 1190, 1191, 1192, 1193, 1195, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1222, 1223, 1224, 1226, 1227, 1229, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1240, 1241, 1242, 1243, 1249, 1251, 1255, 1256, 1257, 1260, 1261, 1262, 1264, 1265, 1266, 1269, 1270, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1285, 1286, 1288, 1289, 1290, 1291, 1292, 1294, 1296, 1297, 1298, 1299, 1300, 1301, 1302, 1303, 1307, 1311, 1314, 1315, 1319, 1325, 1327, 1328, 1331, 1332, 1333, 1337, 1338, 1340, 1341, 1342, 1343, 1344, 1345, 1346, 1347, 1348, 1349, 1350, 1352, 1354, 1356, 1357, 1359, 1360, 1364, 1365, 1366, 1369, 1370, 1371, 1373, 1375, 1376, 1378, 1379, 1381, 1382, 1383, 1384, 1385, 1386, 1387, 1388, 1389, 1391, 1392, 1395, 1396, 1398, 1399, 1400, 1401, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1411, 1412, 1413, 1414, 1418, 1420, 1423, 1424, 1425, 1427, 1429, 1430, 1431, 1433, 1434, 1435, 1436, 1437, 1439, 1440, 1442, 1446, 1447, 1448, 1449, 1450, 1451, 1452, 1453, 1454, 1455, 1456, 1459, 1461, 1462, 1463, 1465, 1466, 1467, 1468, 1469, 1470, 1476, 1477, 1480, 1481, 1483, 1485, 1486, 1488, 1489, 1490, 1491, 1493, 1495, 1496, 1497, 1498, 1499, 1502, 1503, 1504, 1506, 1509, 1511, 1512, 1513, 1514, 1515, 1516, 1517, 1520, 1521, 1523, 1524, 1525, 1526, 1527, 1529, 1530, 1531, 1532, 1533, 1534, 1535, 1538, 1541, 1542, 1544, 1545, 1546, 1548, 1549, 1552, 1553, 1560, 1561, 1562, 1566, 1567, 1568, 1570, 1571, 1572, 1573, 1574, 1575, 1578, 1581, 1582, 1583, 1584, 1585, 1586, 1587, 1588, 1589, 1590, 1591, 1593, 1596, 1597, 1598, 1599, 1603, 1605, 1606, 1608, 1609, 1610, 1611, 1612, 1613, 1614, 1617, 1618, 1621, 1622, 1623, 1624, 1625, 1626, 1628, 1630, 1631, 1632, 1634, 1635, 1637, 1638, 1639, 1641, 1643, 1644, 1645, 1646, 1649, 1650, 1651, 1654, 1655, 1656, 1658, 1659, 1660, 1661, 1662, 1663, 1664, 1665, 1666, 1667, 1668, 1669, 1670, 1671, 1674, 1675, 1676, 1677, 1678, 1679, 1681, 1685, 1686, 1687, 1688, 1689, 1691, 1692, 1694, 1695, 1696, 1697, 1698, 1699, 1701, 1702, 1703, 1705, 1706, 1707, 1708, 1709, 1713, 1714, 1715, 1716, 1717, 1718, 1719, 1720, 1721, 1723, 1724, 1725, 1726, 1727, 1728, 1729, 1731, 1732, 1734, 1735, 1737, 1738, 1740, 1741, 1742, 1743, 1745, 1749, 1750, 1751, 1756, 1757, 1758, 1759, 1760, 1762, 1764, 1765, 1766, 1768, 1770, 1771, 1772, 1773, 1776, 1778, 1780, 1782, 1783, 1785, 1786, 1788, 1789, 1790, 1792, 1793, 1794, 1797, 1798, 1800, 1801, 1803, 1804, 1805, 1806, 1807, 1810, 1812, 1813, 1817, 1819, 1820, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1832, 1834, 1838, 1839, 1840, 1841, 1842, 1844, 1846, 1847, 1848, 1849, 1853, 1854, 1855, 1857, 1858, 1860, 1861, 1865, 1866, 1867, 1869, 1870, 1871, 1872, 1878, 1884, 1886, 1895, 1896, 1897, 1898, 1899, 1900, 1903, 1904, 1907, 1909, 1911, 1915, 1917, 1918, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1938, 1940, 1941, 1942, 1943, 1945, 1946, 1948, 1949, 1952, 1954, 1955, 1957, 1959, 1961, 1962, 1965, 1966, 1967, 1969, 1970, 1971, 1972, 1973, 1974, 1975, 1976, 1979, 1982, 1984, 1986, 1988, 1990, 1991, 1992, 1993, 1994, 1999, 2000, 2001, 2003, 2004, 2005, 2007, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2024, 2025, 2026, 2029, 2030, 2031, 2033, 2036, 2037, 2038, 2039, 2040, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2050, 2051, 2054, 2056, 2057, 2058, 2059, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2073, 2074, 2075, 2078, 2079, 2080, 2082, 2084, 2085, 2086, 2087, 2089, 2090, 2091, 2092, 2093, 2095, 2100, 2101, 2102, 2103, 2105, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2119, 2120, 2123, 2124, 2125, 2126, 2128, 2129, 2130, 2132, 2134, 2135, 2137, 2138, 2139, 2140, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2157, 2160, 2161, 2162, 2163, 2167, 2168, 2169, 2170, 2171, 2172, 2177, 2178, 2179, 2180, 2181, 2183, 2185, 2186, 2187, 2188, 2189, 2190, 2191, 2192, 2193, 2194, 2195, 2196, 2197, 2198, 2199, 2200, 2202, 2203, 2204, 2206, 2208, 2209, 2210, 2211, 2212, 2214, 2215, 2216, 2221, 2223, 2228, 2229, 2231, 2232, 2233, 2234, 2235, 2237, 2238, 2240, 2241, 2242, 2243, 2246, 2247, 2249, 2250, 2251, 2252, 2253, 2254, 2255, 2256, 2258, 2260, 2262, 2263, 2264, 2265, 2266, 2269, 2270, 2275, 2280, 2284, 2286, 2287, 2290, 2292, 2296, 2297, 2298, 2299, 2301, 2303, 2305, 2306, 2310, 2313, 2315, 2316, 2317, 2318, 2319, 2320, 2321, 2324, 2327, 2328, 2329, 2330, 2332, 2333, 2336, 2337, 2340, 2342, 2343, 2344, 2346, 2347, 2348, 2349, 2350, 2351, 2352, 2353, 2355, 2357, 2359, 2360, 2362, 2363, 2364, 2365, 2366, 2367, 2369, 2371, 2374, 2376, 2377, 2378, 2379, 2381, 2382, 2386, 2387, 2388, 2389, 2390, 2391, 2392, 2393, 2394, 2395, 2396, 2398, 2401, 2406, 2407, 2408, 2409, 2411, 2412, 2413, 2414, 2415, 2418, 2419, 2421, 2423, 2424, 2426, 2428, 2431, 2432, 2433, 2436, 2437, 2438, 2441, 2443, 2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2458, 2459, 2460, 2461, 2462, 2463, 2464, 2465, 2466, 2467, 2470, 2471, 2472, 2473, 2474, 2475, 2476, 2477, 2478, 2479, 2480, 2481, 2483, 2485, 2486, 2487, 2488, 2489, 2490, 2491, 2493, 2494, 2495, 2498, 2499, 2500, 2501, 2502, 2503, 2504, 2505, 2507, 2508, 2510, 2511, 2512, 2513, 2514, 2515, 2516, 2517, 2518, 2519, 2520, 2521, 2522, 2523, 2525, 2526, 2527, 2528, 2530, 2531, 2532, 2533, 2534, 2535, 2539, 2540, 2541, 2542, 2545, 2546, 2548, 2553, 2555, 2556, 2557, 2559, 2560, 2561, 2562, 2563, 2568, 2569, 2570, 2571, 2572, 2574, 2575, 2576, 2577, 2578, 2580, 2581, 2582, 2583, 2585, 2586, 2588, 2589, 2590, 2591, 2592, 2593, 2594, 2595, 2598, 2599, 2600, 2601, 2602, 2603, 2605, 2608, 2609, 2610, 2612, 2613, 2615, 2616, 2620, 2621, 2622, 2623, 2624, 2625, 2626, 2628, 2629, 2631, 2632, 2633, 2636, 2637, 2638, 2639, 2642, 2644, 2645, 2649, 2650, 2651, 2652, 2653, 2655, 2656, 2659, 2660, 2661, 2663, 2664, 2665, 2666, 2667, 2668, 2669, 2670, 2671, 2673, 2674, 2675, 2677, 2678, 2679, 2680, 2681, 2682, 2683, 2685, 2686, 2689, 2690, 2691, 2692, 2695, 2696, 2697, 2698, 2701, 2702, 2703, 2708, 2710, 2713, 2714, 2717, 2719, 2721, 2722, 2724, 2725, 2726, 2727, 2729, 2730, 2731, 2732, 2733, 2734, 2737, 2738, 2739, 2740, 2741, 2743, 2744, 2746, 2748, 2751, 2752, 2753, 2754, 2759, 2760, 2762, 2763, 2764, 2765, 2767, 2770, 2771, 2776, 2777, 2778, 2779, 2780, 2781, 2782, 2783, 2784, 2785, 2786, 2787, 2790, 2791, 2792, 2794, 2795, 2796, 2797, 2799, 2800, 2801, 2802, 2803, 2804, 2805, 2807, 2809, 2811, 2812, 2813, 2814, 2820, 2821, 2823, 2824, 2826, 2828, 2830, 2831, 2832, 2833, 2835, 2836, 2838, 2839, 2843, 2845, 2846, 2847, 2852, 2853, 2854, 2855, 2856, 2857, 2858, 2859, 2860, 2861, 2863, 2865, 2866, 2872, 2874, 2875, 2877, 2878, 2880, 2883, 2884, 2885, 2886, 2887, 2888, 2889, 2890, 2891, 2892, 2895, 2896, 2900, 2901, 2902, 2903, 2904, 2905, 2906, 2908, 2910, 2911, 2914, 2915, 2916, 2917, 2919, 2920, 2921, 2922, 2923, 2924, 2925, 2928, 2929, 2930, 2931, 2932, 2934, 2935, 2936, 2937, 2938, 2939, 2940, 2941, 2942, 2944, 2945, 2947, 2948, 2949, 2950, 2951, 2952, 2953, 2954, 2955, 2956, 2957, 2958, 2962, 2964, 2965, 2966, 2967, 2970, 2971, 2972, 2974, 2975, 2976, 2978, 2979, 2980, 2981, 2982, 2983, 2984, 2987, 2988, 2990, 2991, 2992, 2993, 2996, 2997, 2998, 2999, 3000, 3003, 3004, 3005, 3008, 3011, 3012, 3013, 3015, 3016, 3018, 3019, 3020, 3021, 3022, 3023, 3024, 3025, 3026, 3027, 3028, 3030, 3032, 3033, 3034, 3035, 3036, 3037, 3038, 3039, 3042, 3043, 3044, 3045, 3047, 3048, 3049, 3050, 3051, 3052, 3055, 3056, 3057, 3058, 3061, 3062, 3063, 3064, 3065, 3067, 3068, 3069, 3070, 3071, 3072, 3073, 3074, 3076, 3078, 3079, 3080, 3081, 3082, 3083, 3085, 3086, 3087, 3089, 3090, 3091, 3092, 3093, 3094, 3095, 3096, 3097, 3098, 3099, 3100, 3101, 3103, 3104, 3105, 3106, 3107, 3109, 3112, 3114, 3115, 3116, 3117, 3118, 3121, 3122, 3123, 3125, 3126, 3128, 3129, 3130, 3131, 3132, 3133, 3134, 3136, 3137, 3138, 3139, 3140, 3142, 3143, 3144, 3146, 3147, 3149, 3154, 3156, 3157, 3158, 3159, 3160, 3161, 3164, 3166, 3168, 3169, 3174, 3176, 3177, 3178, 3179, 3180, 3181, 3182, 3183, 3185, 3186, 3188, 3189, 3190, 3191, 3192, 3193, 3195, 3196, 3198, 3202, 3206, 3208, 3209, 3211, 3215, 3217, 3218, 3219, 3220, 3221, 3222, 3223, 3224, 3225, 3228, 3230, 3231, 3232, 3234, 3236, 3237, 3238, 3239, 3240, 3241, 3243, 3244, 3245, 3247, 3248, 3249, 3250, 3254, 3255, 3258, 3261, 3262, 3263, 3264, 3265, 3266, 3267, 3270, 3271, 3272, 3274, 3275, 3276, 3277, 3278, 3279, 3281, 3282, 3283, 3284, 3285, 3288, 3292, 3293, 3294, 3296, 3298, 3299, 3300, 3301, 3302, 3303, 3304, 3306, 3307, 3308, 3310, 3311, 3312, 3313, 3314, 3316, 3319, 3320, 3322, 3324, 3325, 3326, 3328, 3329, 3332, 3334, 3336, 3337, 3338, 3339, 3340, 3341, 3342, 3343, 3344, 3345, 3346, 3348, 3349, 3350, 3352, 3355, 3358, 3359, 3360, 3363, 3365, 3366, 3367, 3368, 3369, 3371, 3372, 3374, 3375, 3377, 3378, 3379, 3380, 3383, 3385, 3387, 3391, 3393, 3394, 3395, 3396, 3400, 3401, 3402, 3403, 3405, 3406, 3408, 3409, 3410, 3416, 3417, 3418, 3419, 3421, 3423, 3425, 3427, 3428, 3429, 3432, 3435, 3436, 3438, 3443, 3445, 3446, 3447, 3448, 3449, 3451, 3452, 3453, 3454, 3455, 3459, 3466, 3468, 3470, 3472, 3473, 3476, 3478, 3479, 3480, 3481, 3482, 3483, 3484, 3486, 3487, 3488, 3489, 3490, 3491, 3492, 3493, 3495, 3496, 3500, 3503, 3504, 3505, 3508, 3511, 3512, 3513, 3514, 3516, 3517, 3521, 3522, 3523, 3525, 3526, 3527, 3528, 3529, 3530, 3532, 3533, 3536, 3537, 3541, 3542, 3544, 3545, 3547, 3548, 3550, 3551, 3554, 3555, 3556, 3557, 3562, 3563, 3567, 3569, 3570, 3573, 3574, 3575, 3577, 3578, 3579, 3580, 3581, 3582, 3584, 3585, 3586, 3588, 3590, 3591, 3593, 3594, 3596, 3597, 3598, 3600, 3601, 3602, 3603, 3606, 3607, 3610, 3611, 3612, 3614, 3615, 3616, 3618, 3621, 3624, 3626, 3627, 3628, 3629, 3630, 3633, 3634, 3635, 3636, 3637, 3638, 3639, 3641, 3643, 3644, 3646, 3647, 3649, 3651, 3652, 3654, 3655, 3656, 3657, 3658, 3659, 3660, 3661, 3662, 3664, 3665, 3666, 3669, 3671, 3672, 3673, 3675, 3676, 3678, 3679, 3681, 3682, 3684, 3687, 3688, 3689, 3692, 3694, 3697, 3699, 3700, 3702, 3703, 3705, 3706, 3708, 3709, 3711, 3715, 3716, 3718, 3720, 3721, 3724, 3725, 3726, 3727, 3728, 3729, 3730, 3733, 3735, 3736, 3737, 3741, 3742, 3744, 3745, 3746, 3747, 3748, 3750, 3752, 3753, 3754, 3755, 3756, 3759, 3760, 3763, 3764, 3765, 3766, 3768, 3769, 3770, 3771, 3775, 3776, 3778, 3779, 3780, 3781, 3782, 3783, 3784, 3785, 3786, 3787, 3790, 3791, 3792, 3794, 3796, 3798, 3799, 3802, 3803, 3804, 3805, 3806, 3807, 3808, 3810, 3811, 3812, 3813, 3814, 3815, 3816, 3817, 3818, 3819, 3821, 3822, 3825, 3826, 3827, 3828, 3829, 3831, 3832, 3835, 3836, 3837, 3838, 3839, 3840, 3845, 3846, 3847, 3848, 3849, 3852, 3853, 3854, 3855, 3856, 3857, 3859, 3860, 3862, 3863, 3864, 3865, 3866, 3867, 3868, 3869, 3870, 3872, 3879, 3883, 3884, 3885, 3888, 3891, 3892, 3893, 3895, 3896, 3897, 3898, 3902, 3904, 3906, 3907, 3908, 3909, 3910, 3919, 3920, 3921, 3923, 3924, 3926, 3929, 3930, 3931, 3932, 3934, 3935, 3936, 3937, 3938, 3939, 3940, 3941, 3942, 3946, 3947, 3948]
	new_from_svg=[245, 273, 335, 338, 339, 340, 342, 343, 354, 617, 640, 691, 695, 706, 830, 871, 890, 957, 976, 996, 998, 1166, 1173, 1219, 1438, 1441, 1556, 1989, 2094, 2131, 2165, 2173, 2225, 2274, 2314, 2370, 2380, 2946, 2968, 2985, 2986, 2995, 3173, 3214, 3233, 3333, 3381, 3386, 3461, 3691, 3717, 3731, 3740, 3841, 3951]

	# manual_refined_dict=pickle.load(open( "manual_refined_dict.p" , 'rb'))	
	# final_dataset=pickle.load(open( "final_dataset.p" , 'rb'))
	previous_486=[2, 3, 4, 6, 42, 50, 51, 54, 56, 95, 96, 97, 98, 100, 101, 102, 103, 104, 105, 107, 115, 117, 119, 121, 124, 125, 126, 127, 128, 130, 138, 144, 146, 153, 156, 157, 170, 172, 175, 176, 184, 192, 195, 196, 201, 203, 211, 213, 217, 219, 222, 228, 229, 230, 232, 233, 236, 237, 238, 241, 244, 246, 247, 248, 249, 250, 251, 252, 253, 261, 265, 269, 274, 275, 276, 283, 285, 286, 287, 288, 289, 294, 295, 301, 302, 303, 305, 311, 317, 320, 331, 336, 353, 355, 368, 423, 445, 514, 528, 532, 539, 573, 576, 597, 600, 601, 604, 614, 615, 625, 630, 638, 639, 641, 644, 654, 655, 656, 658, 664, 665, 674, 675, 676, 680, 681, 682, 684, 686, 687, 688, 689, 692, 694, 696, 701, 704, 707, 712, 713, 714, 717, 719, 720, 722, 723, 729, 731, 734, 737, 738, 742, 743, 746, 747, 748, 749, 751, 752, 753, 756, 759, 761, 764, 765, 766, 767, 768, 769, 772, 773, 777, 779, 780, 784, 785, 787, 791, 792, 793, 817, 818, 821, 823, 825, 826, 827, 828, 832, 833, 834, 836, 839, 842, 843, 846, 849, 850, 851, 862, 863, 867, 868, 874, 875, 877, 879, 880, 882, 885, 886, 887, 888, 909, 915, 916, 917, 918, 920, 922, 926, 927, 930, 937, 938, 939, 940, 945, 946, 947, 950, 961, 964, 965, 969, 970, 971, 973, 977, 978, 981, 985, 987, 988, 989, 990, 991, 992, 999, 1002, 1004, 1009, 1010, 1012, 1016, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1028, 1029, 1030, 1032, 1035, 1038, 1046, 1061, 1072, 1075, 1087, 1097, 1100, 1103, 1123, 1137, 1151, 1152, 1171, 1179, 1180, 1187, 1189, 1194, 1218, 1220, 1225, 1239, 1248, 1254, 1259, 1267, 1268, 1293, 1295, 1305, 1306, 1317, 1318, 1321, 1324, 1334, 1335, 1336, 1339, 1351, 1358, 1361, 1372, 1377, 1390, 1393, 1397, 1416, 1426, 1428, 1443, 1478, 1479, 1482, 1484, 1494, 1508, 1522, 1528, 1536, 1537, 1539, 1551, 1555, 1558, 1559, 1564, 1565, 1569, 1600, 1601, 1627, 1633, 1636, 1657, 1672, 1673, 1680, 1693, 1712, 1746, 1761, 1767, 1769, 1774, 1775, 1781, 1791, 1808, 1809, 1856, 1859, 1873, 1876, 1881, 1883, 1887, 1913, 1953, 1958, 1960, 2008, 2027, 2028, 2032, 2055, 2141, 2158, 2174, 2218, 2224, 2239, 2257, 2276, 2293, 2307, 2309, 2334, 2338, 2341, 2345, 2354, 2356, 2358, 2372, 2397, 2427, 2468, 2484, 2492, 2529, 2536, 2537, 2538, 2544, 2558, 2566, 2567, 2635, 2646, 2688, 2693, 2699, 2700, 2705, 2728, 2736, 2769, 2810, 2815, 2819, 2825, 2827, 2829, 2840, 2849, 2868, 2871, 2873, 2876, 2881, 3031, 3040, 3060, 3088, 3102, 3111, 3127, 3153, 3165, 3187, 3200, 3205, 3207, 3257, 3323, 3347, 3354, 3357, 3361, 3362, 3376, 3399, 3433, 3463, 3464, 3467, 3469, 3475, 3477, 3497, 3499, 3518, 3520, 3552, 3553, 3565, 3605, 3632, 3674, 3693, 3696, 3704, 3710, 3713, 3719, 3734, 3738, 3788, 3823, 3824, 3830, 3833, 3834, 3842, 3889]
	file_list_pickles+=previous_486
	# print [x for x in manual_list if x not in file_list_pickles]
	# verify_node_lemmas(manual_refined_dict)
	# save_trees_to_refined()
	pass



