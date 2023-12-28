from datetime import datetime
from django.db import connection



SEQUENCES_DICT = {
    'sale_sequence': {
        'format': 'SALE{date}{current_sequence}', 
        'date': True,
        # zfill apply 7
        'current_sequence_length': 7
    }
}


def create_sequences(sequences):
    """
    Create sequences from array

    sequences: string array
    year: sequence each year will be changed 
    """

    with connection.cursor() as cursor:
        for sequence in sequences:
            has_date = SEQUENCES_DICT[sequence]['date']
            if has_date:
                date = datetime.utcnow()
                date_str = date.strftime("%YYYYMMDD")
            
            current_sequence = f'{sequence}_{date_str}' if has_date else f'{sequence}'
            cursor.execute(f'CREATE SEQUENCE IF NOT EXISTS {current_sequence}')

def get_sequence(sequence_name):
        date = datetime.utcnow()
        date_str = date.strftime("%YYYYMMDD")

        with connection.cursor() as cursor:
            has_date = SEQUENCES_DICT[sequence_name]['date']
            sequence = f'{sequence_name}_{date_str}' if has_date else f'{sequence_name}'
            cursor.execute(f"""SELECT nextval('{sequence}')""")
            current_sequence_id = cursor.fetchone()[0]
            return get_format_sequence(sequence_name, current_sequence_id)

def get_format_sequence(sequence_name, current_sequence_id):
        """
        sequence_name = name of the dictionary
        current_sequence_id = current id in the sequence
        """
        date = datetime.utcnow()
        date_str = str(date.strftime("%m%d%Y"))
        format_sequence = SEQUENCES_DICT[sequence_name]['format']
        length = SEQUENCES_DICT[sequence_name]['current_sequence_length']
        sequence_format = str(current_sequence_id).zfill(length)
        return  format_sequence.format(date=date_str, current_sequence=sequence_format)