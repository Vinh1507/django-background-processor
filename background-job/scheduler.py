from apscheduler.schedulers.blocking import BlockingScheduler
from tasks import print_message, add_numbers, call_api

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', seconds=20)
def scheduled_task():
    print_message.send("Hello from the scheduler!")
    add_numbers.send(5, 7)
    call_api.send()

if __name__ == "__main__":
    print("Starting scheduler...")
    scheduler.start()
