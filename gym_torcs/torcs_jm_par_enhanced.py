#!/usr/bin/env python
"""
Enhanced TORCS Client for Corkscrew Track - 3 Laps
Uses advanced AI driving logic optimized for the challenging Corkscrew track.
Run this with: python torcs_jm_par_enhanced.py
"""

import socket
import sys
import getopt
import os
import time
import math
from corkscrew_driver import AdvancedDriver, DrivingConfig

PI = 3.14159265359
data_size = 2**17

# Command line help
ophelp = 'Options:\n'
ophelp += ' --host, -H <host>    TORCS server host. [localhost]\n'
ophelp += ' --port, -p <port>    TORCS port. [3001]\n'
ophelp += ' --id, -i <id>        ID for server. [SCR]\n'
ophelp += ' --steps, -m <#>      Maximum simulation steps. 1 sec ~ 50 steps. [100000]\n'
ophelp += ' --episodes, -e <#>   Maximum learning episodes. [1]\n'
ophelp += ' --track, -t <track>  Your name for this track. Used for learning. [corkscrew]\n'
ophelp += ' --stage, -s <#>      0=warm up, 1=qualifying, 2=race, 3=unknown. [2]\n'
ophelp += ' --debug, -d          Output full telemetry.\n'
ophelp += ' --help, -h           Show this help.\n'
ophelp += ' --version, -v        Show current version.'
usage = 'Usage: %s [options] \n' % sys.argv[0]
usage = usage + ophelp
version = "20250101-enhanced"


def clip(v, lo, hi):
    """Clip value between lo and hi"""
    if v < lo:
        return lo
    elif v > hi:
        return hi
    else:
        return v


def bargraph(x, mn, mx, w, c='X'):
    """Draws a simple asciiart bar graph for visualization."""
    if not w:
        return ''
    if x < mn:
        x = mn
    if x > mx:
        x = mx
    tx = mx - mn
    if tx <= 0:
        return 'backwards'
    upw = tx / float(w)
    if upw <= 0:
        return 'what?'
    negpu, pospu, negnonpu, posnonpu = 0, 0, 0, 0
    if mn < 0:
        if x < 0:
            negpu = -x + min(0, mx)
            negnonpu = -mn + x
        else:
            negnonpu = -mn + min(0, mx)
    if mx > 0:
        if x > 0:
            pospu = x - max(0, mn)
            posnonpu = mx - x
        else:
            posnonpu = mx - max(0, mn)
    nnc = int(negnonpu / upw) * '-'
    npc = int(negpu / upw) * c
    ppc = int(pospu / upw) * c
    pnc = int(posnonpu / upw) * '_'
    return '[%s]' % (nnc + npc + ppc + pnc)


class Client():
    """TORCS Client for communicating with the race server"""
    
    def __init__(self, H=None, p=None, i=None, e=None, t=None, s=None, d=None):
        self.host = 'localhost'
        self.port = 3001
        self.sid = 'SCR'
        self.maxEpisodes = 1
        self.trackname = 'corkscrew'  # Default to Corkscrew
        self.stage = 2  # 2 = Race
        self.debug = False
        self.maxSteps = 300000  # 6000 seconds for 3 laps
        self.parse_the_command_line()
        
        if H:
            self.host = H
        if p:
            self.port = p
        if i:
            self.sid = i
        if e:
            self.maxEpisodes = e
        if t:
            self.trackname = t
        if s:
            self.stage = s
        if d:
            self.debug = d
        
        self.S = ServerState()
        self.R = DriverAction()
        self.setup_connection()
        print(f"[TORCS Client] Connected to {self.host}:{self.port}")
        print(f"[TORCS Client] Track: {self.trackname}, Stage: {self.stage}")

    def setup_connection(self):
        """Setup UDP connection to TORCS server"""
        try:
            self.so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as emsg:
            print('Error: Could not create socket...')
            sys.exit(-1)
        
        self.so.settimeout(1)
        n_fail = 5
        
        while True:
            # Sensor angles for track reading
            a = "-45 -19 -12 -7 -4 -2.5 -1.7 -1 -.5 0 .5 1 1.7 2.5 4 7 12 19 45"
            initmsg = '%s(init %s)' % (self.sid, a)
            
            try:
                self.so.sendto(initmsg.encode(), (self.host, self.port))
            except socket.error as emsg:
                sys.exit(-1)
            
            sockdata = str()
            try:
                sockdata, addr = self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.error as emsg:
                print("[TORCS Client] Waiting for server on port %d..." % self.port)
                print("[TORCS Client] Retries left: %d" % n_fail)
                if n_fail < 0:
                    print("[TORCS Client] Restarting TORCS...")
                    os.system('pkill torcs')
                    time.sleep(1.0)
                    os.system('torcs -nofuel -nodamage -nolaptime &')
                    time.sleep(2.0)
                    n_fail = 5
                n_fail -= 1
            
            if '***identified***' in sockdata:
                print("[TORCS Client] Successfully connected!")
                break

    def parse_the_command_line(self):
        """Parse command line arguments"""
        try:
            (opts, args) = getopt.getopt(sys.argv[1:], 'H:p:i:m:e:t:s:dhv',
                                        ['host=', 'port=', 'id=', 'steps=',
                                         'episodes=', 'track=', 'stage=',
                                         'debug', 'help', 'version'])
        except getopt.error as why:
            print('getopt error: %s\n%s' % (why, usage))
            sys.exit(-1)
        
        try:
            for opt in opts:
                if opt[0] == '-h' or opt[0] == '--help':
                    print(usage)
                    sys.exit(0)
                if opt[0] == '-d' or opt[0] == '--debug':
                    self.debug = True
                if opt[0] == '-H' or opt[0] == '--host':
                    self.host = opt[1]
                if opt[0] == '-i' or opt[0] == '--id':
                    self.sid = opt[1]
                if opt[0] == '-t' or opt[0] == '--track':
                    self.trackname = opt[1]
                if opt[0] == '-s' or opt[0] == '--stage':
                    self.stage = int(opt[1])
                if opt[0] == '-p' or opt[0] == '--port':
                    self.port = int(opt[1])
                if opt[0] == '-e' or opt[0] == '--episodes':
                    self.maxEpisodes = int(opt[1])
                if opt[0] == '-m' or opt[0] == '--steps':
                    self.maxSteps = int(opt[1])
                if opt[0] == '-v' or opt[0] == '--version':
                    print('%s %s' % (sys.argv[0], version))
                    sys.exit(0)
        except ValueError as why:
            print('Bad parameter \'%s\' for option %s: %s\n%s' % (
                opt[1], opt[0], why, usage))
            sys.exit(-1)
        
        if len(args) > 0:
            print('Superflous input? %s\n%s' % (', '.join(args), usage))
            sys.exit(-1)

    def get_servers_input(self):
        """Receive server data"""
        if not self.so:
            return
        sockdata = str()
        
        while True:
            try:
                sockdata, addr = self.so.recvfrom(data_size)
                sockdata = sockdata.decode('utf-8')
            except socket.error as emsg:
                print('.', end=' ', flush=True)
            
            if '***identified***' in sockdata:
                print("[TORCS Server] Connected")
                continue
            elif '***shutdown***' in sockdata:
                print("\n[TORCS Server] Race finished!")
                print("[TORCS Server] Final position: %d" % self.S.d.get('racePos', 0))
                self.shutdown()
                return
            elif '***restart***' in sockdata:
                print("\n[TORCS Server] Race restarted")
                self.shutdown()
                return
            elif not sockdata:
                continue
            else:
                self.S.parse_server_str(sockdata)
                if self.debug:
                    sys.stderr.write("\x1b[2J\x1b[H")
                    print(self.S)
                break

    def respond_to_server(self):
        """Send driver commands to server"""
        if not self.so:
            return
        try:
            message = repr(self.R)
            self.so.sendto(message.encode(), (self.host, self.port))
        except socket.error as emsg:
            print("Error sending to server: %s" % str(emsg))
            sys.exit(-1)

    def shutdown(self):
        """Close connection"""
        if not self.so:
            return
        print("[TORCS Client] Shutting down...")
        self.so.close()
        self.so = None


class ServerState():
    """Represents current server state/sensor data"""
    
    def __init__(self):
        self.servstr = str()
        self.d = dict()

    def parse_server_str(self, server_string):
        """Parse server string into dictionary"""
        self.servstr = server_string.strip()[:-1]
        sslisted = self.servstr.strip().lstrip('(').rstrip(')').split(')(')
        for i in sslisted:
            w = i.split(' ')
            self.d[w[0]] = destringify(w[1:])

    def __repr__(self):
        return self.fancyout()

    def fancyout(self):
        """Pretty print sensor data"""
        out = str()
        sensors = [
            'stucktimer', 'fuel', 'distRaced', 'distFromStart', 'racePos',
            'damage', 'speedX', 'speedY', 'speedZ', 'trackPos', 'angle'
        ]
        
        for k in sensors:
            if k not in self.d:
                continue
            
            if k == 'damage':
                strout = '%6.0f %s' % (self.d[k], bargraph(self.d[k], 0, 10000, 30, '~'))
            elif k == 'fuel':
                strout = '%6.0f %s' % (self.d[k], bargraph(self.d[k], 0, 100, 30, 'f'))
            elif k == 'speedX':
                strout = '%6.1f' % self.d[k]
            elif k == 'trackPos':
                strout = '%6.3f' % self.d[k]
            else:
                strout = str(self.d[k])
            
            out += "%s: %s\n" % (k, strout)
        
        return out


class DriverAction():
    """Represents driver commands to send to server"""
    
    def __init__(self):
        self.actionstr = str()
        self.d = {
            'accel': 1.0,  # Start with full throttle
            'brake': 0,
            'clutch': 0,
            'gear': 1,
            'steer': 0,
            'focus': [-90, -45, 0, 45, 90],
            'meta': 0
        }

    def clip_to_limits(self):
        """Ensure all values are within valid ranges"""
        self.d['steer'] = clip(self.d['steer'], -1, 1)
        self.d['brake'] = clip(self.d['brake'], 0, 1)
        self.d['accel'] = clip(self.d['accel'], 0, 1)
        self.d['clutch'] = clip(self.d['clutch'], 0, 1)
        if self.d['gear'] not in [-1, 0, 1, 2, 3, 4, 5, 6]:
            self.d['gear'] = 0
        if self.d['meta'] not in [0, 1]:
            self.d['meta'] = 0
        if type(self.d['focus']) is not list or min(self.d['focus']) < -180 or max(self.d['focus']) > 180:
            self.d['focus'] = 0

    def __repr__(self):
        self.clip_to_limits()
        out = str()
        for k in self.d:
            out += '(' + k + ' '
            v = self.d[k]
            if not type(v) is list:
                out += '%.3f' % v
            else:
                out += ' '.join([str(x) for x in v])
            out += ')'
        return out


def destringify(s):
    """Convert string(s) to number(s)"""
    if not s:
        return s
    if type(s) is str:
        try:
            return float(s)
        except ValueError:
            return s
    elif type(s) is list:
        if len(s) < 2:
            return destringify(s[0])
        else:
            return [destringify(i) for i in s]


# ==================== MAIN ====================
if __name__ == "__main__":
    print("="*60)
    print("TORCS Corkscrew AI Driver - 3 Laps")
    print("="*60)
    
    # Create client and driver
    C = Client(p=3001)
    driver = AdvancedDriver()
    
    print(f"[Main] Starting race simulation...")
    print(f"[Main] Max steps: {C.maxSteps}")
    print(f"[Main] Using Advanced Corkscrew Driver")
    
    step_count = 0
    try:
        for step in range(C.maxSteps, 0, -1):
            C.get_servers_input()
            
            # Use advanced driver logic
            driver.drive(C.S, C.R)
            
            C.respond_to_server()
            step_count += 1
            
            # Print status every 500 steps (10 seconds)
            if step_count % 500 == 0:
                speed = C.S.d.get('speedX', 0)
                lap = driver.lap_count
                dist = C.S.d.get('distFromStart', 0)
                print(f"\r[Status] Lap: {lap} | Speed: {speed:.1f} km/h | Distance: {dist:.0f}m ", end='', flush=True)
        
        C.shutdown()
        print("\n[Main] Race completed successfully!")
        
    except KeyboardInterrupt:
        print("\n[Main] User interrupted the race")
        C.shutdown()
    except Exception as e:
        print(f"\n[Main] Error occurred: {e}")
        C.shutdown()
        raise
