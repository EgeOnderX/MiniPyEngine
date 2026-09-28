from MapLoader import MapLoader


class GameMaker:

    def __init__(self, engine):

        self.engine = engine

        self.map_loader = MapLoader(
            engine
        )

    def load_map(self, path):

        return self.map_loader.load(
            path
        )

    def clear_map(self):

        self.map_loader.clear()
