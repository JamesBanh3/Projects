# Notes: 
# Use the following username and password to access the admin rights 
# username: admin
# password: password


#region =====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)
#endregion


#region ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password


# -----Login Loop-----
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ").lower()
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True
#endregion


#=====Variable Functions=====
def user_date_input_yyyy_mm_dd():
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            if due_date_time < datetime.today():
                print("Invalid due date")
            else: break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    return due_date_time   

def save_task_file():
    # Save task_list to file
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
            
def show_task(t):
    ''' Display each task by the following:
    _____________________________________
    Assigned to:
    Date Assigned:
    Due Date:
    Task Complete?
    Task Description:
    '''
    print("_____________________________________")
    disp_str = f"Task {task_list.index(t)+1}: \t {t['title']}\n"
    disp_str += f"Assigned to: \t {t['username']}\n"
    disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task Complete? \t Yes\n" if t['completed'] == True else "Task Complete? \t No\n"
    disp_str += f"Task Description: \n {t['description']}\n"
    print(disp_str)

def modify_task_menu(task_selected):
    # presenting the modify task menu to the user and 
    # making sure that the user input is converted to lower case.
    while True:
        modify = input('''Select one of the following Options below:
    c - Mark task as completed
    a - Change assignment
    d - Change due date
    b - Back
    : ''').lower()
        
        # Match the options the user has choosen
        match modify:
            
            # Mark the task complete and save to file
            case "c":
                confirm = input("Confirm mark as complete 'Yes'/'No'? ").lower()
                if confirm == "yes":
                    task_list[task_selected-1]['completed'] = True
                    save_task_file()
                    print("Task successfully completed.")
                elif confirm == "no":
                    continue
                else:
                    print("You have made a wrong choice, Please Try again")

            # Change to assignment of the task and save to file        
            case "a":
                change_assign = input("Who would you like to assign the task to? ").lower()
                if change_assign == task_list[task_selected-1]['username']:
                    print("Same person assigned.")
                elif change_assign in username_password.keys():
                    task_list[task_selected-1]['username'] = change_assign
                    save_task_file()
                    print("Task successfully re-assigned.")
                else:
                    print ("Username not found")
                    
            # Change to due date of the task and save to file        
            case "d":
                new_due_date = user_date_input_yyyy_mm_dd()
                task_list[task_selected-1]['due_date'] = new_due_date
                save_task_file()
                print("Task due date successfully changed.")
                
            case "b": break
            case _: 
                print("You have made a wrong choice, Please Try again")

def change_to_percentage(number):
    return round(number*100)      

#=====Menu Fuctions=====
def main_menu():
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()
    
    match menu:
        case 'r'    : reg_user()        # Register new user
        case 'a'    : add_task()        # Add new task
        case 'va'   : view_all()        # View all task
        case 'vm'   : view_mine()       # View task for user
        case 'gr'   : generate_reports()# Generate reports
        case 'ds'   : display_stats()   # Display statistics       
        case 'e'    :                   # Exit program
            print('Goodbye!!!')
            exit()
        case _      :                   # Wrong option chosen
            print("You have made a wrong choice, Please Try again")
            
def reg_user():
    '''Add a new user to the user.txt file''' 
    
    # - Request input of a new username   
    while True:
        new_username = input("New Username: ").lower()
        # Check if username exist in dictionary
        if new_username in username_password.keys(): 
            print("Username already exist. Please try again.\n")
            continue
        else: break # Exit loop if not username is unique and continue for password
            
    
    new_password = input("New Password: ")          # - Request input of a new password
    confirm_password = input("Confirm Password: ")  # - Request input of password confirmation.
    
    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
            
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
         - A username of the person whom the task is assigned to,
         - A title of a task,
         - A description of the task and 
         - the due date of the task.'''
    task_username = input("Name of person assigned to task: ").lower()
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    due_date_time = user_date_input_yyyy_mm_dd()


        # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
        }

    task_list.append(new_task)
    save_task_file()
    print("Task successfully added.")
    
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    for t in task_list:
        show_task(t) # for each task in file, print a copy for user

def view_mine():
    '''Reads the task from task.txt file and prints to the 
    console in user friendly format
    '''
    # Display a list of task assigned to current user
    for t in task_list:
        if t['username'] == curr_user:
            show_task(t)
            
    # Loop select task menu until -1 is entered
    while True:
        try:
            # Let user select a task
            task_select = int(input("Select task number(-1 to return to menu): "))
            
            if task_select == -1: # Exit to main menu
                break
            
            # Show selected task if it assigned to user
            elif task_list[task_select-1]['username'] == curr_user:
                show_task(task_list[task_select-1])
                
                # Check if the task is not completed and allow an edit
                if task_list[task_select-1]['completed'] == False:
                    modify_task_menu(task_select)
                    
                else: print("Task selected has been completed")   
            else: print("Invalid task selected")
            
        except ValueError:
            print("Invalid task selected")

def generate_reports():
    '''Create reports in task_overview and user_overview file 
    in user friendly format
    '''
    # Output a task overview text file

    num_tasks = len(task_list)
    num_completed_task = 0
    num_overdue_task = 0
    # Count every task completed and every task overdue
    for t in task_list: 
        if t['completed'] == True: num_completed_task += 1
        if t['completed'] == False and t['due_date'] < datetime.today():
            num_overdue_task += 1
    
    percent_incomplete = change_to_percentage((num_tasks-num_completed_task)/ num_tasks)
    percent_overdue = change_to_percentage(num_overdue_task/ (num_tasks-num_completed_task))
    
    # Save data into file  
    with open("tasks_overview.txt", "w") as task_overview_file:
        
        task_overview_file.write(f'''
---------------------------------------------
Number of tasks:              {num_tasks}
Number of completed tasks:    {num_completed_task}
Number of uncompleted tasks:  {num_tasks-num_completed_task}
Number of over due tasks:     {num_overdue_task}

Percentage of task incomplete:          {percent_incomplete}%
Percentage of overdue uncompleted task: {percent_overdue}%
---------------------------------------------
                                 ''')
         
         
    # Output a user overview text file    
    num_users = len(username_password.keys())
    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f'''
---------------------------------
Number of users: \t {num_users}
Number of tasks: \t {num_tasks}
---------------------------------
                                 ''')
        
        # Create information for each user
        for user in username_password.keys():
            user_task_count = 0
            user_task_completed = 0
            user_task_overdue = 0
            for t in task_list:
                if t['username'] == user: 
                    user_task_count += 1
                    if t['completed'] == True: user_task_completed += 1
                    if t['completed'] == False and t['due_date'] < datetime.today():
                        user_task_overdue += 1
                        
            # output information for each user            
            user_overview_file.write(f'''
------------------------------------------
>>>>>>>>>>>>>>>>   {user}   <<<<<<<<<<<<<<
Number of tasks:                 {user_task_count}
Percentage of task assigned:     {change_to_percentage(user_task_count/num_tasks)if user_task_count > 0 else ""}%
Percentage of task completed:    {change_to_percentage(user_task_completed/user_task_count) if user_task_count > 0 else ""}%
Percentage of task uncompleted:  {change_to_percentage(1-(user_task_completed/user_task_count)) if user_task_count > 0 else ""}%
Percentage of task overdue:      {change_to_percentage(user_task_overdue/(user_task_count-user_task_completed)) if user_task_count > 0 else ""}%
------------------------------------------
                                 ''')            
                    
def display_stats():
    '''Reads the data from task_overview and user_overview file and prints to the 
    console in user friendly format
    '''
    if curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
        and tasks.'''
        
        # Update reports file first before displaying information
        generate_reports()
        with open("tasks_overview.txt", "r", ) as task_overview_file:
            print("Task Overview")
            print(task_overview_file.read())
        
        with open("user_overview.txt", "r", ) as user_overview_file:
            print("User Overview")
            print(user_overview_file.read())
                  

#=====Program Start=====      
while True:
    main_menu()