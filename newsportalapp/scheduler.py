from apscheduler.schedulers.background import BackgroundScheduler


newsportalapp_scheduler = BackgroundScheduler()
newsportalapp_scheduler.add_job(
    id='send_mails',
    func=lambda: print(123),
    trigger='interval',
    seconds=5,
)