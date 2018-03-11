import pickle
from os import walk
import sys
import os
import numpy as np
from ast import literal_eval
import sys;
import copy as cpy
reload(sys);
sys.setdefaultencoding("utf8")
import unicodedata
import operator

# --------------------------------------- local paths -------------------------

dcs_path='/media/mandal/1bdad34f-aa4e-4216-b820-f44f2e99cd49/Sem_9/PG_BTP/BTP_2/work/DCS_pick'


# --------------------------------------- class def ---------------------------

class DCS:
	def __init__(self,sent_id,sentence):
		self.sent_id=sent_id
		self.sentence=sentence
		self.dcs_chunks=[]
		self.lemmas=[]
		self.cng=[]
		pass
	def pickle_print(self):
		print "sent_id = " + str(self.sent_id)
		print "\n" + "sentence = " + str(self.sentence)
		print "\n" + "dcs_chunks = " + list_to_str(self.dcs_chunks)
		print "\n" + "lemmas =" + list_to_str(self.lemmas)
		print "\n" + "cng = " + list_to_str(self.cng)
		print ">>>>>>>>>>>>>>>>"
		pass
	def to_ascii(self):
		self.sentence = utf_to_ascii(self.sentence)
		self.dcs_chunks = [utf_to_ascii(x) for x in self.dcs_chunks]
		self.lemmas = [[utf_to_ascii(y) for y in x] for x in self.lemmas]
		pass
	pass

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

class canto_sent(object):
	"""docstring for canto_sent"""
	def __init__(self, sentence , word_list):
		super(canto_sent, self).__init__()
		# [serial_num , word , in_poem , sandhied_word , possible_morph_list , correct_morph , dependency_rel ]
		self.sentence  = sentence 
		self.word_list  = word_list 
		pass
	def print_sent(self):
		# prints the sentence
		print "Sent : " 
		print self.sentence
		print "\n"
		for cur_word in self.word_list:
			print "word start ----------------------------------- \n"
			cur_word.print_word()
			print "word end ------------------------------------- \n"
			pass
		pass

class canto_word(object):
	"""docstring for canto_word"""
	def __init__(self, s_no, word, sandhied_word, morph_all , morph_in_context, kaaraka_sambandha):
		super(canto_word, self).__init__()
		self.s_no = s_no
		self.word = word
		self.sandhied_word = sandhied_word
		self.morph_all = morph_all
		self.morph_in_context = morph_in_context
		self.kaaraka_sambandha = kaaraka_sambandha
		pass
	def print_word(self):
		print 's_no : ' + str(self.s_no) + '\n'
		print 'word : ' + str(self.word) + '\n'
		print 'sandhied_word : ' + str(self.sandhied_word) + '\n'
		print 'morph_all : ' + str(self.morph_all) + '\n'
		print 'morph_in_context : ' + str(self.morph_in_context) + '\n'
		print 'kaaraka_sambandha : ' + str(self.kaaraka_sambandha) + '\n'
		pass


# --------------------------------------- global variables ---------------------------

# gold_sentence_list=pickle.load( open("gold_sentence_list.p", 'rb' ) )
# dep_tag_cng_dict={} #has entries as cngs of edges with this dependency tags.
	
# -----------------------------------------------------------------------------

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

def get_done_file_list_str(sent_path):
	f = []
	done_list=[]
	for (useless1, useless2, filenames) in walk(sent_path):
		f.extend(filenames)
		break
	for cur_file in f:
		cur_file_index=(cur_file.split('.')[0])
		done_list.append(cur_file_index)
		pass
	done_list.sort()
	# print done_list
	# exit(0)
	return done_list
	pass

def list_to_str(a_list):
	if a_list.__class__.__name__ != 'list':
		return str((a_list))
		pass
	ret_str=" $"
	for cur_item in a_list:
		ret_str+= " , "
		ret_str+= list_to_str(cur_item)
		pass
	ret_str=ret_str.replace("$ ," , "")
	return ret_str
	pass

def list_straightner(a_list):
	ret_list=[]
	for cur_item in a_list:
		if cur_item.__class__.__name__ == 'list':
			ret_list+=cur_item
			pass
		else :
			ret_list.append(cur_item)
			pass
		pass
	return ret_list
	pass

def utf_to_ascii(a):
	# coding: utf-8 
	double_dict={}
	f=open('support/roman/rom2.txt','r')
	for lines in f.readlines():
			words=lines.split(',')
			words[1]=words[1].replace('\n','')
			double_dict[words[0]]=words[1]
	f.close()
	single_dict={}
	q=open('support/roman/rom.txt','r')
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
		if ('adv.' in config) or ('und.' in config) or ('tasil' in config) :
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

def get_gold_sent(cur_sent_id):
	global gold_sentence_list
	for cur_sent in gold_sentence_list:
		if cur_sent.sent_id == cur_sent_id:
			return cur_sent
			pass
		pass
	pass

def get_gold_edge_list(cur_sent_id):
	cur_sent=get_gold_sent(cur_sent_id)
	handle_dep_tag_list=['nirxaranam',  'kalah', 'virayaxikaranam', 'xesaxikaranam', 'kalaxikaranam', 'gonakarma', 'mukyakarma', 'samanaxikaranam']
	ret_list=[]
	for cur_word in cur_sent.content_list:
		if cur_word.to_tag == None:
			continue
			pass
		try:
			if cur_word.dep_tag in handle_dep_tag_list:
				cur_word.dep_tag=dep_tag_handler(cur_word.dep_tag)
				pass
			if cur_word.dep_tag == None:
				continue
				pass
			ret_list.append( [int(cur_word.from_tag) - 1 ,  int(cur_word.to_tag) - 1 ,  str(cur_word.dep_tag)])
			pass
		except Exception, e:
			print "--------------------------------------------------------------"
			print "in sentence : "+ str(cur_sent_id)
			print cur_word.from_tag
			print cur_word.to_tag
			print cur_word.dep_tag
			print "--------------------------------------------------------------"
			pass
		pass
	return ret_list
	pass

def get_map_dict(node_dict):
	map_dict={}
	for cur_node in node_dict.keys():
		if node_dict[cur_node][3] in map_dict.keys():
			map_dict[node_dict[cur_node][3]]+=[cur_node]
			pass
		else:
			map_dict[node_dict[cur_node][3]]=[cur_node]
			pass
		pass
	return map_dict
	pass

def convert_to_int_list(a_list):
	ret_list=[]
	for cur_item in a_list:
		ret_list.append(int(cur_item))
		pass
	return ret_list
	pass

def get_cng_list_straight(a_list):
	return convert_to_int_list(list_straightner(a_list))
	pass

def get_dict_from_list(cng_list):
	ret_dict={}
	for cur_cng in cng_list:
		if cur_cng in ret_dict.keys():
			ret_dict[cur_cng]+=1
			pass
		else :
			ret_dict[cur_cng]=1
			pass
		pass
	return ret_dict
	pass

def get_dcs_cng_dict():
	dcs_master_dict=pickle.load( open("dcs_master_dict.p", 'rb' ) )
	dcs_key_list=dcs_master_dict.keys()
	dcs_key_list.sort()
	dcs_cng_dict={}
	for cur_dcs_id in dcs_key_list:
		print 'now' + ": " +str(cur_dcs_id)
		print 'remaining' + ": " +str(dcs_key_list[-1]-cur_dcs_id)
		cur_sent=dcs_master_dict[cur_dcs_id]
		cng_list=get_cng_list_straight(cur_sent.cng)
		dcs_cng_set=set(cng_list)
		dcs_cng_dict[cur_dcs_id]=dcs_cng_set
		pass
	pickle.dump(dcs_cng_dict,open('dcs_cng_dict.p' , 'w'))
	pass

def get_dcs_pattern_matches(manual_cng_set):
	dcs_cng_dict=pickle.load( open("dcs_cng_dict.p", 'rb' ) )
	dcs_key_list=dcs_cng_dict.keys()
	dcs_key_list.sort()
	ret_list=[]
	for cur_dcs_id in dcs_key_list:
		dcs_cng_set=dcs_cng_dict[cur_dcs_id]
		if manual_cng_set==dcs_cng_set:
			ret_list.append(cur_dcs_id)
			pass
		pass
	return ret_list
	pass

# dcs_master_dict=pickle.load( open("dcs_master_dict.p", 'rb' ) )
# dcs_key_list=dcs_master_dict.keys()
# dcs_key_list.sort()

def handle_lemmas_not_found_in_dcs():
	look_for_cng_patterns_dict=pickle.load(open( "look_for_cng_patterns_dict.p" , 'rb'))
	manual_key_list=look_for_cng_patterns_dict.keys()
	manual_key_list.sort()
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
	pickle.dump(patterns_matched_dict,open('patterns_matched_dict.p' , 'w'))
	pass

def get_lemma_from_patterns(cng_list, dcs_match_list):
	# for no matches look at the complete corpus.
	ret_list=[]
	temp_data=[]
	for cur_cng in cng_list:
		temp_data.append({})
		pass
	for cur_dcs_id in dcs_match_list:
		cur_sent=dcs_master_dict[cur_dcs_id]
		dcs_lemma_list=list_straightner( cur_sent.lemmas)
		dcs_cng_list=list_straightner(cur_sent.cng)
		print "sent :"+str(cur_dcs_id)
		# print "------------------------------"
		# print dcs_lemma_list
		# print dcs_cng_list
		# print "------------------------------"
		for cur_index in range(len(dcs_cng_list)):
			cur_dcs_cng=dcs_cng_list[cur_index]
			cur_dcs_lemma=dcs_lemma_list[cur_index]
			cur_dcs_lemma=utf_to_ascii(cur_dcs_lemma)
			for cng_index in range(len(cng_list)):
				cur_cng=cng_list[cng_index]
				if cur_dcs_cng==str(cur_cng):
					if cur_dcs_lemma in temp_data[cng_index].keys():
						temp_data[cng_index][cur_dcs_lemma]+=1
						pass
					else:
						temp_data[cng_index][cur_dcs_lemma]=1
						pass
					pass
				pass
			pass
		pass
	# exit()
	for cng_index in range(len(cng_list)):
		lemma_count_dict=temp_data[cng_index]
		cur_lemma=None
		if lemma_count_dict.keys()!=[]:
			cur_lemma=max(lemma_count_dict.iteritems(), key=operator.itemgetter(1))[0]
			pass
		print "------------------------------"
		print lemma_count_dict
		print cur_lemma
		print "------------------------------"
		ret_list.append(cur_lemma)
		pass
	return ret_list
	pass

def handle_patterns_matched():
	no_error_list=[9, 62, 71, 90, 111, 135, 144, 157, 161, 162, 197, 225, 289, 343, 345, 351, 355, 502, 512, 521, 551, 591, 621, 642, 646, 690, 775, 840, 915, 941, 963, 964, 966, 969, 1008, 1013, 1044, 1064, 1130, 1142, 1149, 1161, 1179, 1272, 1280, 1285, 1303, 1314, 1315, 1327, 1331, 1341, 1343, 1346, 1409, 1412, 1439, 1443, 1494, 1496, 1506, 1513, 1514, 1532, 1533, 1556, 1574, 1585, 1600, 1630, 1636, 1687, 1709, 1718, 1721, 1743, 1774, 1791, 1801, 1808, 1825, 1842, 1848, 1855, 1861, 1870, 1897, 1925, 1970, 1975, 1979, 1988, 2027, 2050, 2057, 2084, 2092, 2094, 2100, 2119, 2123, 2128, 2137, 2139, 2150, 2157, 2167, 2186, 2188, 2197, 2198, 2212, 2214, 2266, 2319, 2389, 2414, 2418, 2454, 2459, 2475, 2485, 2493, 2530, 2539, 2542, 2571, 2590, 2591, 2612, 2622, 2625, 2639, 2667, 2675, 2681, 2702, 2722, 2796, 2826, 2835, 2860, 2871, 2876, 2998, 3015, 3018, 3026, 3036, 3064, 3090, 3133, 3137, 3140, 3200, 3209, 3214, 3234, 3239, 3240, 3254, 3261, 3263, 3264, 3267, 3275, 3292, 3320, 3322, 3326, 3365, 3371, 3432, 3475, 3489, 3521, 3523, 3547, 3593, 3596, 3602, 3627, 3674, 3676, 3692, 3711, 3724, 3735, 3736, 3740, 3752, 3780, 3815, 3818, 3823, 3826, 3831, 3833, 3845, 3859, 3865, 3883, 3892, 3897, 3936, 3938, 4001, 4009, 4011, 4031, 4032, 4033, 4043, 4044, 4056, 4081, 4085, 4089, 4128, 4131, 4145, 4169, 4186, 4197, 4283, 4291, 4294, 4313, 4365, 4379, 4386, 4403, 4437, 4452, 4472, 4500, 4549, 4556, 4563, 4566, 4574, 4582, 4591, 4658, 4659, 4665, 4666, 4667, 4670, 4672, 4678, 4679, 4680, 4682, 4688, 4692]
	patterns_matched_dict=pickle.load(open( "patterns_matched_dict.p" , 'rb'))
	look_for_cng_patterns_dict=pickle.load(open( "look_for_cng_patterns_dict.p" , 'rb'))
	for cur_sent_id in no_error_list:
		dcs_match_list=patterns_matched_dict[cur_sent_id]
		lemma_cng_list=look_for_cng_patterns_dict[cur_sent_id][3]
		lemma_new_lemma_list=look_for_cng_patterns_dict[cur_sent_id][4]
		temp_list=[x[1] for x in lemma_cng_list]
		new_lemma_list=get_lemma_from_patterns(temp_list,dcs_match_list)
		print new_lemma_list
		for cur_index in range(len(new_lemma_list)):
			cur_lemma=new_lemma_list[cur_index]
			lemma_new_lemma_list[cur_index]=[lemma_new_lemma_list[cur_index][0],cur_lemma]
			pass
		print lemma_new_lemma_list
		look_for_cng_patterns_dict[cur_sent_id][4]=cpy.deepcopy(lemma_new_lemma_list)
		pass
	pickle.dump(look_for_cng_patterns_dict,open('look_for_cng_patterns_dict.p' , 'w'))
	pass

def handle_not_found():
	lemma_error_list=[17, 20, 21, 24, 34, 39, 43, 49, 57, 61, 68, 78, 79, 120, 146, 147, 149, 152, 160, 163, 164, 171, 181, 186, 194, 198, 199, 205, 208, 215, 219, 221, 224, 231, 233, 239, 240, 241, 245, 278, 296, 304, 324, 329, 332, 335, 340, 342, 354, 358, 360, 365, 371, 373, 404, 441, 445, 474, 486, 491, 500, 507, 513, 516, 517, 522, 524, 525, 526, 527, 537, 538, 543, 553, 563, 569, 580, 589, 594, 602, 605, 617, 635, 636, 640, 645, 648, 650, 651, 663, 699, 749, 781, 792, 827, 829, 845, 855, 857, 858, 863, 870, 919, 1011, 1019, 1037, 1045, 1047, 1049, 1050, 1051, 1057, 1060, 1065, 1067, 1069, 1081, 1082, 1083, 1084, 1087, 1091, 1092, 1093, 1094, 1097, 1106, 1107, 1113, 1115, 1118, 1119, 1125, 1138, 1148, 1157, 1158, 1166, 1173, 1183, 1189, 1192, 1214, 1216, 1219, 1222, 1232, 1248, 1257, 1262, 1273, 1274, 1275, 1277, 1281, 1282, 1289, 1290, 1291, 1294, 1299, 1302, 1311, 1333, 1344, 1352, 1357, 1370, 1371, 1381, 1383, 1398, 1400, 1403, 1404, 1405, 1425, 1431, 1436, 1438, 1440, 1441, 1450, 1451, 1459, 1468, 1480, 1483, 1491, 1504, 1509, 1511, 1512, 1515, 1521, 1528, 1531, 1534, 1535, 1549, 1561, 1562, 1570, 1571, 1590, 1593, 1596, 1597, 1598, 1603, 1605, 1606, 1617, 1618, 1625, 1631, 1632, 1635, 1638, 1643, 1646, 1670, 1696, 1701, 1706, 1712, 1714, 1724, 1728, 1735, 1737, 1740, 1741, 1742, 1746, 1759, 1772, 1776, 1778, 1782, 1803, 1806, 1812, 1817, 1823, 1846, 1854, 1857, 1858, 1865, 1899, 1900, 1904, 1911, 1918, 1921, 1933, 1934, 1948, 1949, 1962, 1966, 1969, 2001, 2005, 2017, 2019, 2024, 2036, 2038, 2043, 2044, 2046, 2061, 2064, 2065, 2075, 2080, 2085, 2086, 2091, 2093, 2103, 2109, 2111, 2114, 2120, 2125, 2134, 2144, 2145, 2147, 2148, 2160, 2168, 2171, 2173, 2183, 2187, 2204, 2206, 2209, 2211, 2218, 2221, 2232, 2235, 2237, 2240, 2242, 2250, 2252, 2256, 2299, 2303, 2314, 2318, 2320, 2324, 2327, 2328, 2333, 2336, 2340, 2342, 2346, 2347, 2348, 2364, 2367, 2369, 2370, 2374, 2376, 2377, 2386, 2387, 2390, 2393, 2421, 2423, 2436, 2437, 2438, 2450, 2455, 2456, 2458, 2462, 2483, 2486, 2488, 2498, 2501, 2502, 2503, 2505, 2508, 2510, 2511, 2513, 2519, 2520, 2527, 2528, 2541, 2556, 2561, 2574, 2575, 2577, 2578, 2582, 2583, 2586, 2602, 2610, 2620, 2623, 2624, 2629, 2638, 2644, 2663, 2664, 2669, 2671, 2680, 2689, 2690, 2708, 2710, 2725, 2728, 2730, 2743, 2744, 2748, 2751, 2752, 2754, 2764, 2767, 2770, 2776, 2781, 2783, 2786, 2797, 2801, 2802, 2821, 2839, 2852, 2859, 2865, 2868, 2874, 2891, 2905, 2917, 2930, 2931, 2936, 2939, 2946, 2947, 2950, 2951, 2957, 2964, 2972, 2980, 2985, 2993, 3000, 3003, 3008, 3013, 3025, 3034, 3038, 3039, 3043, 3045, 3047, 3048, 3052, 3056, 3067, 3073, 3076, 3080, 3082, 3093, 3094, 3095, 3096, 3100, 3101, 3103, 3106, 3107, 3125, 3131, 3132, 3138, 3139, 3142, 3143, 3144, 3146, 3149, 3154, 3156, 3157, 3164, 3173, 3178, 3179, 3181, 3183, 3185, 3193, 3208, 3219, 3222, 3224, 3228, 3230, 3233, 3241, 3245, 3248, 3250, 3282, 3288, 3299, 3300, 3307, 3329, 3334, 3336, 3337, 3342, 3345, 3350, 3352, 3359, 3368, 3374, 3386, 3391, 3396, 3403, 3408, 3409, 3425, 3449, 3454, 3461, 3488, 3491, 3495, 3496, 3500, 3508, 3513, 3514, 3516, 3525, 3527, 3565, 3567, 3570, 3575, 3577, 3579, 3582, 3586, 3598, 3601, 3605, 3606, 3607, 3610, 3618, 3626, 3630, 3637, 3641, 3644, 3646, 3649, 3654, 3655, 3657, 3659, 3661, 3669, 3675, 3699, 3705, 3706, 3717, 3733, 3741, 3745, 3755, 3756, 3764, 3769, 3770, 3778, 3785, 3790, 3803, 3805, 3808, 3812, 3816, 3817, 3825, 3827, 3836, 3839, 3847, 3854, 3857, 3860, 3863, 3866, 3867, 3869, 3870, 3884, 3926, 3931, 3932, 3948, 4003, 4004, 4012, 4017, 4019, 4020, 4021, 4022, 4024, 4025, 4030, 4034, 4036, 4037, 4038, 4042, 4045, 4046, 4047, 4048, 4049, 4050, 4054, 4058, 4059, 4063, 4065, 4068, 4069, 4070, 4071, 4073, 4074, 4076, 4079, 4082, 4086, 4087, 4090, 4091, 4093, 4095, 4097, 4099, 4102, 4103, 4104, 4106, 4108, 4110, 4115, 4116, 4117, 4119, 4120, 4123, 4124, 4125, 4126, 4127, 4129, 4132, 4133, 4135, 4139, 4144, 4146, 4148, 4150, 4151, 4155, 4158, 4161, 4163, 4164, 4166, 4167, 4171, 4172, 4173, 4174, 4175, 4176, 4178, 4179, 4181, 4184, 4185, 4187, 4189, 4190, 4193, 4194, 4196, 4198, 4199, 4201, 4202, 4203, 4208, 4209, 4211, 4213, 4216, 4217, 4218, 4220, 4222, 4224, 4227, 4228, 4229, 4230, 4233, 4234, 4235, 4236, 4238, 4239, 4242, 4245, 4246, 4248, 4255, 4260, 4263, 4264, 4268, 4269, 4270, 4271, 4273, 4277, 4279, 4280, 4282, 4284, 4285, 4287, 4289, 4290, 4292, 4295, 4296, 4298, 4301, 4304, 4305, 4307, 4308, 4309, 4311, 4315, 4316, 4317, 4318, 4321, 4322, 4323, 4324, 4327, 4329, 4330, 4332, 4333, 4334, 4335, 4337, 4338, 4339, 4340, 4342, 4344, 4345, 4346, 4348, 4349, 4351, 4352, 4353, 4355, 4356, 4357, 4360, 4361, 4362, 4363, 4368, 4370, 4372, 4375, 4380, 4381, 4384, 4385, 4387, 4388, 4389, 4391, 4392, 4394, 4395, 4396, 4399, 4400, 4401, 4405, 4406, 4407, 4412, 4413, 4414, 4416, 4417, 4418, 4419, 4421, 4422, 4423, 4424, 4425, 4428, 4429, 4431, 4432, 4433, 4436, 4439, 4441, 4444, 4445, 4446, 4447, 4450, 4451, 4453, 4455, 4456, 4458, 4459, 4460, 4461, 4465, 4469, 4471, 4475, 4478, 4479, 4480, 4481, 4482, 4484, 4486, 4487, 4490, 4491, 4492, 4494, 4496, 4498, 4499, 4501, 4503, 4504, 4505, 4507, 4508, 4510, 4512, 4514, 4516, 4517, 4518, 4522, 4524, 4526, 4527, 4529, 4530, 4535, 4536, 4537, 4538, 4541, 4542, 4544, 4546, 4547, 4548, 4551, 4552, 4553, 4554, 4555, 4557, 4558, 4560, 4561, 4565, 4568, 4579, 4580, 4581, 4583, 4584, 4585, 4588, 4593, 4594, 4595, 4596, 4602, 4607, 4608, 4615, 4616, 4618, 4620, 4622, 4623, 4624, 4626, 4628, 4630, 4631, 4632, 4635, 4636, 4637, 4638, 4646, 4647, 4648, 4651, 4652, 4653, 4654, 4663, 4683, 4685, 4691, 4695, 4697]
	look_for_cng_patterns_dict=pickle.load(open( "look_for_cng_patterns_dict.p" , 'rb'))
	# massive_cng_list=[]
	# for cur_sent_id in lemma_error_list:
	# 	lemma_cng_list=look_for_cng_patterns_dict[cur_sent_id][3]
	# 	temp_list=[x[1] for x in lemma_cng_list]
	# 	massive_cng_list+=temp_list
	# 	pass
	# massive_cng_list=list(set(massive_cng_list))
	# pickle.dump(massive_cng_list,open('massive_cng_list.p' , 'w'))
	# massive_cng_list=pickle.load(open( "massive_cng_list.p" , 'rb'))
	# print len(massive_cng_list)
	# massive_lemma_list=get_lemma_from_patterns(massive_cng_list, dcs_key_list)
	# pickle.dump(massive_lemma_list,open('massive_lemma_list.p' , 'w'))
	# print len(massive_lemma_list)
	# count=0
	# for cur_lemma in massive_lemma_list:
	# 	if cur_lemma==None:
	# 		count+=1
	# 		pass
	# 	pass
	# print count
	# exit()
	massive_cng_list=pickle.load(open( "massive_cng_list.p" , 'rb'))
	massive_lemma_list=pickle.load(open( "massive_lemma_list.p" , 'rb'))
	# cng_not_in_dcs=[-211,-197,-194,-191]
	# for cur_cng in cng_not_in_dcs:
	# 	print min(temp_list, key=lambda x:abs(x-cur_cng))
	# 	pass
	# exit()
	cng_not_in_dcs=[-211,-197,-194,-191]
	temp_list=[x for x in massive_cng_list if x not in cng_not_in_dcs]
	for cur_sent_id in lemma_error_list:
		lemma_cng_list=look_for_cng_patterns_dict[cur_sent_id][3]
		lemma_new_lemma_list=look_for_cng_patterns_dict[cur_sent_id][4]
		for cur_index in range(len(lemma_cng_list)):
			cur_cng=lemma_cng_list[cur_index][1]
			if cur_cng in cng_not_in_dcs:
				cur_cng=min(temp_list, key=lambda x:abs(x-cur_cng))
				pass
			cur_lemma=massive_lemma_list[massive_cng_list.index(cur_cng)]
			lemma_new_lemma_list[cur_index]=[lemma_new_lemma_list[cur_index][0],cur_lemma]
			pass
		print lemma_new_lemma_list
		look_for_cng_patterns_dict[cur_sent_id][4]=cpy.deepcopy(lemma_new_lemma_list)
		pass
	pickle.dump(look_for_cng_patterns_dict,open('look_for_cng_patterns_dict.p' , 'w'))
	pass

def verify_lemma_update():
	look_for_cng_patterns_dict=pickle.load(open( "look_for_cng_patterns_dict.p" , 'rb'))
	key_list=look_for_cng_patterns_dict.keys()
	key_list.sort()
	for cur_sent_id in key_list:
		lemma_new_lemma_list=look_for_cng_patterns_dict[cur_sent_id][4]
		print lemma_new_lemma_list
		pass
	pass

if __name__ == '__main__':
	# handle_patterns_matched()
	# handle_not_found()
	verify_lemma_update()
	# pickle.dump(pattern_count_dict,open('pattern_count_dict.p' , 'w'))
	# handle_dcs_notfound()
	# get_dcs_cng_dict()
	pass



