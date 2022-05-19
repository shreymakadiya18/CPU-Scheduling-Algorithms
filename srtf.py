def processData(process_data,no_of_processes):
    newProcessData = []
    for i in range(no_of_processes):
        temp = []
        temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], 0, process_data[i][2]])
        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete
        '''
        newProcessData.append(temp)
    return newProcessData

def srtf(process_data):
    '''
    Time Complexity: O(n^2)
    
    SRTF: Shortest Remaining Job First
    The task is to find the Average Waiting Time and Average Turnaround Time of the given processes with their Burst Time using SRTF Scheduling Algorithm.
    SRTF is a scheduling policy that selects the waiting process with the smallest execution time to execute next.
    The process which has the Least Burst Time will be served first and will be continued to be served till there is any other process with Lower Burst Time priority.
    If there is any process with Lower Burst Time, then switch the process.
    Start Time: Time at which the execution of the process starts
    Completion Time: Time at which the process completes its execution
    Turnaround Time: Completion Time - Arrival Time
    Waiting Time: Turnaround Time - Burst Time
    I have made use of 2 queues in the code:
    Ready Queue: It stores all the processes which have already arrived.
    Normal Queue: It stores all the processes which have not arrived yet.
    '''
    start_time = []
    exit_time = []
    s_time = 0
    sequence_of_process = []
    no_of_processes = len(process_data)
    process_data = processData(process_data,no_of_processes)
    process_data.sort(key=lambda x: x[1])
    '''
    Sort processes according to the Arrival Time
    '''
    while 1:
        ready_queue = []
        normal_queue = []
        temp = []
        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                ready_queue.append(temp)
                temp = []
            elif process_data[i][3] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4]])
                normal_queue.append(temp)
                temp = []
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            ready_queue.sort(key=lambda x: x[2])
            '''
            Sort processes according to Burst Time
            '''
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(ready_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == ready_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            if process_data[k][2] == 0:        #If Burst Time of a process is 0, it means the process is completed
                process_data[k][3] = 1
                process_data[k].append(e_time)
        if len(ready_queue) == 0:
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(normal_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            if process_data[k][2] == 0:        #If Burst Time of a process is 0, it means the process is completed
                process_data[k][3] = 1
                process_data[k].append(e_time)
    at_dic = {}
    for i in range(no_of_processes):
        at_dic[process_data[i][0]] = process_data[i][1]
    f_time = []
    temp = {}
    gd = []
    ct = 0
    for i in range(len(sequence_of_process)):
        if(i==0):
            temp[sequence_of_process[i]]=1
            if(ct<at_dic[sequence_of_process[i]]):
                f_time.append(at_dic[sequence_of_process[i]])
            else:
                f_time.append(ct)
            ct = f_time[-1]
            gd.append([sequence_of_process[i],ct,0,0])
            ct+=1
            continue
        if(sequence_of_process[i]==sequence_of_process[i-1]):
            ct+=1
        else:
            gd[-1][2]=ct
            gd[-1][3]=gd[-1][2]-gd[-1][1]    
            try:
                temp[sequence_of_process[i]]+=1
                gd.append([sequence_of_process[i],ct,0,0])
                ct+=1
            except:
                temp[sequence_of_process[i]]=1
                if(ct<at_dic[sequence_of_process[i]]):
                    f_time.append(at_dic[sequence_of_process[i]])
                else:
                    f_time.append(ct)
                ct = f_time[-1]
                gd.append([sequence_of_process[i],ct,0,0])
                ct+=1
    try:
        temp[sequence_of_process[-1]]+=1
    except:
        if(i<at_dic[sequence_of_process[i]]):
            f_time.append(at_dic[sequence_of_process[i]])
        else:
            f_time.append(i)
    gd[-1][2]=ct
    gd[-1][3]=gd[-1][2]-gd[-1][1]
    for i in range(len(process_data)):
        turnaround_time = process_data[i][5] - process_data[i][1]
        '''
        turnaround_time = completion_time - arrival_time
        '''
        process_data[i].append(turnaround_time)
        waiting_time = process_data[i][6] - process_data[i][4]
        '''
        waiting_time = turnaround_time - burst_time
        '''
        process_data[i].append(waiting_time)
    process_stats = []
    # [pid,at,bt,ft,ct,tat,wt,rt]
    for i in range(no_of_processes):
        temp = []
        temp+=[process_data[i][0]]
        temp += [process_data[i][1]]
        temp+= [process_data[i][4]]
        temp+=[f_time[i]]
        temp+=[process_data[i][5]]
        temp+=[process_data[i][6]]
        temp+=[process_data[i][7]]
        temp+=[f_time[i]-process_data[i][1]]
        process_stats.append(temp)
    return [process_stats,gd]

def getStatsForGanttChart(output): # O(len(output))
    pid = []
    st = []
    ct = []
    dt = []
    for i in range(len(output)):
        ct.append(output[i][2])
        dt.append(output[i][3])
        pid.append(output[i][0])
        st.append(output[i][1])
    
    return [pid,st,ct,dt]
    
   
if __name__ == "main":
    
    processData(no_of_processes)