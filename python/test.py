import sched, time   
    
hour = time.strftime("%I_%M_%S", time.localtime())
day = time.strftime("%m_%d", time.localtime())

print(day)
print(day[0])
if(day[0] == '0'):
    new = day[1:]

print(new)