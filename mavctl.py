import argparse                 # handles command-line arguments like get and set
import sys                      # lets us exit the program if something goes wrong
import time                     # lets us add small delays
from pymavlink import mavutil   # helps us connectto the simulator


def connect(link="tcp:127.0.0.1:5760", timeout=20): # udp:127.0.0.1:5760 is the port that simulator uses to talk over MAVLink
    master = mavutil.mavlink_connection(link) # opens connection to drone simulator
    
    # waits for signal that confirms drone is active
    # if no signal is recieved, exit
    if not master.wait_heartbeat(timeout=timeout): 
        sys.exit("Error: no heartbeat—simulator not up?")
    return master # returns master object - allows us to send/recieve messages over MAVLink

def read_param(master, name): # name is paramter we are trying to read
    # --------------------------------------------------------------------------------------------------
    # SEE ALL PARAMS AND HOW THEY ARE STORED
    #----------------------------------------------------------------------------------
    '''
    master.param_fetch_all()     # triggers fetch
    time.sleep(2)                # wait for drone to respond
    print(master.params)         # dictionary of all param_name → value
    '''
    #------------------------------------------------------------------------------------------
    
    master.param_fetch_one(name)
    msg = master.recv_match(type='PARAM_VALUE', blocking=True, timeout=5)
    if msg is None:
        print(f"Parameter '{name}' not found.")
    else:
        print(f"{msg.param_id} = {msg.param_value}")

    # --------------------------------------------------------------------------------------------------
    # LESS ABSTRACT VERSION
    # --------------------------------------------------------------------------------------------------
    '''
    # request to drone asking for value fo parameter
    master.mav.param_request_read_send(master.target_system, master.target_component, name.encode(), -1) 

    # recieve msg, blocking means wait or time out, timeout means wait for 5 sec
    msg = master.recv_match(type="PARAM_VALUE", blocking=True, timeout=5)
    if not msg:
        sys.exit(f"Error: param '{name}' not found / no response")
    
    print(f"{msg.param_id}: {msg.param_value}")
    '''
    # --------------------------------------------------------------------------------------------------
    # HOW ABSTRACT VERSION WORKS
    # --------------------------------------------------------------------------------------------------
    '''
    def param_fetch_one(self, name):
        # initiate fetch of one parameter
        try:
            idx = int(name)
            self.mav.param_request_read_send(self.target_system, self.target_component, b"", idx)
        except Exception:
            if not isinstance(name, bytes):
                name = bytes(name,'ascii')
            self.mav.param_request_read_send(self.target_system, self.target_component, name, -1)
    '''

def set_param(master, name, value):
    # --------------------------------------------------------------------------------------------------
    # LESS ABSTRACT WAY
    # --------------------------------------------------------------------------------------------------
    '''
    master.mav.param_set_send(master.target_system, master.target_component, name.encode(), float(value), mavutil.mavlink.MAV_PARAM_TYPE_REAL32)

    time.sleep(0.2)
    read_param(master, name)
    '''
    # --------------------------------------------------------------------------------------------------
    master.param_set_send(name, float(value))
    time.sleep(0.2)
    read_param(master, name)
    # --------------------------------------------------------------------------------------------------
    # HOW ABSTRACT VERSION WORKS
    # --------------------------------------------------------------------------------------------------
    '''
    def param_set_send(self, parm_name, parm_value, parm_type=None):
        # wrapper for parameter set
        if self.mavlink10():
            if parm_type is None:
                parm_type = mavlink.MAVLINK_TYPE_FLOAT
            self.mav.param_set_send(self.target_system, self.target_component,
                                    parm_name.encode('utf8'), parm_value, parm_type)
        else:
            self.mav.param_set_send(self.target_system, self.target_component,
                                    parm_name.encode('utf8'), parm_value)
    '''



def main():
    master = connect()
    while True:
        cmd = input("\nEnter command (get <param>, set <param> <value>, or exit): ").strip().split()
        if not cmd:
            continue
        if cmd[0] == "exit":
            break
        elif cmd[0] == "get" and len(cmd) == 2:
            read_param(master, cmd[1])
        elif cmd[0] == "set" and len(cmd) == 3:
            set_param(master, cmd[1], cmd[2])
        else:
            print("Invalid command. Try again.")
    
    '''
    
    # Creates the comand line parse
    # Set to 'ArduPilot param CLI' if users run --help
    parser = argparse.ArgumentParser(description="ArduPilot param CLI") 
    sub = parser.add_subparsers(dest="cmd", required=True)  # stores subcommand get or set in args.cmd

    g = sub.add_parser("get") # defines subcommand get
    g.add_argument("param")   # tells the get command  to expect 1 argument

    s = sub.add_parser("set")           # define subcommand set
    s.add_argument("param")             # first argument is parameter name
    s.add_argument("value", type=float) # second argument is the new value

    args = parser.parse_args() #parse everything user types and store in args

    master = connect()

    # Call the appropriate function based on the command
    if args.cmd == "get":
        read_param(master, args.param)
    else:  # "set"
        set_param(master, args.param, args.value)
    '''

if __name__ == "__main__":
    main()



