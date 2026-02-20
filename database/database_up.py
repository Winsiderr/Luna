from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from database.config import settings
from database.schemes import Company, Category

engine = create_engine(
    url = settings.DATABASE_URL,
    echo = False
)

session_factory = sessionmaker(engine)

def insert_data():
    with session_factory() as session:
        if session.execute(select(Company).limit(1)).scalar_one_or_none() is not None:
            return
        category_eat = Category(name="Еда")

        category_car = Category(name = "Автомобили")
        session.add_all([category_eat, category_car])
        session.flush()


        category_eat_milk = Category(name = "Молочная продукция", parent=category_eat)
        category_eat_meat = Category(name = "Мясная", parent=category_eat)
        category_car_heavy = Category(name = "Грузовые автомобили", parent=category_car)
        category_car_soft = Category(name = "Легковые автомобили", parent=category_car)
        session.add_all([category_eat_milk, category_eat_meat, category_car_heavy, category_car_soft])
        session.flush()

        #Если хотите проверить че будет если создать категории с недопустимым уровнем вложенности
        """
        category_car_soft_details = Category(name="Детали для легковых автомобилей", parent=category_car_soft)
        to_be_continued= Category(name="Детали для деталей для легковых автомобилей", parent=category_car_soft_details)
        session.add_all([to_be_continued, category_car_soft_details])
        session.flush()
        """

        company_one = Company(
            name = "ООО Рога и Копыта",
            number = "+7 911 228 13 37",
            adress = "Москва, Улица Пушкина, 8",
            category = category_eat_milk,
            latitude=55.753077839134995,
            longitude=37.620662594371474
        )

        company_two = Company(
            name = "ОАО Бивни и Мамонты",
            number = "+7 911 248 43 47",
            adress = "Москва, Красная площадь, 9",
            category=category_eat_milk,
            latitude=55.7538462643853,
            longitude=37.6195897107655
        )

        company_three = Company(
            name = "ООО Бнал",
            number = "+7 922 248 48 48",
            adress = "Омск, Улица Седова, 65",
            category=category_eat_meat,
            latitude=54.9474327251976,
            longitude=73.32209745218682
        )

        company_four = Company(
            name = "ООО Челябинский трикотаж",
            number = "+7 999 278 43 28",
            adress = "Челябинск, Улица Абразивная , 73",
            category=category_car_heavy,
            latitude=55.182370621336496,
            longitude=61.43767487517991
        )

        company_five = Company(
            name = "ООО Васян и гребцы",
            number = "+7 921 888 73 78",
            adress = "Санкт-Петербург, Улица Метростроевцев, 2",
            category=category_car_soft,
            latitude=59.900234306088386,
            longitude=30.28241731958622
        )

        company_six = Company(
            name = "ЗАО Толик и Бобик",
            number = "+7 921 888 77 77",
            adress = "Санкт-Петербург, Улица Метростроевцев, 2",
            category=category_car_soft,
            latitude=59.9004445040671,
            longitude=30.2839086277985
        )

        session.add_all([company_one, company_two, company_three, company_four, company_five, company_six])
        session.flush()
        session.commit()