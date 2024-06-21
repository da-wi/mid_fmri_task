# -*- coding: utf-8 -*-
"""
Monetary incentive delay (MID) task implemented in python 2.7
Author:   David Willinger, Silvia Brem
Created:  2018-15-11
Copyright (C) 2019  Department of Children and Adolescent Psychiatry and Psychotherapy
					University Hospital of Psychiatry Zurich, University of Zurich

This programme is licensed under CC BY-NC-SA 4.0 
https://creativecommons.org/licenses/by-nc-sa/4.0/

CHANGELOG
==========
version 5: - neutral condition no longer is used for calculating response time
           - shapetypes implemented

"""
import sys, pygame
import random
import os
import time  # http://stackoverflow.com/questions/20023709/resetting-pygames-timer
import logging
from random import shuffle
import argparse


#################################################
# DEFINITION OF ARGUMENTS AND PARSER
#################################################
parser = argparse.ArgumentParser(description="Monetary incentive delay task")
parser.add_argument('subjectid', help='mandatory subject id')
parser.add_argument('-s', '--screenmode', help='dual or single screenmode [single,dual]', default='dual')
parser.add_argument('-bg', '--bgcolor', help='colortype 1 = black, colortype 2 = grey [1,2]', default='1')
parser.add_argument('-r', '--run', help='determines the run number for the subject [1,2]', default='1')
parser.add_argument('-e', '--emulation', help='Sets emulation mode for use outside the scanner', action='store_true')
parser.add_argument('-o', '--omitcolor', help='Do not use any color', action='store_true')
parser.add_argument('-c', '--colortype', help='colortype blue/orange (LOSS,GAIN,NEUTRAL) - 1=(Blu,Ora,Gray),2=(Ora,Blu,Gray),3=(Ora,Gray,Blu),4=(Gray,Ora,Blu),5=(Gray,Blu,Ora),6=(Blu,Gray,Ora) [1-6]', default='1') 
parser.add_argument('-t', '--shapetype', help='determines the randomization of cues [1,2,3,4,5,6]', default='1')
parser.add_argument('-S', '--shortversion', help='Starts a shortversion of the task',action='store_true')
parser.add_argument('-l', '--forcelogdir', help='Force Logdir creation',action='store_true')

# parameter: DUALSCREEN MODE (dual,single), COLOR_TYPE (1,2), RUN NUMBER ( 1,2 )
args = parser.parse_args()

if args.subjectid == "":
    print "\n\nNo subject ID was specified. Abort."
    parser.exit(1, None)

if args.screenmode == "dual":
    DUALSCREEN = True
else:
	DUALSCREEN = False

try:
	COLOR_TYPE = args.colortype
	COLOR_TYPE = float(COLOR_TYPE)
	if not (0 < COLOR_TYPE < 7):
		raise ValueError
except ValueError:
	print('No valid COLOR_TYPE defined! Use numbers 1-6! Abort.')
	sys.exit()

try:
	SHAPE_TYPE = args.shapetype
	SHAPE_TYPE = int(SHAPE_TYPE)
	if not (0 < SHAPE_TYPE < 7 or SHAPE_TYPE == 666):
		raise ValueError
except ValueError:
	print('No valid SHAPE_TYPE defined! Use numbers 1-6! Abort.')
	sys.exit()

COLOR_BLACK = (10,10,10)
COLOR_WHITE = (220,220,220)
COLOR_GREY = (127, 127, 127)
COLOR_GREEN = (3,237,120)
COLOR_RED = (120,0,0)
COLOR_BLUE = (45,154,204)
COLOR_ORANGE = (188,117,24)

BGCOLOR = COLOR_BLACK
FONTCOLOR = COLOR_WHITE

if args.run == "1":
	RUNCOMMENT = "1"
elif args.run == "2":
	RUNCOMMENT = "2"
else:
	print 'WARNING! Unusual run number!! Continuing...'
	RUNCOMMENT = args.run

if args.bgcolor == "1":
	BGCOLOR = COLOR_BLACK
	FONTCOLOR = COLOR_WHITE
elif args.bgcolor == "2":
	BGCOLOR = COLOR_GREY
	FONTCOLOR = COLOR_BLACK
else:
	BGCOLOR = COLOR_BLACK
	FONTCOLOR = COLOR_WHITE

# setting parameters
size = width, height = 800, 600

if DUALSCREEN == True:
	# THIS IS A HACK FOR PSEUDO-DUAL SCREEN IN THE MR-CENTER
	x = 1920
	y = 0
	import os
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)

if COLOR_TYPE == 1:
	COLOR_LOSS = COLOR_ORANGE
	COLOR_WIN = COLOR_BLUE
	COLOR_NEUTRAL = COLOR_GREY
elif COLOR_TYPE == 2:
	COLOR_LOSS = COLOR_BLUE
	COLOR_WIN = COLOR_ORANGE
	COLOR_NEUTRAL = COLOR_GREY
elif COLOR_TYPE == 3:
	COLOR_LOSS = COLOR_ORANGE
	COLOR_WIN = COLOR_GREY
	COLOR_NEUTRAL = COLOR_BLUE
elif COLOR_TYPE == 4:
	COLOR_LOSS = COLOR_GREY
	COLOR_WIN = COLOR_ORANGE
	COLOR_NEUTRAL = COLOR_BLUE	
elif COLOR_TYPE == 5:
	COLOR_LOSS = COLOR_GREY
	COLOR_WIN = COLOR_BLUE
	COLOR_NEUTRAL = COLOR_ORANGE
elif COLOR_TYPE == 6:
	COLOR_LOSS = COLOR_BLUE
	COLOR_WIN = COLOR_GREY
	COLOR_NEUTRAL = COLOR_ORANGE

if args.omitcolor == True:
	COLOR_LOSS = COLOR_WHITE
	COLOR_WIN = COLOR_WHITE
	COLOR_NEUTRAL = COLOR_WHITE
	args.colortype=-1	

###########################################
# INITIALIZING LOGGER
###########################################
logger = logging.getLogger()
output_handler = logging.StreamHandler()
#content = ""
#with open('logs/current.txt') as f:
#	content = f.readlines()

version = sys.argv[0][-5:-3]

content = args.subjectid
logdir = 'logs/'+content
logfile = 'mid_run_'+RUNCOMMENT+'_'+str(time.time())+'_' + version + '.csv'

created_logdir = False
if not os.path.exists(logdir):
	if args.forcelogdir == False:
		print "Logdir for subject %s does not exist, do you want to create it? [Y/n]" % args.subjectid,
		yes = {'yes','y', 'ye', ''}
		no = {'no','n'}
		while True:
			choice = raw_input().lower()
			if choice in yes:
				os.makedirs(logdir)
				created_logdir = True
				break
			elif choice in no:
				print "No Logdir created. Abort."
				sys.exit(1)
			else:
				sys.stdout.write("Please respond with 'yes' or 'no'")
	else:
		os.makedirs(logdir)
		created_logdir = True


file_handler = logging.FileHandler('logs/' + args.subjectid + '/mid_run_' + RUNCOMMENT + '_' + str(time.time()) + '_' + version + '.csv')
# formatter = logging.Formatter('%(asctime)s;%(name)-12s %(levelname)-8s %(message)s')
formatter = logging.Formatter('%(message)s')
output_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(output_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)
logger.debug('Timestamp;Event')

formatter = logging.Formatter('%(created)s;%(message)s')
output_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#logger.debug('parameters;screenmode=%s;color=%s;run=%s',args.screenmode ,args.colortype,args.run )
logger.debug('parameters;screenmode=%s;color=%s;shape=%s;run=%s;shortversion=%s;version=%s',args.screenmode ,args.colortype, args.shapetype, args.run,args.shortversion,version )
logger.debug('color_loss=%s;color_gain=%s;color_neutral=%s',COLOR_LOSS,COLOR_WIN,COLOR_NEUTRAL)

if  created_logdir == True:
	logger.debug('create_logdir;%s',args.subjectid )

####################################################
# DEFINITION OF GLOBAL VARIABLES
####################################################
global money, status, correct, early, feedback, reaction_time, target_init_time, key_pressed_time, reaction_list, difficulty_time, jitter_trial

TRIAL_LENGTH = 8.5

# money subject has won
money = 0
# log in which trial step we are
status = 0
# log if trial was fast enough
correct = 0

# counts all correct trials
all_correct = 0

# log if participant pressed too early
early = 0
key_pressed = 0
# feedback string
feedback = ''
# reaction time
reaction_time = 0
reaction_time_actual = 0
target_init_time = 0
key_pressed_time = 0

# list of reaction times
reaction_list = [0.5]
reaction_mean = 0.5

jitter_trial = []

# difficulty adaption
difficulty_time = [0.35]

current_time_phase = 0
target_presentation_time_max=0.85
penalty_switch = 1
feedback_given = 0

#########################################################
# FUNCTION DEFINITION
#########################################################

def start_screen():
	logger.debug('showing_start_screen')
	screen.fill(BGCOLOR)
	font = pygame.font.Font("fonts/SourceSansPro-Regular.ttf", 60)
	text = font.render("Geld gewinnen oder verlieren", 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery - 50
	screen.blit(text, textpos)
	font = pygame.font.Font("fonts/seguisym.ttf", 36)
	ustr = u"★"
	text = font.render("Reagiere schnell auf "+ustr, 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery + 50
	screen.blit(text, textpos)

	if args.emulation == True:
		font = pygame.font.Font("fonts/seguisym.ttf", 20)
		ustr = u"★"
		text = font.render(u"Zum Starten \"t\" drücken", 1, FONTCOLOR)
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery + 200
		screen.blit(text, textpos)

		font = pygame.font.Font("fonts/seguisym.ttf", 20)
		ustr = u"★"
		text = font.render(u"Bei ★ versuchen schnell \"b\" zu drücken", 1, FONTCOLOR)
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery + 230
		screen.blit(text, textpos)
	#    textpos = text.get_rect()
	#    textpos.centerx = screen.get_rect().centerx
	#    textpos.centery = screen.get_rect().centery
	#    screen.blit(text, textpos)


	pygame.display.flip()


def end_screen():
	global money
	logger.debug('showing_end_screen')
	screen.fill(BGCOLOR)
	font = pygame.font.Font("fonts/SourceSansPro-Regular.ttf", 60)
	text = font.render("Gewonnenes Geld: "+str(money)+" CHF", 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery - 50
	screen.blit(text, textpos)
	font = pygame.font.Font("fonts/seguisym.ttf", 36)
	text = font.render("[ENTER] um Programm zu beenden.", 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery + 50
	screen.blit(text, textpos)
	pygame.display.flip()


def gimme_feedback(trialtype):
	# type: (object) -> object
	# trial types = highloss, highgain, lowloss, lowgain, neutral
	# highloss = 0
	# highgain = 1
	# lowloss = 2
	# lowgain = 3
	# neutral = 4
	global correct, money, reaction_time, reaction_time_actual, feedback_given, result, early
	result = 0
	losshigh = 4
	losslow = 1
	gainhigh = 4
	gainlow = 1

	old_money = money

	if correct == 1:
		# print money
		result = {
			0: lambda x: money,
			1: lambda x: money + gainhigh,
			2: lambda x: money,
			3: lambda x: money + gainlow,
			4: lambda x: money
		}[trialtype](x)
	else:  # too slow
		# print money
		result = {
			0: lambda x: money - losshigh,
			1: lambda x: money,
			2: lambda x: money - losslow,
			3: lambda x: money,
			4: lambda x: money
		}[trialtype](x)

	if feedback_given == 0:
		money = result
	#print 'CHANGING MONEY FROM ' + str(old_money) + ' TO ' + str(money)
	money_delta = money-old_money
	rt = reaction_time_actual
	corr_str = '' if correct == 1 else ''
 	#print 'CURRENT TRIAL TYPE WAS: '+str(trialtype)
	feedback_given = 1
	if trialtype < 4:
		return [corr_str, money_delta, money]
	else:
		#print rt*1000
		if early == 1:
			return ['', -1, '']
		elif key_pressed == 0:
			return ['', -2, '']
		else:		
			return ['', round(rt * 1000), '']
		

def get_difficulty(mean, trialnumber):
	if feasibility_list[trialnumber] == 1:
		return target_presentation_time_max - (mean + 0.05)
	else:
		return target_presentation_time_max - (mean - 0.05)

def show_cross():  # can only be called when initialized
	# logger.debug('showing_crossfade')
	screen.fill(BGCOLOR)
	font = pygame.font.Font(None, 150)
	text = font.render(u"•", 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)
	pygame.display.flip()


def show_target():  # can only be called when initialized
	# logger.debug('showing_target')
	screen.fill(BGCOLOR)
	font = pygame.font.Font("fonts/seguisym.ttf", 200)
	text = font.render(u"★", 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)
	pygame.display.flip()


def show_feedback(feedback):
	# logger.debug('showing_feedback')
	screen.fill(BGCOLOR)
	# line 1
	font = pygame.font.Font("fonts/SourceSansPro-Bold.ttf", 100)
	#font.set_bold(True)
	text = font.render(str(feedback[0]), 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery - 120
	screen.blit(text, textpos)


	# line 2
	font = pygame.font.Font("fonts/SourceSansPro-Regular.ttf", 100)
	
	if feedback[2] == '':  # neutral
		if int(feedback[1]) > 0:
			text = font.render(str(int(feedback[1]))+" ms", 1, FONTCOLOR)
		if int(feedback[1]) == -1:
			text = font.render("zu schnell", 1, FONTCOLOR)
		if int(feedback[1]) == -2:
			text = font.render(u"nicht gedrückt", 1, FONTCOLOR)
		
	else:  # gain/loss condition
		if feedback[1] > 0:
			text = font.render("+" + '{:01.0f}'.format(feedback[1])+" CHF", 1, FONTCOLOR)
		elif feedback[1] == 0:
			pm = u"±"
			text = font.render(pm + "0 CHF", 1, FONTCOLOR)
		else:
			text = font.render('{:01.0f}'.format(feedback[1])+" CHF", 1, FONTCOLOR)

	textpos = text.get_rect()
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)

	# line 3
	font = pygame.font.Font("fonts/SourceSansPro-Bold.ttf", 80)
	text = font.render('{:01.0f}'.format(feedback[2])+" CHF", 1, FONTCOLOR) if feedback[2] != '' else font.render("", 1, FONTCOLOR)
	textpos = text.get_rect()
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery + 120
	#screen.blit(text, textpos)
	pygame.display.flip()


def show_trialtype(trialtype):
	screen.fill(BGCOLOR)
	font = pygame.font.Font("fonts/seguisym.ttf", 200)
#	result = {
#		0: u"▥",  # 'High Loss Avoidance',
#		1: u"◍",  # 'High Gain',
#		2: u"□",  # 'Low Loss Avoidance',
#		3: u"○",  # 'Low Gain',
#		4: u"△"  # 'Neutral'
#	}[trialtype]
	if SHAPE_TYPE == 1:
		result = {
			0: u"■",  # 'High Loss Avoidance',
			1: u"●",  # 'High Gain',
			2: u"◧",  # 'Low Loss Avoidance',
			3: u"◐",  # 'Low Gain',
			4: u"▲"  # 'Neutral'
			#◭
		}[trialtype]
	elif SHAPE_TYPE == 2:	
		result = {
			0: u"●",  # 'High Loss Avoidance',
			1: u"■",  # 'High Gain',
			2: u"◐",  # 'Low Loss Avoidance',
			3: u"◧",  # 'Low Gain',
			4: u"▲"  # 'Neutral'
			#◭
		}[trialtype]
	elif SHAPE_TYPE == 3:
		result = {
			0: u"■",  # 'High Loss Avoidance',
			1: u"▲",  # 'High Gain',
			2: u"◧",  # 'Low Loss Avoidance',
			3: u"◭",  # 'Low Gain',
			4: u"●"  # 'Neutral'
			#
		}[trialtype]
	elif SHAPE_TYPE == 4:
		result = {
			0: u"▲",  # 'High Loss Avoidance',
			1: u"■",  # 'High Gain',
			2: u"◭",  # 'Low Loss Avoidance',
			3: u"◧",  # 'Low Gain',
			4: u"●"  # 'Neutral'
			#
		}[trialtype]
	elif SHAPE_TYPE == 5:
		result = {
			0: u"●",  # 'High Loss Avoidance',
			1: u"▲",  # 'High Gain',
			2: u"◐",  # 'Low Loss Avoidance',
			3: u"◭",  # 'Low Gain',
			4: u"■"  # 'Neutral'
			#
		}[trialtype]
	elif SHAPE_TYPE == 6:
		result = {
			0: u"▲",  # 'High Loss Avoidance',
			1: u"●",  # 'High Gain',
			2: u"◭",  # 'Low Loss Avoidance',
			3: u"◐",  # 'Low Gain',
			4: u"■"  # 'Neutral'
			#
		}[trialtype]
	elif SHAPE_TYPE == 666: # implemented for demonstration
		result = {
			0: u"●",  # 'High Loss Avoidance',
			1: u"●",  # 'High Gain',
			2: u"●",  # 'Low Loss Avoidance',
			3: u"●",  # 'Low Gain',
			4: u"●"   # 'Neutral'
			#
		}[trialtype]	
	else:
		print 'Something weird happens.'		

	# set color
	# loss condition
	if trialtype % 2 == 0 and trialtype < 4:
		text = font.render(result, 1, COLOR_LOSS)
	# win condition
	elif trialtype % 2 == 1:
		text = font.render(result, 1, COLOR_WIN)
	# neutral
	else:
		text = font.render(result, 1, COLOR_NEUTRAL)

	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)
	pygame.display.flip()

# actual game logic
# time dependent state change
def display_trial(t, trialtype, trialnumber):
	global money, correct, feedback, target_init_time, difficulty_time, status, jitter_before

	# ab 0 ms
	if t < 0.25:
		if status == 0:

			logger.debug('starting_trial;%d;%d', trialtype, trialnumber)
			#print ('STATUS ='+str(status)+',TIME='+str(t))
			status = 1
		show_trialtype(trialtype)
		return 1

	# ab 250ms:
	elif t < 0.25 + jitter_trial[trialnumber]:
		if status == 1:
			# print 'diffulty: '+str(difficulty_time)
			# print 'response_times: '+str(reaction_list)
			#print ('STATUS =' + str(status) + ',TIME=' + str(t))
			logger.debug('showing_cross_1;status=%d;difficulty=%f;t_target_pres=%f', status,
						 difficulty_time[trialnumber], (target_presentation_time_max - difficulty_time[trialnumber]))
			status = 2
		show_cross()
		return 2

	# ab anticipation_jitter + difficulty_time:  + difficulty_time[trialnumber]
	elif t < 0.25 + jitter_trial[trialnumber] + (target_presentation_time_max - difficulty_time[trialnumber]):
		if status == 2:
			#print ('STATUS =' + str(status) + ',TIME=' + str(t))
			logger.debug('showing_target;status=%d', status)
			status = 3
			target_init_time = time.time()
		show_target()
		#print target_presentation_time_max
		#print difficulty_time[trialnumber]
		return 3

	# ab target_ende:
	elif t < 0.25 + jitter_trial[trialnumber] + (target_presentation_time_max) + float((1000 - 1400) / float(4000 - 2200)) * jitter_trial[trialnumber] + 1.8888:
		if status == 3:
			#print ('STATUS =' + str(status) + ',TIME=' + str(t))
			logger.debug('showing_cross_2;status=%d', status)
			status = 4
		show_cross()
		return 4

	elif t < 0.25 + jitter_trial[trialnumber] + (target_presentation_time_max) + float((1000 - 1400) / float(4000 - 2200)) * jitter_trial[trialnumber] + 1.8888 + 1.5:
		#print 0.25 + jitter_trial[trialnumber] + (target_presentation_time_max) + float((750 - 1400) / float(4000 - 2200)) * jitter_trial[trialnumber] + 2.1944
		if status == 4:
			#print ('STATUS =' + str(status) + ',TIME=' + str(t))
			logger.debug('showing_feedback;status=%d;correct=%d', status, correct)
			status = 5	
			feedback = gimme_feedback(trialtype)
			#print t
		show_feedback(feedback)
		return 5

	elif t < TRIAL_LENGTH - mean_jitter + jitter_end[trialtype]:
		#print str(t) + '<' + str(float(6 + float(jitter_before[trialnumber])/1000))
		if status == 5:
			#print ('STATUS =' + str(status) + ',TIME=' + str(t))
			logger.debug('showing_cross_3;status=%d', status)
			status = 6
		show_cross()
		return 6


# calculates median from list
def median(lst):	
	# optionally use window of last 10 items
	# comment if ALL response times should be used
	# print lst
	lst = lst[-3:]
	# print lst

	# take list
	lst = sorted(lst)
	
	if len(lst) < 1:
		return None
	if len(lst) % 2 == 1:
		return lst[((len(lst) + 1) / 2) - 1]
	else:
		return float(sum(lst[(len(lst) / 2) - 1:(len(lst) / 2) + 1])) / 2.0

# finds a sublist in a list
def subfinder(mylist, pattern):
    matches = []
    for i in range(len(mylist)):
        if mylist[i][0] == pattern[0] and mylist[i:i+len(pattern)][0] == pattern[0]:
            matches.append(pattern)
    return matches


###########################################
# START THE PROGRAM
###########################################
# open window
pygame.init()

# NOFRAME
if DUALSCREEN == True:
	width, height = pygame.display.Info().current_w, pygame.display.Info().current_h # call before set_mode to get screen size
	print width
	print height
	screen = pygame.display.set_mode(size,pygame.NOFRAME)
else:
	screen = pygame.display.set_mode(size)	
screen.fill(BGCOLOR)

t_start = 0
# show instruction
start_screen()
# wait for trigger from scanner
trigger = 0
while trigger == 0:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_t:
				trigger = 1
				logger.debug('trigger')

show_cross()
t_start = time.time()

# trial types = highloss, highgain, lowloss, lowgain, neutral
#trials_list = range(0, 5)
trials_list = [4,4]
trials_list = [x for pair in zip(trials_list, trials_list) for x in pair]
#shuffle(trials_list)
#trialtype,feasibility

# Knutson Original task:
# 144 Trials: reward n = 54, loss n = 54, neutral = 36
# Knutson: 144 Trials: reward high n = 18, low n = 18, mid = 18; loss high n = 18, low n = 18 mid = 18; neutral = 36
# Cho Trials: reward high n = 18, low n = 18, mid = 18; loss high n = 18, low n = 18 mid = 18; neutral = 36
# Bei uns 54*2 Trials: reward high n = 12, low n = 12; loss high n = 12, low n = 12; neutral = 9  * 2

if args.shortversion == False:
	trial_type_list = [[0,0],[0,1],[0,1],[1,0],[1,1],[1,1],[2,0],[2,1],[2,1],[3,0],[3,1],[3,1]]*4
	#trial_type_list = [[0,0],[0,1],[0,1]]*6
	neutral_list = [[4,0],[4,1],[4,1]]*4
	#neutral_list = []
	trial_type_list += neutral_list
else:
	trial_type_list = [[0,0],[0,1],[0,1],[1,0],[1,1],[1,1],[2,0],[2,1],[2,1],[3,0],[3,1],[3,1]]*2
	#trial_type_list = [[0,0],[0,1],[0,1]]*6
	neutral_list = [[4,0],[4,1],[4,1]]*2
	#neutral_list = []
	trial_type_list += neutral_list	
	#trial_type_list = [[0,1],[0,1],[0,1]]

# first 3 trials are feasible
while (trial_type_list[0][1] == 0 or trial_type_list[1][1] == 0 or trial_type_list[2][1] == 0):
	random.shuffle(trial_type_list)

# MANUALLY SET TRIAL TYPE LIST HERE
#trial_type_list = [[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1],[4,1]]

print 'Trial type list'
#print trial_type_list[i][0]
#trial_type_list = neutral_list
trials_list = []
feasibility_list = []
for entry in trial_type_list:
	trials_list.append(entry[0])
	feasibility_list.append(entry[1])

print trials_list
print feasibility_list
print len(trials_list)*6.0/60.0

num_trials = len(trials_list)


# jitter list
jitter_list = [0, 0] * ((num_trials / 2) + 2)
shuffle(jitter_list)
print jitter_list

jitter_trial = [2.2, 4.0, 3.1] * (num_trials / 3)
jitter_trial = random.sample(xrange(2200, 4000), num_trials)
jitter_trial = [x / 1000.0 for x in jitter_trial]

# a) jitter end via equal distribution
jitter_end = random.sample(xrange(-100, 100), num_trials)
jitter_end = [x / 1000.0 for x in jitter_end]

# b) jitter end via poisson distribution ( with mean = 0.25 )
jitter_end = [1]
while (max(jitter_end) > 0.7):
	jitter_end = [ random.expovariate(0.001) for i in range(0,num_trials) ]
	jitter_end = [ float(x / sum(jitter_end)*num_trials/4) for x in jitter_end ]

print 'Jitter trial elements:'+str(len(jitter_trial))
#jitter_trial = [ random.uniform (0.1, 0.6) for i in range(0,num_trials)]
shuffle(jitter_trial)

print jitter_end

mean_jitter = sum(jitter_end)/num_trials

print 'Mean jitter: '+ str(mean_jitter)
print 'Task length: '+str(int(len(trials_list)*(TRIAL_LENGTH)/60))+':'+str(int(round(len(trials_list)*(TRIAL_LENGTH)%60,0)))
print 'Number of trials: '+str(num_trials)

pygame.time.wait(2000)


trials_passed = 0
quit_game = 0

# trial loop starts here
for i in range(0, num_trials):
	# print 'Time passed since first trial: '+str(int(time.time()-t_start))

	status = 0
	correct = 0
	key_pressed = 0
	early = 0
	feedback = ''
	feedback_given = 0
	reaction_time = 0
	#pygame.time.wait(jitter_before[i])
	#jitter = jitter_before[i]
	trialtype = trials_list[i]
	t0 = time.time()
	go = 1
	while go:
		# check if time is up
		t1 = time.time()

		# if time is up, define new time points
		if (t1 - t0) > (TRIAL_LENGTH - mean_jitter + jitter_end[trialtype]):
			go = 0
			logger.debug('time_up;%d', i)
			trialtype = trials_list[i]
			#jitter = jitter_list[i]
			#print "APPENDING"
			#difficulty_time.append(get_difficulty(reaction_mean, i))
			#print (t1 - t0)

		if status == 5 and key_pressed == 0:
			logger.debug('no_key_pressed;wrong')
			key_pressed = 1
			
			if trialtype < 4:
				reaction_time = 0.6
				reaction_time_actual  = 0.6
			else:
				reaction_time = reaction_mean

			reaction_list.append(float(reaction_time))
			reaction_mean = median(reaction_list)
			# print "APPENDING"
			difficulty_time.append(get_difficulty(reaction_mean, i))	

		for event in pygame.event.get():
			if (event.type is pygame.KEYDOWN and event.key == pygame.K_f):
				if screen.get_flags() & pygame.FULLSCREEN:
					pygame.display.set_mode([800,600] )
				else:
					pygame.display.set_mode([800,600], pygame.FULLSCREEN)

			if event.type == pygame.QUIT:
				go = 0
				logger.debug('task_aborted_by_user')
			if event.type == pygame.KEYDOWN:
				# Q event
				if event.key == pygame.K_q:
					go = 0
					quit_game = 1
					logger.debug('task_aborted_by_user') 

				# Ctrl+C event
				if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
					go = 0
					quit_game = 1
					logger.debug('task_aborted_by_user') 

				if event.key == pygame.K_b:
					# log: key=left
					if status == 1 or status == 2:
						logger.debug('key_1_pressed;too_early')
						early = 1
						if penalty_switch == 1 and key_pressed == 0 and (t1-t0) > 0.6:
							key_pressed = 1
							#feedback = gimme_feedback(trialtype)
							reaction_time = 0.40
							reaction_list.append(float(reaction_time))
							# reaction_mean = sum(reaction_list)/len(reaction_list)
							reaction_mean = median(reaction_list)
							# print "APPENDING"
							difficulty_time.append(get_difficulty(reaction_mean, i))


					if status == 3 and key_pressed == 0 and feedback_given == 0:
						# subject was fast enough
						correct = 1
						all_correct += 1
						key_pressed = 1
						key_pressed_time = time.time()
						# skip neutral trials
						if trialtype < 4:
							reaction_time = key_pressed_time - target_init_time
							reaction_time_actual = reaction_time
						else:
							reaction_time = reaction_mean
							reaction_time_actual = key_pressed_time - target_init_time
						# logger.debug('Reaction time was: %s', str(reaction_time))

						reaction_list.append(float(reaction_time))
						# reaction_mean = sum(reaction_list)/len(reaction_list)
						reaction_mean = median(reaction_list)
						# print "APPENDING"
						difficulty_time.append(get_difficulty(reaction_mean, i))
						logger.debug('key_1_pressed;correct;%s', str(key_pressed_time - target_init_time))

					if status == 4 and key_pressed == 0 and feedback_given == 0:
						# subject was too slow
						key_pressed = 1
						key_pressed_time = time.time()
						# skip neutral trials
						if trialtype < 4:
							reaction_time = key_pressed_time - target_init_time
							reaction_time_actual = reaction_time
						else:
							reaction_time = reaction_mean	
							reaction_time_actual = key_pressed_time - target_init_time

						reaction_list.append(float(reaction_time))
						# reaction_mean = sum(reaction_list)/len(reaction_list)
						reaction_mean = median(reaction_list)
						# print "APPENDING"
						difficulty_time.append(get_difficulty(reaction_mean, i))
						logger.debug('key_1_pressed;wrong;%s', str(key_pressed_time - target_init_time))

					# print reaction_mean
		# display correct screen
		if quit_game < 1:
			status = display_trial(t1 - t0, trialtype, i)
		else: break

	if quit_game == 1:
		break

	trials_passed += 1	

# pygame.time.wait(15000)
pygame.time.wait(500)
t_end = time.time()
#print(str(int(t_end-t_start)))
logger.debug('money_won;%d', money)
logger.debug('correct;%d', all_correct)
logger.debug('wrong;%d', trials_passed - all_correct ) 
logger.debug('trials_passed;%d', trials_passed)
if trials_passed > 0:
	logger.debug('correct/all ratio;%f', float(float(all_correct) / float(trials_passed)))
else:
	logger.debug('correct/all ratio;%f', float(0.0))	
logger.debug('end_of_task')

if args.emulation == True:
	end_screen()
	trigger = 0
	while trigger == 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					trigger = 1
else:
	show_cross()	
	pygame.time.wait(14000)
pygame.quit()
