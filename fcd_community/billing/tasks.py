from config import celery_app

@celery_app.task()
def validate_user_credit_cards():
    print('validate_user_credit_cards')
