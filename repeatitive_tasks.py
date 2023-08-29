MENU = "1- Add Task\n \
       2- Delete Task\n \
       3- Complete Task"
FILE_NAME = "repeated_tasks.csv"
CSV_LINE = "{task_name},{task_repitition},{last_completetion_date}"

def main():
    close = False

    while not close:
        option = take_option()

        if option == 1:
            add_task()
        elif option == 2:
            delete_task()
        elif option == 3:
            complete_task()


        while True:
            option = input("Go back to the menu? (Y/N): ").upper()

            if option in ("Y", "N"):
                close = (option == "N")
                break


def take_option() -> int:
    print(MENU)

    while True:
        try:
            option = int(input("Please pick an option (1-3): "))

            if 0 < option < 4:
                break

        except:
            continue

    return option

def task_exist(task_name: str) -> tuple[int, str]:
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()

        for i in range(len(lines)):
            if lines[i].split(",")[0] == task_name:
                return (i, lines[i])
        
        return (-1, None)



def add_task() -> None:
    option = None
    task_name = input("Task Name: ")

    task_info = task_exist(task_name)
    
    if (task_info[0] != -1):
        print("Task with same name exists:\n \
                {task_info[1]}\n \
                Do you want to:\n \
                1- Replace the task with the new one.\n \
                2- Pick another name.\n \
                3- Cancel.\n"
                )
        
        while True:
            try:
                option = int(input(f"Please pick an option (1-3): "))

                if 0 < option < 4:
                    break

            except:
                continue
        
        if option == 2:
            add_task()
            return

        if option == 3:
            return


    # Taking the repitition (# days before you need to do the task again)
    while True:
        try:
            task_repitition = int(input("Repeatition (# days): "))

            if task_repitition > 0:
                break
        except:
            continue



    if option == 1:
        replace_task(task_info[0], task_name, task_repitition)
        return
        
    
    with open(FILE_NAME, "a") as file:
        file.write(CSV_LINE.format(
            task_name=task_name,
            task_repitition=task_repitition,
            last_completetion_date=None
        ))


def replace_task(taskline: int, task_name: str, task_repitition: str | int) -> None:
    with open(FILE_NAME, "r") as file:
        lines = file.readlines()
    
    with open(FILE_NAME, "w") as file:
        file.writelines([
            *lines[:taskline],
            CSV_LINE.format(
                        task_name=task_name,
                        task_repitition=task_repitition,
                        last_completetion_date=None
                        ),
            *lines[taskline+1:]    
        ])