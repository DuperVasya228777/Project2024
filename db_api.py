import sqlite3

db = None
cursor = None

def db_open():
    global db, cursor
    db = sqlite3.connect("valorant.db")
    cursor = db.cursor()
    cursor.execute("""PRAGMA foreign_keys=on""")

def db_close():
    db.commit()
    cursor.close()
    db.close()

def db_create():
    db_open()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
                        id INTEGER PRIMARY KEY,
                        name VARCHAR,
                        login VARCHAR,
                        password VARCHAR,
                        mail VARCHAR
                   )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS category(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR,
                        info VARCHAR
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS agent(
                        id INTEGER PRIMARY KEY,
                        title VARCHAR,
                        info VARCHAR,
                   icon VARCHAR,
                   spell_1_image VARCHAR,
                   spell_1_info VARCHAR,
                   spell_1_title VARCHAR,
                   spell_2_image VARCHAR,
                   spell_2_info VARCHAR,
                   spell_2_title VARCHAR,
                   spell_3_image VARCHAR,
                   spell_3_info VARCHAR,
                   spell_3_title VARCHAR,
                   spell_4_image VARCHAR,
                   spell_4_info VARCHAR,
                   spell_4_title VARCHAR,
                        prise VARCHAR,
                        id_category INTEGER,

                        FOREIGN KEY (id_category) REFERENCES category(id)
                   )""")
    
    
    
    db_close()
 
def db_del():
    db_open()
    cursor.execute("""DROP TABLE user""")
    cursor.execute("""DROP TABLE agent""")
    cursor.execute("""DROP TABLE category""")
    db_close()

#===================================== user =====================================================
def reg_user(name:str, login:str, password:str, mail:str):
    """login_user -> [id]"""
    last_id = None

    db_open()
    
    cursor.execute("""SELECT login, mail
                        FROM user
                        WHERE login == ? 
                            OR mail == ?
                    """,(login, mail))
    data = cursor.fetchall()

    if data == None or len(data) == 0:
        cursor.execute("""INSERT INTO user(name, login, password, mail)
                            VALUES (?, ?, ?, ?) 
                        """,(name, login, password, mail))
        last_id = cursor.lastrowid

    db_close()
    
    return last_id

def login_user(login:str, password:str):
    """login_user -> [id]"""
    db_open()
    cursor.execute("""SELECT id
                        FROM user
                        WHERE login == ? 
                            AND password == ?
                    """,(login,password))
    data = cursor.fetchone()
    db_close()
    return data

def get_user(id:int):
    """get_user -> [name, login, mail]"""
    db_open()
    cursor.execute("""SELECT name, login, mail
                        FROM user
                        WHERE id == ? 
                    """,(id,))
    data = cursor.fetchone()
    db_close()
    return data
#===================================== category =================================================
def add_category(title:str,info:str):
    "return id"
    db_open()
    cursor.execute("""INSERT INTO category(title,info)
                            VALUES (?,?)  
                   """,(title,info))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_category(id:int):
    "id, title, info"
    db_open()
    cursor.execute("""SELECT id, title, info
                        FROM category
                        WHERE id == ?  
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

def get_all_category():
    "id, title, info"
    db_open()
    cursor.execute("""SELECT id, title, info
                        FROM category
                   """)
    data = cursor.fetchall()
    db_close()
    return data
#===================================== agent ==================================================
def add_agent(title,info,icon,spell_1_image,spell_1_info,spell_1_title,spell_2_image,spell_2_info,spell_2_title,spell_3_image,spell_3_info,spell_3_title,spell_4_image,spell_4_info,spell_4_title,prise,id_category):
    "add_agent -> id"
    db_open()
    cursor.execute("""INSERT INTO agent(title,info,icon,spell_1_image,spell_1_info,spell_1_title,spell_2_image,spell_2_info,spell_2_title,spell_3_image,spell_3_info,spell_3_title,spell_4_image,spell_4_info,spell_4_title,prise,id_category)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
                   """,(title,info,icon,spell_1_image,spell_1_info,spell_1_title,spell_2_image,spell_2_info,spell_2_title,spell_3_image,spell_3_info,spell_3_title,spell_4_image,spell_4_info,spell_4_title,prise,id_category))
    last_id = cursor.lastrowid
    db_close()
    return last_id

def get_agent(id:int):
    " get_agent -> [id, title, info, prise, id_category] "
    db_open()
    cursor.execute("""SELECT agent.id,agent.title,agent.info,agent.icon,agent.spell_1_image,agent.spell_1_info,agent.spell_1_title,agent.spell_2_image,agent.spell_2_info,agent.spell_2_title,agent.spell_3_image,agent.spell_3_info,agent.spell_3_title,agent.spell_4_image,agent.spell_4_info,agent.spell_4_title,agent.prise,category.title,category.info
                        FROM agent,category
                        WHERE agent.id_category == category.id AND agent.id == ? 
                   """,(id,))
    data = cursor.fetchone()
    db_close()
    return data

def get_all_agent():
    " get_all_agent -> [(id,title,info,icon,spell_1_image,spell_1_info,spell_1_title,spell_2_image,spell_2_info,spell_2_title,spell_3_image,spell_3_info,spell_3_title,spell_4_image,spell_4_info,spell_4_title,prise,id_category), ...] "
    db_open()
    cursor.execute("""SELECT id,title,info,icon,spell_1_image,spell_1_info,spell_1_title,spell_2_image,spell_2_info,spell_2_title,spell_3_image,spell_3_info,spell_3_title,spell_4_image,spell_4_info,spell_4_title,prise,id_category
                        FROM agent
                   """)
    data = cursor.fetchall()
    db_close()
    return data

def get_form_category_agent(id_category:int):
    "get_form_category_agent -> [(id,title,info,icon,spell_1_image,spell_1_info,spell_1_title,spell_2_image,spell_2_info,spell_2_title,spell_3_image,spell_3_info,spell_3_title,spell_4_image,spell_4_info,spell_4_title,prise,id_category), ...] "
    db_open()
    cursor.execute("""SELECT *
                        FROM agent
                        WHERE id_category == ?  
                   """,(id_category,))
    data = cursor.fetchall()
    db_close()
    return data
#===================================== create ===================================================
if __name__ == "__main__":
    db_del()
    db_create()
    if True:
        reg_user("name1", "login1", "password1", "mail1")
        reg_user("name2", "login2", "password2", "mail2")
        reg_user("name3", "login3", "password3", "mail3")

        add_category("СТРАЖИ","их способности помогают им защищаться") # id = 1
        add_category("ДУЭЛЯНТЫ","их способности помогают им атаковать") # id = 2
        add_category("ЗАЧИНЩИКИ","их способности помогают их команде") # id = 3
        add_category("СПЕЦИАЛИСТЫ","их способности помогают им контролировать местность") # id = 4

        add_agent("Brimstone",
                  "Уроженец США Brimstone обеспечивает своей команде преимущество перед противником благодаря орбитальной технике. Возможность удаленно оказывать помощь там, где это требуется, делает его несравненным боевым командиром.",
                  "https://static.wikia.nocookie.net/valorant/images/3/37/Brimstone_artwork.png/revision/latest?cb=20200618070006&path-prefix=ru",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/d7e00a4ad8a1a01b2edcb9fc1193d05e4e50248f-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает зажигательный гранатомет. Нажмите кнопку ОГОНЬ, чтобы запустить гранату, которая падает и взрывается после остановки, образуя горящую область, в которой все игроки получают урон.",
                  "Q - ЗАЖИГАТЕЛЬНАЯ ГРАНАТА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/5325b2340045a32d919d467ce3b09c3725de73ea-126x126.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает тактическую карту. Нажмите кнопку ОГОНЬ, чтобы указать места на карте для сброса дымовой завесы. Нажмите кнопку АЛЬТ. ОГОНЬ, чтобы запустить несколько дымовых завес продолжительного действия, застилающих обзор в указанной области.",
                  "E - НЕБЕСНЫЙ ДЫМ",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/f6c1e1c587dbfe97a4185a47326ce45c42620583-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает маячок-стимулятор. Нажмите кнопку ОГОНЬ, чтобы бросить его перед Brimstone. После приземления маячок повышает скорострельность ближайших игроков.",
                  "C - МАЯЧОК-СТИМУЛЯТОР",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/8cfa836d1d19356685e42c13054f9f5bc8e9e029-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает тактическую карту. Нажмите кнопку ОГОНЬ, чтобы запустить в выбранное место орбитальный удар, наносящий высокий периодический урон игрокам, находящимся в выбранной зоне.",
                  "X - ОРБИТАЛЬНЫЙ УДАР",
                  "free",
                  4)
        add_agent("Cypher",
                  "Уроженец США Brimstone обеспечивает своей команде преимущество перед противником благодаря орбитальной технике. Возможность удаленно оказывать помощь там, где это требуется, делает его несравненным боевым командиром.",
                  "https://static.wikia.nocookie.net/valorant/images/3/37/Brimstone_artwork.png/revision/latest?cb=20200618070006&path-prefix=ru",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/d7e00a4ad8a1a01b2edcb9fc1193d05e4e50248f-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает зажигательный гранатомет. Нажмите кнопку ОГОНЬ, чтобы запустить гранату, которая падает и взрывается после остановки, образуя горящую область, в которой все игроки получают урон.",
                  "Q - ЗАЖИГАТЕЛЬНАЯ ГРАНАТА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/5325b2340045a32d919d467ce3b09c3725de73ea-126x126.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает тактическую карту. Нажмите кнопку ОГОНЬ, чтобы указать места на карте для сброса дымовой завесы. Нажмите кнопку АЛЬТ. ОГОНЬ, чтобы запустить несколько дымовых завес продолжительного действия, застилающих обзор в указанной области.",
                  "E - НЕБЕСНЫЙ ДЫМ",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/f6c1e1c587dbfe97a4185a47326ce45c42620583-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает маячок-стимулятор. Нажмите кнопку ОГОНЬ, чтобы бросить его перед Brimstone. После приземления маячок повышает скорострельность ближайших игроков.",
                  "C - МАЯЧОК-СТИМУЛЯТОР",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/8cfa836d1d19356685e42c13054f9f5bc8e9e029-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает тактическую карту. Нажмите кнопку ОГОНЬ, чтобы запустить в выбранное место орбитальный удар, наносящий высокий периодический урон игрокам, находящимся в выбранной зоне.",
                  "X - ОРБИТАЛЬНЫЙ УДАР",
                  "free",
                  4)
        add_agent("Sova",
                  "Уроженец США Brimstone обеспечивает своей команде преимущество перед противником благодаря орбитальной технике. Возможность удаленно оказывать помощь там, где это требуется, делает его несравненным боевым командиром.",
                  "https://static.wikia.nocookie.net/valorant/images/3/37/Brimstone_artwork.png/revision/latest?cb=20200618070006&path-prefix=ru",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/d7e00a4ad8a1a01b2edcb9fc1193d05e4e50248f-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает зажигательный гранатомет. Нажмите кнопку ОГОНЬ, чтобы запустить гранату, которая падает и взрывается после остановки, образуя горящую область, в которой все игроки получают урон.",
                  "Q - ЗАЖИГАТЕЛЬНАЯ ГРАНАТА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/5325b2340045a32d919d467ce3b09c3725de73ea-126x126.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает тактическую карту. Нажмите кнопку ОГОНЬ, чтобы указать места на карте для сброса дымовой завесы. Нажмите кнопку АЛЬТ. ОГОНЬ, чтобы запустить несколько дымовых завес продолжительного действия, застилающих обзор в указанной области.",
                  "E - НЕБЕСНЫЙ ДЫМ",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/f6c1e1c587dbfe97a4185a47326ce45c42620583-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает маячок-стимулятор. Нажмите кнопку ОГОНЬ, чтобы бросить его перед Brimstone. После приземления маячок повышает скорострельность ближайших игроков.",
                  "C - МАЯЧОК-СТИМУЛЯТОР",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/8cfa836d1d19356685e42c13054f9f5bc8e9e029-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает тактическую карту. Нажмите кнопку ОГОНЬ, чтобы запустить в выбранное место орбитальный удар, наносящий высокий периодический урон игрокам, находящимся в выбранной зоне.",
                  "X - ОРБИТАЛЬНЫЙ УДАР",
                  "free",
                  4)
        