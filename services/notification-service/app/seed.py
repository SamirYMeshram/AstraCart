from random import choice
from app.core.database import Base, SessionLocal, engine
from app.models import NotificationChannel, NotificationEvent
from app.repositories import NotificationRepository
from app.schemas import NotificationCreate
Base.metadata.create_all(bind=engine, checkfirst=True)
db=SessionLocal(); repo=NotificationRepository(db)
if len(repo.list()) < 30:
    events=list(NotificationEvent); channels=list(NotificationChannel)
    for i in range(30):
        event=choice(events)
        repo.create(NotificationCreate(user_id='demo-customer' if i%2 else 'customer-2', channel=choice(channels), event=event, title=f'{event.value.replace("_"," ").title()} #{i+1}', message=f'AstraCart event {event.value} processed through notification-service.', metadata_json={'seed': True, 'index': i}))
db.close(); print('Seeded 30 notifications')
