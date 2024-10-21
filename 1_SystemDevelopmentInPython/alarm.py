class Alarm:
    def __init__(self, alarm_type, level):
        self.alarm_type = alarm_type
        self.level = level

    def __str__(self):
        return f"{self.alarm_type.capitalize()} Alarm {self.level}%"

    def to_dict(self):
        return {"alarm_type": self.alarm_type, "level": self.level}
