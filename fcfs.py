'''
Author: Nilay Patel
Alias: nildarrk
date: 02/03/2022
'''

def fcfs(processes):
    '''
    Implementing fcfs algorithm and returning process stats
    Time Complexity: O(nlogn)
    Space Complexity: O(8*n) ~= O(n)
    
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
    '''
    
    processes = sorted(processes,key=lambda x:x[1]) # sorting input processes on the basis of arrival time and pid  
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
    
def getStatsForGanttChart(output):
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
def display(output):
    for process in output:
        print(*process)
        
if __name__=="main":    
    processes = getProcesses()  
    output = fcfs(processes)
    display(output)
