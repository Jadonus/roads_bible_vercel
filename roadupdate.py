
import os
import json

# Dictionary mapping index to book names
book_names = {
    '1': 'Genesis',
    '2': 'Exodus',
    '3': 'Leviticus',
    '4': 'Numbers',
    '5': 'Deuteronomy',
    '6': 'Joshua',
    '7': 'Judges',
    '8': 'Ruth',
    '9': '1 Samuel',
    '10': '2 Samuel',
    '11': '1 Kings',
    '12': '2 Kings',
    '13': '1 Chronicles',
    '14': '2 Chronicles',
    '15': 'Ezra',
    '16': 'Nehemiah',
    '17': 'Esther',
    '18': 'Job',
    '19': 'Psalms',
    '20': 'Proverbs',
    '21': 'Ecclesiastes',
    '22': 'Song of Solomon',
    '23': 'Isaiah',
    '24': 'Jeremiah',
    '25': 'Lamentations',
    '26': 'Ezekiel',
    '27': 'Daniel',
    '28': 'Hosea',
    '29': 'Joel',
    '30': 'Amos',
    '31': 'Obadiah',
    '32': 'Jonah',
    '33': 'Micah',
    '34': 'Nahum',
    '35': 'Habakkuk',
    '36': 'Zephaniah',
    '37': 'Haggai',
    '38': 'Zechariah',
    '39': 'Malachi',
    '40': 'Matthew',
    '41': 'Mark',
    '42': 'Luke',
    '43': 'John',
    '44': 'Acts',
    '45': 'Romans',
    '46': '1 Corinthians',
    '47': '2 Corinthians',
    '48': 'Galatians',
    '49': 'Ephesians',
    '50': 'Philippians',
    '51': 'Colossians',
    '52': '1 Thessalonians',
    '53': '2 Thessalonians',
    '54': '1 Timothy',
    '55': '2 Timothy',
    '56': 'Titus',
    '57': 'Philemon',
    '58': 'Hebrews',
    '59': 'James',
    '60': '1 Peter',
    '61': '2 Peter',
    '62': '1 John',
    '63': '2 John',
    '64': '3 John',
    '65': 'Jude',
    '66': 'Revelation'
    }
def update_json_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                updated_data = []
                for entry in data:
                    if 'book_id' in entry:
                        book_id = str(entry['book_id'])
                        if book_id in book_names:
                            entry['book_name'] = book_names[book_id]
                        else:
                            entry['book_name'] = 'Unknown Book'
                    
                    updated_data.append(entry)
                
                with open(file_path, 'w') as file:
                    json.dump(updated_data, file, indent=4)# Usage example
folder_path = '/Users/jadong/roads_bible_vercel/static/roads/'

update_json_files(folder_path)

