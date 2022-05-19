def processData(processes,time_Quantum): # O(n)
    process_data = []
    no_of_processes = len(processes)
    for i in range(no_of_processes):
        temporary = []
        temporary.extend([processes[i][0], processes[i][1], processes[i][2], 0,processes[i][2]])
        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete
        
        '''
        process_data.append(temporary)
    timeQuantum = time_Quantum
    return [process_data,processes]
def rr(process_data, timeQuantum):
    '''
    Time Complexity: O(n^2)
    Space Complexity: O(n)
    
    Parameters:
    int process_data[][3] :process data
    int timeQuantum: time quantum  
    
    Returns:
    int [process_stats[][8],executed_process[],f_dic{},bt_dict{}]  
    '''
    start_time = []
    exit_time = []
    executed_process = []
    ready_queue = []
    s_time = 0
    no_of_processes = len(process_data)
    temp = processData(process_data,timeQuantum)
    process_data = temp[0]
    processes = temp[1]
    # print(process_data)
    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        normal_queue = []
        temp = []
        for i in range(no_of_processes):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                present = 0
                if len(ready_queue) != 0:
                    for k in range(len(ready_queue)):
                        if process_data[i][0] == ready_queue[k][0]:
                            present = 1
                '''
                The above if loop checks that the next process is not a part of ready_queue
                '''
                if present == 0:
                    temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                    ready_queue.append(temp)
                    temp = []
                '''
                The above if loop adds a process to the ready_queue only if it is not already present in it
                '''
                if len(ready_queue) != 0 and len(executed_process) != 0:
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == executed_process[len(executed_process) - 1]:
                            ready_queue.insert((len(ready_queue) - 1), ready_queue.pop(k))
                '''
                The above if loop makes sure that the recently executed process is appended at the end of ready_queue
                '''
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            if ready_queue[0][2] > timeQuantum:
                '''
                If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                '''
                start_time.append(s_time)
                s_time = s_time + timeQuantum
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(no_of_processes):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - timeQuantum
                ready_queue.pop(0)
            elif ready_queue[0][2] <= timeQuantum:
                '''
                If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                '''
                start_time.append(s_time)
                s_time = s_time + ready_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(ready_queue[0][0])
                for j in range(no_of_processes):
                    if process_data[j][0] == ready_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
                ready_queue.pop(0)
        elif len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            if normal_queue[0][2] > timeQuantum:
                '''
                If process has remaining burst time greater than the time slice, it will execute for a time period equal to time slice and then switch
                '''
                start_time.append(s_time)
                s_time = s_time + timeQuantum
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(normal_queue[0][0])
                for j in range(no_of_processes):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = process_data[j][2] - timeQuantum
            elif normal_queue[0][2] <= timeQuantum:
                '''
                If a process has a remaining burst time less than or equal to time slice, it will complete its execution
                '''
                start_time.append(s_time)
                s_time = s_time + normal_queue[0][2]
                e_time = s_time
                exit_time.append(e_time)
                executed_process.append(normal_queue[0][0])
                for j in range(no_of_processes):
                    if process_data[j][0] == normal_queue[0][0]:
                        break
                process_data[j][2] = 0
                process_data[j][3] = 1
                process_data[j].append(e_time)
    # Calculating first response time
    f_time = []
    f_dic = {}
    temp = {}
    bt_dict = {}
    for i in range(no_of_processes):
        bt_dict[processes[i][0]] = [processes[i][2],processes[i][1]]
    for i in range(len(executed_process)):
        try:
            temp[executed_process[i]]+=1
        except:
            temp[executed_process[i]]=1
            if(i!=0):
                x = f_time[-1]            
            if(i!=0):
                b = bt_dict[executed_process[i-1]][0]
                a = bt_dict[executed_process[i]][1]
                if(b<timeQuantum):
                    y = x+b
                else:
                    y=((i+1)*timeQuantum)-timeQuantum
                if(y<a):
                    y = a
                f_time.append(y)
                f_dic[executed_process[i]] = y
            else:
                a = bt_dict[executed_process[i]][1]
                if(a!=0):
                    f_time.append(a)
                    f_dic[executed_process[i]] = a
                else:
                    f_time.append(((i+1)*timeQuantum)-timeQuantum)
                    f_dic[executed_process[i]]=((i+1)*timeQuantum)-timeQuantum
    # Calculating turnaround time        
    for i in range(no_of_processes):
        turnaround_time = process_data[i][5] - process_data[i][1]
        '''
        turnaround_time = completion_time - arrival_time
        '''
        process_data[i].append(turnaround_time)
    # Calculating waiting time        
    for i in range(no_of_processes):
        waiting_time = process_data[i][6] - process_data[i][4]
        '''
        waiting_time = turnaround_time - burst_time
        '''
        process_data[i].append(waiting_time)
    process_stats = []
    # [pid,at,bt,ft,ct,tat,wt,rt]
    for i in range(no_of_processes):
        temp=[process_data[i][0],process_data[i][1],process_data[i][4],f_time[i],process_data[i][5],process_data[i][6],process_data[i][7],f_time[i]-process_data[i][1]]
        process_stats.append(temp)
    return [process_stats,executed_process,f_dic,bt_dict]
def getStatsForGanttChart(output,f_dic,bt_dict,timeQuantum): # O(len(output))
    pid = []
    st = []
    ct = []
    dt = []
    trace = {}
        
    for i in range(len(output)):
        if(output[i] not in trace):
            pid.append(output[i])
            st.append(f_dic[output[i]])
            if(bt_dict[output[i]][0]>timeQuantum):
                ct.append(st[-1]+timeQuantum)
                bt_dict[output[i]][0]-=timeQuantum
            else:
                ct.append(st[-1]+bt_dict[output[i]][0])
            dt.append(ct[-1]-st[-1])
            trace[output[i]]=1
        else:
            pid.append(output[i])
            st.append(ct[-1])
            if(bt_dict[output[i]][0]>timeQuantum):
                ct.append(st[-1]+timeQuantum)
                bt_dict[output[i]][0]-=timeQuantum
            else:
                ct.append(st[-1]+bt_dict[output[i]][0])
            dt.append(ct[-1]-st[-1])
            
    return [pid,st,ct,dt]
if __name__ == "__main__":
    pass