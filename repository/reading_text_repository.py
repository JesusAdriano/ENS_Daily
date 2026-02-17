from domain.reading_text import ReadingText

class ReadingTextRepository:
    def __init__(self):
        self._texts = [
            ReadingText(
                1,
                "Pai Nosso",
                "Pai nosso que estais nos céus, Santificado seja o Vosso nome. Venha a nós o Vosso Reino. Seja feita a Vossa vontade, Assim na Terra como no Céu. O pão nosso de cada dia nos dai hoje. Perdoai as nossas ofensas, Assim como nós perdoamos a quem nos tem ofendido. E não nos deixeis cair em tentação, Mas livrai-nos do mal. Amém."
            ),
            ReadingText(
                2,
                "Ave Maria",
                "Ave Maria cheia de graça, o Senhor é convosco. Bendita sois vós entre as mulheres, e bendito é o fruto do vosso ventre, Jesus. Santa Maria, Mãe de Deus, rogai por nós pecadores, agora e na hora de nossa morte. Amém."
            ),
            ReadingText(
                3,
                "Magnificat",
                "O Poderoso fez em mim maravilhas, e Santo é seu nome! A minh’alma engrandece o Senhor, exulta meu espírito em  Deus, meu Salvador! Porque olhou para a humildade de sua serva, doravante as gerações hão de chamar-me de bendita! O Poderoso fez em mim maravilhas, e Santo é seu nome! Seu amor para sempre se estende, sobre aqueles que O temem! Manifesta o poder de seu braço, dispersa os soberbos; derruba os poderosos de seus tronos e eleva os humildes; sacia de bens os famintos, despede os ricos sem nada. Acolhe Israel, seu servidor, fiel ao seu amor, como havia prometido a nossos pais, em favor de Abraão e de seus filhos para sempre! Glória ao Pai, ao Filho e ao Espírito Santo, como era no princípio, agora e sempre Amém!"
            ),
            ReadingText(
                4,
                "Escuta da Palavra",
                "Leitura da Palavra..."
            ),
        ]

    def get_by_id(self, text_id: int) -> ReadingText | None:
        for text in self._texts:
            if text.id == text_id:
                return text
        return None

    def get_all(self):
        return self._texts

    def get_by_index(self, index: int) -> ReadingText:
        return self._texts[index % len(self._texts)]