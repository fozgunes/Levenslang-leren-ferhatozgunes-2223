



def verwijderSpatiesEnKommas(arg1):
    waardeGebruiker = arg1.lower()
    waardeGebruiker = waardeGebruiker.replace(" ", "")
    waardeGebruiker = waardeGebruiker.replace(",", "")

def controleerInputPalindroom(waardeGebruiker, aantalLettersInput):
    vergelijk1 = ""
    vergelijk2 = ""
    for x in waardeGebruiker:
        vergelijk1 = vergelijk1 + x
    for x in reversed(waardeGebruiker):
        vergelijk2 = vergelijk2 + x

    if vergelijk1 == vergelijk2:
        return True
    else:
        return False


def main():
    waardeGebruiker = ""
    aantalLettersInput = 0

    while waardeGebruiker != "exit":
       waardeGebruiker = input("Enter string to test for palindrome or 'exit':")
       aantalLettersInput = len(waardeGebruiker)
       verwijderSpatiesEnKommas(waardeGebruiker)
       print("This is an pallindroom:" , controleerInputPalindroom(waardeGebruiker, aantalLettersInput))

    else:
        exit()

if __name__ == "__main__":
    main()