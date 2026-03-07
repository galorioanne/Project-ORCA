import os
import time

tasks = []
schedule = []

def clear_console(): 
    # Check the operating system name
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def main_menu(): # Main Menu function
    clear_console()
    width = 50  # The Width of the header in the main menu

    print((' '*6) + ((f">> \033[1;36mProject CARO\033[0m <<").center(width)))
    print("="*width)
    print(f"*  \033[92m1.\033[0m - Add Task")
    print(f"*  \033[92m2.\033[0m - Add Schedule")
    print(f"*  \033[92m3.\033[0m - View Schedule and Tasks")
    print(f"*  \033[92m4.\033[0m - Exit")

    output = input(f"\n\033[36mInput Here\033[0m >>  ")
    return output

def prompt_redo(): # Prompts user if they want to go back to main menu
    output = input(f"\033[36mDo you want to continue?\033[0m >>  ")
    output = output.upper()

    yes = {"Y","YES", "YEP", "YEAH", "YE", "SURE", "MHM", "SI", "YASS", "YESS"} # Includes most of the responses for "yes"
    no = {"N", "NO", "NAH", "NOPE", "NAY", "NOO", "NEIN"} # Includes most of the responses for "no"
    if output in yes:
        return main_menu() # Reprompts main_menu() if yes is chosen
    if output in no:
        return "4" # Returns '4' aka the terminate option
    else:
        print("\n", output , " is not a valid option.")
        return prompt_redo()
        
def add_task():
    width = 50  # The Width of the header in the main menu

    print((' '*6) + ((f">> \033[1;36mADD TASK\033[0m <<").center(width)))
    print("="*width)
    task_name = input("\033[36mEnter task name\033[0m >>  ")
    due_date = input("\033[36mEnter due date (YYYY-MM-DD)\033[0m >>  ")
    due_time = input("\033[36mEnter due time (HH:MM)\033[0m >>  ")

    task = {
        "name": task_name,
        "date": due_date,
        "time": due_time
    }

    tasks.append(task)
    print("Task added successfully!\n")

def check_conflict(day, start, end):
    for activity in schedule:
        if activity["day"] == day:
            existing_start = activity["start"]
            existing_end = activity["end"]

            # fortime overlap
            if not (end <= existing_start or start >= existing_end):
                return True
    return False

def add_schedule():
    width = 50  # The Width of the header in the main menu

    print((' '*6) + ((f">> \033[1;36mADD TO SCHEDULE\033[0m <<").center(width)))
    print("="*width)
    activity = input("\033[36mEnter activity name\033[0m >>  ")
    day = input("\033[36mEnter day (YYYY-MM-DD)\033[0m >>  ")
    start = input("\033[36mEnter start time (HH:MM)\033[0m >>  ")
    end = input("\033[36mEnter end time (HH:MM)\033[0m >>  ")

    if check_conflict(day, start, end):
        print("Conflict detected,Time overlaps with an existing activity.\n")
    else:
        schedule.append({
            "activity": activity,
            "day": day,
            "start": start,
            "end": end
        })
        print("Atcivity added to schedule!\n")

def view_all():
    width = 50  # The Width of the header in the main menu

    print((' '*6) + ((f">> \033[1;36mTASK LIST\033[0m <<").center(width)))
    print("="*width)
    if not tasks:
        print("No tasks yet.")
    else:
        for i, t in enumerate(tasks, 1):
            print(f"* \033[92m{i}.\033[0m - {t['name']} - Due: {t['date']} at {t['time']}")
    print("\n")
    print((' '*6) + ((f">> \033[1;36mSCHEDULE\033[0m <<").center(width)))
    print("="*width)
    if not schedule:
        print("No scheduled activities.")
    else:
        for i, s in enumerate(schedule, 1):
            print(f"{i}. {s['activity']} | {s['day']} {s['start']} - {s['end']}")
    print()

output = main_menu()

while output != "4":
    if output == "1" or output == "1." or  output.upper() == "ONE":
        clear_console()
        add_task()

        output = prompt_redo()
    elif output == "2" or output == "2." or  output.upper() == "TWO":
        clear_console()
        add_schedule()

        output = prompt_redo()
    elif output == "3" or output == "3." or  output.upper() == "THREE":
        clear_console()
        view_all()

        output = prompt_redo()
    else:
        print("\n", output , " is not a valid option.")
        output = input(f"\033[36mInput Here\033[0m >>  ")
