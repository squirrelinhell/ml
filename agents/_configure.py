
import mandalka

from worlds import World

@mandalka.node
class configure:
    def __init__(self, cls, **params):
        self.cls = cls
        self.params = params
        self.results = set()

    def __call__(self, *args, **more_params):
        all_params = self.params.copy()
        all_params.update(more_params)

        if len(args) == 0 and len(more_params) >= 1:
            return configure(self.cls, **all_params)
        else:
            assert len(args) == 2
            assert isinstance(args[0], World)
            assert isinstance(args[1], int)
            ret = self.cls(*args, **all_params)
            self.results.add(ret)
            return ret

    def __getattr__(self, name):
        raise ValueError("Object " + str(self.cls)
            + " has not yet been constructed")