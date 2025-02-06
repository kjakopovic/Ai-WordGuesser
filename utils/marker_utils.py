marker_to_int_mapper_dict = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 
    'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 
    'R': 17, 'S': 18, 'T': 19, 'U': 20, 'V': 21, 'Z': 22, '0': 23
}

def convert_letter_to_marker(letter: str) -> int:
    marker = marker_to_int_mapper_dict.get(letter, None)
    
    if not marker:
        return -1
    
    return marker

def convert_marker_to_letter(marker: str) -> int:
    marker = marker.split("/")[1][1:]
    reverse_dict = {v: k for k, v in marker_to_int_mapper_dict.items()}

    letter = reverse_dict.get(int(marker), None)

    if not letter:
        return -1

    return letter