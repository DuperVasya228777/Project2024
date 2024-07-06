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
                  "Торговец информацией из Марокко Cypher может самостоятельно создать целую информационную сеть для отслеживания действий противника. Под неусыпным взором Cypher все тайное становится явным.",
                  "https://static.wikia.nocookie.net/valorant/images/5/55/Cypher_Artwork_Full.png/revision/latest/scale-to-width-down/1200?cb=20220810202731",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/292fbe783ac9e2f638822c5f87f09b005b48a712-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "МГНОВЕННО бросает клетку перед Cypher. Активируйте ее, чтобы ограничить обзор проходящих через нее противников",
                  "Q - КИБЕРКЛЕТКА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/eae012cb583a41bbc0de83f0963a40de58f5534f-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает шпионскую камеру. Нажмите кнопку ОГОНЬ, чтобы поместить камеру на выбранном месте. Используйте умение снова, чтобы управлять камерой. Во время управления камерой нажмите кнопку ОГОНЬ, чтобы выстрелить отслеживающим дротиком. При попадании в игрока дротик отмечает его местонахождение",
                  "E - КАМЕРА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/df43766f56e1e844ed1b179722c9444a1bd1d45c-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает растяжку. Нажмите кнопку ОГОНЬ, чтобы установить в выбранном месте разрушаемую незаметную растяжку, соединяемую с противоположной стеной. Попавшие в нее противники обездвиживаются и ненадолго обнаруживают себя, а через некоторое время оглушаются. Растяжку можно подобрать и использовать ПОВТОРНО.",
                  "C - РАСТЯЖКА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/3e8e1779afeebd0612c019f8b2d41d7a984781b3-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "При наведении прицела на мертвого противника МГНОВЕННО раскрывает местоположение всех живых врагов.",
                  "X - НЕЙРОКРАЖА",
                  "8000kp/1000vp",
                  1)
        add_agent("Sova",
                  "Рожденный в вечной мерзлоте российского заполярья, Sova выслеживает и уничтожает противников с холодной точностью и эффективностью. Этот первоклассный разведчик, экипированный особым луком, найдет вас, где бы вы ни прятались.",
                  "https://static.wikia.nocookie.net/valorant/images/6/61/Sova_artwork.png/revision/latest?cb=20200617183335&path-prefix=ru",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/8ab5a2d03438ff0f8b2ba2d7b26c812ab6b7adbb-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает шоковую стрелу. Нажмите кнопку ОГОНЬ, чтобы выпустить стрелу, летящую по прямой. При столкновении она срабатывает, нанося урон игрокам поблизости. УДЕРЖИВАЙТЕ КНОПКУ ОГОНЬ, чтобы увеличить дальность выстрела. Нажатие кнопки АЛЬТ. ОГОНЬ позволяет стреле отскакивать от стен до двух раз.",
                  "Q - ШОКОВАЯ СТРЕЛА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/b428e1783f98a0990b86d13872f564095442f44b-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает разведстрелу. Нажмите кнопку ОГОНЬ, чтобы выпустить стрелу, летящую по прямой. При столкновении она активируется, показывая местоположение противников в зоне видимости. Враги могут уничтожить стрелу. Удерживайте кнопку ОГОНЬ для увеличения дальности выстрела. При нажатии кнопки АЛЬТ. ОГОНЬ стрела отскакивает от стен до двух раз.",
                  "E - РАЗВЕДСТРЕЛА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/07877d7c79546ef64338eae550ffa5649f3582b0-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает дрон-сову. Нажмите кнопку ОГОНЬ, чтобы выпустить дрон и получить контроль над его передвижением. Управляя дроном, нажмите кнопку ОГОНЬ, чтобы выстрелить помечающим дротиком. При попадании в игрока дротик раскрывает его позицию. Враги могут уничтожить дрон-сову.",
                  "C - ДРОН-СОВА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/7b9f078b0576e87e74b8175b0d33ac682b7a8ab3-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает три дальнобойные стрелы, пробивающие стены особым мощным импульсом. Нажмите кнопку ОГОНЬ, чтобы выпустить импульс по прямой перед агентом, нанося урон и раскрывая позицию всех раненых врагов. Умение можно использовать еще два раза, пока активен таймер.",
                  "X - ГНЕВ ОХОТНИКА",
                  "free",
                  3)
        add_agent("Phoenix",
                  "Представитель Великобритании Phoenix демонстрирует звездную силу во всех аспектах своего боевого стиля: он сражается красиво и ярко, всегда навязывает противнику свои условия и отважно устремляется в бой даже без поддержки.",
                  "https://static.wikia.nocookie.net/valorant/images/f/f8/Phoenix_Artwork.png/revision/latest?cb=20200617130247&path-prefix=ru",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/beb874d19c79982f0e99e858098c067d9132a95a-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает ослепляющую сферу, летящую по дуге и взрывающуюся вскоре после броска. При взрыве сфера ослепляет всех игроков, смотревших на нее в момент взрыва. Нажмите кнопку ОГОНЬ, чтобы загнуть дугу сферы влево, и кнопку АЛЬТ. ОГОНЬ – вправо.",
                  "Q - КРУЧЕНАЯ ПОДАЧА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/67df9ca3cb158a945fc9b13eb0e3949683c4c65d-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает огненный шар. Нажатием кнопки ОГОНЬ выпускается огненный шар, который взрывается после задержки или при падении на землю, создавая охваченную огнем область, наносящую урон противникам.",
                  "E - ГОРЯЧИЕ РУКИ",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/d807a982ce70475acb2e8461b4f8737204e35d96-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "Выбирает огненную стену. Нажатием кнопки ОГОНЬ вперед выпускается пламя, образующее стену огня. Она заслоняет обзор и наносит урон проходящим через нее игрокам. УДЕРЖИВАЙТЕ КНОПКУ ОГОНЬ, чтобы изогнуть стену в сторону прицела.",
                  "C - ПЕКЛО",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/d428c0c6c73ba34676e063092a7ae7157268db0c-128x128.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "МГНОВЕННО помечает текущую позицию Phoenix. Если время действия умения истекает или если Phoenix погибает, пока оно действует, то он воскресает в точке, где начал применять умение, с полным запасом здоровья.",
                  "X - ВОЗВРАТ",
                  "free",
                  2)
        add_agent("Gekko",
                  "Gekko из Лос-Анджелеса заправляет дружной командой безбашенных существ. Его верные зверята смело бросаются в драку, разнося врагов в пух и прах. А когда Gekko подбирает питомцев с поля боя, можно перевести дух и повторить!",
                  "https://static.wikia.nocookie.net/valorant-lore/images/2/27/Gekko_-_Full_body.png/revision/latest?cb=20230304231856",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/6a9ead27349e4fa318bc426ac57f9addb2ecf143-252x175.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "ВЫБИРАЕТ Тыдыща. Нажмите ОГОНЬ, чтобы бросить Тыдыща, как гранату. Нажмите АЛЬТ. ОГОНЬ, чтобы сделать бросок снизу. Коснувшись поверхности, Тыдыщ разделяется, покрывая большую площадь, и после небольшой задержки взрывается.",
                  "Q - ТЫДЫЩ",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/0be9c33b718eb7f941890558e661f147802cf762-256x236.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "ВЫБИРАЕТ Бегуна. Нажмите ОГОНЬ, чтобы отправить Бегуна вперед искать противников. Бегун высвобождает энергию в сторону первого увиденного врага, совершая оглушающий взрыв. Нажмите АЛЬТ. ОГОНЬ, нацелившись на точку установки Spike или на установленный Spike, чтобы Бегун установил или обезвредил его. Spike должен быть в инвентаре Gekko, чтобы Бегун мог его установить. Когда энергия заканчивается, Бегун превращается в шарик и бездействует. ВЗАИМОДЕЙСТВУЙТЕ с шариком, чтобы забрать его, и спустя короткое время Бегун получит новый заряд энергии.",
                  "E - БЕГУН",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/5cd2d39b6747b897e6648172d084d355477ea545-255x248.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "ВЫБИРАЕТ Кляксу. Нажмите ОГОНЬ, чтобы запустить Кляксу высоко в воздух и послать ее вперед. Зарядившись, Клякса запускает взрывающиеся сгустки плазмы в сторону противников в зоне видимости. Когда энергия заканчивается, Клякса превращается в шарик и бездействует. ВЗАИМОДЕЙСТВУЙТЕ с шариком, чтобы забрать его, и спустя короткое время Клякса получит новый заряд энергии.",
                  "C - КЛЯКСА",
                  "https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data/589f75f0e50a8c1c465e2bf95599d140c52c69f4-254x241.png?auto=format&fit=crop&q=80&h=57&w=57&crop=center",
                  "ВЫБИРАЕТ Бабах. Нажмите ОГОНЬ, чтобы установить мысленную связь с Бабах и управлять ее передвижением по вражеской территории. Нажмите кнопку АКТИВАЦИИ, чтобы Бабах сделала рывок вперед и устроила взрыв, замедлив врагов на небольшом расстоянии от себя. Когда энергия заканчивается, Бабах превращается в шарик и бездействует. ВЗАИМОДЕЙСТВУЙТЕ с шариком, чтобы забрать его, и спустя короткое время Бабах получит новый заряд энергии. Повторный заряд Бабах можно использовать только один раз.",
                  "X - БАБАХ",
                  "8000kp/1000vp",
                  3)