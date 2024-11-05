from itertools import zip_longest
import unicodedata
def remove_accents(text):
    # Normalize the text to decompose accented characters into base characters and combining marks
    normalized_text = unicodedata.normalize('NFD', text)
    # Filter out combining diacritical marks (accents)
    return ''.join(char for char in normalized_text if unicodedata.category(char) != 'Mn')

class Cipher:
    def __init__(self, name, explanation, example_text, requires_parameter=False, default_parameter=""):
        """
        Initialize the cipher with a name, an example, and any additional settings.
        """
        self.name = name
        self.explanation = explanation
        self.example_text = example_text
        self.requires_parameter = requires_parameter
        self.default_parameter = default_parameter
    
    def encode(self, text):
        """
        Method to encode a given text. To be implemented in subclasses.
        """
        raise NotImplementedError("Encode method must be implemented in subclass")

    def decode(self, text):
        """
        Method to decode a given text. To be implemented in subclasses.
        """
        raise NotImplementedError("Decode method must be implemented in subclass")


class AlfabetoNumerico(Cipher):
    def __init__(self):
        super().__init__("Alfabeto numerico sem loop",
        "Cada letra do alfabeto corresponde a um número. Para identificar o código é preciso dar a chave. " +
        "Se, por exemplo, a chave do código for 12, A = 12, B = 13, C = 14 ... Z = 37" 
        ,"ALERTA = 12 23 16 29 31 12", requires_parameter=True, default_parameter="1")
        # Create a dictionary where each letter is mapped to its encoded value
        self.letter_to_number = {letter: number for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
        self.number_to_letter = {number: letter for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
        self.number_to_letter[""] = " "
    
    def encode(self, text, shift):
        text = remove_accents(text.lower())
        shift = int(shift)
        return ' '.join(str((self.letter_to_number[char] + shift)) if char.isalpha() else char for char in text)

    def decode(self, text, shift):
        numbers = text.split(" ")
        shift = int(shift)
        return   ''.join(self.number_to_letter[int(num) - shift] for num in numbers)

class AlfabetoNumericoLoop(Cipher):
    def __init__(self):
        super().__init__("Alfabeto numerico com loop",
        "Cada letra do alfabeto corresponde a um número, a partir do 26 volta para o 1. Para identificar o código é preciso dar a chave. " +
        "Se, por exemplo, a chave do código for 12, A = 12, B = 13, C = 14 ..., N = 25, O = 26, P = 1, Q = 2,..." 
        ,"ALERTA = 12 23 16 3 5 12", requires_parameter=True, default_parameter="1")
        # Create a dictionary where each letter is mapped to its encoded value
        self.letter_to_number = {letter: number for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
        self.number_to_letter = {number: letter for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
        self.number_to_letter[""] = " "
    
    def encode(self, text, shift):
        text = remove_accents(text.lower())
        shift = int(shift)
        return ' '.join(str((self.letter_to_number[char] + shift -1) % 26 + 1) if char.isalpha() else char for char in text)# -1 and +1 so it starts with 1 instead of 0

    def decode(self, text, shift):
        numbers = text.split(" ")
        shift = int(shift)
        return   ''.join(self.number_to_letter[(int(num) - shift) % 26 ] if num.isnumeric() else num for num in numbers) 


class AlfabetoTransposto(Cipher):
    def __init__(self):
        super().__init__("Alfabeto Transposto",
        "Por baixo do alfabeto nomal, escreve-se mesmo alfabeto, mas começando na letra chave do código. " +
        "Se, por exemplo, a chave do código for V (A = V), temos: A = V, B = W, .., F = A, G = B..." 
        ,"ESCUTEIRO = ZNXPOZDMJ , com chave: A = V", requires_parameter=True, default_parameter="V")
        self.letter_to_number = {letter: number for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
        self.number_to_letter = {number: letter for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}

    def encode(self, text, shift):
        shift = shift.lower()
        text = remove_accents(text.lower())
        return ''.join(
            self.number_to_letter[(self.letter_to_number[char] + self.letter_to_number[shift]) % 26] if char.isalpha() else char
            for char in text
        )

    def decode(self, text, shift):
        text = remove_accents(text.lower())
        shift = shift.lower()
        return ''.join(
            self.number_to_letter[(self.letter_to_number[char] - self.letter_to_number[shift]) % 26] if char.isalpha() else char
            for char in text
        )

class AlfabetoInvertido(Cipher):
    def __init__(self):
        super().__init__("Alfabeto Invertido",
        "Por baixo do alfabeto nomal, escreve-se o mesmo alfabeto, mas invertido. As letras de baixo são a codificação das de cima."
        ," ESCUTEIRO = VHXFGVRIL")
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'
        self.inverse_map = {self.alphabet[i]: self.alphabet[::-1][i] for i in range(len(self.alphabet))}
        

    def encode(self, text):
        text = remove_accents(text.lower())
        return ''.join(
            self.inverse_map[char] if char.isalpha() else char
            for char in text
        )

    def decode(self, text):
        return self.encode(text)

"""class Caranguejo(Cipher):
    def __init__(self):
        super().__init__("Caranguejo", 
                         "As letras e as palavras são escritas ao contrário",
                         "BOA CAÇA E SEMPRE ALERTA = ATRELA ERPMES E AÇAC AOB")

    def encode(self, text):
        words = text.split(" ")
        result = ""
        for word in words:
            result += word[::-1] + " "
        return result[:-1]

    def decode(self, text):
        return self.encode(text)"""

class Caranguejo(Cipher):
    def __init__(self):
        super().__init__("Caranguejo", 
                         "As letras e as palavras são escritas ao contrário",
                         "BOA CAÇA E SEMPRE ALERTA = ATRELA ERPMES E AÇAC AOB")

    def encode(self, text):
        return text[::-1]

    def decode(self, text):
        return self.encode(text)

    
class Metades(Cipher):
    def __init__(self):
        super().__init__("Metades", 
                         "As letras da mensagem são dispostas alternadamente numa tabela de duas colunas.",
                         "CHAMAR O SOCORRISTA: CAAOOORSA HMRSCRIT")

    def encode(self, text):
        # Remove spaces from the input text
        text = text.replace(" ", "")
        # Use slicing to get characters at even and odd indices
        first, second = text[::2], text[1::2]
        return f"{first} {second}"

    def decode(self, text):
        # Split the encoded text into two parts
        first, second = text.split(" ")
        # Interleave characters from both parts using zip_longest
        result = ''.join(a + b for a, b in zip_longest(first, second, fillvalue=""))
        return result
class RomanoArabe(Cipher):
    def __init__(self):
        super().__init__("Romano-Árabe", 
                         "As vogais são numeradas de em romano, e as consoantes em árabe.",
                         "ALERTA = I 9 II 14 16 I")
        self.encode_map = {"a":"I", "e": "II", "i": "III", "o": "IV", "u": "V",
        'b': '1', 'c': '2', 'd': '3', 'f': '4', 'g': '5', 'h': '6',
        'j': '7', 'k': '8', 'l': '9', 'm': '10', 'n': '11', 'p': '12',
        'q': '13', 'r': '14', 's': '15', 't': '16', 'v': '17', 'w': '18',
        'x': '19', 'y': '20', 'z': '21'}
        self.reverse_map = {
        'I': 'a', 'II': 'e', 'III': 'i', 'IV': 'o', 'V': 'u',  # Roman numerals to vowels
        '1': 'b', '2': 'c', '3': 'd', '4': 'f', '5': 'g', '6': 'h',  # Custom numbers to consonants
        '7': 'j', '8': 'k', '9': 'l', '10': 'm', '11': 'n', '12': 'p',
        '13': 'q', '14': 'r', '15': 's', '16': 't', '17': 'v', '18': 'w',
        '19': 'x', '20': 'y', '21': 'z', "": " "
        }

    def encode(self, text):
        text = text.lower() 
        return ' '.join(self.encode_map.get(char, char) for char in text)

    def decode(self, text):
        text = text.split(" ")
        return ''.join(self.reverse_map.get(char, char) for char in text)
    

    

# Function to get all cipher instances
def get_all_ciphers():
    return [Caranguejo(), Metades(), AlfabetoInvertido(), RomanoArabe(), AlfabetoNumerico(), AlfabetoNumericoLoop(), AlfabetoTransposto()]