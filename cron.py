from crontab import CronTab

cron = CronTab()
job = cron.new(command='python3 cleaner.py')
job.day.every(2)

cron.write()
