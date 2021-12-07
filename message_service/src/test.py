from celery import Celery


app = Celery(
    broker='pyamqp://guest@localhost//'
)


@app.task
def ola_mundo():
    return "Ola Mundo"