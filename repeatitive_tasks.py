MENU = "1- Add Task\n \
       2- Delete Task\n \
       3- Complete Task"


def main:
    close = False

    while not close:
        option = take_option()

        if option = 1:
            add_task()
        elif option = 2:
            delete_task()
        elif option = 3:
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

def task_exist(task_name: str) -> bool:
    with open("repeated_tasks", "r") as file:
        file.readlines().split


def add_task() -> None:
    task_name = input("Task Name: ")
    task_repitition = input("Repeatition (# days): ")

    duplicate_task: str = task_exist(task_name)  # It should be either "" or "task details"
    if (duplicate_task):
        print("Task with same name exists:\n \
                {duplicate_task}\n \
                Do you want to:\n \
                1- Replace the task with the new one\n \
                2- Change the name of the new task\n \
                3- Cancel\n"
                )
        
        while True:
            try:
                option = input(f"Please pick an option (1-3): ")

                if 0 < option < 4:
                    break

            except:
                continue

        