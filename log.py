import time


def log(e, print_error=True, title="Error"):
    if print_error:
        print(f"{title}: {e}")

    datetime = time.localtime()
    formatted_datetime = f"DATE - {datetime[2]}/{datetime[1]}/{datetime[0]}, \
        TIME -{datetime[3]}:{datetime[4]}:{datetime[5]}"
    with open("error.log", "a") as f:
        f.write(f"\n-----------------\n\n{title}\n{formatted_datetime}\n{e}")
