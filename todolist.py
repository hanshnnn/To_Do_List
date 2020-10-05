from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
# session.query(Task).delete()
# session.commit()


def add_task(name, deadline):
    checker = 0
    rows = session.query(Task).filter(Task.deadline == deadline)
    if rows:
        for i in rows:
            if name == i.task:
                print('The task has been added!')
                checker = 1
    if checker == 0:
        new_row = Task(task=name, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()


def today_task():
    today = datetime.today()
    rows = session.query(Task).all()
    print(f"\nToday {today.day} {today.strftime('%b')}:")
    if not rows:
        print('Nothing to do!')
    else:
        for i in rows:
            print(i.task)
    print()


def week_task():
    x = 0
    today = datetime.today()
    rows = session.query(Task).filter(today.date() <= Task.deadline).all()
    for i in range(7):
        current = today + timedelta(days=i)
        print(f'\n{current.strftime("%A")} {current.day} {current.strftime("%b")}')
        for j in rows:
            if j.deadline == current.date():
                x += 1
                print(f'{x}. {j.task}')
        if x == 0:
            print('Nothing to do!')
        x = 0


def all_task(do_or_delete):
    rows = session.query(Task).order_by(Task.deadline).all()
    x = 0
    if not rows:
        if do_or_delete == 'do':
            print('Nothing to do!')
        elif do_or_delete == 'delete':
            print('Nothing to delete')
            return 1
    else:
        for i in rows:
            x += 1
            print(f'{x}. {i.task}. {i.deadline.day} {i.deadline.strftime("%b")}')


choice = 1
menu = f"1) Today's tasks\n" \
       f"2) Week's tasks\n" \
       f"3) All tasks\n" \
       f"4) Missed tasks\n" \
       f"5) Add task\n" \
       f"6) Delete task\n" \
       f"0) Exit\n"
while choice != 0:
    choice = int(input(menu))
    if choice == 1:
        today_task()
    elif choice == 2:
        week_task()
        print()
    elif choice == 3:
        print('\nAll tasks:')
        all_task('do')
        print()
    elif choice == 4:
        x = 0
        print('\nMissed tasks:')
        rows = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        if rows:
            for i in rows:
                x += 1
                print(f'{x}. {i.task}. {i.deadline.day} {i.deadline.strftime("%b")}')
        else:
            print('Nothing is missed!')
        print()
    elif choice == 5:
        t = input('\nEnter task\n')
        ddl = input('Enter deadline\n')
        add_task(t, ddl)
        print('The task has been added!\n')
    elif choice == 6:
        print('\nChoose the number of the task you want to delete:')
        watcher = all_task('delete')
        if not watcher:
            delete = int(input())
            print('The task has been deleted!\n')
            rows = session.query(Task).order_by(Task.deadline).all()
            session.delete(rows[delete - 1])
            session.commit()
