class Logger:
    __active = True

    @classmethod
    def info(cls, message):
        if not cls.__active: return
        print("Info:", message)

    @classmethod
    def error(cls, message):
        if not cls.__active: return
        print("Error:", message)

    @classmethod
    def warning(cls, message):
        if not cls.__active: return
        print("Warning:", message)

    @classmethod
    def on(cls):
        cls.__active = True

    @classmethod
    def off(cls):
        cls.__active = False

    def __repr__(self):
        return "Logger for debugging"
