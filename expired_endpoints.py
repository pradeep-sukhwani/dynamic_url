import subprocess

from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    print('inside job')
    bash_command = ["python", "manage.py", "expired_endpoints"]
    process = subprocess.Popen(bash_command, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output, error)
    print('outside job')


if __name__ == '__main__':
    scheduler.start()
