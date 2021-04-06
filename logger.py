import sys
import argparse
import csv
from time import time
from datetime import datetime

filename = "log.log"
START = "start"
END = "end"

def main():
    parser = argparse.ArgumentParser(description="Do some logging")
    parser.add_argument("-s", "--start", help="Start logging", action="store_true")
    parser.add_argument("-e", "--end", help="End logging", action="store_true")
    parser.add_argument("-t", "--total", help="Print total time worked", action="store_true")
    parser.add_argument("-d", "--display", help="Display logs", action="store_true")
    parser.add_argument("-p", "--plot", help="Plot times", action="store_true")
    args = parser.parse_args()
    
    if args.start and args.end:
        print("It doesn't make sense to start and end at the same time.")
        sys.exit()    
    
    if args.start:
        log(START)
    elif args.end:
        log(END)
        
    if args.total:
        calc_total_time()
        
    if args.display:
        list_times()
        
    if args.plot:
        plot_times()    
    
def log(action):
    message = input("Input a message: ")
    
    try:
        with open(filename, 'r', newline='') as file:
            data = [i for i in csv.reader(file)]
            prev_entry = data[-1][0]
    except FileNotFoundError:
        init(message)
        sys.exit()
    
    if prev_entry == action:
        raise NotImplementedError("Not sure how to handle this right now.")
        
    data.append([action, time(), message])
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerows(data)
    
    print("Successfully executed", action)
    
def init(message):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([START, time(), message])
        
    print("Succesfully initialized log and started.")
    
def calc_total_time():
    with open(filename, 'r', newline='') as file:
        data = [i for i in csv.reader(file)]
        
    start_times, end_times = [], []
    for entry in data:
        if entry[0] == START:
            start_times.append(float(entry[1]))
        elif entry[0] == END:
            end_times.append(float(entry[1]))
    
    if len(start_times) == len(end_times) + 1:
        end_times.append(time())
        
    if len(start_times) != len(end_times):
        raise Exception("Something weird has occurred")
        
    total_time = 0
    for i in range(len(start_times)):
        total_time += end_times[i] - start_times[i]
    
    print("Total time spent on this project is {:.4f} hours.".format(total_time/3600))
    
def list_times():
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for entry in reader:
            if entry[0] == START:
                print("START: ", end="")
            elif entry[0] == END:
                print("END:   ", end="")
            print(datetime.fromtimestamp(float(entry[1])), end=" ")
            print(entry[2])
            
def plot_times():
    from matplotlib import pyplot as plt # I probably shouldn't do this here, but I don't need this anywhere else.
    
    with open(filename, 'r', newline='') as file:
        data = [i for i in csv.reader(file)]
        
    start_times, end_times = [], []
    for entry in data:
        if entry[0] == START:
            start_times.append(float(entry[1]))
        elif entry[0] == END:
            end_times.append(float(entry[1]))
    
    if len(start_times) != len(end_times) + 1:
        start_times.append(time())
        
    if len(start_times) != len(end_times) + 1:
        raise Exception("Something weird has occurred")
    
    c = 0
    for i in range(len(end_times)):
        diff = end_times[i] - start_times[i]
        plt.plot([start_times[i], end_times[i]], [c, c+diff], 'b-')
        c += diff
        plt.plot([end_times[i], start_times[i+1]], [c, c], 'b-')
        plt.xlabel("Seconds since 1970")
        plt.ylabel("Total seconds")
        plt.title("Time worked on project")
        
    plt.show()

def usage():
    return """This will have more info sometime."""
    
if __name__ == "__main__":
    main()