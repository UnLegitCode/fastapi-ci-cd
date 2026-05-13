import time

def send_notification(task_id: int, task_title: str):
   print(f"[Notification] Task {task_id} - {task_title} created\n")

   time.sleep(2)