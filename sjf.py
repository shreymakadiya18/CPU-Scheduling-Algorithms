from bisect import insort
import sys
def fcfsUtility(processes):
    '''
    Implementing FCFS(without sorting) for SJF and returning process stats
    Time Complexity: O(n)
    Space Complexity: O(8*n) ~= O(n)
    '''
    
    no_of_processes = len(processes) # no of processes
    output = [] # an 2d array for output process stats 
    current_time = 0 # current time of cpu
    for i in range(no_of_processes): # calculating stats according to FCFS Algorithm for every process
        at = processes[i][1] # arrival time for ith process 
        bt = processes[i][2] # burst time for ith process
        if(current_time<=at): # checking if current time<=at 
            current_time = at # then update current_time to at i.e cpu is ideal for at-current_time time 
        ct = current_time+bt # completion time = first allotment time + burst time
        tat = ct-at # turn around time = completion time - arrival time
        wt = tat-bt # waiting time = turn around time - burst time
        rt = current_time-at # response time = first allotment time - arrival time
        output.append([processes[i][0],at,bt,current_time,ct,tat,wt,rt]) # appending list of output stats to output list
        current_time = ct # updating cpu current time to completion time of latest completed process

    return output # return output list

def sjf(processes):
    """
    Implementing SJF Algorithm in two steps:
    1. getting a list of process in sequence they would be executed according to sjf algorithm in O(n^2) 
    2. calculating process stats using above list using fcfs algo without sorting (as done before in above step) in O(n)
    
    Time Complexity: O(nlogn) + O(n^2) + O(n) ~= O(n^2)
    Space Complexity: O(n)
    
    Parameters:
    int list[][3]: 2d integer list of process info
    
    Format for input parameter 'processes' is [pid,at,bt]
    pid: process id
    at: arrival time
    bt: burst time

    Returns:
    int list[][8]: 2d integer list of calculated process stats

    Format for output process stats is [pid,at,bt,ft,ct,tat,wt,rt]
    pid: process id
    at: arrival time
    bt: burst time
    ft: first cpu allotment time
    ct: completion time
    tat: turn around time
    wt: waiting time
    rt: response time
    """
    no_of_processes = len(processes) # no of processes
    queue = [] # queue which will store processes to be executed in sequence according to sjf algorithm
    queue_cntr = 0 # counter for processes in queue
    processes_cntr = 0 # counter for processes got in queue
    current_time = 0 # current time 
    last_normal_insert = 0 # index of last process that was appended at last

    #sorting on basis of arrival time then burst time then process id
    processes = sorted(processes,key=lambda x:(x[1],x[2],x[0])) # O(nlogn)
    
    # while all processes does not get into queue
    while(processes_cntr<no_of_processes): 
        if(queue_cntr==0): # if first process, append to queue
            queue.append([processes[processes_cntr][2],processes[processes_cntr]])
            last_normal_insert = 0 # update last_normal_insert
            processes_cntr+=1 # increment process counter
            current_time = queue[-1][1][1]+queue[-1][1][2] # update current time to arrival time + burst time of first process
            queue_cntr+=1 # increment queue counter
            continue # continue to next process

        # calculating min burst time of process arrived while previous process was executing and placing comming process to their sequence of 
        # execution according to sjf algorithm using bisect.insort 
        minBt = sys.maxsize 
        while(processes_cntr<no_of_processes and processes[processes_cntr][1]<=current_time):
            insort(queue,[processes[processes_cntr][2],processes[processes_cntr]],last_normal_insert+1) # O(n) 
            minBt = min(minBt,processes[processes_cntr][2])
            queue_cntr+=1
            processes_cntr+=1
        # check if any process has arrived while execution of previous process
        if(minBt!=sys.maxsize): # if yes, increment current time with minBt and increment last_normal_insert
            current_time+=minBt
            last_normal_insert+=1    
        # else append the process at end of queue and update last normal insert index to queue_cntr 
        else:            
            queue.append([processes[processes_cntr][2],processes[processes_cntr]])
            last_normal_insert = queue_cntr # update last normal insert index 
            current_time = queue[-1][1][1]+queue[-1][1][2] # update current time to arrival time + burst time of current process
            queue_cntr+=1 # increment queue counter
            processes_cntr+=1 # increment process counter
            
    # unzip process info and burst time from queue list to calculate further
    temp,newProcesses = zip(*queue)
    
    # At this point, newProcesses is a list that contains process in proper sequence of execution according to sjf algorithm
    # from this execution will be as same as fcfs
    return fcfsUtility(newProcesses) # O(n)

#--Utility Function-----------------------------------------------------------------------#
# utitlity function to get process stats in desirable format for plotting gantt chart
def getStatsForGanttChart(output): 
    """
    Time Complexity: O(no_of_processes)
    Space Complexity: O(4*no_of_processes) ~= O(no_of_processes) 
    """
    pid = []
    st = []
    ct = []
    dt = []
    for process in output:
        pid.append(process[0])
        st.append(process[3])
        ct.append(process[4])
        dt.append(process[4]-process[3])
    return [pid,st,ct,dt]
if __name__=="main":
    processes = [[0,5,2],[1,2,6],[2,1,8],[3,0,3],[4,4,4]]    
    sjf(processes)