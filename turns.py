class TurnCounter:
    singleton = None

    def __new__(cls):
        if TurnCounter.singleton is None:
            obj = super(TurnCounter, cls).__new__(cls)
            TurnCounter.singleton = obj
            return obj
        return TurnCounter.singleton

    def __init__(self):
        self.actions = {}
        self.current = -1
    
    @property
    def current(self):
        return self._current

    @current.setter
    def current(self, value):
        self._current = value
        if not value in self.actions:
            return
        for action in self.actions[value]:
            action()
        del self.actions[value]

    def queue_action(self, turn, action):
        if not turn in self.actions:
            self.actions[turn] = []
        self.actions[turn].append(action)
    
    def schedule_in_x_turns(self, turns, action):
        if not self.current + turns in self.actions:
            self.actions[self.current+turns] = []
        self.actions[self.current+turns].append(action)

    def schedule_for_x_turns(self, turns, action):
        for i in range(self.current+1, self.current+turns+1):
            if not i in self.actions:
                self.actions[i] = []
            self.actions[i].append(action)
