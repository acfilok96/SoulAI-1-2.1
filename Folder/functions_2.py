import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from functions import *
from groq import Groq
import pandas as pd

def watchSummary():
    
    Gorq_Key = str("Enter Groq API Key")
    groq_model = Groq(api_key = str(Gorq_Key))
    
    database = "Image_Record_SQLDB.db"
    sql_query = "SELECT * FROM Image_Record_SQLDB_TABLE"
    data = read_sql_databse(database, sql_query)
    data = [i for i in data]
    table_column = ["Image Id", "Image Name", "Image Details", "Image Summary"]
    
    prompt_2 = f"""You task is to convert the Given List of Details into a DataFrame.
                Given List of Details: {data}
                """
    # Given table Column Name: {table_column}
    system_prompt = f"""Share your response in tabular format. Share only response, nothing extra, nothing else. \
                    Do not share any additional information."""
    response_2 = groq_model.chat.completions.create(
                        model = "llama3-70b-8192", 
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": prompt_2
                            }
                        ],
                        temperature = 0.3,
                        max_tokens = 1024,
                        top_p = 1,
                        stream = False,
                        stop = None # ", 6"
                    )

    return response_2.choices[0].message.content



def read_sql_databse(database, sql_query):

    connection_1 = sqlite3.connect(database)
    cursor_1 = connection_1.cursor()
    cursor_1.execute(sql_query)
    datas = cursor_1.fetchall()
    connection_1.commit()
    connection_1.close()

    return datas

# database = "/content/Image_Record_SQLDB.db"
# sql_query = "SELECT * from Image_Record_SQLDB_TABLE"
# read_sql_databse(database, sql_query)

def searchDB(database, filename):
    filename = str(filename)
    connection_1 = sqlite3.connect(database)
    cursor_1 = connection_1.cursor()
    sql_query = str("SELECT Image_Name from Image_Record_SQLDB_TABLE where Image_Name = '")+str(filename)+str("'")
    cursor_1.execute(sql_query)
    datas = cursor_1.fetchall()
    connection_1.commit()
    connection_1.close()

    return datas


engine = create_engine('sqlite:///Image_Record_SQLDB.db')
Base = declarative_base()

class ImageSummary(Base):
    __tablename__ = 'Image_Record_SQLDB_TABLE'
    id = Column("Image_Id", Integer, primary_key=True)
    filename = Column("Image_Name", String, unique=True)
    details = Column("Image_Details", Text)
    summary = Column("Image_Summary", Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def store_image_summary(images):
    database = "Image_Record_SQLDB.db"
    image_name = images.name
    if searchDB(database, str(image_name)) == []:
        response_details, response_summary = mainFunc(images)
        image_summary = ImageSummary(filename=image_name, details=response_details, summary=response_summary)
        session.add(image_summary)
        session.commit()

# # Example usage:
# filename = # "1.jpg"
# summary = LLmFunc(filename)# "3 Example summary text."
# database = "Image_Record_SQLDB.db"
# store_image_summary(database, filename, summary)

def downloadData():
    database = "Image_Record_SQLDB.db"
    sql_query = "SELECT * FROM Image_Record_SQLDB_TABLE"
    data = read_sql_databse(database, sql_query)
    if data:
        data = [i for i in data]
        column_name = ["Id", "Name", "Details", "Summary"]
        data_frame = pd.DataFrame(data, columns = column_name)
        data_frame = data_frame.drop(columns = ['Id'])
        data_frame = data_frame.to_csv().encode('utf-8')
    else:
        data =  [[None, None, None]]
        column_name = ["Name", "Details", "Summary"]
        data_frame = pd.DataFrame(data, columns = column_name)
        data_frame = data_frame.to_csv().encode('utf-8')
    st.download_button(label="Data.csv",
                       data=data_frame,
                       file_name="Image_Details.csv",
                       key='download-button')
