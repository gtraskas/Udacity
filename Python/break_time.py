import time
import webbrowser

total_breaks = 2
break_count = 0

print("This program started on " + time.ctime())
while(break_count < total_breaks):
    time.sleep(3)
    webbrowser.open("https://www.youtube.com/watch?v=Ij99dud8-0A")
    break_count = break_count + 1
