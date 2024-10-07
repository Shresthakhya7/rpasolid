from robocorp.tasks import task,teardown
from app.bot import bot


main = bot()
@task
def start():
    main.start()

@teardown
def end(self):
    main.teardown()
