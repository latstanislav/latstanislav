import pendulum
from airflow.decorators import dag, task
from steps.messages import send_telegram_success_message, send_telegram_failure_message
from steps.func_transformation import remove_duplicates, remove_outliers, remove_none
import pandas as pd
import numpy as np
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import MetaData, Table, Column, Integer, inspect, UniqueConstraint, Float, Boolean, BigInteger

@dag(
    schedule='@once',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    catchup=False,
    tags=["ETL Project"],
    on_success_callback=send_telegram_success_message,
    on_failure_callback=send_telegram_failure_message,
)
    

def clean_target_price_dataset(): 
    ''' 
    Выше называл основную функция DAG второго этапа

    Ниже создаю функцию для создания таблицы с параметрами данных для дальнейшего ее наполнения 
    '''
    @task() 
    def create_table():

        '''подключение к собственной базе данных '''
        hook=PostgresHook('destination_db')
        db_conn=hook.get_sqlalchemy_engine()
        metadata = MetaData()
        new_table_target_price=Table(
        'clean_flat_target_price',
        metadata,
        Column('id', Integer, primary_key=True),
        Column('floor', Integer),
        Column('is_apartment', Boolean),
        Column('kitchen_area', Float),
        Column('living_area', Float),
        Column('rooms', Integer),
        Column('studio', Boolean),
        Column('total_area', Float),
        Column('price', BigInteger),
        Column('build_year', Integer),
        Column('building_type_int', Integer),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('ceiling_height', Float),
        Column('flats_count', Integer),
        Column('floors_total', Integer),
        Column('has_elevator', Boolean),
        UniqueConstraint('id', name='uni_flat_id')
) 
        if not inspect(db_conn).has_table(new_table_target_price.name): 
            metadata.create_all(db_conn) 


    @task()
    def extract():
        hook = PostgresHook('destination_db')
        conn = hook.get_conn()
        sql = """
        SELECT
                f.id,
                f.floor,
                f.kitchen_area,
                f.living_area,
                f.rooms,
                f.is_apartment,
                f.studio,
                f.total_area,
                f.price,
                b.build_year,
                b.building_type_int,
                b.latitude,
                b.longitude,
                b.ceiling_height,
                b.flats_count,
                b.floors_total,
                b.has_elevator
        FROM flats AS f
        LEFT JOIN buildings AS b ON b.id = f.building_id;
        """
        data = pd.read_sql(sql, conn)
        conn.close()
        return data

    @task()
    def transform(data: pd.DataFrame):
        
        '''Удаляем дубли'''
        data = remove_duplicates(data)
        
        '''Удаляем выбросы'''
        
        data = remove_outliers(data)

        '''Удаляем пустые строки или None'''
        
        data = remove_none(data)
        
        return data

    @task()
    def load(data: pd.DataFrame):
        hook = PostgresHook('destination_db')
        hook.insert_rows(
            table="clean_flat_target_price",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['id'],
            rows=data.values.tolist()
            )

    create_table()
    data = extract()
    transformed_data = transform(data)
    load(transformed_data)
    
clean_target_price_dataset()