from airflow.providers.telegram.hooks.telegram import TelegramHook # импортируем хук телеграма
from airflow.models import Variable

def send_telegram_success_message(context): # на вход принимаем словарь с контекстными переменными
    token_telegram=Variable.get('token')
    chat_id_telegram=Variable.get('chat_id')
    hook = TelegramHook(token=token_telegram, chat_id=chat_id_telegram)
    dag = context['dag'].dag_id
    run_id = context['run_id']
    
    message = f'Исполнение DAG {dag} с id={run_id} прошло успешно!' # определение текста сообщения
    hook.send_message({
        'chat_id': chat_id_telegram,
        'text': message
    })
def send_telegram_failure_message(context):
    token_telegram=Variable.get('token')
    chat_id_telegram=Variable.get('chat_id')
    hook = TelegramHook(token=token_telegram, chat_id=chat_id_telegram)
    run_id = context['run_id']
    task_instance_key_str= context['task_instance_key_str']
    
    message = f'Исполнение DAG {task_instance_key_str} с id={run_id} упало!' # определение текста сообщения
    hook.send_message({
        'chat_id': chat_id_telegram,
        'text': message
    })
    