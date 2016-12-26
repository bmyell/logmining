import random
import subprocess
import time
//这里设置在左边的球队
TEAM_L = "e"
//下面是对手的路径
//example 
OPP_LIST = ["/home/scom/Documents/RoboCup/team/rc_14/WrightEagle/start.sh",
            "/home/scom/Documents/RoboCup/team/rc_14/CYRUS/startAll",
            "/home/scom/Documents/RoboCup/team/rc_14/Gliders2014/src/start.sh",
            "/home/scom/Documents/RoboCup/team/rc_14/InfoGraphics/Info80/src/start.sh",
            "/home/scom/Documents/RoboCup/team/rc_14/Oxsy/start.sh",
            "/home/scom/Documents/RoboCup/team/rc_14/Yushan2014/start.sh"
           ]
NUM_OPP = len(OPP_LIST) //得到对手列表的长度
LOG_DIRECTORY = "/home/scom/test/" //设置存放日志的地方
NUM_SIM = 5

for i in range(0, NUM_SIM):
    random_opp = random.randint(0, NUM_OPP - 1)//生成指定范围内的整数a<=n<=b
    TEAM_R = OPP_LIST[random_opp]//
    p = subprocess.Popen([
                    "rcssserver", \
                    "server::auto_mode=1", \
                    "server::synch_mode=true", \
                    "server::team_l_start=" + TEAM_L, \
                    "server::team_r_start=" + TEAM_R, \
                    "server::kick_off_wait=10", \
                    "server::game_logging=1", \
                    "server::text_logging=1", \
                    "server::game_log_dir=" + LOG_DIRECTORY, \
                    "server::text_log_dir=" + LOG_DIRECTORY
                    ], stdout=subprocess.PIPE)
    output, err = p.communicate()
    print output
    print err
    time.sleep(6)
