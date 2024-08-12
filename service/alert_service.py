from models import Alert


def get_alert():
    alert = Alert.get_or_none()

    if alert:
        alert = alert.get_dto()

    return alert


def set_alert(text: str):
    alert = Alert.update(text=text).where(Alert.id == 1)
    alert.execute()

    return alert.get_dto()
