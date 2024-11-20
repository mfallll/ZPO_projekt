from typing import Optional
import re
import abc
 

class Product:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą argumenty wyrażające nazwę produktu (typu str) i jego cenę (typu float) -- w takiej kolejności -- i ustawiającą atrybuty `name` (typu str) oraz `price` (typu float)
    def __init__(self, name: str, price: float) -> None:
        if re.fullmatch('[a-zA-Z]{1,}+\\d{1,}', name):
            self.name = name
            self.price = price
        else:
            raise ValueError

    def __eq__(self, other) -> bool:
        if isinstance(other, Product):
            if self.name == other.name and self.price == other.name:
                return True
            else:
                return False
        else:
            return False
 
    def __hash__(self):
        return hash((self.name, self.price))
 
 
class TooManyProductsFoundError(Exception):
    # Reprezentuje wyjątek związany ze znalezieniem zbyt dużej liczby produktów.
    def __init__(self):
         self.message = "Found too many products"
    pass
 
 
# FIXME: Każada z poniższych klas serwerów powinna posiadać:
#   (1) metodę inicjalizacyjną przyjmującą listę obiektów typu `Product` i ustawiającą atrybut `products` zgodnie z typem reprezentacji produktów na danym serwerze,
#   (2) możliwość odwołania się do atrybutu klasowego `n_max_returned_entries` (typu int) wyrażający maksymalną dopuszczalną liczbę wyników wyszukiwania,
#   (3) możliwość odwołania się do metody `get_entries(self, n_letters)` zwracającą listę produktów spełniających kryterium wyszukiwania



class Server(abc.ABC):
    @abc.abstractmethod
    def get_entries(self, n_letters : int = 1):
        pass


class ListServer(Server):
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    n_max_returned_entries = 4

    def __init__(self, LP : list[Product]):
        self.products = LP
    
    def get_entries(self, n_letters : int = 1):
        if n_letters < 1:
            raise ValueError
        
        self.retprodlist = []
        for prod in self.products:
            if prod.name[n_letters-1] not in self.numbers:
                if prod.name[n_letters] in self.numbers:
                    self.retprodlist.append(prod)

        if len(self.retprodlist) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(self.retprodlist, key = lambda product : product.price)
 
 



class MapServer(Server):
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    n_max_returned_entries = 4

    DP = dict()
    def __init__(self, LP : list[Product]):
        self.products = {element.name : element for element in LP}


    def get_entries(self, n_letters : int = 1):
        if n_letters < 1:
            raise ValueError
        
        self.retprodlist = []
        for name, product in self.products.items():
            if name[n_letters-1] not in self.numbers:
                if name[n_letters] in self.numbers:
                    self.retprodlist.append(product)

        if len(self.retprodlist) > self.n_max_returned_entries:
            raise TooManyProductsFoundError
        return sorted(self.retprodlist, key = lambda product : product.price)
 
 
class Client:
    # FIXME: klasa powinna posiadać metodę inicjalizacyjną przyjmującą obiekt reprezentujący serwer
    def __init__(self, server : Server) -> None:
        self.server = server

    def get_total_price(self, n_letters : int = 1) -> Optional[float]:
        try:
            entries = self.server.get_entries(n_letters)
            if entries:
                return sum([e.price for e in entries])
            else:
                return None
        except TooManyProductsFoundError:
            return None