import json

class Watchlist:
    def __init__(self, file_path='watchlist.json'):
        self.file_path = file_path

    def load_watchlist(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_watchlist(self, symbols):
        with open(self.file_path, 'w') as file:
            json.dump(symbols, file)

    def add_to_watchlist(self, symbol):
        watchlist = self.load_watchlist()
        if symbol not in watchlist:
            watchlist.append(symbol)
            self.save_watchlist(watchlist)

    def remove_from_watchlist(self, symbol):
        watchlist = self.load_watchlist()
        if symbol in watchlist:
            watchlist.remove(symbol)
            self.save_watchlist(watchlist)