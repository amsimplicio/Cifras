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


class CaesarCipher(Cipher):
    def __init__(self):
        super().__init__("Caesar Cipher","explanation" ,"HELLO -> KHOOR with a shift of 3", requires_parameter=True, default_parameter="3")
        

    def encode(self, text, shift):
        shift = int(shift)
        return ''.join(
            chr(((ord(char) - 65 + shift) % 26) + 65) if char.isupper() else
            chr(((ord(char) - 97 + shift) % 26) + 97) if char.islower() else char
            for char in text
        )

    def decode(self, text, shift):
        shift = int(shift)
        return ''.join(
            chr(((ord(char) - 65 - shift) % 26) + 65) if char.isupper() else
            chr(((ord(char) - 97 - shift) % 26) + 97) if char.islower() else char
            for char in text
        )


class ReverseCipher(Cipher):
    def __init__(self):
        super().__init__("Reverse Cipher", "explanation","HELLO -> OLLEH")

    def encode(self, text):
        return text[::-1]

    def decode(self, text):
        return text[::-1]


# Function to get all cipher instances
def get_all_ciphers():
    return [CaesarCipher(), ReverseCipher()]