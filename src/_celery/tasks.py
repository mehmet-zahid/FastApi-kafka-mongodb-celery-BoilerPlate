from _celery.celery_main import celery_app, async_to_sync


@celery_app.task(bind=True)
@async_to_sync
async def example_task_async_with_bind(self, file_data: bytes, file_name: str): ...


@celery_app.task
@async_to_sync
async def example_task_async(): ...


# also it is possible to define non-async tasks as usual in celery


@celery_app.task
def example_task(): ...
